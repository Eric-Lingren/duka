import pandas as pd

class Data_Resampler():
    def __init__(self, settings):
        self.location = settings['location']
        self.asset = settings['asset']
        self.year = settings['year']
        self.input_file = f'{self.location}/{self.asset}/{self.year}/{self.asset}-{self.year}-ticks.csv'
        self.output_file = ''
        self.timeframes = ('1Min', '5Min', '15Min', '30Min', '60Min', '1D', '1W', '1M')


    #* Init resampling conversion - 
        #* User can pass in ticks dataset file manually. Without a file, it is loaded automatically
        #* User can pass in a list or set of desired timeframes. Without timeframes, it will convert to all timeframes
    def resample_tick_data(self, input_file=None, timeframes=None):
        if input_file == None:
            input_file = self.input_file
        ticks_df = self._load_ticks_csv(input_file)
        if timeframes == None:
            timeframes = self.timeframes
        self._timeframe_resample(ticks_df, timeframes)


    #* Reusable method accepts any CSV filepath with tick data and converts to DF
    def _load_ticks_csv(self, file):
        df = pd.read_csv(file, names=['TIME', 'ASKP', 'BIDP'], parse_dates=True)
        df.set_index('TIME', inplace=True)
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S:%f')
        return df


    #* Resamples ticks DF into all requested timeframes
    def _timeframe_resample(self, df, timeframes):
        for timeframe in timeframes:
            bids_dataset = df['BIDP'].resample(timeframe).ohlc().dropna()
            python_csv_file_name = self._save_df_as_python_compatible_csv(bids_dataset, timeframe)
            self.convert_python_csv_to_mt4_csv(python_csv_file_name)


    #* Saves resampled DF to new CSV with python compatable datetime fields
    def _save_df_as_python_compatible_csv(self, df, timeframe):
        output_filename = self.input_file.replace('ticks', f'{timeframe}-py', 1)
        df.to_csv(output_filename, float_format='%g', date_format='%Y-%m-%d %H:%M:%S', mode='a', header=True, index=True)
        return output_filename


    #* Converts saved python CSV to new CSV with MT4 compatable datetime fields
    def convert_python_csv_to_mt4_csv(self, filepath):
        mt4_dataset = pd.read_csv(filepath, parse_dates=['TIME'],)
        mt4_dataset.index = mt4_dataset['TIME'] 
        mt4_dataset.index = pd.to_datetime(mt4_dataset.index)
        mt4_dataset['date']= mt4_dataset.index.map(lambda t: t.strftime('%Y.%m.%d'))
        mt4_dataset['time']= mt4_dataset.index.map(lambda t: t.strftime('%H:%M'))
        mt4_dataset['volume']= mt4_dataset.index.map(lambda t: 0)
        mt4_dataset = mt4_dataset[[ 'date', 'time', 'open', 'high', 'low', 'close', 'volume']]
        mt4_dataset.reset_index(drop=True, inplace=True)
        mt4_output_filename = filepath.replace('py', 'mt4', 1)
        mt4_dataset.to_csv(mt4_output_filename, float_format='%g', mode='a', header=False, index=False)


    #TODO - allow loading any timeframe mt4 csv and convert to same timeframe python csv
    