'''
Author: your name
Date: 2021-10-06 17:44:48
LastEditTime: 2021-10-08 23:49:19
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \exercise_4\temperature_correlation.py
'''
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

stations_file = sys.argv[1]
city_data = sys.argv[2]
output = sys.argv[3]

stations = pd.read_json(stations_file, lines=True)
stations['avg_tmax'] = stations['avg_tmax']/10

cities =pd.read_csv(city_data)
cities.dropna(inplace=True)
cities['area'] = cities['area']/1000000
# Exclude cities with area greater than 10000 km²
cities = cities[cities.area <= 10000]
cities.reset_index(drop=True)
cities['density'] =  cities['population']/cities['area']

def deg2rad(deg):
    return deg*(math.pi/180)

def distance(city, stations):
    R = 6371
    dlat = np.deg2rad(stations['latitude']-city['latitude'])
    dlong = np.deg2rad(stations['longitude']-city['longitude'])
    a = np.sin((dlat)/2.0)**2 + np.cos(np.deg2rad(city['latitude'])) * np.cos(np.deg2rad(stations['latitude'])) * np.sin((dlong)/2.0)**2
    return R * np.arcsin(np.sqrt(a)) * 2 * 1000

def best_tmax(city, stations):
    stations['distance'] = distance(city, stations)
    minimum = np.argmin(stations['distance'])
    return stations.iloc[minimum].avg_tmax

cities['avg_tmax'] = cities.apply(best_tmax, axis = 1, stations=stations)

plt.figure(figsize=(15, 10))
plt.scatter(cities['avg_tmax'],cities['density'],color='b')
plt.title("Temperature vs Population Density")
plt.xlabel("Avg Max Temperature (\u00b0C)")
plt.ylabel("Population Density (people/km\u00b2)")

plt.savefig(output)
