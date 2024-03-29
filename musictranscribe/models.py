from django.db import models

NOTE_CHOICES = (
    ('A', 'A'), ('A#' , 'A#'), ('B', 'B'), ('C', 'C'), ('C#', 'C'), ('D', 'D'), 
    ('D#', 'D#'), ('E', 'E'), ('F', 'F'), ('F#', 'F#'), ('G', 'G'), ('G#', 'G#')
)

class Note(models.Model):
    name = models.CharField(max_length=2, choices=NOTE_CHOICES)
    length = models.DecimalField(max_length=1, decimal_places=2, max_digits=5)
    clef = models.CharField(max_length=6, default="treble")