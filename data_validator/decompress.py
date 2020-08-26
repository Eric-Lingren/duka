import lzma
import struct
import pandas as pd

def decompress_data():
    print('ran')
    chunk_size = 128
    fmt = '>3i2f'
    chunk_size = struct.calcsize(fmt)
    data = []
    with lzma.open('../scraper/test.bi5') as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                data.append(struct.unpack(fmt, chunk))
            else:
                break
    df = pd.DataFrame(data)
    print(df)
    return df

# decompress_data()


# DATA FORMAT:

# [ TIME  ] [ ASKP  ] [ BIDP  ] [ ASKV  ] [ BIDV  ]

# TIME is a 32-bit big-endian integer representing the number of milliseconds that have passed since the beginning of this hour.
# ASKP is a 32-bit big-endian integer representing the asking price of the pair, multiplied by 100,000.
# BIDP is a 32-bit big-endian integer representing the bidding price of the pair, multiplied by 100,000.
# ASKV is a 32-bit big-endian floating point number representing the asking volume, divided by 1,000,000.
# BIDV is a 32-bit big-endian floating point number representing the bidding volume, divided by 1,000,000.





