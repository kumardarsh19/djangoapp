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

        self.sixBeatNote = [generateNote('C', 6), generateNote('C', 2)]

    def testSplitNotes(self):
        print("Testing splitNotes...")
        halfNotes = splitNotes(self.fourHalfNotes)
        assert len(halfNotes) == 4, "Measure is wrong length"
        for note in halfNotes:
            assert note['duration'] == '2', "Duration is wrong"

        sixbeats = splitNotes(self.sixBeatNote)
        for note in sixbeats:
            print(note)
        assert len(sixbeats) == 3, print(sixbeats)

        for i in range(len(sixbeats)):
            assert(sixbeats[i]['duration'] in ['4', '2']), "Wrong note duration"

        print("Passed!")