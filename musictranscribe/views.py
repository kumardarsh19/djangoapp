from django.shortcuts import render
from audioprocessing.pitchprocessor import getPitchList
from audioprocessing.rhythmprocessor import getOnsetList
from audioprocessing.integrator import getNoteList
from .forms import AudioForm

def home_view(request):
    context = {'form': AudioForm()}
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            timeSignature = form.cleaned_data['time_signature']
            clef = form.cleaned_data['clef']
            # print(f"file: {file}, clef: {clef}, time_signature: {time_signature}")
            notesPitches = getPitchList(file)
            notesOnsets = getOnsetList(file)
            context['numBars'] = getNumBars(notesPitches, timeSignature)
            context['pitches'] = notesPitches
            context['onsets'] = notesOnsets
            context['clef'] = clef
            context['timeSignature'] = timeSignature
            return render(request, 'home.html', context)
    return render(request, "home.html", context)

def getNumBars(pitchList, time_sig):
    return len(pitchList) // int(time_sig[0])