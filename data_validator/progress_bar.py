from tqdm import tqdm

def progress_bar(tasks, responses):
    pbar = tqdm(total=len(tasks))
    pbar.update(n=len(responses))
    return pbar