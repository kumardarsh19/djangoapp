from scipy.io import wavfile
import matplotlib.pyplot as plt
import math
import numpy as np
from IPython.display import clear_output
from scipy.fftpack import fft, fftshift
from scipy.signal import *
from statistics import mean
from audioprocessing.globalvars import *



'''
Apply rectangular window of size window_width to signal
starting at index starti
'''
def segmentSignal(signal, window_width, starti):
    segment = np.zeros(signal.shape)
    segment[starti:starti+window_width] = signal[starti:starti+window_width]
    return segment

def getPitchList(sample_rate, time_domain_sig, tempo=DEFAULT_TEMPO, plot=0):
    notes = []
    
    if (plot):
        plt.plot(time_domain_sig)
        plt.show()

    #Normalize method from preprocessing.py
    num_samples = len(time_domain_sig)
    clip_len = num_samples // sample_rate
    onesec = sample_rate

    #determines size of window as 1/8 of a beat
    window_width = int((DEFAULT_TEMPO / tempo) * onesec // WINDOW_SIZE)
    df = sample_rate / num_samples
    time_ax = np.linspace(0, clip_len, num_samples)
    freq_ax = np.linspace(0, df * (num_samples - 1), num_samples)
    print(f"freq_ax: {freq_ax}")
    print(f"\n\nfreq_ax.shape: {freq_ax.shape}\n\n")
    
    #Apply window over signal (clip_length * 8 * tempo/60 times)
    print("Pitch processor: iterating over %d samples with interval %d" % (int(num_samples), int(window_width)))
    for i in range(0, num_samples, window_width):
        segment = segmentSignal(time_domain_sig, window_width, i)
        assert(segment.shape == time_domain_sig.shape)

        #pass over negligible segments
        #may be changed later to consider rests
        if np.amax(segment) < LOW_THRESHOLD:
            notes.append("R")
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
        #TODO: dirty fix for the two values at a list index.
        freq = freq_ax[maxout] if not type(freq_ax[maxout]).__module__ == np.__name__ else mean(freq_ax[maxout])
        try:
            if (freq == 0):
                notes.append("R/4")
                continue
        except:
            print(f"freq: {freq}; type: {type(freq_ax[maxout])}")
            return

        octave = 4
        if freq < 250: octave = 3
        if freq > 510: octave = 5
        #Apply standard formula to determine number of steps away from A
        num_semitones = round(12 * math.log2(freq / A4))
        note = LNOTES[num_semitones % 12]
        x = note + '/' + str(octave)
        notes.append(note + '/' + str(octave))
    print(f"\n--------Pitch Processor output--------\n{notes}")
    return notes

#For visualizing signals
def getNoteGraph(fileName, plot=True):
    sample_rate, time_domain_sig = wavfile.read(fileName)
    num_samples = len(time_domain_sig)
    clip_len = num_samples // sample_rate
    onesec = sample_rate
    window_width = onesec // 4
    df = sample_rate / num_samples
    time_ax = np.linspace(0, clip_len, num_samples)
    freq_ax = np.linspace(0, df * (num_samples - 1), num_samples)

    segment = segmentSignal(time_domain_sig, window_width, int(sample_rate * 2.5))

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
        plt.plot(windows.gaussian(window_width, std=window_width//50))

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