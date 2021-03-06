import os
import sys
import pandas as pd
import time
import datetime


# hdf5_filename = '/Users/ericlingren/Desktop/week-1.h5'
# hdf5_filename2 = '/Users/ericlingren/Desktop/week-2.h5'
# hdf5_filename = '/Users/ericlingren/Desktop/EURUSD-2019-1D.h5'
# hdf5_filename = '/Volumes/External/Trading/historical-data/forex/EURUSD/2019/EURUSD-2019-1Min.h5'
# hdf5_filename = '/Volumes/External/Trading/historical-data/forex/EURUSD/2018/EURUSD-2018-1Min.h5'
# hdf5_filename = '/Volumes/External/Trading/historical-data/forex/EURUSD/2021/h5/USDJPY-2020-1M.h5'
hdf5_filename = '/Volumes/External/Trading/historical-data/forex/EURUSD/2013/h5/EURUSD-2013-1Min.h5'


start_time = time.time()


# This prints a list of all group names:
df = pd.DataFrame()
with pd.HDFStore(hdf5_filename) as hdf:
    keys = hdf.keys()
    print('\nHDF KEYS ARE: ')
    print(keys)


# # Reads a HDF5 datastore with only one dataset
df = pd.read_hdf(hdf5_filename)
print(df.tail())

count_row = df.shape[0]
print(count_row)

# print(df.iloc[0].index)
# print(type(df.index[0]))
# print(df.index[0])


# # Reads a portion of a HDF5 datastore with multiple datasets
# df = pd.read_hdf(hdf5_filename, key='/FX_week-1_tick')
# # print(df)
# print(df.head())


# # Combines multiple hdf files into 1 DF
# df1 = pd.read_hdf(hdf5_filename)
# df2 = pd.read_hdf(hdf5_filename2)
# frames = [df1, df2]
# df = pd.concat(frames)
# df.sort_index()
# print(df.head())
# print(df.tail())


# # Obtain only a specific date range from the hdf 
# start_date = '2020-01-02'
# end_date = '2020-01-03'

# start_date = str(pd.Timestamp(start_date))
# end_date = str(pd.Timestamp(end_date))

# query = 'index>"' + start_date + '" & index<"' + end_date + '"'

# df = pd.read_hdf(hdf5_filename, where=query)
# print(df.head())
# print(df.tail())




print("Completed in %s Seconds" % (time.time() - start_time))


