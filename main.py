import time

from utilities.system_utilities import create_downloads_folders, create_csv_folders, organize_csv_files, zip_raw_downloads_data_folder
from downloaders.tick_downloader import Tick_Downloader
from validators.file_size_validator import File_Size_Validator
from decompression.bi5_decompression import Bi5_Decompression
from resamplers.data_resampler import Data_Resampler

class Main():
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
        print('Runtime (sec): ', end - start)
        print('\nCompleted! You may now run another task...\n')


