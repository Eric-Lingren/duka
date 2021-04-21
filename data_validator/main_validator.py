from .file_size import init_file_size_check
from .tick_deviations import init_tick_deviations
from .improved_decompress import init_improved_decompress
from .file_existence_tick_data import init_file_existence_ticks



def set_global_vars(current_commodity, current_year, dir_path):
    global currency
    global year 
    global base_directory
    global data_directory
    global log_directory
    global data_output_directory 
    global timeframe

    currency = current_commodity
    year = current_year
    base_directory = dir_path
    data_directory = f'{base_directory}/{currency}/{year}/raw-download-data' 
    log_directory = f'{base_directory}/{currency}/{year}'  
    data_output_directory = f'{base_directory}/{currency}/{year}/{currency}-{year}-ticks.csv' 
    timeframe = 'tick'  




def init_main_validator(currency, year, dir_path):
    set_global_vars(currency, year, dir_path)
    init_file_existence_ticks(data_directory, log_directory)
    init_file_size_check(data_directory, log_directory)
    # init_tick_deviations(data_directory, log_directory)
    init_improved_decompress(data_directory, data_output_directory)