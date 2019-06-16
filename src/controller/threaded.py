from src.controller.map_reduce import MapReduce
from src.controller.utils import chunks
from src.controller.thread import Thread


class Threaded(MapReduce):

    def __init__(self, map_func, reduce_fun):
        self.processes = []
        super().__init__(map_func=map_func, reduce_func=reduce_fun)

    def map(self, inputs, num_workers=1):
        splitted_data = chunks(inputs, num_workers)
        self.statistics.start('global')
        self.statistics.start('parallel')
        for i in range(0, num_workers):
            arg = splitted_data[i]
            self.processes.append(Thread(target=self.map_func, args=arg))
        map_responses = []
        self.statistics.start('global')
        self.statistics.start('parallel')
        for process in self.processes:
            process.start()
        for process in self.processes:
            process.join()
            map_responses += process.get_output()
        self.statistics.stop('parallel')
        map_responses = list(filter(lambda x: len(x) != 0, map_responses))
        return self.partition(map_responses)

    def reduce(self, partitioned_data, num_workers=1):
        output = []
        self.statistics.start('serial')
        for item in partitioned_data:
            output.append(self.reduce_func(item))
        self.statistics.stop('serial')
        self.statistics.stop('global')
        return output
