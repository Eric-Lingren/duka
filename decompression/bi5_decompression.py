import asyncio 
from glob import glob

class Bi5_Decompression():
    def __init__(self, settings):
        print('init')
        self.location = settings['location']
        self.asset = settings['asset']
        self.year = settings['year']
        self.input_dir = f'{self.location}/{self.asset}/{self.year}/raw-download-data'
        self.output_dir = f'{self.location}/{self.asset}/{self.year}/{self.asset}-{self.year}-ticks.csv'
        self.bi5_files = []
        self.processed_count = 0


    def build_decompression_tasks(self):
        files = [f for f in glob(self.input_dir  + "**/*.bi5")]
        self.bi5_files = sorted(files)


    def run_decompression_tasks(self):
        for file in self.bi5_files:
            self._decompress_file(file)


    def _decompress_file(self, file):
        print(file)



