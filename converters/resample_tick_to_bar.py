import os
import sys
import pandas as pd
import tables
import time

    ## Set Variables Here
input_filename = '/Users/ericlingren/Documents/EURUSD-2017-ticks.csv'
output_filename = '/Users/ericlingren/Documents/EURUSD-2017-1M.csv'
timeframe = '1M'  ## IE - 1Min , 5Min , 15Min , 30Min , 60Min , 1W , 1M


print('\nBegining Resampling...\n')
start_time = time.time()

df = pd.read_csv(input_filename, names=['TIME', 'ASKP', 'BIDP'], parse_dates=True)
df.set_index('TIME', inplace=True)
df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S:%f')
data_bid = df['BIDP'].resample(timeframe).ohlc().dropna()
data_bid.to_csv(output_filename, float_format='%g', date_format='%Y-%m-%d %H:%M:%S:%f', mode='a', header=True, index=True)

print("\nResampling Completed in %s Seconds\n" % (time.time() - start_time))