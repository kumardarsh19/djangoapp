function writeNotes(notelist) {
    let notes = [];

    for (let i=0; i<notelist.length; i++) {
        curr = new StaveNote({keys: [notelist[i]], duration: "q"});
        notes[i] = curr;
    }

    // Helper function to justify and draw a 4/4 voice.
    Formatter.FormatAndDraw(context, stave, notes);

    const doc = new jsPDF();
    const svgElement = div.childNodes[0];
    doc.svg(svgElement).then(() => doc.save("score.pdf"));

    console.log("Saved score.pdf");
}