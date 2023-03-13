from sklearn import preprocessing
import numpy as np

THRESHOLD = 0.15;


def normalize(signal):
    signal = signal.reshape(-1,);
    signal = signal / np.amax(signal);
    for i in range(len(signal)):
        if np.abs(signal[i]) < THRESHOLD: signal[i] = 0;

    return signal;