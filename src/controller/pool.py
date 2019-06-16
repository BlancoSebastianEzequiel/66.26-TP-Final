import multiprocessing
from src.controller.map_reduce import MapReduce


class Pool(MapReduce):

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
        pool.close()
        self.statistics.stop('parallel')
        partitioned_data = self.partition(map_responses)
        return partitioned_data

    def reduce(self, partitioned_data, num_workers=1):
        self.statistics.start('serial')
        pool = multiprocessing.Pool(num_workers)
        reduced_values = pool.map(self.reduce_func, partitioned_data)
        pool.close()
        self.statistics.stop('serial')
        self.statistics.stop('global')
        return reduced_values
