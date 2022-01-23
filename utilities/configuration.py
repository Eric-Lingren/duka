import os

class Configuration():
    def __init__(self, settings):
        self.location = settings['location']
        self.asset = settings['asset']
        self.year = settings['year']

    def build_downloads_folder_structure(self):
        try:
            if not os.path.isdir(f'{self.location}/{self.asset}'):
                os.mkdir(f'{self.location}/{self.asset}')
            if not os.path.isdir(f'{self.location}/{self.asset}/{self.year}'):
                os.mkdir(f'{self.location}/{self.asset}/{self.year}')
            if not os.path.isdir(f'{self.location}/{self.asset}/{self.year}/raw-download-data'):
                os.mkdir(f'{self.location}/{self.asset}/{self.year}/raw-download-data')
        except:
            raise Exception('\n--- Folder or asset not selected ---\n')