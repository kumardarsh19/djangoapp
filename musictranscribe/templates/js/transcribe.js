// Note class for Vex.Flow
export default class Note {
    constructor(name, length) {
        this.name = name;
        this.length = length;
    }
}

// getNoteList integrates the output of rhythm and pitch processor
// into a list of notes that can be used by Vex.Flow.
export function getNoteList(pitches , onsets) {
    notes = [];
    length = pitches.length;
    duration = 1;
    for (let i = 1; i < length; i++) {
        if (pitches[i] == pitches[i-1]) {
            // print("increment duration")
            duration += 1;
        } else if (pitches[i] != pitches[i-1] && onsets[i-1] == 1) {
            // Incorporate a regular note
            // print("regular")
            note = new Note(pitches[i-1], duration/8);
            notes.push(note);
            duration = 1;
        } else {
            // Incorporate a rest note
            // print("rest")
            note = new Note('##', duration/8);
            notes.push(note);
        }
    }
    // Add the last note.
    if (onsets[length-1] == 1) {
        note = new Note(pitches[length-1], duration/8);
        notes.push(note);
    } else {
        note = new Note('##', duration/8);
        notes.push(note);
    }
    return notes;
}