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
    note['duration'] = str(duration)

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

    return notes

    

def splitNotes(notelist, time_signature="4/4"):
    newNotes = []
    unitsPerMeasure = 8 * int(time_signature[-1])

    measureIndex = 0
    totalDuration = 0
    for i in range(len(notelist)):
        key, duration, type = notelist[i]['key'], int(notelist[i]['duration']), notelist[i]['typ']
        totalDuration += duration
        if (totalDuration <= unitsPerMeasure):
            newNotes.append(notelist[i])
        else:
            overflow = totalDuration - unitsPerMeasure
            duration0 = duration - overflow
            for dur in [duration0, overflow]:
                if (dur > 0): newNotes.append(generateNote(key[0], dur))
            totalDuration = overflow
    
    

    return newNotes

def formatDuration(duration, time_signature='4/4'):
    unitsPerMeasure = 8 * int(time_signature[-1])
    margin = 2
    duration = int(duration)
    assert(duration > 0)
    if (duration <= 4 + margin): return '8' #eighth note
    elif (duration <= 8 + 2*margin): return "4" #quarter note
    elif (duration <= 16 + 4*margin): return "2" #half note
    else: return "1" #whole note


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
            integratedList = integrate(notesPitches, notesOnsets)
            context['integrated'] = json.dumps(integratedList, indent=1)
            
            print("Integrated list: ", context['integrated'])

            splitList = splitNotes(integratedList, timeSignature)
            print("After splitting long notes: ", json.dumps(splitList, indent=1))

            for note in splitList:
                duration = note['duration']
                note['duration'] = formatDuration(duration, timeSignature)
            for n in splitList:
                assert(n['duration'] in ['1', '2', '4', '8'])
            context['formatted'] = json.dumps(splitList, indent=1)
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