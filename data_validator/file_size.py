import os
import asyncio
import logging
import time
from logger import config_logger
tasks = []
error_count = 0

def init_file_size_check(file_directory, log_directory):
    print('\n\nValidating file sizes...\n')
    global path
    path = file_directory

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


async def check_size(file):
    file_size = os.path.getsize(file)
    
    if file_size == 0:
        logger.warning(f'*** NO FILE DATA *** - {file} has no data and will fail decompression')
        print('******  WARNING  ****** - The following file has no data and will fail decompression:')
        print(file)
        
        val = input("\n Would you like to delete it? (y/n): ")
        if val == 'y':
            try:
                os.remove(file)
                print("\nFile was successfully deleted.\n\n")
                logger.info(f'*** FILE SUCCESSFULLY DELETED *** - {file} has been deleted')
            except:
                print("\nAttempted file deletion failed.  Please manually remove it.\n\n")
                logger.info(f'*** FILE FAILED DELETION *** - {file} was unable to be deleted')
        global error_count
        error_count = error_count+1
        


loop = asyncio.get_event_loop()

def build_tasks(sorted_files):
    start_time = time.time()
    for file in sorted_files:
        current_file = os.path.join(path, file)
        task = asyncio.ensure_future(check_size(current_file.format(current_file)))
        tasks.append(task)
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Canceling tasks...")

    print(f'\nFile Checking Completed in {time.time() - start_time} Seconds\n')

    result = ''
    if error_count > 0:
        result = f'***** ERROR ***** - There were {error_count} files found with no data. These should be resolved or decompresson of these files will likely cause an error. \nPlease check the log file in the directory you specified for more details.\n'
    else:
        result = f'*** SUCCESS - There were {error_count} files with problems.\n'
    print(result)
