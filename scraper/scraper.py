import asyncio
import requests
from datetime import date, timedelta
from aiohttp import ClientSession
import os.path
import os
import sys
import time
from tqdm import tqdm

# url = "https://datafeed.dukascopy.com/datafeed/AUDCAD/2020/07/03/04h_ticks.bi5"  # WORKING EXAMPLE PATH
url = 'https://datafeed.dukascopy.com/datafeed/PAIR/YYYY/MM/DD/HHh_ticks.bi5'
data_urls = []
requested_dates = []
tasks = []
responses = []



def initilize_scraper(requested_output_path, requested_currency, start_date, end_date):
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


# Builds the 24 unique urls needed for each day of tick data and saves those in the data_urls array 
def build_url(pair, date):
    year = f'{date.year}'
    month = f'{date.month}' if date.month > 9 else f'0{date.month}' 
    day = f'{date.day}' if date.day > 9 else f'0{date.day}' 
    hour = None
    for i in range(24):
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
    month = url.split('/')[-3]
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
                    response = await response.read()
                    with open(file_name, 'wb') as fd:
                        fd.write(response)
                    attempts = 5
                else:
                    attempts+=1
                responses.append(1)
                progress_status(len(tasks), responses)


loop = asyncio.get_event_loop()

def build_tasks():
    start_time = time.time()
    for url in data_urls:
        task = asyncio.ensure_future(get_data(url.format(url)))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
    print("--- Finished in %s Seconds ---" % (time.time() - start_time))



def progress_status(tasks, res):
    with tqdm(total=tasks) as pbar:
        for x in res:
            pbar.update(1)