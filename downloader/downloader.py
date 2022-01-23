import asyncio
import os
import datetime 
from aiohttp import ClientSession


class Downloader():
    def __init__(self, settings):
        self.location = settings['location']
        self.asset = settings['asset']
        self.years = settings['years']
        self.iter_year = settings['starting_year']
        self.starting_year = settings['starting_year']
        self.ending_year = settings['ending_year']
        self.timeframe = 'tick' 
        self.start_date = datetime.date(year=self.starting_year, month=1, day=1)
        self.end_date = datetime.date(year=self.ending_year+1, month=1, day=1)
        # self.end_date = datetime.date(year=self.ending_year, month=1, day=5)
        self.task_count = None
        self.current_task_num = 0
        self.download_location = f'{self.location}/{self.asset}/{self.iter_year}/raw-download-data' 
        # self.configure_folders()
        self.run_downloader()
        print('COMPLETE!!')
    

    # def configure_folders(self):
    #     try:
    #         if not os.path.isdir(f'{self.location}/{self.asset}'):
    #             os.mkdir(f'{self.location}/{self.asset}')
    #         for year in self.years:
    #             if not os.path.isdir(f'{self.location}/{self.asset}/{year}'):
    #                 os.mkdir(f'{self.location}/{self.asset}/{year}')
    #             if not os.path.isdir(f'{self.location}/{self.asset}/{year}/raw-download-data'):
    #                 os.mkdir(f'{self.location}/{self.asset}/{year}/raw-download-data')
    #     except:
    #         # print('\n--- Folder or asset not selected ---\n')
    #         raise Exception('\n--- Folder or asset not selected ---\n')


    def run_downloader(self):
        delta = self.end_date - self.start_date
        self.task_count = delta.days
        day_iterator = datetime.timedelta(days=1)
        for i in range((self.end_date - self.start_date).days):
            current_date = self.start_date + i*day_iterator
            print(current_date)
            self.build_url(current_date)
            print(f'{self.current_task_num} of {self.task_count}' )

    
    def build_url(self, current_date):
        base_url = 'https://datafeed.dukascopy.com/datafeed/PAIR/YYYY/MM/DD/HHh_ticks.bi5'
        year = f'{current_date.year}'
        month_int = int(current_date.month)-1
        month = f'{month_int}' if current_date.month > 10 else f'0{month_int}' 
        day = f'{current_date.day}' if current_date.day > 9 else f'0{current_date.day}' 

        def daily_urls():
            for i in range(25):
                if i < 10:
                    hour = f'0{i}'
                else:
                    hour = f'{i}'
                new_url = base_url.replace('PAIR', self.asset)
                new_url = new_url.replace('YYYY', year)
                new_url = new_url.replace('MM', month)
                new_url = new_url.replace('DD', day)
                new_url = new_url.replace('HH', hour)
                yield new_url
        urls = daily_urls()

        tasks = []
        for url in urls:
            task = asyncio.ensure_future(self.get_data(url.format(url)))
            tasks.append(task)
        self.run_download_tasks(tasks)
        self.current_task_num = self.current_task_num + 1


    def run_download_tasks(self, tasks):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.wait(tasks))
        except KeyboardInterrupt:
            print("Caught keyboard interrupt. Canceling tasks...")


    async def get_data(self, url):
        file_name = self.generate_file_name(url)
        attempts = 0
        while attempts < 5:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.read()
                        with open(file_name, 'wb') as fd:
                            fd.write(data)
                        attempts = 5
                    else:
                        attempts+=1


    def generate_file_name(self, url):
        year = url.split('/')[-4]
        orig_month = int(url.split('/')[-3])+1
        month = f'{orig_month}' if orig_month > 9 else f'0{orig_month}' 
        day = url.split('/')[-2]
        hour = url.split('/')[-1]
        name = f'{self.asset}-{year}-{month}-{day}-{hour}'
        complete_name = f'{self.location}/{self.asset}/{year}/raw-download-data/'+name
        return complete_name

