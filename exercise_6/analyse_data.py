'''
Author: your name
Date: 2021-10-20 13:34:04
LastEditTime: 2021-10-22 17:42:33
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \exercise_6\analyse_data.py
'''
from ast import Index
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv("data.csv")
anova = stats.f_oneway(data['qs1'], data['qs2'], data['qs3'], data['qs4'], data['qs5'], data['merge1'], data['partition_sort'])
print("p-value = ", round(anova.pvalue, 2)) 
describe = data.describe().reset_index(0)
print(describe)
print(data.describe().loc['mean',:].sort_values())
x_melt = pd.melt(data)
posthoc = pairwise_tukeyhsd(
    x_melt['value'], x_melt['variable'],
    alpha=0.05)

fig = posthoc.plot_simultaneous()
plt.show()