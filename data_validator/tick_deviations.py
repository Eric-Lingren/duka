import os
import asyncio
import lzma
import struct
import pandas as pd
import time
from datetime import datetime
from statistics import mean, stdev
from progress_bar import progress_bar
from logger import config_logger

tasks = []
responses = []
file_tick_counts = []
deviation_violiation_count = 0

def init_tick_deviations(data_directory, log_directory):
    print('\n\nChecking Files for Tick Data Statistical Anomalies...\n')
    global path
    path = data_directory

    # Initilize logger for the file
    global log_path
    log_path = log_directory
    global logger
    logger = config_logger(log_path)
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
    print(f'\nFile Checking Completed in {time.time() - start_time} Seconds\n')
    tick_mean = int(mean(file_tick_counts))
    deviation = int(stdev(file_tick_counts))

    
    global deviation_violiation_count
    for i in range(len(file_tick_counts)):
        ticks = file_tick_counts[i]
        if ticks < tick_mean - 1 * deviation:
            deviation_violiation_count += 1
            logger.warn(f'*** LOW TICK DATA *** - {sorted_files[i]} has {ticks} ticks which is more than 1 standard deviation of {deviation} below the mean of {tick_mean} for this data set')

    result = ''
    if deviation_violiation_count > 0:
        result = f'***** WARNING ***** \nThere were {deviation_violiation_count} files found with tick data counts more than 1 standard deviation below the mean. \n\n     Mean Ticks per file in this data set : {tick_mean} \n     Standard Deviation for this data set : {deviation} \n\nThis could potentially be an indication of gaps in the data set. \nIt is recommended the logs be examined for more details. \n'
    else:
        result = f'*** SUCCESS - There were {deviation_violiation_count} files with low statistical deviation anomalies.\n'
    print(result)



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
    res = count_df_rows(df)
    responses.append(res)
    progress_bar(tasks, responses)


def count_df_rows(df):
    index = df.index
    number_of_rows = len(index)
    file_tick_counts.append(number_of_rows)
    return True
