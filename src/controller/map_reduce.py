import collections
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

    @staticmethod
    def get_chunksize(inputs, num_workers):
        chunksize = int(len(inputs) / num_workers)
        if chunksize == 0:
            return 1
        return chunksize

    def get_statistics(self):
        return self.statistics

    def keys_repeated(self, map_responses):
        if not map_responses:
            return True
        keys = {}
        self.statistics.start('serial')
        for a_mapped_value in map_responses:
            pos, values = a_mapped_value
            if pos not in keys:
                keys[pos] = 0
            else:
                self.statistics.stop('serial')
                return True
        self.statistics.stop('serial')
        return False

    @staticmethod
    def partition(mapped_values):
        """
        Organize the mapped values by their key.
        Returns an unsorted sequence of tuples with a key and a sequence of
        values.
        """
        partitioned_data = collections.defaultdict(list)
        for a_mapped_value in mapped_values:
            key, value = a_mapped_value
            partitioned_data[key].append(value)
        return list(partitioned_data.items())

    def map(self, inputs, num_workers=None):
        """
        :param inputs: data to map-reduce
        :param chunksize: The portion of the input data to hand to each worker.
        This can be used to tune performance during the mapping phase.
        :param num_workers: The number of workers to create.
        :return: Process the inputs through the map and reduce functions given.
        """

    def reduce(self, partitioned_data, num_workers=1):
        """
        :param partitioned_data:
        :param num_workers: The number of workers to create.
        :return:
        """
