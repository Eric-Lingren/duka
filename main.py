import time
from scraper import main_scraper
from data_validator import main_validator
from converters import resample_tick_to_bar
from converters import integrated_csv_to_hdf5

# Duka URL Tags
# XAGUSD XAUUSD BRENTCMDUSD GASCMDUSD SOYBEANCMDUSX SUGARCMDUSD

pair = 'BTCUSD'
# years = ['2020', '2019', '2018', '2017', '2016']
# years = ['2015', '2014', '2013', '2012', '2011', '2010']
# years = ['2009', '2008', '2007', '2006', '2005']
# years = ['2009', '2008']
# years = ['2016']
years = ['2021']
# years = ['2018', '2017', '2016']
# dir_path = '/Volumes/External/Trading/historical-data/forex'
# dir_path = '/Volumes/External/Trading/historical-data/commodities'
dir_path = '/Volumes/External/Trading/historical-data/crypto'
# dir_path = '/Users/ericlingren/Desktop'


start_time = time.time()

def scrape_resample_clean():
    for year in years:
        main_scraper.init_main_scraper(pair, year, dir_path)
        main_validator.init_main_validator(pair, year, dir_path)
        resample_tick_to_bar.init_resample_data(pair, year, dir_path)
        integrated_csv_to_hdf5.init_h5_conversion(pair, year, dir_path)
    print("\n\n **************    FULL PROCESS COMPLETED IN %s SECONDS    ******************* \n\n" % (time.time() - start_time))


def main():
    scrape_resample_clean()


if __name__ == '__main__':
    main()
