from sklearn import preprocessing
import numpy as np
from audioprocessing.globalvars import *


'''
Reshape to 1-D array (if not already)
Divide every sample by the max value
Apply threshold to each sample
'''
def normalize(signal):
    signal = signal.reshape(-1,)
    initlen = len(signal)
    max = np.amax(signal)
    newsig = np.zeros(signal.shape)
    for i in range(len(signal)):
        newsig[i] = signal[i] / max
        if np.abs(newsig[i]) < LOW_THRESHOLD: newsig[i] = 0
    newlen = len(newsig)
    assert(newlen == initlen)
    return newsig