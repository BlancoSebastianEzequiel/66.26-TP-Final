import numpy
from math import sqrt


class Measurer:
    def __init__(self):
        self._values = []
        self._size = 0
        self._values_sum = 0
        self._mean = 0
        self._error = 0

    def add_value(self, v):
        self._values.append(v)
        self._size = len(self._values)
        self._values_sum += v
        self._mean = self._values_sum/self._size
        if self._size > 1:
            self._error = numpy.std(self._values, ddof=1)/sqrt(self._size)
        else:
            self._error = 0

    def get_mean(self):
        return self._mean

    def get_error(self):
        return self._error
