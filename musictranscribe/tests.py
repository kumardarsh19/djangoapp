from django.test import TestCase
from musictranscribe.noteformatting import *

# Create your tests here.

class FormattingTestCase(TestCase):
    def setUp(self):
        self.fourQuarterNotes = [{
            'key': 'C/4',
            'duration': '4',
            'typ': 'n'
        }] * 4

        self.fourHalfNotes = [{
            'key': 'C/4',
            'duration': '2',
            'typ': 'n'
        }] * 4

    def testSplitNotes(self):
        halfNotes = splitNotes(self.fourHalfNotes)
        assert len(halfNotes) == 4, "Measure is wrong length"
        for note in halfNotes:
            assert note['duration'] == '2', "Duration is wrong"