from scipy.io import wavfile
import matplotlib.pyplot as plt
import math
import numpy as np
from IPython.display import clear_output
from scipy.fftpack import fft, fftshift
from scipy.signal import *

LOW_THRESHOLD = 2e-4
HIGH_THRESHOLD = 0.7
MUSIC_RANGE = np.linspace(16, 7903, 88)
PITCH_RANGE = 15.55
A4 = 440
LNOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
NOTES = {
    261.63: 'C',
    277.18: 'C#',
    293.66: 'D',
    311.13: 'D#',
    329.63: 'E',
    349.23: 'F',
    369.99: 'F#',
    392.00: 'G',
    415.30: 'G#',
    440.00: 'A',
    466.16: 'A#',
    493.88: 'B'
}

'''
Apply rectangular window of size sixteenth to signal
starting at index starti
'''
def segmentSignal(signal, sixteenth, starti):
    segment = np.zeros(signal.shape)
    segment[starti:starti+sixteenth] = signal[starti:starti+sixteenth]
    return segment

'''
Apply gaussian window of size windowsize
starting at index starti
window has standard of deviation of windowsize // 2
'''
def gaussWindow(signal, windowsize, starti):
    segment = np.copy(signal)
    endi = starti + windowsize
    window = windows.gaussian(windowsize, std= windowsize // 2, sym=True).reshape(-1,)
    
    for i in range(len(signal)):
        if i >= starti and i < endi:
            segment[i] *= window[i-starti]
        else:
            segment[i] = 0
    return segment.reshape(signal.shape)

def getPitchList(sample_rate, time_domain_sig, plot=0):
    notes = []
    
    if (plot):
        plt.plot(time_domain_sig)
        plt.show()

    #Normalize method from preprocessing.py
    

    num_samples = len(time_domain_sig)
    clip_len = num_samples // sample_rate
    onesec = sample_rate

    #determines size of window as 1/8 of a second
    #currently assuming 60 bpm
    sixteenth = onesec // 8
    df = sample_rate / num_samples
    time_ax = np.linspace(0, clip_len, num_samples)
    freq_ax = np.linspace(0, df * (num_samples - 1), num_samples)

    overlap = 0
    
    #Apply window over signal ~16 times
    #print("Pitch processor: iterating over %d samples with interval %d" % (int(num_samples), int(sixteenth)))

    for i in range(0, num_samples, sixteenth):
        segment = segmentSignal(time_domain_sig, sixteenth, i)

        assert(segment.shape == time_domain_sig.shape)

        #pass over negligible segments
        #may be changed later to consider rests
        if np.amax(segment) < 0.15:
            notes.append("##")
            continue


        #If you want to see the graph with segment 
        #highlighted every iteration
        if (plot):
            plt.plot(time_domain_sig)
            plt.plot(segment)
            plt.show()

        freq_domain_sig = np.abs(fft(segment))

        max = np.amax(freq_domain_sig[0: 8000])
        maxi = np.where(freq_domain_sig[0:8000] == max)[0]
        maxout = maxi

        #Ensures we don't take logarithm of 0
        if (freq_ax[maxout] == 0):
            notes.append("##")
            continue

        #Apply standard formula to determine number of steps away from A
        num_semitones = round(12 * math.log2(freq_ax[maxout] / A4))
        note = LNOTES[num_semitones % 12]
        notes.append(note)
    print(f"\n--------Pitch Processor output--------\n{notes}")
    return notes

#For visualizing signals
def getNoteGraph(fileName, plot=True):
    sample_rate, time_domain_sig = wavfile.read(fileName)
    num_samples = len(time_domain_sig)
    clip_len = num_samples // sample_rate
    onesec = sample_rate
    sixteenth = onesec // 4
    df = sample_rate / num_samples
    time_ax = np.linspace(0, clip_len, num_samples)
    freq_ax = np.linspace(0, df * (num_samples - 1), num_samples)

    segment = segmentSignal(time_domain_sig, sixteenth, int(sample_rate * 2.5))

    freq_domain_sig = fft(segment)

    max = np.amax(freq_domain_sig[0: 8000])
    maxi = np.where(freq_domain_sig[0:8000] == max)[0]
    print(maxi)

    print("Note detected at ", freq_ax[maxi])

    num_semitones = (12 * math.log2(freq_ax[maxi] / A4))
    print(LNOTES[int(num_semitones % 13)])

    if plot:
        plt.subplot(4, 1, 1)
        plt.plot(time_ax, time_domain_sig)
        plt.title("Original Signal")
        plt.xlim([0, clip_len])

        plt.subplot(4, 1, 2)
        plt.plot(windows.gaussian(sixteenth, std=sixteenth//50))

        plt.subplot(4, 1, 3)
        plt.plot(time_ax, segment)
        plt.title("Segmented Signal")
        plt.xlim([0, clip_len])

        plt.subplot(4, 1, 4)    
        plt.plot(freq_ax, abs(freq_domain_sig))
        plt.title("Frequency Domain")
        plt.xlim([200, 600])
        plt.show()
    return None