
import { Vex, Stave, StaveNote, Formatter } from "vexflow";
import { JSDOM } from "jsdom";
import { jsPDF } from "jspdf";
import "svg2pdf.js";

const VF = Vex.Flow;
console.log("VexFlow Build: " + JSON.stringify(VF.BUILD));

const dom = new JSDOM('<!DOCTYPE html><html><body><div id="vf"></div><body></html>');
global.window = dom.window;
global.document = dom.window.document;

// Create an SVG renderer and attach it to the DIV element named "vf".
const div = document.getElementById("notebox");
const renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

const stave = new Stave(10, 0, 190);

// Add a clef and time signature.
stave.addClef("treble").addTimeSignature("4/4");

// Connect it to the rendering context and draw!
stave.setContext(context).draw();

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

    /** 
    console.log("VexFlow Build:", Vex.Flow.BUILD);


    const { Factory } = Vex.Flow;

    const factory = new Factory({
        renderer: { elementId: "output", width: 500, height: 200 },
    });

    const score = factory.EasyScore();

    factory
        .System()
        .addStave({
            voices: [score.voice(score.notes("C#5/q, B4, A4, G#4", { stem: "up" })), score.voice(score.notes("C#4/h, C#4", { stem: "down" }))],
        })
        .addClef("treble")
        .addTimeSignature("4/4");
    factory.draw();
    */

}
