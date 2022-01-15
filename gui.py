import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import Label
from tkinter import Text
from tkinter import Button
from tkinter import filedialog
from tkinter.messagebox import askyesno
# from main import main_gui


#* Global Option Select Varibles
forex_options_list = ["EURAUD", "SGDJPY", "AUDUSD", "USDGBP"]
commodity_options_list = ["XAUUSD", "XAGUSD", ]
crypto_options_list = ["BTCUSD", "ETHUSD", "LTCUSD" ]
metal_options_list = ["BTCUSD", "ETHUSD", "LTCUSD" ]
indice_options_list = ["BTCUSD", "ETHUSD", "LTCUSD" ]
bond_options_list = ["BTCUSD", "ETHUSD", "LTCUSD" ]


class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.selected_asset = ''
        self.chosen_years = []
        self.chosen_download_location = ''
        self.init_build_app_options()
    

    def init_build_app_options(self):
        asset_heading = Label(root, text='Choose an Asset:', font=("Helvetica", 20)) 
        asset_heading.grid(row = 2, column = 1, pady=(5, 10))
        self.init_forex_options()
        self.init_crypto_options()
        self.init_commodity_options()
        self.init_folder_options()
        self.init_year_options()
        self.init_download_button()


    #* Renders Forex Pairs Submenu
    def init_forex_options(self):
        forex_options_list.sort()
        selected_forex_pair = tk.StringVar(root)
        selected_forex_pair.set("Select A Forex Pair")
        forex_options = tk.OptionMenu(root, selected_forex_pair, *forex_options_list)

        def handle_fx_selected(*args):
            self.selected_asset = selected_forex_pair.get()

        selected_forex_pair.trace("w", handle_fx_selected)
        forex_options.grid(row = 3, column = 0)


    #* Renders Crypto Pairs Submenu
    def init_commodity_options(self):
        commodity_options_list.sort()
        selected_commodity_pair = tk.StringVar(root)
        selected_commodity_pair.set("Select a Commodity")
        commodity_options = tk.OptionMenu(root, selected_commodity_pair, *commodity_options_list)

        def handle_fx_selected(*args):
            self.selected_asset = selected_commodity_pair.get()

        selected_commodity_pair.trace("w", handle_fx_selected)
        commodity_options.grid(row = 3, column = 1)


    #* Renders Crypto Pairs Submenu
    def init_crypto_options(self):
        crypto_options_list.sort()
        selected_crypto_pair = tk.StringVar(root)
        selected_crypto_pair.set("Select a Crypto")
        crypto_options = tk.OptionMenu(root, selected_crypto_pair, *crypto_options_list)

        def handle_fx_selected(*args):
            self.selected_asset = selected_crypto_pair.get()

        selected_crypto_pair.trace("w", handle_fx_selected)
        crypto_options.grid(row = 3, column = 2)


    #* Renders Browse Folder Download Location
    def init_folder_options(self):
        output_path_label = Label(
            root, 
            text='Choose a Download Location:', 
            font=("Helvetica", 20) 
        )
        output_path_label.grid(row = 4, column = 1, pady=(40, 10))

        def getFolderPath():
            self.chosen_download_location = filedialog.askdirectory()
            output_path_text.config(text = 'Download Location: '+ self.chosen_download_location)

        folder_btn = ttk.Button(root, text="Browse Folders",command=getFolderPath)
        folder_btn.grid(row = 5, column = 1, pady=(5, 5))
        output_path_text = Label(root, text='Download Location: ' )
        output_path_text.grid(row = 6, column = 1, pady=(5, 5))


    #* Renders Year Selection 
    def init_year_options(self):
        year_label = Label(
            root, 
            text='Choose a Year:', 
            font=("Helvetica", 20) 
        )
        year_label.grid(row = 7, column = 1, pady=(40, 10))

        current_year = datetime.datetime.now().year
        starting_year = 1999
        year_options_list = []
        for i in range(current_year, starting_year, -1):
            year_options_list.append( str(i) )

        selected_year = tk.StringVar(root)
        selected_year.set("Select a Year")
        year_options = tk.OptionMenu(root, selected_year, *year_options_list)
        year_options.grid(row = 8, column = 1)

        def handle_year_selected(*args):
            chosen_year = selected_year.get()
            self.chosen_years.append(chosen_year)
            self.chosen_years.sort(reverse=True)
            chosen_years_str = ''
            for year in self.chosen_years:
                chosen_years_str =  chosen_years_str + year + ' '
            output_years_text.config(text = 'Selected Years: '+ chosen_years_str)

        choose_year_button = tk.Button(
            root, 
            text="Add Year", 
            command=handle_year_selected)
        choose_year_button.grid(row = 9, column = 1)

        output_years_text = Label(root, text='Selected Years: ' )
        output_years_text.grid(row = 10, column = 1, pady=(5, 5))
    

    #* Download Button
    def init_download_button(self):
        download_button = ttk.Button(self, text='Download', command=self.confirm_download)
        # download_button.grid(row = 10, column = 1)
        download_button.grid()


    #* Popup confirmation
    def confirm_download(self):
        answer = askyesno(
            title='Confirmation',
            message=f'Are you sure that you want to download:\n{self.selected_asset}\nfor\n{self.chosen_years}\nto\n{self.chosen_download_location}')
        if answer:
            self.run_download()
        if answer == False:
            self.selected_asset = ''
            self.chosen_years = []
            self.chosen_download_location = ''
    

    #* If popup confirmed, begin download
    def run_download(self):
        print('ran run dld')
        print(self.selected_asset)
        print(self.chosen_years)
        print(self.chosen_download_location)





#* Configures Global GUI App Settings and Starts App
if __name__ == "__main__":
    root = tk.Tk()
    App(root).grid(sticky="nsew")
    root.title('DukasCopy Download Scraper')
    root.geometry('1000x600')
    heading=Label(root, text='Historical Data Downloader', font=("Helvetica", 28))
    heading.grid(row=0, column=1, pady=(0,20))
    root.grid_columnconfigure((0, 1, 2), weight=1)
    root.mainloop()

