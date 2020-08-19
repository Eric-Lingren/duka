from datetime import date
from scraper import initilize_scraper

currency = 'AUDUSD'
start_year =  2020
start_month =  2
start_day = 1
end_year =  2020
end_month =  3
end_day =  7

def run_main():
    initilize_scraper(
        currency,  
        date(start_year , start_month, start_day), 
        date(end_year, end_month, end_day) )

run_main()