import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']
SumTotalsRows = np.sum(totals,axis=1)
SumTotalsColumns = np.sum(totals,axis=0)
SumCountsColumns = np.sum(counts,axis=0)
EachMonthPre = SumTotalsColumns/SumCountsColumns
SumCountsRows = np.sum(counts,axis=1)
DailyPerCity = SumTotalsRows / SumCountsRows
#number of rows
RowNum = totals.shape[0]
QuarterlyReshape = totals.reshape((4*RowNum,3))
QuarterSum = np.sum(QuarterlyReshape,axis = 1)
QuarterSum = QuarterSum.reshape((RowNum,4))
print('Row with lowest total precipitation:')
print(np.argmin(SumTotalsRows))
print('Average precipitation in each month:')
print(EachMonthPre)
print('Average precipitation in each city:')
print(DailyPerCity)
print('Quarterly precipitation totals:')
print(QuarterSum)