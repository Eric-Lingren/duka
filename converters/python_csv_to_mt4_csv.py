import pandas as pd

def generate_mt4_data(filepath):
    mt4_dataset = pd.read_csv(filepath, parse_dates=['TIME'],)
    mt4_dataset.index = mt4_dataset['TIME'] 
    mt4_dataset.index = pd.to_datetime(mt4_dataset.index)
    mt4_dataset['date']= mt4_dataset.index.map(lambda t: t.strftime('%Y.%m.%d'))
    mt4_dataset['time']= mt4_dataset.index.map(lambda t: t.strftime('%H:%M'))
    mt4_dataset['volume']= mt4_dataset.index.map(lambda t: 0)
    mt4_dataset = mt4_dataset[[ 'date', 'time', 'open', 'high', 'low', 'close', 'volume']]
    mt4_dataset.reset_index(drop=True, inplace=True)
    mt4_output_filename = filepath.replace('py', 'mt4', 1)
    mt4_dataset.to_csv(mt4_output_filename, float_format='%g', mode='a', header=False, index=False)