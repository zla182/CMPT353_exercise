'''
Author: your name
Date: 2021-11-03 12:45:45
LastEditTime: 2021-11-05 14:43:41
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \exercise_8\weather_city.py
'''
import numpy as np
import pandas as pd
from skimage.color import lab2rgb
import sys
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from skimage.color import rgb2lab
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


labelled_data = pd.read_csv(sys.argv[1])
unlabelled_data = pd.read_csv(sys.argv[2])

X_temp = labelled_data.drop(['city', 'year'], axis=1)
y_temp = labelled_data["city"]
X_train, X_test, y_train, y_test = train_test_split(X_temp, y_temp)


bayes_model = make_pipeline(StandardScaler(),GaussianNB())
bayes_model.fit(X_train, y_train)
# print("Bayes train:", bayes_model.score(X_train, y_train))
# print("Bayes test:", bayes_model.score(X_test, y_test))
# Bayes train: 0.759493670886076
# Bayes test: 0.6551724137931034

knn_model = make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors = 5))
knn_model.fit(X_train, y_train)
print("Knn train:", knn_model.score(X_train, y_train))
print("Knn test:", knn_model.score(X_test, y_test))
# Knn train: 0.7917146144994246
# Knn valid: 0.6551724137931034

rf_model = make_pipeline(StandardScaler(),RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_leaf=10))
rf_model.fit(X_train, y_train)
# print("RandomForest train:", rf_model.score(X_train, y_train))
# print("RandomForest valid:", rf_model.score(X_test, y_test))
# RandomForest train: 0.7779056386651323
# RandomForest test: 0.6275862068965518

unlabelled_data = unlabelled_data.drop(['city', 'year'], axis=1)
prediction = knn_model.predict(unlabelled_data)


pd.Series(prediction).to_csv(sys.argv[3], index=False, header=False)