import lzma, struct, logging
import pandas as pd
from glob import glob
from datetime import datetime
from loggers.logger import setup_logger

class Bi5_Decompression():
    def __init__(self, settings):
        self.location = settings['location']
        self.asset = settings['asset']
        self.year = settings['year']
        self.input_dir = f'{self.location}/{self.asset}/{self.year}/raw-download-data'
        self.output_file = f'{self.location}/{self.asset}/{self.year}/{self.asset}-{self.year}-ticks.csv'
        self.bi5_files = []
        self.processed_count = 0
        self.failed_decompressions = set()
        self.failed_file_saves = set()
        self.logger = setup_logger('decompression_logger', f'{self.location}/{self.asset}/{self.asset}-Decompression.log')
        self.decompression_logger = logging.getLogger('decompression_logger')


    def run_file_decompression(self):
        self._build_decompression_tasks()
        self._run_decompression_tasks()


    def _build_decompression_tasks(self):
        files = [f for f in glob(self.input_dir  + "**/*.bi5")]
        self.bi5_files = sorted(files)


    def _run_decompression_tasks(self):
        for file in self.bi5_files:
            self._decompress_file(file)
            self.processed_count += 1
            print(f'Processed {self.processed_count} decompressions of {len(self.bi5_files)} for {self.asset} in {self.year}')
        self._save_logs()


    def _decompress_file(self, file):
        chunk_size = 128
        fmt = '>3i2f'
        chunk_size = struct.calcsize(fmt)
        data = []
        try:
            with lzma.open(file) as f:
                while True:
                    chunk = f.read(chunk_size)
                    if chunk:
                        data.append(struct.unpack(fmt, chunk))
                    else:
                        break
            df = pd.DataFrame(data)
            self._clean_and_save_data(df, file)
        except:
            self.failed_decompressions.add(file)

    
    def _clean_and_save_data(self, df, file):
        #  Clean Columns
        df.columns = ['TIME', 'ASKP', 'BIDP', 'ASKV', 'BIDV']
        df = df.drop(columns=['ASKV', 'BIDV'])
        df = df.dropna()

        #  Clean Times
        year = int(file[-24:-20])
        month = int(file[-19:-17])
        day = int(file[-16:-14])
        hour = int(file[-13:-11])
        df = df.sort_values(by=['TIME'])
        df.drop_duplicates(subset ="TIME", inplace=True, keep = False) 
        file_date_object = datetime(year, month, day, hour)   # Build date object from integers in file name
        ms_since_epoch = file_date_object.timestamp() * 1000 # Converts the file date to ms since epoch
        df['TIME'] = pd.to_datetime(df['TIME'] + ms_since_epoch, unit='ms') # Adds timestamp + epoch offset and converts format

        # Set Decimal Values
        instrument = file[-31:-25]
        decimal_factor = self._generate_decimal_places(instrument)
        df['ASKP'] = df['ASKP'].astype('float64') 
        df['ASKP'] = df['ASKP'].div(decimal_factor)
        df['BIDP'] = df['BIDP'].astype('float64') 
        df['BIDP'] = df['BIDP'].div(decimal_factor)

        # Save Result
        try:
            df.to_csv(self.output_file, float_format='%g', date_format='%Y-%m-%d %H:%M:%S:%f', mode='a', header=False, index=False)
        except:
            self.failed_file_saves.add(file)


    def _generate_decimal_places(self, instrument):
        decimal_factors = [
            { 'instrument' : 'XAUUSD', 'decimal_factor' : 1000 },
            { 'instrument' : 'XAGUSD', 'decimal_factor' : 1000 },
            { 'instrument' : 'BTCUSD', 'decimal_factor' : 10 }
        ]
        decimal_factor = None
        try:
            #  Use for specialized instruments
            match = next(x for x in decimal_factors if x["instrument"] == instrument)
            decimal_factor = match['decimal_factor']
        except:
            # Use for all forex pairs to output 5 decimal paces
            decimal_factor = 100000
        return decimal_factor


    def _save_logs(self):
        total_tasks = len(self.bi5_files)
        total_failures = self.failed_decompressions | self.failed_file_saves
        total_failures_count = len(total_failures)
        sorted_failures = sorted(total_failures)
        mapped_file_failures = ''

        if total_failures_count > 0 :
            for failed_file in sorted_failures:
                mapped_file_failures += '\n    '+failed_file
        else:
            mapped_file_failures = '\n    NONE'

        log_msg = f' \n--- DECOMPRESSION LOG FOR {self.asset} {self.year} ---\n  Total Tasks: {total_tasks}\n  Total Failures: {total_failures_count}\n  Failed Files: {mapped_file_failures}\n\n'
        self.decompression_logger.info(log_msg)
        print('\n\n', log_msg)
        log_msg = ''
