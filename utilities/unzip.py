import zipfile
import os

path_to_zip_file = open(os.path.expanduser("~/Desktop/HISTDATA_COM_MT_EURUSD_M12000.zip"))

# path_to_zip_file = '/Desktop/HISTDATA_COM_MT_EURUSD_M12000.zip'
directory_to_extract_to = '/Desktop'


with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)