


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