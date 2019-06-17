import threading


class Thread(threading.Thread):

    def __init__(self, target, args):
        self.target = target
        self.args = args
        self.output = []
        super().__init__(target=target, args=args)

    def run(self):
        for an_arg in self.args:
            self.output.append(self.target(an_arg))

    def get_output(self):
        return self.output
