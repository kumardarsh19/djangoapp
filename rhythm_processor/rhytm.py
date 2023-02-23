from scipy.signal import find_peaks
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

#time_interval is a sixteenth note

def plot(left_bound, right_bound, y, peak_pos, height):
    x = np.linspace(left_bound, right_bound, len(y))
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot(x,y)
    print("\n\nISSUE HERE!\n")
    ax.scatter(peak_pos, height, color = 'r', s = 15, marker = 'D', label = 'Maxima')
    ax.legend()
    ax.grid()
    plt.show()

def plot_time(audio_data, audio_length, samples):
    time = np.linspace(0, audio_length, samples)
    plt.plot(time, audio_data)
    plt.show()

def rhythm(audio_file):
    sampling_rate, audio_data = wavfile.read("../audios/C-scale.wav")
    print(audio_data)
    time_interval = sampling_rate // 8
    samples = len(audio_data)
    audio_length = samples // sampling_rate
    peaks = []
    print(f"\n\taudio_length: {audio_length}\n\tsamples: {samples}\n\tsampling_rate: {sampling_rate}\n\ttime_interval: {time_interval}")
    #plot_time(audio_data, audio_length, samples)

    for i in np.arange(0, samples, time_interval):
        left_bound = i
        right_bound = i + time_interval
        signal = audio_data[left_bound:right_bound]
        localPeaks = find_peaks(signal, height=1, threshold=1, distance=1) #TODO: what parameters should we use for finding the peaks.
        height = localPeaks[1]['peak_heights']
        peak_pos = signal[localPeaks[0]]

        # Plot for testing.
        if i == 0:
            plot(left_bound, right_bound, signal, peak_pos, height)

        # Append a 1 if there is a peak, 0 otherwise.
        if len(localPeaks) > 0:
            peaks.append(1)
        else:
            peaks.append(0)

       #time = np.linspace(start=0, stop=time_interval, num=1) #TODO: not sure about num/samples parameter.
       #plt.plot(time, signal)
    print(peaks)

if __name__ == "__main__":
    audio_file = "audio_files/C scale.m4a"
    rhythm(audio_file)