from multiprocessing import Pool
from time import time
from math import ceil
from src.controller.utils import chunks


def loop(s):
    return sum(s)


size = 100000000
a_list = list(range(size))
pool = Pool(processes=4)
start = time()
pool_sum = pool.map(loop, chunks(a_list, 4), chunksize=ceil(size/4))
pool.close()
pool.join()
end = time()
pool_elapsed_time = end - start
start = time()
serial_sum = loop(a_list)
end = time()
elapsed_time = end - start
ratio = pool_elapsed_time/elapsed_time
print(f"pool_elapsed_time: {pool_elapsed_time}")
print(f"elapsed_time: {elapsed_time}")
print(f"ratio: {ratio}")
