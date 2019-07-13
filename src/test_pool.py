from multiprocessing import Pool
from time import time
from math import ceil
from src.controller.utils import chunks
from src.controller.generate_output_data import OutputData
import pandas as pd

SIZE = 10000000


def loop(s):
    acum = 0
    size = len(s)
    for i in range(0, size):
        acum += s[i]
    return acum


a_list = list(range(SIZE))
pool = Pool(processes=4)
start = time()
pool_sum = pool.map(loop, chunks(a_list, 4), chunksize=ceil(SIZE/4))
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

test_pool_output_data = OutputData()
test_pool_df = test_pool_output_data.get_df_from_csv("src/data/test_pool.csv")
test_pool_df = test_pool_df.append(
    pd.Series(
        ["python", str(elapsed_time), str(float(SIZE)), "1"],
        index=test_pool_df.columns),
    ignore_index=True)
test_pool_df = test_pool_df.append(
    pd.Series(
        ["python using pool", str(pool_elapsed_time), str(float(SIZE)), "4"],
        index=test_pool_df.columns),
    ignore_index=True)
test_pool_output_data.save_df_in_image(test_pool_df, "test_pool.png")
