from multiprocessing import Process, Queue
import time


class MyProcess(Process):

    def __init__(self, target, args):
        self.target = target
        self.args = args
        self.output = Queue()
        self.finish = Queue()
        self.output_list = []
        super().__init__(target=target, args=args)

    def run(self):
        for an_arg in self.args:
            self.output.put(self.target(an_arg))
        self.finish.put(True)

    def get_queue_data(self):
        output_list = []
        while self.output.qsize() != 0:
            output_list.append(self.output.get())
        return output_list

    def get_output(self):
        return self.output_list

    def has_finished(self):
        return self.finish.qsize() != 0

    def join(self, **kwargs):
        while self.finish.empty():
            time.sleep(0.000000000000000001)
        self.finish.get()
        self.finish.close()
        self.finish.join_thread()
        self.output_list = self.get_queue_data()
        self.output.close()
        self.output.join_thread()
        super().join(**kwargs)
