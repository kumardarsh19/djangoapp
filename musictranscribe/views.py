from django.shortcuts import render
from scipy.io import wavfile

from audioprocessing.pitchprocessor import getPitchList
from audioprocessing.rhythmprocessor import getOnsetList
from audioprocessing.preprocessing import normalize
from audioprocessing.signaltonoise import signaltonoise
from .forms import AudioForm

def home_view(request):
    context = {'form': AudioForm()}
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            # Get form data.
            file = form.cleaned_data['file']
            timeSignature = form.cleaned_data['time_signature']
            clef = form.cleaned_data['clef']
            fs, signal = wavfile.read(file)

            # Check SNR >= 60 dB.
            snr = abs(signaltonoise(signal)[0])
            if snr < 60:
                print(f"SNR is too low: {snr}. Please upload a better quality audio file.")
                return render(request, "home.html", context)

            # Call rhythm and pitch processors.
            signal = normalize(signal)
            notesOnsets = getOnsetList(fs, signal)
            notesPitches = getPitchList(fs, signal)
            numPitch = len(notesPitches)
            numOn = len(notesOnsets)
            assert(numPitch == numOn)
            
            context['numBars'] = getNumBars(notesPitches, timeSignature)
            context['pitches'] = notesPitches
            context['onsets'] = notesOnsets
            context['clef'] = clef
            context['timeSignature'] = timeSignature
            return render(request, 'home.html', context)
    return render(request, "home.html", context)

def getNumBars(pitchList, time_sig):
    return len(pitchList) // int(time_sig[0])