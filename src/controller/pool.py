import time
import multiprocessing
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
        self.statistics.stop('parallel')
        data = self.join_mapped_values(map_responses, pool, num_workers)
        pool.close()
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
