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

#detect_beats_channels detects if there is a sound at a specific window for
# an audio containing more than one channel.
def detect_beats_channels(audio_data) -> np.array:
    try:
        if len(audio_data) > 1:
            beats = []
            data_length = len(audio_data)
            channel_length = len(audio_data[0])
            for data in range(data_length):
                greatest_beat = 0
                for channel in range(channel_length):
                    if np.abs(audio_data[data][channel]) > greatest_beat:
                        greatest_beat = np.abs(audio_data[data][channel])
                beats.append(greatest_beat)
            print("New beats\n")
            return np.array(beats)
    except:
        print("Same beats\n")
        return audio_data

def getOnsetList(audio_file):
    #TODO: If wavfile.read returns 2D array, this code will not work.
    sampling_rate, audio_data = wavfile.read(audio_file)
    audio_data = detect_beats_channels(audio_data)
    time_interval = sampling_rate // 8
    samples = len(audio_data)
    audio_length = samples // sampling_rate
    peaks = []
    start_time = time.time()
    for i in np.arange(0, samples, time_interval):
        left_bound = i
        right_bound = i + time_interval
        signal = audio_data[left_bound:right_bound]
        localPeaksX, localPeaksInfo = find_peaks(signal, 
                                                 distance=time_interval, 
                                                 height=onset_height)
        if len(localPeaksX) > 0:
            peaks.append(found)
        else:
            peaks.append(not_found)
    print(f"\n{peaks}")
    print("\n\n--- %s seconds ---" % (time.time() - start_time))
    return peaks

if __name__ == '__main__':
    getOnsetList("audios/Random.wav")