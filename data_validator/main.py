import pandas as pd
from file_existence import init_file_existence
from file_size import init_file_size_check
from decompress import init_file_decompression
from tick_deviations import init_tick_deviations

# DECLARE CONFIG VARIBLES HERE BEFORE RUNNING THE INIT_VALIDATOR SCRIPT :
    # Location where the data files are stored:
data_directory = '/Volumes/Primary/Forex/historical-data/EURUSD/2020'  
    # Location where you would like the log output file: 
        # Place in a differnt location from the data files to avoid problems.
log_directory = '/Users/ericlingren/Documents'  
    # Location where you would like the uncompressed ticks CSV File to be saved:
        # Place in a differnt location from the data files to avoid problems.
data_output_directory = '/Volumes/Primary/Forex/historical-data/EURUSD/EURUSD-clean-data.csv' 

## Alternative Sample Paths
# '/Volumes/Primary/Forex/historical-data/EURUSD/2020/'  
# /Users/ericlingren/Desktop
# '/Users/ericlingren/Documents/test.csv'


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


    ## These are quick function shortcuts that can be used to bypas the user input full scripts above
    # init_file_decompression(data_directory, data_output_directory)
    # init_tick_deviations(data_directory, log_directory)
    # init_file_size_check(data_directory)
    # init_file_decompression(data_directory, data_output_directory)

    ## This Shortcut is for re-importing the completed CSV file into a pandas dataframe for verrifyng the data.
    # data = pd.read_csv('/Users/ericlingren/Desktop/test.csv')
    # data = pd.read_csv('/Volumes/Primary/Forex/historical-data/EURUSD/EURUSD-clean-data.csv')
    # print(data)
    # new = pd.to_datetime(data['TIME'], unit='ms')y
    # print(new)
    # for i, row in data.iterrows():
    #     print(row[0])

init_validator()

