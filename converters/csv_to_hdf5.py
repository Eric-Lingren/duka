import os
import sys
import pandas as pd
import time

## GLOBAL VARIBLES THAT CAN BE CHANGED BY THE USER:
equity = 'USDCAD'
year = '2017'
base_path = '/Volumes/External/Trading/historical-data/forex'


start_time = time.time()

input_filename = f'{base_path}/{equity}/{year}/{equity}-{year}-ticks.csv'
output_filename = f'{base_path}/{equity}/{year}/{equity}-{year}-ticks.h5'

folder = f'{base_path}/{equity}/{year}'

if not os.path.isdir(f"{folder}/csv"):
    csv_path = os.path.join(folder, 'csv') 
    os.mkdir(csv_path)
if not os.path.isdir(f"{folder}/h5"):
    h5_path = os.path.join(folder, 'h5') 
    os.mkdir(h5_path)



df = pd.read_csv(input_filename)
# print(df)


df.columns = ['TIME', 'ASKP', 'BIDP'] # For Tick Data
# df.columns = ['TIME', 'OPEN', 'HIGH', 'LOW', "CLOSE"]  # For 1 min or greater data
df.set_index('TIME', inplace=True)

start_index = input_filename.rfind('/')+1
end_index = input_filename.rfind('.')
name = input_filename[start_index:end_index]
name = name.replace('-', '_')
key = 'FX_' + name

print(key)


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