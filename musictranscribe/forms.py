from django import forms;
from audioprocessing.pitchprocessor import getPitchList;

class AudioForm(forms.Form):
    file = forms.FileField(label='Upload an audio file')
    clef = forms.ChoiceField(label='Select a clef', choices=[('treble', 'Treble'), ('bass', 'Bass')])
    time_signature = forms.ChoiceField(label='Select a time signature', 
        choices=[('4/4', '4/4'), ('3/4', '3/4'), ('2/4', '2/4'), ('6/8', '6/8'), ('3/8', '3/8')])