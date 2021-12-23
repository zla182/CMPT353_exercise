# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


totals = pd.read_csv('totals.csv').set_index(keys=[ 'name' ])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

SumTotalsRows = totals.sum(axis=1)
LowestCity = SumTotalsRows.idxmin()
SumTotalsColumns = totals.sum(axis=0)
SumCountsColumns = counts.sum(axis=0)
EachMonthPre = SumTotalsColumns/SumCountsColumns
SumCountsRows = counts.sum(axis=1)
DailyPerCity = SumTotalsRows / SumCountsRows
print('City with lowest total precipitation:')
print(LowestCity)
print('Average precipitation in each month:')
print(EachMonthPre)
print('Average precipitation in each city:')
print(DailyPerCity)
