import math


def generateNote(key, duration):
    note = {}
    if '/4' in key: key = key[0]
    note['key'] = key + '/4'
    note['duration'] = str(duration)
    if (key == 'R'): note['typ'] = 'r'
    else: note['typ'] = 'n'
    return note

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
        
        while (duration >= 32):
            newNotes.append(generateNote(key, 32))
            duration -= 32

        while (duration >= 16):
            newNotes.append(generateNote(key, 16))
            duration -= 16

        while (duration >= 8):
            newNotes.append(generateNote(key, 8))
            duration -= 8

        while (duration >= 4):
            newNotes.append(generateNote(key, 4))
            duration -= 4

        
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
def assignStaves(notelist, numStaves):
    stavei = 0
    totalDuration = 0
    for note in notelist:
        assert(stavei < numStaves)
        note['stave'] = stavei
        totalDuration += int(note['duration'])
        if (totalDuration >= 32):
            totalDuration = 0
            stavei += 1

#changes duration to vexform
def convertToVexflow(notelist):
    vexdict = {
        '4': '8', #eigth note 
        '8': '4', #quarter note
        '16': '2', #half note
        '32': '1', #whole note (one full measure)
    }

    for note in notelist:
        prevduration = note['duration']
        note['duration'] = vexdict[prevduration]


#input integrator output
def completeFormatting(notelist):
    #1. round durations to nearest multiples of 4
    formatDuration(notelist)
    for note in notelist:
        assert int(note['duration']) % 4 == 0, "formatDuration fails"
        
    #2. split notes that aren't multiples of 8
    notelist = splitNotes(notelist)
    for note in notelist:
        assert int(note['duration']) % 8 == 0 or int(note['duration']) == 4, "splitNotes fails"
        assert note['duration'] != '0', "found note with duration 0"
        assert (int(note['duration']) <= 32), "notes too long"
    #3. assign a stave index to each note
    numStaves = getNumStaves(notelist)
    assignStaves(notelist, numStaves)
    #4. format duration to Vexflow format
    convertToVexflow(notelist)
    return notelist