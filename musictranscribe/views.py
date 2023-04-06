from django.shortcuts import render
from scipy.io import wavfile

from audioprocessing.pitchprocessor import getPitchList
from audioprocessing.rhythmprocessor import getOnsetList
from audioprocessing.preprocessing import normalize
from audioprocessing.signaltonoise import signaltonoise
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
    return snr >= 60

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
            fs, signal = wavfile.read(file)

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
            else: tempo = int(tempo)

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
            print("Integrated list: ", context['integrated'])

            # Calculate number of staves needed with total duration of notes.
            context['number_staves'] = getNumStaves(integratedList, timeSignature)

            formattedList = completeFormatting(integratedList)
            
            context['formatted'] = json.dumps(formattedList, indent=1)
            print("Formatted list, ")
            print(context['formatted'])
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