from django import forms;
from pitchprocessor import getNoteList;

class audioForm(forms.Form):
    file = forms.FileField();

    