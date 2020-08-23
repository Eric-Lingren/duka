from datetime import date
from scraper import initilize_scraper
import asyncio


# Declare config varibles here before running the run_main script
    # Change the output_path to the path you want the file to save in
    # If None is used for the output_path the file will download in the directory where the script lives

# output_path = '/Users/ericlingren/Desktop/'  
output_path = '/Volumes/Primary/Forex/historical-data/AUDCAD/2020/07'  
# output_path = None  
currency = 'AUDCAD'
# start_year =  2020
# start_month =  7
# start_day = 3
# end_year =  2020
# end_month =  7
# end_day =  3
start_year =  2020
start_month =  7
start_day = 1
end_year =  2020
end_month =  7
end_day =  7


def run_main():
    return initilize_scraper(
        output_path,
        currency,  
        date(start_year, start_month, start_day), 
        date(end_year, end_month, end_day) )

def init():
    response = run_main()
    print(response)

init()
