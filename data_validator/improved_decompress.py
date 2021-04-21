import os
import time
import lzma
import struct
import pandas as pd
from glob import glob
from datetime import datetime
from .progress_bar import progress_bar



responses = []
start_time = time.time()

def init_improved_decompress(data_directory, output_directory):
    print('\n\nDecompressing files and cleaning data...\n')
    global path
    global output_file
    path = data_directory
    output_file = output_directory
    begin()


def begin():
    files = [f for f in glob(path + "**/*.bi5")]
    files.sort()

    for file in files:
        decompress_data(file)
        responses.append(True)
        progress_bar(files, responses)

    print(f'\nFile Decompression Completed in {time.time() - start_time} Seconds\n')



def decompress_data(file):
    chunk_size = 128
    fmt = '>3i2f'
    chunk_size = struct.calcsize(fmt)
    data = []
    with lzma.open(file) as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                data.append(struct.unpack(fmt, chunk))
            else:
                break
    df = pd.DataFrame(data)
    df.columns = ['TIME', 'ASKP', 'BIDP', 'ASKV', 'BIDV']
    # df.columns = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']

    #  CLEANS UP COLUMNS
    df = df.drop(columns=['ASKV', 'BIDV'])
    df = df.dropna()

    #  CLEANS UP TIMES
    year = int(file[-24:-20])
    month = int(file[-19:-17])
    day = int(file[-16:-14])
    hour = int(file[-13:-11])
    df = df.sort_values(by=['TIME'])
    df.drop_duplicates(subset ="TIME", inplace=True, keep = False) 
    file_date_object = datetime(year, month, day, hour)   # Build date object from integers in file name
    ms_since_epoch = file_date_object.timestamp() * 1000 # converts the file date to ms since epoch
    df['TIME'] = pd.to_datetime(df['TIME'] + ms_since_epoch, unit='ms') # adds timestamp + epoch offset and converts format

    # CONVERTS VALUES INTO DECIMALS
    df['ASKP'] = df['ASKP'].astype('float64') 
    df['ASKP'] = df['ASKP'].div(100000)
    df['BIDP'] = df['BIDP'].astype('float64') 
    df['BIDP'] = df['BIDP'].div(100000)

    df.to_csv(output_file, float_format='%g', date_format='%Y-%m-%d %H:%M:%S:%f', mode='a', header=False, index=False)

    return True
