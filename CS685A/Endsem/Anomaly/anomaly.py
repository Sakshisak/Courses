import pandas as pd
import numpy as np


df = pd.read_table("anomaly-s050.dat", sep="\s+",header=None)
data = df.to_numpy().flatten()

# list storing whether a data point is an anomaly or not
is_anomaly = []

# Using Z-score to identify outliers
mean = data.mean()
std = data.std()
threshold = 2.0 # taking z-score threshold as 2.0 to get almost 5% of data as anomalies
count_anomaly = 0

for x in data:
    z_score = (x-mean)/std
    if z_score>threshold:
        count_anomaly = count_anomaly+1
        is_anomaly.append(1)
    else:
        is_anomaly.append(0)

is_anomaly = np.asarray(is_anomaly)
outliers = is_anomaly.reshape([100,100])
# print(count_anomaly)
# print(outliers)


filename = 'answer-s050.dat'
f_save = open(filename, 'w')

for i in range(100):
    for j in range(99):
        f_save.write(str(outliers[i][j])+'\t')
    f_save.write(str(outliers[i][99])+'\n')

f_save.close()
