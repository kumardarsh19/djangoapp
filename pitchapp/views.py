from django.shortcuts import render
from .forms import audioForm
from pitchprocessor import getPitchList
from rhythmprocessor import getOnsetList
from integrator import getNoteList

# Create your views here.

def home_view(request):
    if request.POST:
        context = {};
       
        file = request.FILES.get('filen')
        context['notes'] = getPitchList(file.name)
        return render(request, 'home.html', context)
    
    return render(request, "home.html")

def return_view(request):
    context = {}
    data = request.FILES
    
    file = request.FILES.get('filen')
    clef = request.get('clef') # TODO: GET CLEF FROM FORM.
    notesPitches = getPitchList(file.name)
    notesOnsets = getOnsetList(file.name)
    context['notes'] = getNoteList(notesPitches, notesOnsets, clef)

    return render(request, "return.html", context)
