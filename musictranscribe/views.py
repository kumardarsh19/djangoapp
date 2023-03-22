from django.shortcuts import render
from audioprocessing.pitchprocessor import getPitchList
from audioprocessing.rhythmprocessor import getOnsetList
from audioprocessing.integrator import getNoteList
from .forms import AudioForm

# Create your views here.

def home_view(request):
    context = {'form': AudioForm()}
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            clef = form.cleaned_data['clef']
            time_signature = form.cleaned_data['time_signature']
            file = form.cleaned_data['file']
            print(f"file: {file}, clef: {clef}, time_signature: {time_signature}")

            notesPitches = getPitchList(file)
            context['pitches'] = notesPitches;
            notesOnsets = getOnsetList(file)
            context['notes'] = getNoteList(notesPitches, notesOnsets, clef)
            print(context)
            return render(request, 'home.html', context)
    return render(request, "home.html", context)
