import pandas as pd
import sys 
import matplotlib.pyplot as plt

# input from terminal
filename1 = sys.argv[1]
filename2 = sys.argv[2]

reader1=pd.read_csv(filename1, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])
reader2=pd.read_csv(filename2, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

reader1_sorted = reader1.sort_values(by='views', ascending=False)
reader1['views2'] = reader2['views']

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(reader1_sorted['views'].values)
plt.title('Popularity Distribution')
plt.ylabel('Views')
plt.xlabel('Rank')

plt.subplot(1, 2, 2)
plt.scatter(reader1['views'], reader2['views2'])
plt.xscale('log')
plt.yscale('log')
plt.title('Daily Correlation')
plt.ylabel('Day 2 Views')
plt.xlabel('Day 1 Views')
plt.savefig('wikipedia.png')