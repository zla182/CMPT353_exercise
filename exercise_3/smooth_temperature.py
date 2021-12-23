from datetime import timedelta
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from pandas.io.feather_format import read_feather
from pandas.io.sql import DatabaseError
from pykalman import KalmanFilter

file = sys.argv[1]
data = pd.read_csv(file)
data['timestamp'] = pd.to_datetime(data['timestamp'])
plt.figure(figsize=(12, 4))
plt.plot(data['timestamp'], data['temperature'], 'b.', alpha=0.5)
loess_smoothed = lowess(data.temperature, data.timestamp, 0.05)
plt.plot(data['timestamp'], loess_smoothed[:, 1], 'r-', label="LOESS-smoothed line")

kalman_data = data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]
initial_state = kalman_data.iloc[0]
kalman_std = kalman_data.std()
observation_covariance = np.diag([kalman_std[0],kalman_std[1],kalman_std[2],kalman_std[3]]) ** 2 # TODO: shouldn't be zero
transition_covariance = np.diag([0.1, 0.1, 0.1, 0.1]) ** 2 # TODO: shouldn't be zero
transition = [[0.97,0.5,0.2,-0.001], [0.1,0.4,2.2,0], [0,0,0.95,0], [0,0,0,1]] # TODO: shouldn't (all) be zero
kf = KalmanFilter(
            initial_state_mean=initial_state,
            initial_state_covariance=observation_covariance,
            observation_covariance=observation_covariance,
            transition_covariance=transition_covariance,
            transition_matrices=transition
        )
kalman_smoothed , _ = kf.smooth(kalman_data) 
plt.plot(data[ 'timestamp' ], kalman_smoothed[:, 0 ], 'g-', alpha=1, label = "Kalman Smoothing")
plt.legend()
plt.savefig('cpu.svg')