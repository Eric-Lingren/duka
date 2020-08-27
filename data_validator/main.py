from file_existence import init_file_existence
from file_size import init_file_size_check
from decompress import init_file_decompression

import pandas as pd

# Declare config varibles here before running the init_validator script
file_directory = '/Users/ericlingren/Desktop'


def init_validator():
    # init_file_existence(file_directory)
    # val = input("Would you like to proceed to data cleaning? (y/n): ")
    # if val != 'y':
    #     print("Program Terminating.")
    # else:
    #     print('Carrying on then bud!')
    #     init_file_decompression(file_directory)
    init_file_size_check(file_directory)
    # init_file_decompression(file_directory)

    # data = pd.read_csv('/Users/ericlingren/Desktop/test.csv')
    # print(data)
    # new = pd.to_datetime(data['TIME'], unit='ms')
    # print(new)
    # for i, row in data.iterrows():
    #     print(row[0])



init_validator()

