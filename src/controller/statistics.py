from time import time


class Statistics:
    def __init__(self):
        self.timers = {
            'serial': float(0),
            'parallel': float(0),
            'global': float(0),
        }
        self.time_elapsed = {
            'serial': float(0),
            'parallel': float(0),
            'global': float(0),
        }

    def start(self, key):
        self.timers[key] = time()

    def stop(self, key):
        stop_time = time()
        self.time_elapsed[key] += (stop_time - self.timers[key])*1000

    def get_time_elapsed(self, key):
        return self.time_elapsed[key]
