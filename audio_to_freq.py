from scipy.io import wavfile
import matplotlib.pyplot as plt
import math
import numpy as np
from IPython.display import clear_output
from scipy.fftpack import fft, fftshift
from scipy.signal import *
from sklearn.preprocessing import *

LOW_THRESHOLD = 2e-4;
HIGH_THRESHOLD = 0.7;
MUSIC_RANGE = np.linspace(16, 7903, 88);

PITCH_RANGE = 15.55;
A4 = 440;

LNOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'];

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

def isValidNote(freq):
    return freq > MUSIC_RANGE[0] and freq < MUSIC_RANGE[-1];

def getFreq(start, end, sig):
    segment = sig[start:end];
    freq = np.abs(fft(segment));
    
    return np.mean(freq);

def getFirstNonzero(sig, starti):
    for i in range(starti, len(sig)):
        if sig[i] != 0:
            return i;

def findClosestKey(freq, d=NOTES):
    keys = list(d.keys());
    for i in range(len(keys) - 1):
        if keys[i] < freq and keys[i+1] > freq:
            return keys[i];

    return keys[-1];


#time is array of time values
#freq is frequency at each time value
def detectNotes(time, freq, box_size):
    ret = {};
    step = time.size // box_size;
    for i in range(0, len(freq), box_size):
        segment = freq[i : i + box_size];
        avgFreq = np.mean(segment);
        print(avgFreq / A4);
        num_semitones = int(12 * math.log2(avgFreq / A4));
        ret[i // box_size] = LNOTES[num_semitones % 13];

    print(ret);
    return ret;

def getSTFT(fileName):
    sample_rate, time_domain_sig = wavfile.read("audios/C-scale.wav");
    notes = [];
    frequencies = [];

    num_samples = len(time_domain_sig);
    clip_len = num_samples // sample_rate;
    onesec = sample_rate;

    time_ax = np.linspace(0, clip_len, num_samples);
    plt.subplot(2, 1, 1)
    plt.plot(time_ax, time_domain_sig);
    plt.xlim([0, 8]);



    sixteenth = onesec // 8;
    f, t, Zxx = stft(time_domain_sig, fs=sample_rate, window = 'hann', nperseg = sixteenth, noverlap = sixteenth // 8);

    
    print("Shape of Zxx is equal to (f.shape, t.shape)")
    print("Examine a column ti to get magnitudes at that specific time")
    magZ = np.abs(Zxx);
    #normalMagZ = normalize(magZ, 'l1', axis=0)
    
    magZ = normalize(magZ, 'l1', axis=0);

    

    
    print("Mean: %f | Median: %f | Max: %f | Min: %f" % (np.mean(magZ), np.median(magZ), np.amax(magZ), np.amin(magZ)));
    boolMat = (magZ > np.mean(magZ)).astype('int');
    
    assert(boolMat.shape == magZ.shape);

    plt.subplot(2, 1, 2)
    plt.pcolormesh(t, f, magZ, shading='gouraud')

    plt.title('STFT Magnitude')

    plt.ylabel('Frequency [Hz]')
    plt.ylim((0, 500));
    
    plt.xlabel('Time [sec]')

    plt.show()

    return t, f, magZ, sixteenth;


def getNotes(fileName):

   

    sample_rate, time_domain_sig = wavfile.read("audios/C-scale.wav");
    notes = [];
    frequencies = [];

    num_samples = len(time_domain_sig);
    clip_len = num_samples // sample_rate;
    onesec = sample_rate;

    time_ax = np.linspace(0, clip_len, num_samples);
    plt.subplot(2, 1, 1)
    plt.plot(time_ax, time_domain_sig);
    plt.xlim([0, 8]);

    print(time_domain_sig.shape)

    sixteenth = onesec // 4;
    f, t, Zxx = stft(time_domain_sig, fs=sample_rate, window = 'hann', nperseg = sixteenth, noverlap = sixteenth // 8);

    
    print("Shape of Zxx is equal to (f.shape, t.shape)")
    print("Examine a column ti to get magnitudes at that specific time")
    magZ = np.abs(Zxx);
    #normalMagZ = normalize(magZ, 'l1', axis=0)
    print(magZ.shape)
    print(f.shape)
    print(t.shape)

    med = np.median(magZ);
    
    #Remove frequencies outside of musical range
    for fi in range(len(f)):
        if not isValidNote(f[fi]):
            magZ[fi] = np.where(False, magZ[fi], 0);

    secSize = len(t) // clip_len;
    
    for val in range(clip_len):
        start = secSize * val;
        end = secSize * val + secSize;
        print(tuple(range(start, end)));
        print(f[start:end])
        mean = np.mean(f[start:end]);
        key = findClosestKey(mean);
        print("Mean is %f, corresponds to %s" % (mean, NOTES[key]));

    plt.subplot(2, 1, 2)
    plt.pcolormesh(t, f, magZ, shading='gouraud')

    plt.title('STFT Magnitude')

    plt.ylabel('Frequency [Hz]')
    plt.ylim((0, 500));
    
    plt.xlabel('Time [sec]')

    plt.show()

    return {};
    for i in range(0, clip_len, sample_rate):
        if (i + sample_rate >= len(f)): break;
        avgFreq = np.mean(f[i:i+sample_rate]);
        frequencies.append(avgFreq);

    for freq in frequencies:
        print(freq)
        key = findClosestKey(freq, NOTES);
        notes.append(NOTES[key]);

    print(notes);
    return notes;



def main():
    t, f, MagZ, box_size = getSTFT("audios/C-scale.wav");
    notes = detectNotes(t, f, box_size);
    print(notes);