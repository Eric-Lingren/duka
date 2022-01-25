import sys, time

#* LEGACY ------------------------------------------- :
from scraper import main_scraper
from data_validator import main_validator
from converters import resample_tick_to_bar
from converters import integrated_csv_to_hdf5


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




#* NEW ------------------------------------------- :

from utilities.system_utilities import create_downloads_folders, create_csv_folders, organize_csv_files, zip_raw_downloads_data_folder
from downloaders.tick_downloader import Tick_Downloader
from validators.file_size_validator import File_Size_Validator
from decompression.bi5_decompression import Bi5_Decompression
from resamplers.data_resampler import Data_Resampler

class NewMain():
    def __init__(self, settings):
        self.settings = settings
        self.location = self.settings['location']
        self.asset = self.settings['asset']
        self.years = self.settings['years']


    def init_downloader(self):
        start = time.time()

        for year in self.years:
            self.settings['year'] = year
            create_downloads_folders(self.location, self.asset, year)
            downloader =  Tick_Downloader(self.settings)
            downloader.build_download_tasks()
            downloader.run_download_tasks()
            file_size_validator = File_Size_Validator(self.settings)
            file_size_validator.build_file_size_validation_tasks()
            file_size_validator.run_file_size_validation_tasks()
            file_decompression = Bi5_Decompression(self.settings)
            file_decompression.run_file_decompression()
            data_resampler = Data_Resampler(self.settings)
            data_resampler.resample_tick_data()

            # Cleanups & Organization
            create_csv_folders(self.location, self.asset, year)
            organize_csv_files(self.location, self.asset, year)
            zip_raw_downloads_data_folder(self.location, self.asset, year)

        end = time.time()
        print('Runtime (s): ', end - start)
        print('\nCompleted! You may now run another task...\n')


