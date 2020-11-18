import os
import sys
import pandas as pd
import tables
import time


# input_filename = '/Users/ericlingren/Documents/EURUSD-clean-data.csv'
# input_filename = '/Volumes/External/test-data/week-1.csv'
input_filename = '/Users/ericlingren/Desktop/EURUSD-2019-1Min.csv'
output_filename = '/Users/ericlingren/Desktop/EURUSD-2019-1Min.h5'
# output_filename = '/Volumes/External/test-data/week-1.h5'


start_time = time.time()


df = pd.read_csv(input_filename)
# print(df)


# df.columns = ['TIME', 'ASKP', 'BIDP'] # For Tick Data
df.columns = ['TIME', 'OPEN', 'HIGH', 'LOW', "CLOSE"]  # For 1 min or greater data
df.set_index('TIME', inplace=True)

start_index = input_filename.rfind('/')+1
end_index = input_filename.rfind('.')
name = input_filename[start_index:end_index]
key = 'FX_' + name + '_tick'


# Write initial data to the database
store = pd.HDFStore(output_filename)

store.put(  key, 
            df,
            format='table',
            data_columns=True,
            complib='blosc:snappy',
            complevel=1)
store.close()


# Append new data to data store
store = pd.HDFStore(output_filename)
store.append(   key,
                df,
                format='table',
                data_columns=True,
                complib='blosc:snappy',
                complevel=1)
store.close()


print("Completed in %s Seconds" % (time.time() - start_time))