import logging

class Logger():
    def __init__(self, location, asset, year):
        self.config = logging.basicConfig(
            filename = f'{location}/{asset}/{year}/example.log', 
            encoding='utf-8', 
            level=logging.DEBUG
        )

    def create_download_log():
        print('in download log')

logging.debug('This is debug message')
logging.info('This is information message')
logging.warning('This is warning message')
logging.error('This is warning message')