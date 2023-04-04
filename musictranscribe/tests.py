from django.test import TestCase
from musictranscribe.noteformatting import *

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

        # Test fourQuarterNotes
        halfNotes = splitNotes(self.fourHalfNotes)
        assert len(halfNotes) == 4, "Measure is wrong length"
        for note in halfNotes:
            assert note['duration'] == '2', f"Expected duration 2, got duration {note['duration']}"

        # Test fourHalfNotes
        sixbeats = splitNotes(self.sixBeatNote)
        for note in sixbeats: print(note)
        assert len(sixbeats) == 3, print(sixbeats)
        for i in range(len(sixbeats)):
            assert(sixbeats[i]['duration'] in ['4', '2']), f"Expected duration 4 or 2, got duration {sixbeats[i]['duration']}"

        # Test fourQuarterNotes
        quarterNotes = splitNotes(self.fourQuarterNotes)
        assert len(quarterNotes) == 4, print(quarterNotes)
        for note in quarterNotes: 
            assert note['duration'] == '4', f"Expected duration 4, got {note['duration']}"

        print("Passed!")