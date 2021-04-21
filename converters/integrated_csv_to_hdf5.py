import os
import sys
import time
import tables
import pandas as pd

## GLOBAL VARIBLES THAT CAN BE CHANGED BY THE USER:
# equity = 'EURNZD'
# # years = ['2020']
# years = ['2020', '2019', '2018', '2017', '2016']
# base_path = '/Volumes/External/Trading/historical-data/forex/'



start_time = time.time()


def set_global_vars(currency, current_year, dir_path):
    global equity
    global year
    global base_path
    global folder
    global all_dir_files
    global csv_files 
    equity = currency
    year = current_year
    base_path = dir_path
    folder = f'{base_path}/{equity}/{year}'
    all_dir_files = os.listdir(folder)
    csv_files = []


def build_folder_structure():
# for year in years:
    # folder = f'{base_path}{equity}/{year}'
    # all_dir_files = os.listdir(folder)
    # csv_files = []

    for file in all_dir_files:
        if file.endswith('.csv'):
            if not file.startswith('._'):
                csv_files.append(file)

    if not os.path.isdir(f"{folder}/csv"):
        csv_path = os.path.join(folder, 'csv') 
        os.mkdir(csv_path)
    if not os.path.isdir(f"{folder}/h5"):
        h5_path = os.path.join(folder, 'h5') 
        os.mkdir(h5_path)



def convert_file(file):

    input_filepath = f'{folder}/{file}'
    output_filepath = input_filepath.replace('.csv', '.h5')
    output_filename = file.replace('.csv', '.h5')

    print(f'\n\n---------  CURRENTLY PROCESSING: {input_filepath}  -----------')

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

    df.to_hdf(output_filepath, key=key, mode='w', complevel=5, complib='blosc:zlib')

    os.rename(f"{input_filepath}", f"{folder}/csv/{file}")
    os.rename(f"{output_filepath}", f"{folder}/h5/{output_filename}")



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
        try:
            convert_file(file)
        except:
            if error_counter < 3:
                error_counter += 1
                convert_file(file)
                raise Exception("Will not try again, have tried 3 times")  
            error_counter = 0
    cleanup()



def init_h5_conversion(currency, current_year, dir_path):
    set_global_vars(currency, current_year, dir_path)
    build_folder_structure()
    build_file_names()


print("Completed in %s Seconds" % (time.time() - start_time))