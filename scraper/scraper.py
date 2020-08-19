import duka
import asyncio
import requests
from datetime import date, timedelta

def initilize_scraper(currency, start_date, end_date):
    print(currency)
    print(start_date)
    print(end_date)

# url = "https://datafeed.dukascopy.com/datafeed/AUDCAD/2020/07/03/04h_ticks.bi5"
url = 'https://datafeed.dukascopy.com/datafeed/PAIR/YYYY/MM/DD/HHh_ticks.bi5'

urls = []

def compile_dates(requested_dates):
    # print(requested_dates) 
    for date in requested_dates:
        # print(date)
        build_url('AUDUSD', date)
    print(urls)




# def build_url(pair, year, month, day):
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
        urls.append(new_url)
    

# build_url('AUDCAD', '2020', '07', '03' )





requested_dates = []

def build_dates(start_date, end_date):
    delta = end_date - start_date       
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        print(day)
        requested_dates.append(day)
    compile_dates(requested_dates)   

# build_dates( date(2020, 2, 1), date(2020, 2, 1) )






def generate_file_name(url):
    pair = url.split('/')[-5]
    year = url.split('/')[-4]
    month = url.split('/')[-3]
    day = url.split('/')[-2]
    hour = url.split('/')[-1]
    name = f'{pair}-{year}-{month}-{day}-{hour}'
    return name


def get_data():
    file_name = generate_file_name(url)
    try:
        res = requests.get(url, allow_redirects=True)
        if res.status_code == 200:
            with open(file_name, 'wb') as fd:
                for chunk in res.iter_content(chunk_size=128):
                    fd.write(chunk)
    except:
        print('ERROR - FAILED')

# get_data()



# generate_file_name()