from django.shortcuts import render
from scipy.io import wavfile

from audioprocessing.pitchprocessor import getPitchList
from audioprocessing.rhythmprocessor import getOnsetList
from audioprocessing.preprocessing import normalize
from audioprocessing.signaltonoise import signaltonoise
from audioprocessing.globalvars import *

from .forms import AudioForm
import numpy as np
import math
import json
import librosa

from musictranscribe.noteformatting import *

def validSNR(signal):
    snr = signaltonoise(signal)
    if isinstance(snr, float):
        snr = abs(snr)
    else:
        snr = abs(snr[0])
    return snr >= SNR_THRESHOLD

def home_view(request):
    context = {'form': AudioForm()}
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        print("form not valid")
        if form.is_valid():
            print("form is valid")
            # Get form data.
            file = form.cleaned_data['file']
            timeSignature = form.cleaned_data['time_signature']
            clef = form.cleaned_data['clef']
            tempo = int(form.cleaned_data['tempo'])
            signal, fs = librosa.load(file, mono=1)
            
            print("Librosa signal shape: ", signal.shape)

            # Check SNR >= 60 dB.
            if not validSNR(signal):
                print(f"SNR is too low. Please upload a better quality audio file.")
                context['reject'] = True
                return render(request, "home.html", context)
            
            # Normalize signal.
            signal = normalize(signal)
            print("Original signal size: %d" % signal.size)
            signal = signal[np.where(signal != 0)[0][0]:]
            print("New signal size: %d" % signal.size)

            # Estimate tempo if user does not enter it.
            estTempo, beats = librosa.beat.beat_track(y=signal, sr=fs)
            if tempo == 0: tempo = estTempo
            else: tempo = int(10 * round(tempo / 10))

            print(f"tempo: {tempo}")
            print(f"beats: {beats}")

            # Call rhythm and pitch processors.
            notesOnsets = getOnsetList(fs, signal, tempo)
            notesPitches = getPitchList(fs, signal, tempo)
            lenPitches = len(notesPitches)
            lenOnsets = len(notesOnsets)
            print(f"lenPitches: {lenPitches}; lenOnsets: {lenOnsets}")
            assert(lenPitches == lenOnsets)

            # Integrate the rhythm and pitch processor outputs.
            integratedList = integrate(notesPitches, notesOnsets)
            context['integrated'] = json.dumps(integratedList, indent=1)

            # Get notes assigned to respective stave index.
            formattedList, keyList, durList = completeFormatting(integratedList)

            # Calculate number of staves needed with total duration of notes.
            context['number_staves'] = len(formattedList)
            print(f"\nformattedList: {formattedList}\n")
            
            context['formatted'] = json.dumps(formattedList, indent=1)
            context['numBars'] = getNumBars(notesPitches, timeSignature)

            context['clef'] = clef
            context['time_signature'] = timeSignature
            print(f"time_signature: {timeSignature}")

            context['keysInOrder'] = keyList
            context['durationsInOrder'] = durList

            context['post'] = 1

            print("Number of onsets: %d" % len(durList))
            return render(request, 'home.html', context)
    return render(request, "home.html", context)

def getNumBars(pitchList, time_sig):
    return len(pitchList) // int(time_sig[0])