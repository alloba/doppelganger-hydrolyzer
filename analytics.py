# import dtaidistance.dtw_ndim
from dtw import *
# from dtaidistance import *
# import numpy as np

# alignment = dtw(series1, series2, keep_internals=True)  # not sure if keep internals is required.

# idx = np.linspace(0,6.28,num=100)
# query = np.sin(idx) + np.random.uniform(size=100)/10.0
# print(query)


def dtw_distance_d(series1, series2):
    alignment = dtw(series1, series2, keep_internals=True)  # not sure if keep internals is required.
    return alignment.distance


def dtw_distance_i(series1, series2, dimensionality=0):
    distances = []
    for i in range(dimensionality):
        s1 = [x[i] for x in series1]
        s2 = [z[i] for z in series2]
        distances.append(dtw(s1, s2).distance)
    return sum(distances)
