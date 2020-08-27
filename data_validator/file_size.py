import os
import asyncio

tasks = []


def init_file_size_check(file_directory):
    print('\n\nValidating file sizes...\n')
    global path
    path = file_directory
    start_loop()


def start_loop():
    dir_list = os.listdir(path)
    sorted_files = sorted(dir_list)
    build_tasks(sorted_files)


async def check_size(file):
    file_size = os.path.getsize(file)
    print(file_size)
    if file_size == 0:
        print('TOO SMALL')
    else:
        print("Checks Out")


loop = asyncio.get_event_loop()

def build_tasks(sorted_files):
    # start_time = time.time()
    for file in sorted_files[2:]:
        current_file = os.path.join(path, file)
        task = asyncio.ensure_future(check_size(current_file.format(current_file)))
        tasks.append(task)

    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Canceling tasks...")


