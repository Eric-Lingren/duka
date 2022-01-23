import asyncio
import requests
from datetime import date, datetime, timedelta
import pytz
from aiohttp import ClientSession
import os.path
import os
import sys
import time
from tqdm import tqdm
import urllib.request

from io import BytesIO, DEFAULT_BUFFER_SIZE

# url = "https://datafeed.dukascopy.com/datafeed/AUDCAD/2020/07/03/04h_ticks.bi5"  # WORKING EXAMPLE PATH
url = 'https://datafeed.dukascopy.com/datafeed/PAIR/YYYY/MM/DD/HHh_ticks.bi5'
data_urls = []
requested_dates = []
tasks = []
responses = []



def initilize_tick_scraper(requested_output_path, requested_currency, start_date, end_date):
    global output_path
    output_path = requested_output_path
    global currency;
    currency = requested_currency
    build_dates(start_date, end_date)
    return True
    


# Calls the build_url function for each day of data requested
def compile_dates(requested_dates):
    for date in requested_dates:
        build_url(currency, date)
    build_tasks()

def is_dst(date):
    tz = pytz.timezone('US/Eastern')
    # date = datetime(2020, 8, 1)
    now = pytz.utc.localize(date)
    return now.astimezone(tz).dst() != timedelta(0)



# Builds the 24 unique urls needed for each day of tick data and saves those in the data_urls array 
def build_url(pair, date):
    hours = list(range(24))
    year = f'{date.year}'
    month_int = int(date.month)-1
    month = f'{month_int}' if date.month > 10 else f'0{month_int}' 
    day = f'{date.day}' if date.day > 9 else f'0{date.day}' 

    for i in hours:
        if i < 10:
            hour = f'0{i}'
        else:
            hour = f'{i}'
        new_url = url.replace('PAIR', pair)
        new_url = new_url.replace('YYYY', year)
        new_url = new_url.replace('MM', month)
        new_url = new_url.replace('DD', day)
        new_url = new_url.replace('HH', hour)
        data_urls.append(new_url)





#  Collates all the dates that will be required to build the array of urls
def build_dates(start_date, end_date):
    delta = end_date - start_date       
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        requested_dates.append(day)
        compile_dates(requested_dates)    


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
async def get_data(url):
    file_name = generate_file_name(url)
    attempts = 0
    while attempts < 5:
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    with open(file_name, 'wb') as fd:
                        fd.write(data)
                    attempts = 5
                else:
                    attempts+=1
                responses.append(1)
                # progress_status(len(tasks), responses)


loop = asyncio.get_event_loop()

def build_tasks():
    if len(data_urls) == 0:
        return
    start_time = time.time()
    for url in data_urls:
        task = asyncio.ensure_future(get_data(url.format(url)))
        tasks.append(task)

    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Canceling tasks...")
    cleanup()
    print("\n ----------------------------------------------------------------")
    print("|              Completed in %s Seconds            |" % (time.time() - start_time))
    print(" ----------------------------------------------------------------\n\n\n")


# def progress_status(tasks, res):
    # print(tasks)
    # print(res)
    # with tqdm(total=tasks) as pbar:
    #     for x in res:
    #         pbar.update(1)


def cleanup():
    tasks.clear()
    data_urls.clear()
    requested_dates.clear()
    responses.clear()