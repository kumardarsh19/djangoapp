function getTimeSignature(timeSignature) {
    switch (timeSignature) {
        case 1:
            timeSignature = "4/4";
        case 0.75:
            timeSignature = "3/4";
        case 0.5:
            timeSignature = "2/4";
        case 0.25:
            timeSignature = "1/4";
        case 0.752: // added a 2 at end since 6/8 = 3/4 in terms of decimal value
            timeSignature = "6/8";
        case 0.375:
            timeSignature = "3/8";
    }
    return timeSignature
}