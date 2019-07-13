import itertools
import multiprocessing as mp
from src.controller.map_reduce import MapReduce
from src.controller.utils import chunks
from src.controller.my_process import MyProcess


class Process(MapReduce):

    def __init__(self, map_func, reduce_fun):
        self.processes = []
        super().__init__(map_func=map_func, reduce_func=reduce_fun)

    def map(self, inputs, num_workers=1):
        num_cpu = mp.cpu_count()
        if num_workers > num_cpu:
            num_workers = num_cpu
        splitted_data = chunks(inputs, num_workers)
        for i in range(0, num_workers):
            arg = splitted_data[i]
            self.processes.append(MyProcess(target=self.map_func, args=arg))
        map_responses = []
        self.statistics.start('parallel')
        for process in self.processes:
            process.daemon = True
            process.start()
        for process in self.processes:
            process.join()
            map_responses += process.get_output()
        self.statistics.stop('parallel')
        print(f"parallel: {self.statistics.get_time_elapsed('parallel')}")
        map_responses = list(filter(lambda x: len(x) != 0, map_responses))
        return self.group_by_key(map_responses)

    def reduce(self, partitioned_data, num_workers=1):
        output = []
        self.statistics.start('serial')
        for item in partitioned_data:
            output.append(self.reduce_func(item))
        self.statistics.stop('serial')
        print(f"serial: {self.statistics.get_time_elapsed('serial')}")
        return output
