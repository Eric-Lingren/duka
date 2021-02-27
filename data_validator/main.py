import pandas as pd
from file_size import init_file_size_check
from decompress import init_file_decompression
from improved_decompress import init_improved_decompress
from tick_deviations import init_tick_deviations
from file_existence_bar_data import init_file_existence_bars
from file_existence_tick_data import init_file_existence_ticks



# DECLARE CONFIG VARIBLES HERE BEFORE RUNNING THE INIT_VALIDATOR SCRIPT :
pair = 'EURNZD'
year = '2020' 



base_path = '/Volumes/External/Trading/historical-data/forex/' + pair + '/' + year + '/' 
data_directory = base_path + 'raw-download-data' # Location where the data files are stored
log_directory = base_path  # Location where you would like the log output file
data_output_directory = base_path + pair + '-' + year + '-ticks.csv' # Location where you would like the uncompressed ticks CSV File to be saved
timeframe = 'tick'  


def init_validator():

    if timeframe == 'tick':
        init_file_existence_ticks(data_directory, log_directory)
    else:
        init_file_existence_bars(data_directory, log_directory)

    val = input("Would you like to proceed to file validation? (y/n): ")
    if val != 'y':
        print("\nProgram Terminating.\n")
    else:
        init_file_size_check(data_directory, log_directory)
        val = input("Would you like to proceed to statistical analysis of file data? (y/n): ")
        if val != 'y':
            print("\nProgram Terminating.\n")
        else:
            init_tick_deviations(data_directory, log_directory)
            val = input("Would you like to proceed to file decompression? (y/n): ")
            if val != 'y':
                print("\nProgram Terminating.\n")
            else:
                init_improved_decompress(data_directory, data_output_directory)
                # init_file_decompression(data_directory, data_output_directory)

    ## These are quick function shortcuts that can be used to bypas the user input full scripts above:
    # init_file_existence_ticks(data_directory, log_directory)
    # init_tick_deviations(data_directory, log_directory)
    # init_file_size_check(data_directory, log_directory)
    # init_file_decompression(data_directory, data_output_directory)
    # init_improved_decompress(data_directory, data_output_directory)


# init_validator()


def main():
    init_validator()


if __name__ == '__main__':
    main()








    ## This Shortcut is for re-importing the completed CSV file into a pandas dataframe for verrifyng the data.
    # data = pd.read_csv('/Users/ericlingren/Desktop/test.csv')
    # data = pd.read_csv('/Volumes/Primary/Forex/historical-data/EURUSD/EURUSD-clean-data.csv')
    # print(data)
    # new = pd.to_datetime(data['TIME'], unit='ms')y
    # print(new)
    # for i, row in data.iterrows():
    #     print(row[0])







## PRACTICING MULTITHREADING

# import os
# import lzma
# import struct
# from multiprocessing import Pool

# dir_list = os.listdir(data_directory)
# sorted_files = sorted(dir_list)


# def decompress_data(files):
#     print(files)
    # chunk_size = 128
    # fmt = '>3i2f'
    # chunk_size = struct.calcsize(fmt)
    # data = []
    # with lzma.open(file) as f:
    #     while True:
    #         chunk = f.read(chunk_size)
    #         if chunk:
    #             data.append(struct.unpack(fmt, chunk))
    #         else:
    #             break
    # df = pd.DataFrame(data)
    # df.columns = ['TIME', 'ASKP', 'BIDP', 'ASKV', 'BIDV']
    
    # print(df)
    # res = write_file(file, df)

    # responses.append(res)
    # progress_bar(tasks, responses)



# if __name__ == '__main__':
#     with Pool(5) as p:
#         p.map(decompress_data, sorted_files)


