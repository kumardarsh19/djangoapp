import math
import numpy as np


def generateNote(key, duration):
    note = {}
    if '/4' in key: key = key[0]
    note['key'] = key + '/4'
    note['duration'] = str(int(duration))
    if (key == 'R'): note['typ'] = 'r'
    else: note['typ'] = 'n'
    return note

def tieNotes(note1, note2):
    note1['next'] = note2

def integrate(pitches, onsets):
    notes = []
    duration = 1
    for i in range(1, len(pitches)):
        if (pitches[i] == pitches[i-1]): duration += 1
        elif (onsets[i-1] == 1):
            notes.append(generateNote(pitches[i-1], duration))
            duration = 1
        else:
            notes.append(generateNote('R', duration))
            duration = 1
    if (onsets[-1] == 1):
        notes.append(generateNote(pitches[-1], duration))
    else:
        notes.append(generateNote('R', duration))
    return notes

def splitNotes(notelist, time_signature="4/4"):
    newNotes = []
    for note in notelist:
        key, duration = note['key'], int(note['duration'])
        notesadded = 0
        while (duration >= 32):
            newNotes.append(generateNote(key, 32))
            duration -= 32
            notesadded += 1

        while (duration >= 16):
            newNotes.append(generateNote(key, 16))
            duration -= 16
            notesadded += 1

        while (duration >= 8):
            newNotes.append(generateNote(key, 8))
            duration -= 8
            notesadded += 1

        while (duration >= 4):
            newNotes.append(generateNote(key, 4))
            duration -= 4
            notesadded += 1

        #add ties
        for i in range(len(newNotes) - notesadded, len(newNotes)-1):
            tieNotes(newNotes[i], newNotes[i+1])

    for note in newNotes:
        assert(int(note['duration']) % 8 == 0 or note['duration'] == '4')
        assert note['duration'] != '0', "found 0 duration"
    return newNotes

#rounds number of units to nearest multiple of 4
def formatDuration(notelist, time_signature='4/4'):
    for note in notelist:
        duration = int(note['duration'])
        assert(duration > 0)
        if (duration <= 4): newDuration = 4
        elif (duration % 4 == 0): newDuration = duration
        else:
            remainder = duration % 4
            if (remainder in [1, 2]): newDuration = duration - remainder #rounding down
            else: newDuration = duration + (4 - remainder) #rounding up

        assert(newDuration > 0)
        note['duration'] = str(newDuration)

def getNumStaves(notelist, time_signature='4/4'):
    # Determine how many eighth notes we can get per stave.
    time_signature_frac = time_signature.split('/')
    numerator, denominator = int(time_signature_frac[0]), int(time_signature_frac[1])
    if denominator == 4: staveDuration = 2 * numerator
    elif denominator == 8: staveDuration = numerator

    # Determine how many staves we need.
    totalDuration = 0
    numStaves = 1
    for i in range(len(notelist)):
        duration = int(notelist[i]['duration'])
        totalDuration += duration
        if (totalDuration > staveDuration):
            numStaves += 1
            totalDuration = duration

    # Round to the nearest multiple of 3.
    print(f"numStaves: {numStaves}\nnumStaves rounded to multiple of 3: {3 * round(numStaves / 3)}")
    return 3 * round(numStaves / 3)

#gives each note a stave index to determine which stave it goes in
def assignStaves(notelist, numStaves, beatsPerMeasure, oneBeat):
    stavei = 0
    totalDuration = 0
    staveNoteList = {0: []}
    for note in notelist:
        assert(stavei < numStaves)
        note['stave'] = stavei
        staveNoteList[stavei].append(note)
        totalDuration += oneBeat / int(note['duration']) #convert from vex-form to number-of-beats
        if (totalDuration >= beatsPerMeasure):
            totalDuration = 0
            stavei += 1
            staveNoteList[stavei] = []
    return staveNoteList

#changes duration to vexform
def convertToVexflow(staveNoteList):
    vexdict = {
        '4': '8', #eigth note 
        '8': '4', #quarter note
        '16': '2', #half note
        '32': '1', #whole note (one full measure)
    }
    for staveNotes in staveNoteList.values():
        for note in staveNotes:
            prevduration = note['duration']
            note['duration'] = vexdict[prevduration]

def removeTies(staveNoteList):
    for stave in staveNoteList.values():
        for note in stave:
            next = note.get('next', None)
            if next != None:
                if (int(note['duration']) == int(next['duration']) * 2):
                    note['dot'] = 1
                    note.pop('next')
                    next['invisible'] = 1


def removeLargeNotes(notelist, maxSize):
    ret = []
    for note in notelist:
        duration = int(note['duration'])
        while (duration > maxSize):
            ret.append(generateNote(note['key'], maxSize))
            duration -= maxSize
        
        ret.append(generateNote(note['key'], duration))


    return ret

def vexForm(notelist, time_sig, windowsize=8):
    oneBeat = int(time_sig[-1])
    
    beatList = []
    for note in notelist:
        key = note['key']
        rawDuration = int(note['duration'])
        duration = rawDuration / windowsize #find duration in number-of-beats
        duration = (round(duration * 2) / 2) #round to nearest half beat
        duration = max(duration, 0.5)

        numVexBeats = oneBeat / duration

        while (math.log(numVexBeats, 2) % 1 != 0): #Add largest note possible, then deal with what's left
            nearestPower = 2 ** int(math.log(numVexBeats, 2))
            beatList.append(generateNote(key, oneBeat / nearestPower))
            duration -= nearestPower
            numVexBeats = oneBeat / duration

        beatList.append(generateNote(key, numVexBeats))


    return beatList

#input integrator output
def completeFormatting(notelist, time_sig = '4/4'):
    assert(len(time_sig.split('/')) == 2)
    beatsPerMeasure, oneBeat = time_sig.split('/')
    beatsPerMeasure = int(beatsPerMeasure)
    oneBeat = int(oneBeat)
    windowsize = 8
    
    #1. remove notes that are longer than one full measure in length
    notelist = removeLargeNotes(notelist, windowsize * beatsPerMeasure)


    #2. convert to vexflow

    notelist = vexForm(notelist, time_sig, windowsize)
        
    for note in notelist:
        duration = int(note['duration'])
        assert(math.log(duration, 2) % 1 == 0)


    #3. assign a stave index to each note
    numStaves = getNumStaves(notelist)
    staveNoteList = assignStaves(notelist, numStaves, beatsPerMeasure, oneBeat)

    
    #removeTies(staveNoteList)


    # Sort dictionary by keys indexes.
    sortedIndexes = sorted(list(staveNoteList.keys()))
    staveNoteList = {index: staveNoteList[index] for index in sortedIndexes}


    
    for measure in staveNoteList.values():
        assert(len(measure) > 0)
    return staveNoteList