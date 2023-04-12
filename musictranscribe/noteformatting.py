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

#return duration(s) of input
def getDurations(notelist):
    if isinstance(notelist, dict):
        return int(notelist['duration'])
    elif isinstance(notelist, list):
        return [int(note['duration']) for note in notelist]
    else:
        assert(0), "getDurations fails"

#return note name(s) of input
def getKeys(notelist):
    if isinstance(notelist, dict):
        return notelist['key']
    elif isinstance(notelist, list):
        return [note['key'] for note in notelist]
    else:
        assert(0), "getKeys fails"

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

def getNumStaves(notelist, time_signature='4/4'):
    assert(len(notelist) > 0)
    # Determine how many eighth notes we can get per stave.
    time_signature_frac = time_signature.split('/')
    numerator, denominator = int(time_signature_frac[0]), int(time_signature_frac[1])
    if denominator == 4: staveDuration = 2 * numerator
    elif denominator == 8: staveDuration = numerator

    beatsPerMeasure = int(time_signature[0])
    oneBeat = int(time_signature[-1])

    # Determine how many staves we need.
    totalDuration = 0
    numStaves = 1
    for i in range(len(notelist)):
        duration = int(notelist[i]['duration'])
        totalDuration += oneBeat / duration
        if (totalDuration > beatsPerMeasure):
            numStaves += 1
            totalDuration = duration

    # Round to the nearest multiple of 3.
    print(f"numStaves: {numStaves}\nnumStaves rounded to multiple of 3: {3 * math.ceil(numStaves / 3)}")
    return 3 * math.ceil(numStaves / 3)

#gives each note a stave index to determine which stave it goes in
def assignStaves(notelist, numStaves, beatsPerMeasure, oneBeat):
    stavei = 0
    totalDuration = 0
    staveNoteList = {0: []}
    #print(f"\n\noneBeat: {oneBeat}\nbeatsPerMeasure: {beatsPerMeasure}")
    for i, note in enumerate(notelist):
        assert(stavei < numStaves)
        note['stave'] = stavei
        noteDuration = oneBeat / int(note['duration'])
        totalDuration += noteDuration #convert from vex-form to number-of-beats
        #print(f"\n------------------------\nNote_{i}\nnoteduration: {noteDuration}\ntotalDuration: {totalDuration}\n\n")
        if (totalDuration > beatsPerMeasure):
            totalDuration = noteDuration
            stavei += 1
            staveNoteList[stavei] = [note]
        else: staveNoteList[stavei].append(note)
    return staveNoteList

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

        assert(duration > 0 and numVexBeats > 0)

        if (math.log(numVexBeats, 2) % 1 == 0):
            beatList.append(generateNote(key, numVexBeats))
        else:
            while (math.log(numVexBeats, 2) % 1 != 0): #Add largest note possible, then deal with what's left
                nearestPower = 2 ** int(math.log(numVexBeats, 2))
                beatList.append(generateNote(key, oneBeat / nearestPower))
                duration -= nearestPower
                numVexBeats = oneBeat / duration
                if numVexBeats <= 0: break
    return beatList

#input integrator output
#notelist: each duration is in units of 1/8th beat
#duration 4 -> 4* 1/8th beats long
def completeFormatting(notelist, time_sig = '4/4'):
    assert(len(time_sig.split('/')) == 2)
    beatsPerMeasure = int(time_sig[0])
    oneBeat = int(time_sig[-1])

    originalsize = len(notelist)

    #1. remove notes that are longer than one full measure in length
    notelist = removeLargeNotes(notelist, 8 * beatsPerMeasure)
    assert(len(notelist) >= originalsize)
    for note in notelist:   
        assert(int(note['duration']) > 0)

    #2. convert to vexflow
    originalsize = len(notelist)
    notelist = vexForm(notelist, time_sig)
    assert(len(notelist) >= originalsize)
    for note in notelist:
        duration = int(note['duration'])
        assert(math.log(duration, 2) % 1 == 0)

    #3. assign a stave index to each note
    numStaves = getNumStaves(notelist, time_sig)
    staveNoteList = assignStaves(notelist, numStaves, beatsPerMeasure, oneBeat)

    #removeTies(staveNoteList)

    # Sort dictionary by keys indexes.
    sortedIndexes = sorted(list(staveNoteList.keys()))
    staveNoteList = {index: staveNoteList[index] for index in sortedIndexes}
    return staveNoteList