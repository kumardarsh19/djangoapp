


function getStaves(num, startStave) {
    const {Stave} = Vex.Flow;
    ret = [startStave];
    startx = startStave.x;
    starty = startStave.y;
    width = startStave.width;
    height = startStave.height;
    cW = startStave.getContext().height;
    cH = startStave.getContext().height;
    for (let i=1; i<num; i++) {
        prev = ret[i-1];
        curr = new Stave((startx + i * width) % cW, (starty + i * height) % cH, width);
        ret.push(curr);
    }

    return ret;
    
}