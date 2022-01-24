import asyncio
import logging
import datetime 
from aiohttp import ClientSession




class Downloader():
    def __init__(self, settings):
        self.location = settings['location']
        self.asset = settings['asset']
        self.year = settings['year']
        self.timeframe = 'tick' 
        self.start_date = datetime.date(year=int(self.year), month=1, day=1)
        # self.end_date = datetime.date(year=int(self.year)+1, month=1, day=1)
        self.end_date = datetime.date(year=int(self.year), month=1, day=15)
        self.task_count = None
        self.current_task_num = 0
        self.download_location = f'{self.location}/{self.asset}/{self.year}/raw-download-data' 
        self.tasks = []
        self.urls = []
        self.processed = 0
        self.errored_urls_list = []
        self.errored_urls_set = set()
    


    def build_download_tasks(self):
        delta = self.end_date - self.start_date
        self.task_count = delta.days
        day_iterator = datetime.timedelta(days=1)
        for i in range((self.end_date - self.start_date).days):
            current_date = self.start_date + i*day_iterator
            weekday = datetime.date(current_date.year, current_date.month, current_date.day).weekday()
            if weekday != 6: #! Omitts Saturdays
                self._build_daily_urls(current_date)

    
    def _build_daily_urls(self, current_date):
        base_url = 'https://datafeed.dukascopy.com/datafeed/PAIR/YYYY/MM/DD/HHh_ticks.bi5'
        year = f'{current_date.year}'
        month_int = int(current_date.month)-1
        month = f'{month_int}' if current_date.month > 10 else f'0{month_int}' 
        day = f'{current_date.day}' if current_date.day > 9 else f'0{current_date.day}' 

        def _hourly_urls_generator():
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
        urls = _hourly_urls_generator()

        for url in urls:
            fetch_task = asyncio.ensure_future(self._get_data(url.format(url)))
            self.tasks.append(fetch_task)
            self.urls.append(url)


    async def _get_data(self, url):
        file_name = self._generate_download_file_name(url)
        sem = asyncio.Semaphore(1)
        async with sem:
            async with ClientSession() as session:
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.read()
                            with open(file_name, 'wb') as fd:
                                fd.write(data)
                        else:
                            self.errored_urls_set.add(url)
                        self.processed += 1
                except:
                    # self.errored_urls_set.add(url)
                    self.processed += 1
        #             print('ERROR GET URL: ', url)
        # return 1



    def _generate_download_file_name(self, url):
        year = url.split('/')[-4]
        orig_month = int(url.split('/')[-3])+1
        month = f'{orig_month}' if orig_month > 9 else f'0{orig_month}' 
        day = url.split('/')[-2]
        hour = url.split('/')[-1]
        name = f'{self.asset}-{year}-{month}-{day}-{hour}'
        complete_name = f'{self.location}/{self.asset}/{year}/raw-download-data/'+name
        return complete_name


    async def get_and_update(self, item):
        await self._get_data(item)
        # self.processed += 1
        # print(self.processed)
        print(f'Processed {self.processed} downloads of {len(self.tasks)} for {self.asset} in {self.year}')

    
    async def run(self):
        await asyncio.gather(*[
            asyncio.create_task(
                self.get_and_update(url)
            ) for url in self.urls
        ])
    

    def run_download_tasks(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())
    # def run_download_tasks(self):
    #     loop = asyncio.get_event_loop()
    #     try:
    #         print('here')
    #         loop.run_until_complete(asyncio.wait(self.tasks))
    #         print('now here')
    #     except KeyboardInterrupt:
    #         print("Caught keyboard interrupt. Canceling tasks...")

