from django.shortcuts import render
from audioprocessing.pitchprocessor import getPitchList
from audioprocessing.rhythmprocessor import getOnsetList
from .forms import AudioForm

def home_view(request):
    context = {'form': AudioForm()}
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            timeSignature = form.cleaned_data['time_signature']
            clef = form.cleaned_data['clef']
            notesOnsets = getOnsetList(file)
            notesPitches = getPitchList(file)
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