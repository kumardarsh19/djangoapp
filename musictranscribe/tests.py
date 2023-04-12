from django.test import TestCase
from musictranscribe.noteformatting import *
from audioprocessing.globalvars import *

class FormattingTestCase(TestCase):
    def setUp(self):
        #4/4 time

        bpm = 4
        onebeat = 4
        self.fourQuarterNotes = [generateNote('C', 8*8)] * 4

        self.fourHalfNotes = [generateNote('C', 16*8)] * 4

        self.sixBeatNote = [generateNote('C', 6*8*8), generateNote('C', 2*8*8)]

        self.twoQuarterOneHalf = [generateNote('C', 4), generateNote('F',4), 
                                  generateNote('D', 2)]
        
        self.oneLargeNote = [generateNote('C', 40)]
        
    def testRemoveLargeNotes(self):
        print("Testing removeLargeNotes...")
        beatsPerMeasure = 4

    

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