from datetime import date
import asyncio
from datetime import datetime, timedelta
from tqdm import tqdm
from tick_scraper import initilize_tick_scraper
from bar_scraper import initilize_bar_scraper

# Declare config varibles here before running the run_main script
    # Change the output_path to the location you want the data files saved to
    # If None is used for the output_path the file will download in the directory where the script lives

output_path = '/Volumes/Primary/Trading/historical-data/forex/EURUSD/2017/ticks'  
# Other sample paths:
    # output_path = '/Users/ericlingren/Desktop/'  
    # output_path = None  
currency = 'EURUSD'
start_date = '2017-01-01'  # First date of data requested. Format =  'YYYY-MM-DD'
end_date = '2017-01-02'    # Last date of data requested. Format = 'YYYY-MM-DD'
timeframe = 'tick'    # tick, min_1, etc


def run_scraper(start_on, end_on, task_count):
    if timeframe == 'tick':
        return initilize_tick_scraper(
            output_path,
            currency,  
            start_on,
            end_on
        )
    else:
        res = initilize_bar_scraper(
            output_path,
            currency,  
            start_on,
            end_on,
            timeframe
        )
        # print(res)
        with tqdm(total=task_count) as pbar:
            for x in res:
                pbar.update(1)

        

def init_main():
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


init_main()




# https://datafeed.dukascopy.com/datafeed/EURUSD/2019/00/02/23h_ticks.bi5   # January 2
# https://datafeed.dukascopy.com/datafeed/EURUSD/2019/01/05/02h_ticks.bi5   # Feb 5
# https://datafeed.dukascopy.com/datafeed/EURUSD/2019/08/04/01h_ticks.bi5   # Sept 3
# https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/03/00h_ticks.bi5  # October 3

# https://datafeed.dukascopy.com/datafeed/EURUSD/2019/06/05/21h_ticks.bi5