import os
import sys
import time
import tables
import pandas as pd

## GLOBAL VARIBLES THAT CAN BE CHANGED BY THE USER:
equity = 'EURUSD'
year = '2021'
base_path = '/Volumes/External/Trading/historical-data/forex/'




start_time = time.time()

folder = f'{base_path}{equity}/{year}'
all_dir_files = os.listdir(folder)
csv_files = []

for file in all_dir_files:
    if file.endswith('.csv'):
        if not file.startswith('._'):
            csv_files.append(file)



def convert_file(input_filepath, output_filepath):
    print(' ')
    print(f'---------  CURRENTLY PROCESSING: {input_filepath}  -----------')

    df = pd.read_csv(input_filepath)

    is_tick_data = 'ticks' in input_filepath
    if is_tick_data: # For Tick Data
        df.columns = ['TIME', 'ASKP', 'BIDP'] 
    elif not is_tick_data: # For 1 min or greater data
        df.columns = ['TIME', 'OPEN', 'HIGH', 'LOW', "CLOSE"]  

    # Set databse indexes
    df.set_index('TIME', inplace=True)
    start_index = input_filepath.rfind('/')+1
    end_index = input_filepath.rfind('.')
    name = input_filepath[start_index:end_index]
    name = name.replace('-', '_')
    key = 'FX_' + name

    # Write initial data to the database
    store = pd.HDFStore(output_filepath)
    store.put(  key, 
                df,
                format='table',
                data_columns=True,
                complib='blosc:snappy',
                complevel=1)
    store.close()

    # Append new data to data store
    store = pd.HDFStore(output_filepath)
    store.append(   key,
                    df,
                    format='table',
                    data_columns=True,
                    complib='blosc:snappy',
                    complevel=1)
    store.close()



def cleanup():
    print('')
    for file in all_dir_files:
        if file.endswith('.tmp'):
            os.remove(f'{folder}/{file}')
    print('FREINDLY CLEANUP RAN')
    print('ALL FILES PROCESSED')



def build_file_names():
    error_counter = 0
    for file in csv_files:
        input_filepath = f'{folder}/{file}'
        output_filepath = input_filepath.replace('.csv', '.h5')

        
        
        try:
            convert_file(input_filepath, output_filepath)
        except:
            if error_counter < 3:
                error_counter += 1
                convert_file(input_filepath, output_filepath)
                raise Exception("Will not try again, have tried 3 times")  
            error_counter = 0
    cleanup()

build_file_names()





# start_time = time.time()

# try:
#     df = pd.read_csv(input_filename)
#     # print(df)


#     # df.columns = ['TIME', 'ASKP', 'BIDP'] # For Tick Data
#     df.columns = ['TIME', 'OPEN', 'HIGH', 'LOW', "CLOSE"]  # For 1 min or greater data
#     df.set_index('TIME', inplace=True)

#     start_index = input_filename.rfind('/')+1
#     end_index = input_filename.rfind('.')
#     name = input_filename[start_index:end_index]
#     name = name.replace('-', '_')
#     key = 'FX_' + name + '_tick'

#     print(key)


#     # Write initial data to the database
#     store = pd.HDFStore(output_filename)

#     store.put(  key, 
#                 df,
#                 format='table',
#                 data_columns=True,
#                 complib='blosc:snappy',
#                 complevel=1)
#     store.close()


#     # Append new data to data store
#     store = pd.HDFStore(output_filename)
#     store.append(   key,
#                     df,
#                     format='table',
#                     data_columns=True,
#                     complib='blosc:snappy',
#                     complevel=1)
#     store.close()
# except:
#     print('Try Again')


print("Completed in %s Seconds" % (time.time() - start_time))