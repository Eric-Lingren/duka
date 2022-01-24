import os, asyncio, logging
from loggers.logger import setup_logger


class File_Size_Validator():
    def __init__(self, settings):
        self.location = settings['location']
        self.asset = settings['asset']
        self.year = settings['year']
        self.download_location = f'{self.location}/{self.asset}/{self.year}/raw-download-data'
        self.processed_count = 0
        self.successfully_validated_count = 0
        self.file_list = []
        self.successfully_deleted_files_set = set()
        self.failed_deleted_files_set = set()
        self.logger = setup_logger('file_size_logger', f'{self.location}/{self.asset}/{self.asset}-File_Sizes.log')
        self.file_size_logger = logging.getLogger('file_size_logger')


    def build_file_size_validation_tasks(self):
        all_files = os.listdir(self.download_location)
        for file in all_files:
            current_file_path = os.path.join(self.download_location, file)
            self.file_list.append(current_file_path)


    def run_file_size_validation_tasks(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run_tasks())
        self._save_logs()

    
    async def _run_tasks(self):
        await asyncio.gather(*[
            asyncio.create_task(
                self._check_and_notify(file)
            ) for file in self.file_list
        ])


    async def _check_and_notify(self, file):
        await self._check_size(file)
        print(f'Processed {self.processed_count} checks of {len(self.file_list)} for {self.asset} in {self.year}')


    async def _check_size(self, file):
        file_size = os.path.getsize(file)
        if file_size == 0:
            try:
                os.remove(file)
                self.successfully_deleted_files_set.add(file)
            except:
                self.failed_deleted_files_set.add(file)
        else:
            self.successfully_validated_count += 1
        self.processed_count += 1

    
    def _save_logs(self):
        total_files_count = len(self.file_list)
        deleted_files_count = len(self.successfully_deleted_files_set)
        failed_deletions_count = len(self.failed_deleted_files_set)
        total_without_data = self.successfully_deleted_files_set | self.failed_deleted_files_set
        total_without_data_count = len(total_without_data)
        sorted_failures = sorted(self.failed_deleted_files_set)
        mapped_file_failures = ''

        if failed_deletions_count > 0 :
            for failed_file in sorted_failures:
                mapped_file_failures += '\n    '+failed_file
        else:
            mapped_file_failures = '\n    NONE'

        log_msg = f' /n--- EMPTY FILES LOG FOR {self.asset} {self.year} ---\n  Total Tasks: {total_files_count}\n  Total Checked: {self.processed_count} \n  Total With Data: {self.successfully_validated_count}\n  Total Without Data: {total_without_data_count}\n  Successful Deletions: {deleted_files_count}\n  Failed Deletions: {failed_deletions_count}\n  Failures (manually delete): {mapped_file_failures}\n\n'
        self.file_size_logger.info(log_msg)
        print('\n\n', log_msg)
        log_msg = ''
