def generateNote(key, duration):
    note = {}
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
    unitsPerMeasure = int(time_signature[-1])
    measureIndex = 0
    totalDuration = 0
    for i in range(len(notelist)):
        key, duration, type = notelist[i]['key'], int(notelist[i]['duration']), notelist[i]['typ']
        totalDuration += duration
        if (totalDuration < unitsPerMeasure):
            newNotes.append(notelist[i])
        else:
            overflow = totalDuration - unitsPerMeasure
            duration0 = duration - overflow
            for dur in [duration0, overflow]:
                if (dur > 0): newNotes.append(generateNote(key[0], dur))
            totalDuration = overflow
    return newNotes

def formatDuration(duration, time_signature='4/4'):
    margin = 2
    duration = int(duration)
    assert(duration > 0)
    if (duration <= 4 + margin): return '8' #eighth note
    elif (duration <= 8 + 2*margin): return "4" #quarter note
    elif (duration <= 16 + 4*margin): return "2" #half note
    else: return "1" #whole note

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