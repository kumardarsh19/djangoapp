import math
import numpy as np
from audioprocessing.globalvars import *

def generateNote(key, duration):
    note = {}
    if '/4' in key: key = key[0]
    note['key'] = key + '/4'
    note['duration'] = duration
    if (key == 'R'): note['typ'] = 'r'
    else: note['typ'] = 'n'
    return note




#return duration(s) of input
def getDurations(notelist):
    if isinstance(notelist, dict):
        return (notelist['duration'])
    elif isinstance(notelist, list):
        return [(note['duration']) for note in notelist]
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

def splitNote(note, dur1, dur2):
    note1 = generateNote(note['key'], dur1)
    
    note2 = generateNote(note['key'], dur2)
    
    tieNotes(note1, note2)
    return [note1, note2]

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
    for i in range(len(durationList)):
        duration = int(durationList[i]['duration'])
        totalDuration += duration
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
    staveNoteList = {key: [] for key in range(numStaves)}
    print(f"\n\noneBeat: {oneBeat}\nbeatsPerMeasure: {beatsPerMeasure}")
    for i, note in enumerate(notelist):
        assert(stavei < numStaves)
        note['stave'] = stavei
        noteDuration = getDurations(note)
        totalDuration += noteDuration #convert from vex-form to number-of-beats
        #print(f"\n------------------------\nNote_{i}\nnoteduration: {noteDuration}\ntotalDuration: {totalDuration}\n\n")
        if (totalDuration < beatsPerMeasure):
            staveNoteList[stavei].append(note)
        elif (totalDuration == beatsPerMeasure):
            staveNoteList[stavei].append(note)
            totalDuration = 0
            stavei += 1
        else:
            assert(totalDuration > beatsPerMeasure)
            #split note into two smaller notes, tie together
            overflow = totalDuration - beatsPerMeasure
            assert(overflow > 0)
            note1, note2 = splitNote(note, noteDuration - overflow, overflow)
            #add first note to current stave
            assert(getDurations(note1) > 0)
            assert(getDurations(note2) > 0)
            if stavei not in staveNoteList.keys():
                staveNoteList[stavei] = []

            staveNoteList[stavei].append(note1)
            note1['stave'] = stavei
            #add second note to next stave
            stavei += 1
            staveNoteList[stavei] = [note2]
            note2['stave'] = stavei
            totalDuration = overflow

    #fill in empty staves
    for i in range(numStaves-1, 0, -1):
        stave = staveNoteList[i]
        totalBeats = sum(getDurations(stave))
        while(totalBeats < beatsPerMeasure):
            difference = beatsPerMeasure - totalBeats
            for remainder in [4, 2, 1, .5]:
                while (difference >= remainder):
                    stave.append(generateNote('R', remainder))
                    difference -= remainder
            totalBeats = sum(getDurations(stave))

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
        duration = getDurations(note)
        while (duration > maxSize):
            ret.append(generateNote(note['key'], maxSize))
            duration -= maxSize
        ret.append(generateNote(note['key'], duration))
    return ret

def convertToBeat(note: dict, time_sig, windowsize = WINDOW_SIZE):
    oneBeat = int(time_sig.split('/')[-1])
    rawDuration = getDurations(note)
    duration_beats = rawDuration / windowsize
    duration_beats = round(duration_beats * 2) / 2
    duration_beats = max(duration_beats, 0.5)
    assert(duration_beats > 0)
    return duration_beats

def vexForm(notelist, time_sig, windowsize=8):
    oneBeat = int(time_sig[-1])
    beatlist = []
    for i, note in enumerate(notelist):
        beatDuration = getDurations(note)
        opposite = oneBeat / beatDuration
        if math.log(opposite, 2) % 1 == 0:
            beatlist.append(generateNote(note['key'], int(opposite)))
        else:
            beatlist.append(generateNote(note['key'], int(oneBeat / ( 2/3 * beatDuration))))
            beatlist.append(generateNote(note['key'], int(oneBeat / (1 / 3 * beatDuration))))

    return beatlist
                

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
        assert(getDurations(note) > 0)

    for note in notelist:
        note['duration'] = convertToBeat(note, time_sig)

    durationList = getDurations(notelist)
    keyList = getKeys(notelist)

    assert(0 not in durationList)

    numStaves = math.ceil(sum(durationList) / beatsPerMeasure)
    while (numStaves % 3 != 0): numStaves += 1

    #3. assign a stave index to each note
    
    staveNoteList = assignStaves(notelist, numStaves, beatsPerMeasure, oneBeat)

    #removeTies(staveNoteList)

    # Sort dictionary by keys indexes.
    sortedIndexes = sorted(list(staveNoteList.keys()))
    staveNoteList = {index: staveNoteList[index] for index in sortedIndexes}

    for key in staveNoteList:
        stave = staveNoteList[key]
        durations = getDurations(stave)
        assert(0 not in durations)
        assert(sum(durations) == beatsPerMeasure)
        staveNoteList[key] = vexForm(stave, time_sig)


    
    return staveNoteList, keyList, durationList