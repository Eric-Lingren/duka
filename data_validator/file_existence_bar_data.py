import os
import time
from datetime import datetime, timedelta
from logger import config_logger



def init_file_existence_bars(file_directory, log_directory):
    print('\n\nChecking all files for existence...')
    global path
    path = file_directory

    # Initilize logger for the file
    global log_path
    log_path = log_directory
    global logger
    logger = config_logger(log_path)

    verify_files_exist()



def generate_expected_file_name(file):
    current_date = file[7:17]
    date_object = datetime.strptime(current_date, '%Y-%m-%d')
    tomorrow_date_obj =  date_object + timedelta(days=1)

    expected_year_int = tomorrow_date_obj.year
    expected_year = f"{expected_year_int}"

    expected_month = ''
    expected_month_int = tomorrow_date_obj.month
    if expected_month_int < 10:
        expected_month = f"0{expected_month_int}"
    else:
        expected_month = f"{expected_month_int}"

    expected_day = ''
    expected_day_int = tomorrow_date_obj.day
    if expected_day_int < 10:
        expected_day = f"0{expected_day_int}"
    else:
        expected_day = f"{expected_day_int}"

    expected_file_name = file[:7] + expected_year + file[11:12] + expected_month + file[14:15] + expected_day + file[17:]

    return expected_file_name



def verify_files_exist():
    start_time = time.time()
    dir_list = os.listdir(path)
    sorted_files = sorted(dir_list)
    current_file = sorted_files[0]
    expected_file_name = current_file
    file_validation_errors = 0

    for file in sorted_files:
        if file != expected_file_name:
            file_validation_errors += 1
            logger.error(f'*** MISSING FILE *** -  Expected: {expected_file_name}   Received: {file}')

        expected_file_name = generate_expected_file_name(file)

    print(f'\nFile Checking Completed in {time.time() - start_time} Seconds\n')
    if file_validation_errors == 0:
        print(f'Files Checked: \n{sorted_files[0]} - {sorted_files[-1]}\n')
        print('SUCCESS - All files existed. No Errors Found. :)\n\n')
    else:
        print(f'Files Checked: \n{sorted_files[0]} - {sorted_files[-1]}\n')
        print(f'***** FOUND {file_validation_errors} Missing file(s). \nPlease check the log file in the directory you specified for more details.\n\n')
