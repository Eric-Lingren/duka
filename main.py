from logging import exception
import time
import sys
import os
from scraper import main_scraper
from data_validator import main_validator
from converters import resample_tick_to_bar
from converters import integrated_csv_to_hdf5

from utilities.system_utilities import create_downloads_folders
# from loggers.logger import create_info_log


from downloader.downloader import Downloader
# Duka URL Tags
# XAGUSD XAUUSD BRENTCMDUSD GASCMDUSD SOYBEANCMDUSX SUGARCMDUSD BTCUSD

#! Set these varibles if you want to use the CLI
#! If you are using the gui, you only need to interact via that
pair = 'XAGUSD'
years = ['2020']
dir_path = '/Users/ericlingren/Desktop'

#* Example Data:
# years = ['2020', '2019', '2018', '2017', '2016']
# years = ['2009', '2008']
# dir_path = '/Volumes/External/Trading/historical-data/forex'
# dir_path = '/Volumes/External/Trading/historical-data/commodities'
# dir_path = '/Volumes/External/Trading/historical-data/crypto'


start_time = time.time()

def scrape_resample_clean():
    for year in years:
        main_scraper.init_main_scraper(pair, year, dir_path)
        main_validator.init_main_validator(pair, year, dir_path)
        resample_tick_to_bar.init_resample_data(pair, year, dir_path)
        #! HDF pandas conversion wont work on M1 chipsets
        # integrated_csv_to_hdf5.init_h5_conversion(pair, year, dir_path)
    print("\n\n **************    FULL PROCESS COMPLETED IN %s SECONDS    ******************* \n\n" % (time.time() - start_time))


def main():
    scrape_resample_clean()


def cancel_main():
    print('Gracefully Exiting App')
    sys.exit()


def start_main(download_asset, download_years, output_folder_selected):
    global pair
    pair = download_asset
    global years
    years = download_years
    global dir_path
    dir_path = output_folder_selected
    main()

if __name__ == '__main__':
    main()


class NewMain():
    def __init__(self, settings):
        self.settings = settings
        self.location = self.settings['location']
        self.asset = self.settings['asset']
        self.init_downloader()



    def init_downloader(self):
        years = self.settings['years']
        years.sort()
        start = time.time()

        for year in years:
            self.settings['year'] = year
            create_downloads_folders(self.location, self.asset, year)
            downloader =  Downloader(self.settings)
            downloader.build_download_tasks()
            downloader.run_download_tasks()

        end = time.time()
        print('Runtime (s): ', end - start)
        print('\nCompleted! You may now run another task...\n')


