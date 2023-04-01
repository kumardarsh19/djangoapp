from django import forms;
from audioprocessing.pitchprocessor import getPitchList;

class AudioForm(forms.Form):
    file = forms.FileField(label='Upload an audio file',)
    clef = forms.ChoiceField(label='Select a clef', choices=[('treble', 'Treble'), ('bass', 'Bass')])
    time_signature = forms.ChoiceField(label='Select a time signature', 
        choices=[('4/4', '4/4'), ('3/4', '3/4'), ('2/4', '2/4'), ('6/8', '6/8'), ('3/8', '3/8')])
    tempo = forms.CharField(max_length=3, min_length=2, empty_value="60")

    def clean(self):
        cleaned_data = super().clean()
        clef = cleaned_data.get('clef')
        time_signature = cleaned_data.get('time_signature')
        return cleaned_data