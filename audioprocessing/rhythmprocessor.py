from scipy.signal import find_peaks
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import time
from audioprocessing.preprocessing import normalize;

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
            return np.array(beats)
    except: 
        print("Same beats")
        return audio_data

def getOnsetList(sampling_rate, audio_data, tempo):
    # plot_time(audio_data, len(audio_data) // sampling_rate, len(audio_data))
    time_interval = int((60 / tempo) * sampling_rate // 8)
    samples = len(audio_data)
    
    audio_length = samples // sampling_rate
    peaks = []
    start_time = time.time()
    index = 0
    #print("Rhythm processor: iterating over %d samples with interval %d" % (int(samples), int(time_interval)))
    for i in range(0, samples, time_interval):
        index += 1
        left_bound = i
        right_bound = i + time_interval
        signal = audio_data[left_bound:right_bound]

        localPeaksX, localPeaksInfo = find_peaks(signal, 
                                                 distance=time_interval, 
                                                 height=0.1)
        
        if len(localPeaksX) > 0:
            #print("Peak detected at index %d" % index)
            peaks.append(found)
        else:
            peaks.append(not_found)
    print(f"\n--------Rhythm Processor output--------\n{peaks}\n")
    return peaks

if __name__ == '__main__':
    fs, signal = wavfile.read("audios/C-scale.wav")
    signal = normalize(signal)
    plot_time(signal, len(signal) // fs, len(signal))