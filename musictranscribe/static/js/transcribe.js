// Note class for Vex.Flow
export class Note {
    constructor(name, length) {
        this.name = name;
        this.length = length;
    }
}

// getNoteList integrates the output of rhythm and pitch processor
// into a list of notes that can be used by Vex.Flow.
export function getNoteList(pitches , onsets) {
    let notes = [];
    let length = pitches.length;
    let duration = 1;
    for (let i = 1; i < length; i++) {
        if (pitches[i] == pitches[i-1]) {
            // print("increment duration")
            duration ++;
        } else if (onsets[i-1] == 1) {
            // Incorporate a regular note
            // print("regular")
            let note = new Note(pitches[i-1], duration/8);
            notes.push(note);
            duration = 1;
        } else {
            // Incorporate a rest note
            // print("rest")
            let note = new Note('##', duration/8);
            notes.push(note);
            duration = 1;
        }
    }
    // Add the last note.
    if (onsets[length-1] == 1) {
        let note = new Note(pitches[length-1], duration/8);
        notes.push(note);
    } else {
        let note = new Note('##', duration/8);
        notes.push(note);
    }
    return notes;
}