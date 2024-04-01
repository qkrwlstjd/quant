import concurrent.futures
import multiprocessing


class ProcessAndThread:
    def __init__(self, func, item, max_workers=30, max_process=4, args=None):
        self.max_workers = max_workers
        self.max_process = max_process
        self.func = func
        self.item = item
        self.args = args

    def funcc(self, item):
        self.func(item, self.args)

    def thread(self, chunk):
        max_workers = self.max_workers

        atr_results = chunk

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Process AtrResults in parallel
            results = list(executor.map(self.funcc, atr_results))
        return results

    def process(self):
        max_process = self.max_process
        items = self.item
        chunk_size = len(items) // max_process
        chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

        with multiprocessing.Pool(processes=max_process) as pool:
            chunks = pool.map(self.thread, chunks)
        return chunks
