export function getStaves(startx, starty, width, height, cw, ch, Vex) {
    const {Stave} = Vex.Flow;
    var ret = [];
    for (let i=0; i<ch; i++) {
        for (let j=0; j<cw; j++) {
            let curr = new Stave(startx + j*width, starty + i*height, width);
            ret.push(curr);
        }
    }

    return ret;
    
}

export function getBaseLog(x, y) {
    return Math.log(y) / Math.log(x);
}

export function isValidDuration(dur) {
    return dur == 1 || dur == 2 || dur == 4 || dur == 8 || dur == 16;
}

export function formatDuration(duration) { //assume duration of 8 is a quarter note
    if (duration <= 8) return '8';
    else if (duration <= 16) return '4';
    else if (duration > 24 && duration <= 32) return '2';
    else return '1';
}

export function getStaveNotes(pitches, onsets, Vex) {
    const {Stave, StaveNote} = Vex.Flow;
    var ret = [];
    let startIndex = pitches.findIndex(element => element != "R");
    let currNote = pitches[startIndex];
    let endIndex = startIndex + 1;
    while (pitches[endIndex] == currNote && endIndex < pitches.length) endIndex++;
    
    console.log(startIndex);
    console.log(endIndex);
    console.log(pitches.length);
    while (startIndex < pitches.length && endIndex < pitches.length && endIndex > startIndex) {
        let onsetSlice = onsets.slice(startIndex, onsets.findIndex(element => element == 0));
        let duration = Math.round(onsetSlice.length / 8);
        currNote = [pitches[startIndex]];
        while (!isValidDuration(duration)) duration++;
        let keys = currNote + '/4';
        let type = 'n';
        if (currNote == 'R') type = 'r';
        console.log(keys, duration, types[keys.length]);
        let vexNote = new StaveNote({
            keys: keys,
            duration: duration,
            type: type,
        })
        console.log('PUSHING')
        ret.push(vexNote);
        startIndex = endIndex;
        endIndex = startIndex + 1;
        while (pitches[endIndex] == currNote && endIndex < pitches.length) endIndex++;
        if (startIndex == -1 || endIndex == -1) break;
    }
    return ret;
}

export function convertToVex(notes, Vex) {
    var ret = []
    
    notes.forEach(note => {
        console.log(note.duration);
        console.log(formatDuration(note.duration));
        ret.push(new Vex.Flow.StaveNote({
            keys: [note.key],
            duration: formatDuration(note.duration),
            type: note.typ,
        }));
    });

    return ret;
}