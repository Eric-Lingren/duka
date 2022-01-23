import os
import asyncio
from tqdm import tqdm
from datetime import date
from datetime import datetime, timedelta
from .tick_scraper import initilize_tick_scraper


def set_global_vars(current_commodity, current_year, dir_path):
    global currency
    global year 
    global base_directory
    global output_path
    global start_date 
    global end_date 
    global timeframe
    currency = current_commodity
    year = current_year
    base_directory = dir_path
    output_path = f'{base_directory}/{currency}/{year}/raw-download-data'
    start_date = f'{year}-01-01'    # First date of data requested. Format =  'YYYY-MM-DD'
    # end_date = f'{year}-12-31'      # Last date of data requested. Format = 'YYYY-MM-DD'
    end_date = f'{year}-01-02'      # Last date of data requested. Format = 'YYYY-MM-DD'
    timeframe = 'tick'  


def build_nonexisting_directories():
    if not os.path.isdir(f'{base_directory}/{currency}'):
        os.mkdir(f'{base_directory}/{currency}')
    if not os.path.isdir(f'{base_directory}/{currency}/{year}'):
        os.mkdir(f'{base_directory}/{currency}/{year}')
    if not os.path.isdir(f'{base_directory}/{currency}/{year}/raw-download-data'):
        os.mkdir(f'{base_directory}/{currency}/{year}/raw-download-data')



def run_scraper(start_on, end_on, task_count):
    return initilize_tick_scraper(
        output_path,
        currency,  
        start_on,
        end_on
    )
    # Prints status bars:
    # with tqdm(total=task_count) as pbar:
    #     for x in res:
    #         pbar.update(1)



def init_main_scraper(currency, year, dir_path):
    set_global_vars(currency, year, dir_path)
    build_nonexisting_directories()

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    iteration_start_date = ''
    iteration_end_date = end_date_obj - timedelta(days=1)
    day_diff = end_date_obj- start_date_obj
    task_count = day_diff.days+1

    count = 0
    while ( iteration_end_date <= end_date_obj):
        if count == 0 :
            iteration_start_date = start_date_obj - timedelta(days=0) 
            iteration_end_date = iteration_start_date + timedelta(days=1) 
        else :
            iteration_start_date = iteration_end_date + timedelta(days=0)  
            iteration_end_date = iteration_start_date + timedelta(days=1)
        count += 1
        print('\n------------------------------------------------------------------')
        print('                       GETTING DATA FOR:')
        print(f"                            {currency}")
        print(f"                      {iteration_start_date}")
        print('------------------------------------------------------------------\n')
        run_scraper(iteration_start_date, iteration_start_date, task_count)
        # return

