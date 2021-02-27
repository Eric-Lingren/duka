# Takes Approximates 30 minutes to resample 1 yerar of tick data into all timeframes.
import os
import sys
import time
import tables
import pandas as pd

## Set Variables Here
pair = 'EURNZD'
years = [ '2020', '2019', '2018', '2017', '2016']
# years = ['2011', '2010']


print('\n---------- Begining Resampling... ---------- \n')
start_time = time.time()

def resample_data():

    for year in years:
        base_folder = '/Volumes/External/Trading/historical-data/forex/' + pair + '/' + year + '/'
        input_filename = pair + '-' + year + '-ticks.csv'
        input_data = base_folder + input_filename
        timeframes = ['1Min', '5Min', '15Min', '30Min', '60Min', '1D', '1W', '1M']

        for timeframe in timeframes:
            print(f'\nResampling {pair} {year} for {timeframe}')
            output_filename = input_data.replace('ticks', timeframe, 1)
            df = pd.read_csv(input_data, names=['TIME', 'ASKP', 'BIDP'], parse_dates=True)
            df.set_index('TIME', inplace=True)
            df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S:%f')
            data_bid = df['BIDP'].resample(timeframe).ohlc().dropna()
            data_bid.to_csv(output_filename, float_format='%g', date_format='%Y-%m-%d %H:%M:%S:%f', mode='a', header=True, index=True)

resample_data()

print("\n---------- Resampling Completed in %s Seconds ----------\n\n\n" % (time.time() - start_time))
