from sklearn import preprocessing
import numpy as np

THRESHOLD = 0.15;

'''
Reshape to 1-D array (if not already)
Divide every sample by the max value
Apply threshold to each sample
'''
def normalize(signal):
    signal = signal.reshape(-1,);
    signal = signal / np.amax(signal);
    for i in range(len(signal)):
        if np.abs(signal[i]) < THRESHOLD: signal[i] = 0;

    return signal;