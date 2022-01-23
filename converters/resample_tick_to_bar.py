import time
import pandas as pd
from .python_csv_to_mt4_csv import generate_mt4_data 

print('\n---------- Begining Resampling... ---------- \n')
start_time = time.time()

def init_resample_data(currency, year, dir_path):

    base_folder = f'{dir_path}/{currency}/{year}'
    input_filename = f'{currency}-{year}-ticks.csv'
    input_data = f'{base_folder}/{input_filename}'
    timeframes = ['1Min', '5Min', '15Min', '30Min', '60Min', '1D', '1W', '1M']

    for timeframe in timeframes:
        print(f'\nResampling {currency} {year} for {timeframe}')
        output_filename = input_data.replace('ticks', timeframe+'-py', 1)
        df = pd.read_csv(input_data, names=['TIME', 'ASKP', 'BIDP'], parse_dates=True)

        #! Builds MT4 compatable Dataset
        python_dataset = df
        python_dataset.set_index('TIME', inplace=True)
        python_dataset.index = pd.to_datetime(python_dataset.index, format='%Y-%m-%d %H:%M:%S:%f')
        python_dataset = python_dataset['BIDP'].resample(timeframe).ohlc().dropna()
        python_dataset.to_csv(output_filename, float_format='%g', date_format='%Y-%m-%d %H:%M:%S:%f', mode='a', header=True, index=True)
        #! Builds MT4 compatable Dataset
        generate_mt4_data(output_filename)


print("\n---------- Resampling Completed in %s Seconds ----------\n\n\n" % (time.time() - start_time))
