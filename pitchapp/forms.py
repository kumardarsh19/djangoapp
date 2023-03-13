from django import forms;
from pitchprocessor import getPitchList;

class audioForm(forms.Form):
    class Meta:
        fields = ['file', 'clef', 'time signature']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'clef': forms.Select(attrs={'class': 'form-control'}),
            'time signature': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'file': 'Upload an audio file',
            'clef': 'Select a clef',
            'time signature': 'Select a time signature'
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file is None:
            raise forms.ValidationError("You did not upload a file.")
        if file.name.endswith('.wav') is False:
            raise forms.ValidationError("You did not upload a .wav file.")
        return file