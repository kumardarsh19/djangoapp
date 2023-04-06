from django import forms;
from audioprocessing.pitchprocessor import getPitchList;

TIME_SIGNATURE_CHOICES = (
    ('4/4', '4/4'), ('3/4', '3/4'), ('2/4', '2/4'), 
    ('0.752', '6/8'), ('3/8', '3/8')
)
CLEF_CHOICES = (
    ('treble', 'Treble'), ('bass', 'Bass')
)

class AudioForm(forms.Form):
    file = forms.FileField(label='Upload an audio file',)
    clef = forms.ChoiceField(label='Select a clef', choices=CLEF_CHOICES)
    time_signature = forms.ChoiceField(label='Select a time signature', 
        choices=TIME_SIGNATURE_CHOICES)
    tempo = forms.CharField(max_length=3, min_length=2, empty_value="00", required=False)

    def clean(self):
        cleaned_data = super().clean()
        clef = cleaned_data.get('clef')
        time_signature = cleaned_data.get('time_signature')
        return cleaned_data