


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

function isValidDuration(dur) {
    return dur == 1 || dur == 2 || dur == 4 || dur == 8 || dur == 16;
}
export function getStaveNotes(pitches, onsets, Vex) {
    const {Stave, StaveNote} = Vex.Flow;
    var ret = [];
    let startIndex = pitches.findIndex(element => element != "##");
    let currNote = pitches[startIndex];
    let endIndex = pitches.slice(startIndex).findIndex(element => element != currNote);
    
    console.log(startIndex);
    console.log(endIndex);
    console.log(pitches.length);
    while (startIndex < pitches.length && endIndex < pitches.length) {
        let onsetSlice = onsets.slice(startIndex, onsets.findIndex(element => element == 0));
        let duration = Math.round(onsetSlice.length / 8);
        while (!isValidDuration(duration)) duration++;
        let keys = [pitches[startIndex] + '/4'];
        if (keys[0] == '##') keys = [];
        let types = ['r', 'n'];
        if (keys.length == 0) type = 'r';
        let vexNote = new StaveNote({
            keys: keys,
            duration: duration,
            type: types[keys.length - 1],
        })
        ret.push(vexNote);
        startIndex = endIndex;
        endIndex = pitches.slice(startIndex).findIndex(element => element != currNote);
        if (startIndex == -1 || endIndex == -1) break;
    }

    return ret;
}