class MultiplyMatricesInterface:

    @staticmethod
    def pre_processing(matrix_a, matrix_b):
        raise NotImplementedError

    @staticmethod
    def map_worker(chunk):
        raise NotImplementedError

    @staticmethod
    def reduce_worker(item):
        raise NotImplementedError
