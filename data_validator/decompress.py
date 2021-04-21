import os
import lzma
import time
import struct
import asyncio
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta
from .progress_bar import progress_bar
from multiprocessing import Pool

tasks = []
responses = []

def init_file_decompression(data_directory, output_directory):
    print('\n\nDecompressing files and cleaning data...\n')
    global path
    path = data_directory
    global output_file
    output_file = output_directory
    start_loop()


def start_loop():
    dir_list = os.listdir(path)
    sorted_files = sorted(dir_list)
    build_tasks(sorted_files)


loop = asyncio.get_event_loop()



def build_tasks(sorted_files):
    start_time = time.time()

    for file in sorted_files:
        current_file = os.path.join(path, file)
        task = asyncio.ensure_future(decompress_data(current_file.format(current_file)))
        tasks.append(task)

        
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Canceling tasks...")
    print(f'\nFile Decompression Completed in {time.time() - start_time} Seconds\n')




async def decompress_data(file):
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
    res = write_file(file, df)

    responses.append(res)
    progress_bar(tasks, responses)



def write_file(file, df):
    year = int(file[-24:-20])
    month = int(file[-19:-17])
    day = int(file[-16:-14])
    hour = int(file[-13:-11])

    df = df.drop(columns=['ASKV', 'BIDV'])
    df = df.dropna()
    df = df.sort_values(by=['TIME'])


    # SAMPLE DATAFRAME FOR TESTING SMALL SETS:
    # df2 = pd.DataFrame(np.array([[1, 2, 3], [2, 5, 6], [1, 8, 9]]),
    # columns=['a', 'b', 'c'])
    # print('starting valuie : ')
    # print(df2)
    # df2 = df2.sort_values(by=['a'])

    # duplicateDFRow = df2[df2.duplicated(['a'])]
    # print(duplicateDFRow)
    # prev_val = ''
    # for i, row in df2.iterrows():
    #     print('----------------------------')
    #     if prev_val == row[0] :
    #         print("TEY ARE SAME TIME")
    #         # df2.drop(df2.index[i])
    #         df2.drop(i, inplace=True)
    #     else:
    #         print('not same')
    #     prev_val = row[0]
    # print('ending val :')
    # print(df2)


    file_date_object = datetime(year, month, day, hour)             # Build date object from integers in file name
    prev_row_time = ''  # Used from comparing current column to prev column in loop below

    for i, row in df.iterrows():
        if prev_row_time == row[0]:
            df.drop(i, inplace=True)    # Remove any rows from dataframe with duplicate timestamps
        else:
            time_stamp = file_date_object + timedelta(milliseconds=int(row[0]))
            df.at[i,'TIME'] = time_stamp
            ask = row[1]/100000     # Convert ASK price into decimal
            df.ASKP = df.ASKP.astype('float64') 
            df.at[i,'ASKP'] = ask
            bid = row[2]/100000     # Convert BID price into decimal
            df.BIDP = df.BIDP.astype('float64') 
            df.at[i,'BIDP'] = bid
        prev_row_time = row[0]
    
    # df['BIDP'] = pd.to_float64(df.BIDP)
    df['TIME'] = pd.to_datetime(df.TIME)
    # print(df)
    # df['BIDP'] = pd.to_float64(df.BIDP)

    df.to_csv(output_file, float_format='%g', date_format='%Y-%m-%d %H:%M:%S:%f', mode='a', header=False, index=False)
    return True



# pool = multiprocessing.Pool(multiprocessing.cpu_count())
# for current_task in tasks:
#     pool.apply_async(decompress_data, (current_file.format(current_file)))
# pool.close()
# pool.join()



# DATA FORMAT:

# [ TIME  ] [ ASKP  ] [ BIDP  ] [ ASKV  ] [ BIDV  ]

# TIME is a 32-bit big-endian integer representing the number of milliseconds that have passed since the beginning of this hour.
# ASKP is a 32-bit big-endian integer representing the asking price of the pair, multiplied by 100,000.
# BIDP is a 32-bit big-endian integer representing the bidding price of the pair, multiplied by 100,000.
# ASKV is a 32-bit big-endian floating point number representing the asking volume, divided by 1,000,000.
# BIDV is a 32-bit big-endian floating point number representing the bidding volume, divided by 1,000,000.





