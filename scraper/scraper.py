import asyncio
import requests
from datetime import date, timedelta
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



def initilize_scraper(requested_output_path, requested_currency, start_date, end_date):
    global output_path
    output_path = requested_output_path
    global currency;
    currency = requested_currency
    build_dates(start_date, end_date)
    # test_download('https://datafeed.dukascopy.com/datafeed/EURUSD/2020/01/02/22h_ticks.bi5')
    return True
    


# Calls the build_url function for each day of data requested
def compile_dates(requested_dates):
    for date in requested_dates:
        build_url(currency, date)
    build_tasks()


# Builds the 24 unique urls needed for each day of tick data and saves those in the data_urls array 
def build_url(pair, date):
    weekday = date.weekday()
    hours = list(range(24))

    if weekday == 4:
        del hours[15:]  # Its Friday, market closes at 15:00 - dont include any files after that time
    if weekday == 6:
        del hours[:22]  # Its Sunday, market opens at 22:00GMT - dont include any files before that time

    month_int = int(date.month)-1
    year = f'{date.year}'
    month = f'{month_int}' if date.month > 9 else f'0{month_int}' 
    day = f'{date.day}' if date.day > 9 else f'0{date.day}' 
    hour = None

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
        weekday = day.weekday()
        if weekday != 5: # Ignores all Saturdays
            requested_dates.append(day)
            compile_dates(requested_dates)  
        else:
            print('SATURDAY - Skipping Date')
    # print(requested_dates)
    # compile_dates(requested_dates)   


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
                progress_status(len(tasks), responses)

        # try:
        #     res = await loop.run_in_executor(None, lambda: requests.get(url, stream=True))
        #     if res.status_code == 200:
        #         print(res.status_code)
        #         for chunk in res.iter_content(DEFAULT_BUFFER_SIZE):
        #             print(chunk)
        #             buffer.write(chunk)
        #         # Logger.info("Fetched {0} completed in {1}s".format(id, time.time() - start))
        #         if len(buffer.getbuffer()) <= 0:
        #             print('empty format')
        #             # Logger.info("Buffer for {0} is empty ".format(id))
        #         # return buffer.getbuffer()
        #     else:
        #         print('error')
        #         # Logger.warn("Request to {0} failed with error code : {1} ".format(url, str(res.status_code)))
        # except Exception as e:
        #     print('task failed')
        #     # Logger.warn("Request {0} failed with exception : {1}".format(id, str(e)))
        #     # time.sleep(0.5 * i)


loop = asyncio.get_event_loop()

def build_tasks():
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


def progress_status(tasks, res):
    with tqdm(total=tasks) as pbar:
        for x in res:
            pbar.update(1)


def cleanup():
    tasks.clear()
    data_urls.clear()
    requested_dates.clear()
    responses.clear()



# Data Fetcher
def test_download(url):
    file_name = generate_file_name(url)
    # attempts = 0
    # print(url)
    # # loop = asyncio.get_event_loop()
    # # buffer = BytesIO()


    # r = requests.get(url)
    # print(r)
    # print(r.status_code)
    # # data = r.json()
    # print(r.headers["content-type"])
    # x = urllib.request.urlopen(url)
    # print(x.read())
    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    print(meta)
    # file_size = int(meta.getheaders("Content-Length")[0])
    # print(file_size)
    # print("Downloading: %s Bytes: %s" % (file_name, file_size))

    # file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        print(buffer)
        if not buffer:
            break

    #     file_size_dl += len(buffer)
    #     f.write(buffer)
    #     status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    #     status = status + chr(8)*(len(status)+1)
    #     print(status)

    # f.close()


    # while attempts < 5:
    #     async with ClientSession() as session:
    #         async with session.get(url) as response:
                
    #             if response.status == 200:
    #                 data = await response.read()
    #                 print(data)
    #                 with open(file_name, 'wb') as fd:
    #                     fd.write(data)
    #                 attempts = 5
    #             else:
    #                 attempts+=1
    #             responses.append(1)
    #             progress_status(len(tasks), responses)

