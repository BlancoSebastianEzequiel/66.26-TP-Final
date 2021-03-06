import time
import multiprocessing as mp
from src.controller.map_reduce import MapReduce


class Pool(MapReduce):

    def __init__(self, map_func, reduce_fun):
        super().__init__(map_func=map_func, reduce_func=reduce_fun)
        self.sleep_sec = 0.5

    def map(self, inputs, num_workers=1):
        num_cpu = mp.cpu_count()
        if num_workers > num_cpu:
            num_workers = num_cpu
        chunksize = self.get_chunksize(inputs, num_workers)
        pool = mp.Pool(processes=num_workers)
        self.statistics.start('parallel')
        map_responses = pool.map(
            self.map_func,
            inputs,
            chunksize=chunksize
        )
        # data = self.group_by_key_mapped_values(map_responses, num_workers)
        data = self.group_by_key(map_responses)
        pool.close()
        pool.join()
        self.statistics.stop('parallel')
        # time.sleep(self.sleep_sec)
        return data

    def reduce(self, partitioned_data, num_workers=1):
        # pool = mp.Pool(processes=num_workers)
        self.statistics.start('serial')
        # reduced_values = pool.map(self.reduce_func, partitioned_data)
        reduced_values = []
        for data in partitioned_data:
            reduced_values.append(self.reduce_func(data))
        # pool.close()
        # pool.join()
        self.statistics.stop('serial')
        # time.sleep(self.sleep_sec)
        return reduced_values
