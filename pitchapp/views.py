from django.shortcuts import render
from .forms import audioForm;
from pitchprocessor import getNoteList;
# Create your views here.

def home_view(request):
    if request.POST:
        context = {};
       
        
        file = request.FILES.get('filen');
        context['notes'] = getNoteList(file.name);
        #integrate rhythm and pitch processsors
        #generate the Models and Forms
        return render(request, 'home.html', context);
    
    return render(request, "home.html");

def return_view(request):
    context = {};
    data = request.FILES;
    
    file = request.FILES.get('filen');
    context['notes'] = getNoteList(file.name);

    return render(request, "return.html", context);
