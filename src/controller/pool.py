import time
import multiprocessing
import itertools
from src.controller.map_reduce import MapReduce


class Pool(MapReduce):

    def __init__(self, map_func, reduce_fun):
        super().__init__(map_func=map_func, reduce_func=reduce_fun)
        self.sleep_sec = 0.5

    def map(self, inputs, num_workers=None):
        chunksize = self.get_chunksize(inputs, num_workers)
        self.statistics.start('global')
        self.statistics.start('parallel')
        pool = multiprocessing.Pool(processes=num_workers)
        map_responses = pool.map(
            self.map_func,
            inputs,
            chunksize=chunksize
        )
        data = []
        while not self.keys_repeated(data):
            chunksize = self.get_chunksize(map_responses, num_workers)
            data = pool.map(
                self.partition,
                map_responses,
                chunksize=chunksize
            )
            data = list(itertools.chain.from_iterable(data))
        pool.close()
        self.statistics.stop('parallel')
        time.sleep(self.sleep_sec)
        return data

    def reduce(self, partitioned_data, num_workers=1):
        self.statistics.start('serial')
        pool = multiprocessing.Pool(processes=num_workers)
        reduced_values = pool.map(self.reduce_func, partitioned_data)
        pool.close()
        self.statistics.stop('serial')
        time.sleep(self.sleep_sec)
        self.statistics.stop('global')
        return reduced_values
