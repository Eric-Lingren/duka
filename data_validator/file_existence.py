import os
from datetime import datetime, timedelta


def init_file_existence(file_directory):
    global path
    path = file_directory
    verify_files_exist()


def generate_expected_hour(current_hour):
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
    dir_list = os.listdir(path)
    sorted_files = sorted(dir_list)
    current_file = sorted_files[2]
    expected_file_name = current_file
    file_validation_errors = 0
    error_string = ''

    for file in sorted_files[2:]:
        if file != expected_file_name:
            file_validation_errors += 1
            error_string = error_string + f'ERROR #{file_validation_errors} --  Expected: {expected_file_name}   Received: {file} \n'
            
        current_hour = file[18:20]
        expected_hour_string = generate_expected_hour(current_hour)
        expected_day_string = generate_expected_day(file, expected_hour_string)
        expected_month_string = generate_expected_month(file, expected_hour_string)
        expected_year_string = generate_expected_year(file, expected_hour_string)
        expected_file_name = generate_expected_file_name(file, expected_year_string, expected_month_string, expected_day_string, expected_hour_string)

    if file_validation_errors == 0:
        print('\n\n---------- FILE EXISTENCE COMPLETION LOG ----------\n')
        print(f'Files Checked: \n{sorted_files[2]} - {sorted_files[-1]}\n')
        print('SUCCESS - All files existed. No Errors Found. :) \n\n')
    else:
        print('\n\n---------- FILE EXISTENCE COMPLETION LOG ----------\n')
        print(f'Files Checked: \n{sorted_files[2]} - {sorted_files[-1]}\n')
        print(f'***** FOUND {file_validation_errors} ERROR(s) - Missing the following files: *****')
        print(f'{error_string}\n\n')

