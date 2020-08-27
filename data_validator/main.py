import pandas as pd
from file_existence import init_file_existence
from file_size import init_file_size_check
from decompress import init_file_decompression
from tick_deviations import init_tick_deviations

# Declare config varibles here before running the init_validator script
data_directory = '/Users/ericlingren/Desktop'   # Location where the dat files are stored
log_directory = '/Users/ericlingren/Documents'  # Location where you would like the log output file. Place in a differnt location from the data files to avoid problems.
data_output_directory = '/Users/ericlingren/Documents/test.csv' # Location where you would like the uncompressed ticks saved

def init_validator():
    init_file_existence(data_directory, log_directory)
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
                init_file_decompression(data_directory, data_output_directory)

    # init_file_decompression(data_directory, data_output_directory)
    # init_tick_deviations(data_directory, log_directory)
    # init_file_size_check(data_directory)
    # init_file_decompression(data_directory, data_output_directory)

    # data = pd.read_csv('/Users/ericlingren/Desktop/test.csv')
    # print(data)
    # new = pd.to_datetime(data['TIME'], unit='ms')
    # print(new)
    # for i, row in data.iterrows():
    #     print(row[0])



init_validator()

