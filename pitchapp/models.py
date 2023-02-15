from django.db import models

# Create your models here.

class Note(models.Model):
    name = models.CharField(max_length=2);
    name = models.CharField(max_length=2, choices=[('A', 'A'), ('As' , 'A#'), ('B', 'B'), ('C', 'C'), ('Cs', 'C'), ('D', 'D'), ('Ds', 'D#'), ('E', 'E'),
                                                   ('F', 'F'), ('Fs', 'F#'), ('G', 'G'), ('Gs', 'G#')]);
    length = models.DecimalField(max_length=1, decimal_places=2, max_digits=5);
    clef = models.TextChoices('treble', 'bass');