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
            print("increment duration")
            duration += 1
        elif pitches[i] != pitches[i-1] and onsets[i-1] == 1:
            # Incorporate a regular note
            print("regular")
            note = Note(name = pitches[i-1],
                        length = duration/8,
                        clef = clef)
            notes.append(note)
            duration = 1
        else:
            # Incorporate a rest note
            print("rest")
            note = Note(name = "##",
                        length = duration/8,
                        clef = clef)
            notes.append(note)
    
    # Add the last note.
    if onsets[length-1] == 1:
        note = Note(name = pitches[length-1],
                    length = duration/8,
                    clef = clef)
        notes.append(note)
    else:
        note = Note(name = "##",
                    length = duration//8,
                    clef = clef)
        notes.append(note)
    
    for note in notes:
        print(f"Note name: {note.name}, length: {note.length}")
    return notes