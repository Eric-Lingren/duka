from logging import exception
import time
import sys
import os
from scraper import main_scraper
from data_validator import main_validator
from converters import resample_tick_to_bar
from converters import integrated_csv_to_hdf5

from utilities.system_utilities import create_downloads_folders
from loggers.logger import Logger


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
        self.init_downloader()


    def init_downloader(self):
        years = self.settings['years']
        years.sort()
        start = time.time()

        for year in years:
            self.settings['year'] = year
            create_downloads_folders(self.settings['location'], self.settings['asset'], year)
            downloader =  Downloader(self.settings)
            downloader.build_download_tasks()
            downloader.run_download_tasks()
            
            # print(sorted(downloader.errored_urls_set))
            sorted_errored_urls = sorted(downloader.errored_urls_set)
            for errored_url in sorted_errored_urls:
                print(errored_url)
            print('\ntotal tasks : ', len(downloader.urls))
            print('errored URLs : ', len(downloader.errored_urls_set))
            print('exceptions URLs : ', len(downloader.exception_urls_set))
            print('completed urls : ', len(downloader.completed_urls_set))
            total_failed_requests = downloader.errored_urls_set & downloader.exception_urls_set
            print('total failures : ', len(total_failed_requests))
            files = len([f for f in os.listdir(downloader.download_location)
                if os.path.isfile(os.path.join(downloader.download_location, f))])
            print('total files downloaded: ', files)

            download_logger = Logger(self.settings['location'], self.settings['asset'], year)

        end = time.time()
        print('Runtime (s): ', end - start)
        print('\nCompleted! You may now run another task...\n')


