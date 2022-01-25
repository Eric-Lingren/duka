import os, shutil
from os import listdir
from os.path import isfile, join

#* Contains reusable filesystem utilities


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


def create_csv_folders(location, asset, year):
    if not os.path.isdir(f'{location}/{asset}/{year}/csv-python-data'):
        os.mkdir(f'{location}/{asset}/{year}/csv-python-data')
    if not os.path.isdir(f'{location}/{asset}/{year}/csv-mt4-data'):
        os.mkdir(f'{location}/{asset}/{year}/csv-mt4-data')


def organize_csv_files(location, asset, year):
    base_folder = f'{location}/{asset}/{year}'
    all_files = [f for f in listdir(base_folder) if isfile(join(base_folder, f))]
    py_files = [f for f in all_files if 'py' in f]
    mt4_files = [f for f in all_files if 'mt4' in f]
    for name in py_files:
        source_file = os.path.join(f'{base_folder}/', name)
        dest_file = os.path.join(f'{base_folder}/csv-python-data', name)
        shutil.move(source_file, dest_file)
    for name in mt4_files:
        source_file = os.path.join(f'{base_folder}/', name)
        dest_file = os.path.join(f'{base_folder}/csv-mt4-data', name)
        shutil.move(source_file, dest_file)


def zip_raw_downloads_data_folder(location, asset, year):
    folder = f'{location}/{asset}/{year}/raw-download-data'
    try:
        shutil.make_archive(folder, 'zip', folder)
        try:
            shutil.rmtree(folder)
        except:
            print('failed deleting folder')
    except:
        print('failed compressing folder')