import asyncio
import requests
from datetime import date, timedelta
import os.path
import os
import sys


# url = "https://datafeed.dukascopy.com/datafeed/EURUSD/2020/00/03/BID_candles_min_1.bi5"  # WORKING EXAMPLE PATH
url = 'https://datafeed.dukascopy.com/datafeed/PAIR/YYYY/MM/DD/BID_candles_TIMEFRAME.bi5'
data_urls = []
requested_dates = []
tasks = []
responses = []



def initilize_bar_scraper(requested_output_path, requested_currency, start_date, end_date, time_frame):
    global output_path
    output_path = requested_output_path
    global currency;
    currency = requested_currency
    global timeframe
    timeframe = time_frame
    compile_date(start_date)
    return responses



# Calls the build_url function for each day of data requested
def compile_date(start_date):
    weekday = start_date.weekday()
    if weekday != 5: # Ignores all Saturdays
        requested_dates.append(start_date) 
    else:
        print('SATURDAY - Skipping Date')
    build_url(start_date)



# Builds the 24 unique urls needed for each day of tick data and saves those in the data_urls array 
def build_url(date):
    month_int = int(date.month)-1
    year = f'{date.year}'
    month = f'{month_int}' if date.month > 9 else f'0{month_int}' 
    day = f'{date.day}' if date.day > 9 else f'0{date.day}' 

    new_url = url.replace('PAIR', currency)
    new_url = new_url.replace('YYYY', year)
    new_url = new_url.replace('MM', month)
    new_url = new_url.replace('DD', day)
    new_url = new_url.replace('TIMEFRAME', timeframe)
    get_data(new_url)



#  Builds a dynamic file names for the data that will be downloaded
def generate_file_name(url):
    pair = url.split('/')[-5]
    year = url.split('/')[-4]
    orig_month = int(url.split('/')[-3])+1
    month = f'{orig_month}' if orig_month > 9 else f'0{orig_month}' 
    day = url.split('/')[-2]
    hour = url.split('/')[-1]
    name = f'{pair}-{year}-{month}-{day}-{hour}'
    complete_name = None
    if output_path != None:
        complete_name = os.path.join(output_path, name)
    else:
        complete_name = name  
    return complete_name



# Data Fetcher
def get_data(url):
    file_name = generate_file_name(url)
    attempts = 0

    while attempts < 5:
        r = requests.get(url, allow_redirects=True)
        if len(r.content) > 0:
            open(file_name, 'wb').write(r.content)
            attempts = 5
            responses.append(1)
        else:
            attempts+=1
