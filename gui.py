import datetime
import time
import tkinter as tk
from tkinter import ttk
from tkinter import Label
from tkinter import Text
from tkinter import Button
from tkinter import filedialog
from tkinter.messagebox import askyesno
import tkinter.font as font
from main import Main


#* Global Option Select Varibles
forex_options_list = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDSGD', 'AUDUSD', 'CADCHF', 'CADHKD', 'CADJPY', 'CHFJPY', 'CHFSGD', 'EURAUD', 'EURCAD', 'EURCHF', 'EURCZK', 'EURDKK', 'EURGBP', 'EURHKD', 'EURHUF', 'EURJPY', 'EURNOK', 'EURNZD', 'EURPLN', 'EURRUB', 'EURSEK', 'EURSGD', 'EURTRY', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'HKDJPY', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'SGDJPY', 'TRYJPY', 'USDCAD', 'USDCHF', 'USDCNH', 'USDCZK', 'USDDKK', 'USDHKD', 'USDHUF', 'USDILS', 'USDJPY', 'USDMXN', 'USDNOK', 'USDPLN', 'USDRON', 'USDRUB', 'USDSEK', 'USDSGD', 'USDTHB', 'USDTRY', 'USDZAR', 'ZARJPY'  
]
commodity_options_list = ['BRENTCMDUSD', 'GASCMDUSD', 'SOYBEANCMDUSX', 'SUGARCMDUSD', 'COPPERCMDUSD', 'DIESELCMDUSD', 'LIGHTCMDUSD', 'COCOCMDUSD', 'COFFEECMDUSD', 'COTTONCMDUSD', 'OJUICECMDUSD' ]
crypto_options_list = ["BTCUSD", "ETHUSD", "LTCUSD", 'ADAUSD', 'AVEUSD', 'BATUSD', 'BCHUSD', 'CMPUSD', 'DSHUSD', 'ENJUSD', 'EOSUSD', 'LNKUSD', 'MATUSD', 'MKRUSD', 'TRXUSD', 'UNIUSD', 'XLMUSD', 'XMRUSD', 'YFIUSD' ]
metal_options_list = ["XAUUSD", "XAGUSD" ]
indice_options_list = ["BTCUSD", "ETHUSD", "LTCUSD" ]
bond_options_list = ["BTCUSD", "ETHUSD", "LTCUSD" ]


class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.selected_asset = ''
        self.chosen_years = []
        self.chosen_download_location = ''
        self.init_build_app_options()
        # Build Progress Bar
        self.progress_bar = ttk.Progressbar(
            root, 
            orient ='horizontal',
            length = 500, 
            mode = 'determinate')
        self.progress_bar.grid(row = 17, column = 1, pady=(5, 5))
        # Init Progress Label
        self.progress_label = None
        self.cancel_download_button = None
        self.downloading_confirm_msg = None
    

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
        output_path_label.grid(row = 5, column = 1, pady=(40, 10))

        def getFolderPath():
            self.chosen_download_location = filedialog.askdirectory()
            output_path_text.config(text = 'Download Location: '+ self.chosen_download_location)

        folder_btn = ttk.Button(root, text="Browse Folders",command=getFolderPath)
        folder_btn.grid(row = 6, column = 1, pady=(5, 5))
        output_path_text = Label(root, text='Download Location: ' )
        output_path_text.grid(row = 7, column = 1, pady=(5, 5))


    #* Renders Year Selection 
    def init_year_options(self):
        year_label = Label(
            root, 
            text='Select Years:', 
            font=("Helvetica", 20) 
        )
        year_label.grid(row = 8, column = 1, pady=(40, 10))

        current_year = datetime.datetime.now().year
        starting_year = 1999
        year_options_list = []
        for i in range(current_year, starting_year, -1):
            year_options_list.append( str(i) )

        selected_year = tk.StringVar(root)
        selected_year.set("Select a Year")
        year_options = tk.OptionMenu(root, selected_year, *year_options_list)
        year_options.grid(row = 9, column = 1)

        def handle_year_selected(*args):
            chosen_year = selected_year.get()
            self.chosen_years.append(chosen_year)
            self.chosen_years.sort(reverse=True)
            chosen_years_str = ''
            for year in self.chosen_years:
                chosen_years_str =  chosen_years_str + year + ' '
            output_years_text.config(text = 'Selected Years: '+ chosen_years_str)

        choose_year_button = ttk.Button(
            root, 
            text="Add Year", 
            command=handle_year_selected)
        choose_year_button.grid(row = 10, column = 1)

        def clear_years_selected():
            self.chosen_years = []
            chosen_years_str = ''
            output_years_text.config(text = 'Selected Years: '+ chosen_years_str)

        clear_years_button = ttk.Button(
            root, 
            text="Clear Years", 
            command=clear_years_selected)
        clear_years_button.grid(row = 11, column = 1)

        output_years_text = Label(root, text='Selected Years: ' )
        output_years_text.grid(row = 12, column = 1, pady=(5, 5))
    

    #* Download Button
    def init_download_button(self):
        download_button = tk.Button(
            root, 
            text='Download', 
            # command=self.confirm_download
            command=self.run_download
        )
        download_btn_font = font.Font(family='Helvetica', size=18, weight='bold')
        download_button['font'] = download_btn_font
        download_button.grid(row = 13, column = 1, pady=(30, 5))


    # #* Popup confirmation
    # def confirm_download(self):
    #     answer = askyesno(
    #         title='Confirmation',
    #         message=f'Are you sure that you want to download:\n{self.selected_asset}\nfor\n{self.chosen_years}\nto\n{self.chosen_download_location}')
    #     if answer:
    #         self.run_download()
    #     if answer == False:
    #         self.selected_asset = ''
    #         self.chosen_years = []
    #         self.chosen_download_location = ''
    

    #* If popup confirmed, begin download
    def run_download(self):
        # Append Progress Bar Label to App
        message=f'Downloading: {self.selected_asset} for {self.chosen_years} to {self.chosen_download_location}'
        self.downloading_confirm_msg = ttk.Label(root, text=message)
        self.downloading_confirm_msg.grid(row=14, column=1)

        # Append Progress Bar Label to App
        self.progress_label = ttk.Label(root, text=self.update_progress_label())
        self.progress_label.grid(row=15, column=1)

        self.update_progress_bar()
    
        # Build Cancel Button
        self.cancel_download_button = tk.Button(
            root, 
            text='Cancel', 
            command=self.cancel_download)
        download_btn_font = font.Font(family='Helvetica', size=16)
        self.cancel_download_button['font'] = download_btn_font
        self.cancel_download_button.grid(row = 16, column = 1, pady=(5, 5))

        settings = {
            'asset': self.selected_asset,
            'years': self.chosen_years,
            'location': self.chosen_download_location
        }
        NewMain(settings).init_downloader()

        # start_main(self.selected_asset, self.chosen_years, self.chosen_download_location)


    def update_progress_label(self):
        return f"Current Progress: {self.progress_bar['value']}%"


    def update_progress_bar(self):
        if self.progress_bar['value'] < 100:
            self.progress_bar['value'] += 20
            self.progress_label['text'] = self.update_progress_label()
        else:
            print('complete')
            # showinfo(message='The progress completed!')


    #* Cancel Download
    def cancel_download(self):
        print('Canceling Downloads...')
        self.progress_bar['value'] = 0
        self.progress_label['text'] = ''
        self.progress_label.destroy()
        self.cancel_download_button.destroy()
        self.downloading_confirm_msg.destroy()
        cancel_main()




#* Configures Global GUI App Settings and Starts App
if __name__ == "__main__":
    root = tk.Tk()
    App(root).grid(sticky="nsew")
    root.title('DukasCopy Download Scraper')
    root.geometry('1000x700')
    heading=Label(root, text='Historical Data Downloader', font=("Helvetica", 28))
    heading.grid(row=0, column=1, pady=(0,20))
    root.grid_columnconfigure((0, 1, 2), weight=1)
    root.mainloop()

