from django.test import TestCase
from musictranscribe.noteformatting import *
from audioprocessing.globalvars import *

class FormattingTestCase(TestCase):
    def setUp(self):
        #4/4 time

        bpm = 4
        self.onebeat = 8
        self.fourQuarterNotes = [generateNote('C', self.onebeat*1)] * 4

        self.fourHalfNotes = [generateNote('C', self.onebeat*2)] * 4

        self.oneLargeNote = [generateNote('C', self.onebeat*4*12)]

        self.smallLarge = [
            generateNote('C', self.onebeat*1),
            generateNote('C', self.onebeat*5),
        ]
        
    def testRemoveLargeNotes(self):
        print("Testing removeLargeNotes...")
        beatsPerMeasure = 4
        
        currTest = removeLargeNotes(self.oneLargeNote, self.onebeat*beatsPerMeasure)
        assert(len(currTest) > 1)
        assert(len(currTest) == 12)

        for notelist in [self.fourHalfNotes, self.fourQuarterNotes]:
            currTest = removeLargeNotes(notelist, self.onebeat*beatsPerMeasure)
            assert(getDurations(notelist) == getDurations(currTest))


        print("Passed!")

    def testVexNotes(self):
        print("Testing vex-formatting notes...")

        singlebeat = [generateNote('C', 8)]

        currTest = vexForm(singlebeat, '4/4')
        for note in currTest:
            assert float(note['duration']) == 4.0, print(currTest)

        currTest = vexForm(singlebeat, '3/8')
        for note in currTest:
            assert float(note['duration']) == 8.0, print(currTest)


        currTest = vexForm(singlebeat, '2/2')
        for note in currTest:
            assert note['duration'] == '2', print(currTest)

        currTest = vexForm([generateNote('C', 8), generateNote('C', 4)], '4/4')
        assert(
            len(currTest) == 2 and currTest[0]['duration'] == '4' and currTest[1]['duration'] == '8'
        ), print(currTest)

        currTest = vexForm([generateNote('C', 8), generateNote('C', 4)], '3/8')
        assert(
            len(currTest) == 2 and currTest[0]['duration'] == '8' and currTest[1]['duration'] == '16'
        ), print(currTest)


        print("Passed!")
        return