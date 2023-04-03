from django.shortcuts import render
from scipy.io import wavfile

from audioprocessing.pitchprocessor import getPitchList
from audioprocessing.rhythmprocessor import getOnsetList
from audioprocessing.preprocessing import normalize
from audioprocessing.signaltonoise import signaltonoise
from .forms import AudioForm
import numpy as np

import json

def validSNR(signal):
    snr = signaltonoise(signal)
    if isinstance(snr, float):
        snr = abs(snr)
    else:
        snr = abs(snr[0])
    return snr >= 60

def generateNote(key, duration):
    note = {}
    note['key'] = key + '/4'
    note['duration'] = duration

    if (key == 'R'): note['typ'] = 'r'
    else: note['typ'] = 'n'

    return note

def integrate(pitches, onsets):
    notes = []
    duration = 1

    for i in range(1, len(pitches)):
        if (pitches[i] == pitches[i-1]): duration += 1
        elif (onsets[i-1] == 1):
            notes.append(generateNote(pitches[i-1], duration))
            duration = 1
        else:
            notes.append(generateNote('R', duration))
            duration = 1

    if (onsets[-1] == 1):
        notes.append(generateNote(pitches[-1], duration))
    else:
        notes.append(generateNote('R', duration))

    return json.dumps(notes, indent=1)



def home_view(request):
    context = {'form': AudioForm()}
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            # Get form data.
            file = form.cleaned_data['file']
            timeSignature = form.cleaned_data['time_signature']
            clef = form.cleaned_data['clef']
            tempo = int(form.cleaned_data['tempo'])
            
            fs, signal = wavfile.read(file)

            # Check SNR >= 60 dB.
            if not validSNR(signal):
                print(f"SNR is too low. Please upload a better quality audio file.")
                context['reject'] = True
                return render(request, "home.html", context)

            # Call rhythm and pitch processors.
            signal = normalize(signal)
            print("Original signal size: %d" % signal.size)
            signal = signal[np.where(signal != 0)[0][0]:]
            print("New signal size: %d" % signal.size)
            notesOnsets = getOnsetList(fs, signal)
            notesPitches = getPitchList(fs, signal, tempo)
            lenPitches = len(notesPitches)
            lenOnsets = len(notesOnsets)
            
            print(f"lenPitches: {lenPitches}; lenOnsets: {lenOnsets}")
            assert(lenPitches == lenOnsets)
            
            context['integrated'] = integrate(notesPitches, notesOnsets)
            print(f"Integrated list: {context['integrated']}")
            context['numBars'] = getNumBars(notesPitches, timeSignature)
            context['pitches'] = notesPitches
            context['onsets'] = notesOnsets
            context['clef'] = clef
            context['timeSignature'] = timeSignature
            print(f"time_signature: {timeSignature}")
            return render(request, 'home.html', context)
    return render(request, "home.html", context)

def getNumBars(pitchList, time_sig):
    return len(pitchList) // int(time_sig[0])