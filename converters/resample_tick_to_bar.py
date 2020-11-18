# Takes Approximates 30 minutes to resample 1 yerar of tick data into all timeframes.
import os
import sys
import pandas as pd
import tables
import time

## Set Variables Here
pair = 'EURUSD'
year = '2020'
base_folder = '/Volumes/External/' + pair + '/' + year + '/'
input_filename = pair + '-' + year + '-ticks.csv'
input_data = base_folder + input_filename
timeframes = ['1Min', '5Min', '15Min', '30Min', '60Min', '1D', '1W', '1M']

print('\n---------- Begining Resampling... ---------- \n')
start_time = time.time()

for timeframe in timeframes:
    print(f'\nResampling for {timeframe}')
    output_filename = input_data.replace('ticks', timeframe, 1)
    df = pd.read_csv(input_data, names=['TIME', 'ASKP', 'BIDP'], parse_dates=True)
    df.set_index('TIME', inplace=True)
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S:%f')
    data_bid = df['BIDP'].resample(timeframe).ohlc().dropna()
    data_bid.to_csv(output_filename, float_format='%g', date_format='%Y-%m-%d %H:%M:%S:%f', mode='a', header=True, index=True)

print("\n---------- Resampling Completed in %s Seconds ----------\n" % (time.time() - start_time))