import os
import time
import pytz
from .logger import config_logger
from datetime import datetime, timedelta

def init_file_existence_ticks(file_directory, log_directory):
    print('\n\nChecking all files for existence...')
    global path
    path = file_directory
    print(path)

    # Initilize logger for the file
    global log_path
    log_path = log_directory
    global logger
    logger = config_logger(log_path)

    verify_files_exist()

def is_dst(date):
    tz = pytz.timezone('US/Eastern')
    # date = datetime(2020, 8, 1)
    now = pytz.utc.localize(date)
    return now.astimezone(tz).dst() != timedelta(0)



def generate_expected_hour(file, current_hour):
    current_date = file[7:17]
    date_object = datetime.strptime(current_date, '%Y-%m-%d')
    weekday = date_object.weekday()

    christmas = datetime(date_object.year, 12, 25) #  Its chrismas day, market is closed from 0800 - 2200 gmt
    if date_object == christmas and int(current_hour) == 7:
        expected_hour_int = int(current_hour)+15
        expected_hour = f"{expected_hour_int}"
        return expected_hour


    # if(is_dst(date) == False):   # Its not day light savings on Sunday, market opens at 2200 gmt
    #     del hours[22:]  
    # else:   # It is not day light savings on Sunday, market opens at 2100 gmt
    #     del hours[21:] 


    # For For Non-Daylight Savings (Winter):
    if weekday == 4 and int(current_hour) == 21 and is_dst(date_object) == False: # Its Friday market close, set up for expecting next file on Sunday @ 22:00
        expected_hour_int = int(current_hour)+1

        # if(is_dst(date_object) == False):   # Its not day light savings
        #     expected_hour_int = int(current_hour)+9
        # else:   # It is day light savings
        #     expected_hour_int = int(current_hour)+8


    # For Daylight Savings (Summer):
    if weekday == 4 and int(current_hour) == 20 and is_dst(date_object): # Its Friday market close, set up for expecting next file on Sunday @ 22:00
        expected_hour_int = int(current_hour)+1

    else:
        expected_hour_int = int(current_hour)+1
        expected_hour = ''

    if expected_hour_int < 10:
        expected_hour = f"0{expected_hour_int}"
    elif expected_hour_int == 24:
        expected_hour = "00"
    else:
        expected_hour = f"{expected_hour_int}"
    return expected_hour


def generate_expected_day(file, expected_hour_string):
    current_date = file[7:17]
    expected_day = ''
    if expected_hour_string == '00':
        date_object = datetime.strptime(current_date, '%Y-%m-%d')
        tomorrow_date_obj =  date_object + timedelta(days=1)
        expected_day_int = tomorrow_date_obj.day
        if expected_day_int < 10:
            expected_day = f"0{expected_day_int}"
        else:
            expected_day = f"{expected_day_int}"
    else :
        current_date = file[7:17]
        date_object = datetime.strptime(current_date, '%Y-%m-%d')
        weekday = date_object.weekday()

        if weekday == 4 and int(expected_hour_string) == 22 and is_dst(date_object) == False: # Its market close, set up for expecting next file on Sunday @ 22:00
            sunday_date_obj =  date_object + timedelta(days=2)
            expected_day_int = sunday_date_obj.day
            if expected_day_int < 10:
                expected_day = f"0{expected_day_int}"
            else:
                expected_day = f"{expected_day_int}"
        elif weekday == 4 and int(expected_hour_string) == 21 and is_dst(date_object):
            sunday_date_obj =  date_object + timedelta(days=2)
            expected_day_int = sunday_date_obj.day
            if expected_day_int < 10:
                expected_day = f"0{expected_day_int}"
            else:
                expected_day = f"{expected_day_int}"
        else:
            expected_day = current_date[8:10]

    return expected_day


def generate_expected_month(file, expected_hour_string):
    current_date = file[7:17]
    expected_month = ''
    if expected_hour_string == '00':
        date_object = datetime.strptime(current_date, '%Y-%m-%d')
        tomorrow_date_obj =  date_object + timedelta(days=1)
        expected_month_int = tomorrow_date_obj.month
        if expected_month_int < 10:
            expected_month = f"0{expected_month_int}"
        else:
            expected_month = f"{expected_month_int}"
    else :
        date_object = datetime.strptime(current_date, '%Y-%m-%d')
        weekday = date_object.weekday()
        #  Its daylight Savings (winter) & market close, set up for expecting next file on Sunday @ 22:00
        if weekday == 4 and int(expected_hour_string) == 22 and is_dst(date_object) == False: 
            sunday_date_obj =  date_object + timedelta(days=2)
            expected_month_int = sunday_date_obj.month
            if expected_month_int < 10:
                expected_month = f"0{expected_month_int}"
            else:
                expected_month = f"{expected_month_int}"
        #  Its Non-Daylight Savings (summer) & market close, set up for expecting next file on Sunday @ 22:00
        elif weekday == 4 and int(expected_hour_string) == 21 and is_dst(date_object):
            sunday_date_obj =  date_object + timedelta(days=2)
            expected_month_int = sunday_date_obj.month
            if expected_month_int < 10:
                expected_month = f"0{expected_month_int}"
            else:
                expected_month = f"{expected_month_int}"
        else:
            expected_month = current_date[5:7]

    return expected_month



def generate_expected_year(file, expected_hour_string):
    current_date = file[7:17]
    expected_year = ''
    if expected_hour_string == '00':
        date_object = datetime.strptime(current_date, '%Y-%m-%d')
        tomorrow_date_obj =  date_object + timedelta(days=1)
        expected_year_int = tomorrow_date_obj.year
        expected_year = f"{expected_year_int}"
    else :
        expected_year = current_date[0:4]
    return expected_year


def generate_expected_file_name(file, expected_year, expected_month, expected_day, expected_hour):
    expected_file_name = file[:7] + expected_year + file[11:12] + expected_month + file[14:15] + expected_day + file[17:18] + expected_hour + file[20:]
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
            # error_string = error_string + f'ERROR #{file_validation_errors} --  Expected: {expected_file_name}   Received: {file} \n'
            
        current_hour = file[18:20]
        expected_hour_string = generate_expected_hour(file, current_hour)
        expected_day_string = generate_expected_day(file, expected_hour_string)
        expected_month_string = generate_expected_month(file, expected_hour_string)
        expected_year_string = generate_expected_year(file, expected_hour_string)
        expected_file_name = generate_expected_file_name(file, expected_year_string, expected_month_string, expected_day_string, expected_hour_string)

    print(f'\nFile Checking Completed in {time.time() - start_time} Seconds\n')
    if file_validation_errors == 0:
        print(f'Files Checked: \n{sorted_files[0]} - {sorted_files[-1]}\n')
        print('SUCCESS - All files existed. No Errors Found. :)\n\n')
    else:
        print(f'Files Checked: \n{sorted_files[0]} - {sorted_files[-1]}\n')
        print(f'***** FOUND {file_validation_errors} Missing file(s). \nPlease check the log file in the directory you specified for more details.\n\n')


