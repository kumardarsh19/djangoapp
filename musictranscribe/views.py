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
            clef = form.cleaned_data['clef']
            time_signature = form.cleaned_data['time_signature']
            print(f"file: {file}, clef: {clef}, time_signature: {time_signature}")
            
            notesPitches = getPitchList(file)
            context['numBars'] = getNumBars(notesPitches, time_signature);
            notesOnsets = getOnsetList(file)
            context['notes'] = getNoteList(notesPitches, notesOnsets, clef)
            print(context)
            print(f"file: {file}, clef: {form.cleaned_data['clef']}, time_signature: {form.cleaned_data['time_signature']}")
            context['pitches'] = getPitchList(file)
            context['onsets'] = getOnsetList(file)
            context['clef'] = form.cleaned_data['clef']
            context['timeSignature'] = form.cleaned_data['time_signature']
            return render(request, 'home.html', context)
    return render(request, "home.html", context)


def getNumBars(pitchList, time_sig):
    return len(pitchList) // int(time_sig[0]);
