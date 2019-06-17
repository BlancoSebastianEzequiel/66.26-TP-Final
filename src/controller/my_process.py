from multiprocessing import Process, Queue


class MyProcess(Process):

    def __init__(self, target, args):
        self.target = target
        self.args = args
        self.output = Queue()
        super().__init__(target=target, args=args)

    def run(self):
        for an_arg in self.args:
            self.output.put(self.target(an_arg))

    def get_output(self):
        output_list = []
        while self.output.qsize() != 0:
            output_list.append(self.output.get())
        return output_list
