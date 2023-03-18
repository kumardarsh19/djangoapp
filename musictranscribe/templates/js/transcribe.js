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
const div = document.getElementById("vf");
const renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

// Configure the rendering context.
renderer.resize(200, 200);
const context = renderer.getContext();
context.setFont("Arial", 10);

const stave = new Stave(10, 0, 190);

// Add a clef and time signature.
stave.addClef("treble").addTimeSignature("4/4");

// Connect it to the rendering context and draw!
stave.setContext(context).draw();

const notes = [
    new StaveNote({ keys: ["c/4"], duration: "q" }),
    new StaveNote({ keys: ["d/4"], duration: "q" }),
    new StaveNote({ keys: ["b/4"], duration: "qr" }),
    new StaveNote({ keys: ["c/4", "e/4", "g/4"], duration: "q" }),
];

// Helper function to justify and draw a 4/4 voice.
Formatter.FormatAndDraw(context, stave, notes);

const doc = new jsPDF();
const svgElement = div.childNodes[0];
doc.svg(svgElement).then(() => doc.save("score.pdf"));

console.log("Saved score.pdf");