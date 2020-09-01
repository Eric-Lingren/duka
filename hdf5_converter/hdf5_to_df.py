import os
import sys
import pandas as pd
import time


hdf5_filename = '/Volumes/External/test-data/test.h5'


start_time = time.time()


# This prints a list of all group names:
df = pd.DataFrame()
with pd.HDFStore(hdf5_filename) as hdf:
    keys = hdf.keys()
    print('\nHDF KEYS ARE: ')
    print(keys)


# # Reads a HDF5 datastore with only one dataset
# df = pd.read_hdf(hdf5_filename)
# print(df)


# Reads a portion of a HDF5 datastore with multiple datasets
df = pd.read_hdf(hdf5_filename, key='/FX_test-2020-1_tick')
# print(df)
print(df.head())



print("Completed in %s Seconds" % (time.time() - start_time))