from musictranscribe.models import Note

def getNoteList(pitches, onsets, clef):
    # Iterate through the lists at the same time.
        # If pitch is same, keep track of duration.
        # If pitch is different, add the note to the list.
    notes = []
    length = len(pitches)
    duration = 1
    for i in range(1, length):
        if pitches[i] == pitches[i-1]:
            duration += 1
        elif pitches[i] != pitches[i-1] and onsets[i-1] == 1:
            # Incorporate a regular note
            note = Note(name = pitches[i-1],
                        length = duration//8,
                        clef = clef)
            notes.append(note)
            duration = 1
        else:
            # Incorporate a rest note
            note = Note(name = "##",
                        length = duration//8,
                        clef = clef)
            notes.append(note)
    return notes