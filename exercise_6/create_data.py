'''
Author: your name
Date: 2021-10-20 13:06:10
LastEditTime: 2021-10-20 13:32:58
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \e6\create_data.py
'''
import time
from implementations import all_implementations
import pandas as pd
import numpy as np

data = pd.DataFrame(columns=['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort'], index = np.arange(200))

for i in range(200):
    random_array = np.random.randint(-1000,700,size = 5000)
    for sort in all_implementations:
        st = time.time()
        res = sort(random_array)
        en = time.time()
        data.iloc[i][sort.__name__] = en - st
        

data.to_csv('data.csv', index=False)