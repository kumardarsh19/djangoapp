from scipy.signal import find_peaks
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import time
from preprocessing import normalize;

found = 1
not_found = 0
onset_height = 1000

def plot(left_bound, right_bound, y, peak_pos, height):
    x = np.linspace(left_bound, right_bound, len(y))
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot(x,y)
    ax.scatter(peak_pos, height, color = 'r', s = 15, marker = 'D', label = 'Maxima')
    ax.legend()
    ax.grid()
    plt.show()

def plot_time(audio_data, audio_length, samples):
    time = np.linspace(0, audio_length, samples)
    plt.plot(time, audio_data)
    plt.show()

def getOnsetList(audio_file):
    sampling_rate, audio_data = wavfile.read("audios/C-scale.wav")
    aduio_data = normalize(audio_data)
    max_amplitude = np.max(np.abs(audio_data))
    time_interval = sampling_rate // 8
    samples = len(audio_data)
    audio_length = samples // sampling_rate
    peaks = []

    #print(audio_data)
    #print(f"\n\taudio_length: {audio_length}\n\tsamples: {samples}\n\tsampling_rate: {sampling_rate}\n\ttime_interval: {time_interval}")
    #plot_time(audio_data, audio_length, samples)
    start_time = time.time()
    for i in np.arange(0, samples, time_interval):
        left_bound = i
        right_bound = i + time_interval
        signal = audio_data[left_bound:right_bound]
        localPeaksX, localPeaksInfo = find_peaks(signal, 
                                                 distance=time_interval, 
                                                 height=onset_height)

        # Append a 1 if there is a peak, 0 otherwise.
        if len(localPeaksX) > 0:
            peaks.append(found)
        else:
            peaks.append(not_found)
    print(f"peaks: {peaks}")
    print("--- %s seconds ---" % (time.time() - start_time))

    return peaks

if __name__ == "__main__":
    audio_file = "audio_files/C scale.m4a"
    rhythm(audio_file)