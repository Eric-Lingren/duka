import os


def create_downloads_folders(location, asset, year):
    try:
        if not os.path.isdir(f'{location}/{asset}'):
            os.mkdir(f'{location}/{asset}')
        if not os.path.isdir(f'{location}/{asset}/{year}'):
            os.mkdir(f'{location}/{asset}/{year}')
        if not os.path.isdir(f'{location}/{asset}/{year}/raw-download-data'):
            os.mkdir(f'{location}/{asset}/{year}/raw-download-data')
    except:
        raise Exception('\n--- Please ensure a folder, asset and year are selected ---\n')