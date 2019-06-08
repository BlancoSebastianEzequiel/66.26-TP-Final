import collections
import itertools
import multiprocessing
from src.controller.statistics import Statistics


class MapReduce(object):

    def __init__(self, map_func, reduce_func):
        """
        :param map_func: Function to map inputs to intermediate data. Takes as
        argument one input value and returns a tuple with the key and a value
        to be reduced.
        :param reduce_func: Function to reduce partitioned version of
        intermediate data to final output. Takes as argument a key as produced
        by map_func and a sequence of the values associated with that key.
        """
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.statistics = Statistics()

    def get_statistics(self):
        return self.statistics

    @staticmethod
    def partition(mapped_values):
        """
        Organize the mapped values by their key.
        Returns an unsorted sequence of tuples with a key and a sequence of
        values.
        """
        partitioned_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()

    def map(self, inputs, chunksize=1, num_workers=None):
        """
        :param inputs: data to map-reduce
        :param chunksize: The portion of the input data to hand to each worker.
        This can be used to tune performance during the mapping phase.
        :param num_workers: The number of workers to create in the pool.
        Defaults to the number of CPUs available on the current host.
        :return: Process the inputs through the map and reduce functions given.
        """
        self.statistics.start('global')
        self.statistics.start('parallel')
        pool = multiprocessing.Pool(num_workers)
        map_responses = pool.map(
            self.map_func,
            inputs,
            chunksize=chunksize
        )
        pool.close()
        self.statistics.stop('parallel')
        partitioned_data = self.partition(itertools.chain(*map_responses))
        return partitioned_data

    def reduce(self, partitioned_data, num_workers=1):
        """
        :param partitioned_data:
        :param num_workers: The number of workers to create in the pool.
        Defaults to the number of CPUs available on the current host.
        :return:
        """
        self.statistics.start('serial')
        pool = multiprocessing.Pool(num_workers)
        reduced_values = pool.map(self.reduce_func, partitioned_data)
        pool.close()
        self.statistics.stop('serial')
        self.statistics.stop('global')
        return reduced_values
