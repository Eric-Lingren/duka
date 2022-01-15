import tkinter as tk
from tkinter import ttk
from tkinter import Label
from tkinter import Text
from tkinter import filedialog

# from main import main_gui
# Global Option Select Varibles
forex_options_list = ["EURAUD", "SGDJPY", "AUDUSD", "USDGBP"]
commodity_options_list = ["XAUUSD", "XAGUSD", ]
crypto_options_list = ["BTCUSD", "ETHUSD", "LTCUSD" ]
metal_options_list = ["BTCUSD", "ETHUSD", "LTCUSD" ]
indice_options_list = ["BTCUSD", "ETHUSD", "LTCUSD" ]
bond_options_list = ["BTCUSD", "ETHUSD", "LTCUSD" ]


# Configures Global App Settings
window = tk.Tk()
window.title('DukasCopy Download Scraper')
window.geometry('700x500')



def handle_chosen_asset(asset):
    print(asset)
    global download_asset
    download_asset = asset
    return None


# Renders Forex pairs submenu if forex is chosen from main asset class list
# def render_forex_menu():
forex_options_list.sort()
selected_forex_pair = tk.StringVar(window)
selected_forex_pair.set("Select A Forex Pair")
forex_options = tk.OptionMenu(window, selected_forex_pair, *forex_options_list)

def handle_fx_selected(*args):
    selected_asset = selected_forex_pair.get()
    handle_chosen_asset(selected_asset)

selected_forex_pair.trace("w", handle_fx_selected)
forex_options.pack()




# Renders Crypto pairs submenu if crypto is chosen from main asset class list
# def render_crypto_menu():
crypto_options_list.sort()
selected_crypto_pair = tk.StringVar(window)
selected_crypto_pair.set("Select A Cryptocurrency")
crypto_options = tk.OptionMenu(window, selected_crypto_pair, *crypto_options_list)

def handle_fx_selected(*args):
    selected_asset = selected_crypto_pair.get()
    handle_chosen_asset(selected_asset)

selected_crypto_pair.trace("w", handle_fx_selected)
crypto_options.pack()



# # Decides which sub-asset class menup to render in the app based on asset class selection
# def render_suboption(selected_asset_class):
#     if(selected_asset_class == 'Forex'):
#         render_forex_menu()
#     if(selected_asset_class == 'Cryptos'):
#         render_crypto_menu()


# def handle_chosen_commodity(*args):
#     chosen_asset_class = asset_class_value.get()
#     render_suboption(chosen_asset_class)
#     return None


# # Builds Intitial Asset Class Dropdown
# commodity_options_list = ["Forex", "Indices", "Commodities", "Cryptos"]
# commodity_options_list.sort()
# asset_class_value = tk.StringVar(window)
# asset_class_value.set("Select Asset Class")
# asset_class_value.trace("w", handle_chosen_commodity)
# asset_options = tk.OptionMenu(window, asset_class_value, *commodity_options_list)
# asset_options.pack()








output_path_label = Label(window, text='Choose Download Location')
output_path_label.pack()

def getFolderPath():
    global output_folder_selected
    output_folder_selected = filedialog.askdirectory()
    print(output_folder_selected)
    # output_path_text = Text(window ,text='Downloaded data will be saved to ' + output_folder_selected)
    # output_path_text.pack()
    output_path_text.config(text = 'Download Location: '+ output_folder_selected)


btnFind = ttk.Button(window, text="Browse Folder",command=getFolderPath)
btnFind.pack()
output_path_text = Label(window, text='Download Location: ' )
output_path_text.pack()



def download_data():
    print('downloding')
    print(download_asset)
    print(download_year)
    print(output_folder_selected)
    # main_gui(download_asset, download_year, output_folder_selected)



year_label = tk.Label(text="Year")
year_entry = tk.Entry()
year_label.pack()
year_entry.pack()

def set_year(*args):
    year_value = year_entry.get()
    global download_year
    download_year = year_value
    download_data()


button = tk.Button(window, text="Download Data", command=set_year)
button.pack()




window.mainloop()
