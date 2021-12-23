import pandas as pd
import numpy as np
import sys 
import matplotlib.pyplot as plt
import os

# input from terminal
try:
        filename1 = sys.argv[1]
        filename2 = sys.argv[2]
except:
        print("cannot get the fileName input")

reader1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1,
                 names=['lang', 'page', 'views', 'bytes'])
reader2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1,
                 names=['lang', 'page', 'views', 'bytes'])
reader1_sorted = reader1.sort_values('views', ascending=False)['views']
reader2_sorted = reader2.sort_values('views', ascending=False)['views']

reader1_sorted.name = "view1"
reader2_sorted.name = "view2"


plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
plt.plot(reader1_sorted.values)
plt.title("Popularity Distribution")
plt.xlabel("Rank")
plt.ylabel("Views")


plt.subplot(1, 2, 2)
join = pd.concat([reader1_sorted, reader2_sorted], axis=1).reset_index()
plt.scatter(join['view1'], join['view2'], color='b')
plt.xscale("log")
plt.yscale("log")
plt.title("Daily Correlation")
plt.xlabel("Day 1 views")
plt.ylabel("Day 2 views")
plt.savefig('wikipedia.png')

