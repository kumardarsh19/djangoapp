from django.shortcuts import render
from pitchprocessor import getPitchList
from rhythmprocessor import getOnsetList
from integrator import getNoteList
from .forms import AudioForm

# Create your views here.

def home_view(request):
    print("IN HOME VIEW!")
    context = {}
    if request.method == 'POST':
        print("IN POST!")
        file = request.FILES.get('file')
        context['notes'] = getPitchList(file.name)
        context['form'] = AudioForm()
        return render(request, 'home.html', context)
    context['form'] = AudioForm()
    return render(request, "home.html", context)
    

def return_view(request):
    context = {}
    data = request.FILES
    
    file = request.FILES.get('filen')
    clef = request.get('clef') # TODO: GET CLEF FROM FORM.
    notesPitches = getPitchList(file.name)
    notesOnsets = getOnsetList(file.name)
    context['notes'] = getNoteList(notesPitches, notesOnsets, clef)

    return render(request, "return.html", context)
