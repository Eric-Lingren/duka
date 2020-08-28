from datetime import date
from scraper import initilize_scraper
import asyncio
from datetime import datetime, timedelta

# Declare config varibles here before running the run_main script
    # Change the output_path to the location you want the data files saved to
    # If None is used for the output_path the file will download in the directory where the script lives

output_path = '/Volumes/Primary/Forex/historical-data/EURUSD/2020/'  
# Other sample paths:
    # output_path = '/Users/ericlingren/Desktop/'  
    # output_path = None  
currency = 'EURUSD'
start_date = '2020-03-06'  # First date of data requested. Format =  'YYYY-MM-DD'
end_date = '2020-03-06'    # Last date of data requested. Format = 'YYYY-MM-DD'


def run_scraper(start_on, end_on):
    return initilize_scraper(
        output_path,
        currency,  
        start_on,
        end_on,
    )


def init_main():
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    iteration_start_date = ''
    iteration_end_date = end_date_obj - timedelta(days=1)

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

        run_scraper(iteration_start_date, iteration_start_date)

init_main()
