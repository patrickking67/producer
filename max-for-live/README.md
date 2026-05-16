# MINA Claude — Max for Live Device Setup Guide

A companion Max for Live device for the [Producer plugin](../plugins/producer/README.md). Sits inside Ableton Live, reads your session context in real time, and uses Claude to generate MIDI patterns (drums, melodies, chords) and suggest what to do next — all without leaving Ableton.

> Producer is the chat-side toolkit. MINA Claude is the in-Live device.
> Use them together: Producer brainstorms, writes, and ships; MINA Claude generates inside the running set.

By **Patrick King & Aden Mina**.

## What you're building
A Max for Live device that sits inside Ableton Live. It reads your session
context in real time and uses Claude AI to generate MIDI patterns (drums,
melodies, chords) and suggest what to do next — all without leaving Ableton.

---

## Step 1 — Create your device folder

1. Open Finder
2. Navigate to: ~/Music/Ableton/User Library/Presets/MIDI Effects/Max MIDI Effect/
3. Create a new folder called: MINA Claude
4. Copy the file "mina_claude.js" into this folder

---

## Step 2 — Open Max for Live

1. In Ableton, go to your browser on the left
2. Click "Max for Live" in the sidebar
3. Double-click any existing MIDI Effect device to open the Max editor
   (or go to File > New > Max MIDI Effect)
4. You'll see the Max patcher window open

---

## Step 3 — Build the patch (copy exactly)

In the Max patcher window, you need to create these objects.
Use Cmd+N or double-click the canvas to add each object.

### Objects to add (type the text inside each box):

TOP ROW — JavaScript engine:
  [node.script mina_claude.js]

API KEY INPUT:
  [textedit]          ← user types API key here
  [prepend set_api_key]
  Connect: textedit → prepend → node.script

SESSION CONTEXT READER:
  [live.thisdevice]
  [js get_context.js]   ← see Step 4 for this file
  [prepend set_context]
  Connect: live.thisdevice → js → prepend → node.script

CLIP LENGTH SELECTOR:
  [umenu]             ← add items: 1 bar, 2 bars, 4 bars, 8 bars, 16 bars
  [prepend clip_length]

SUGGESTION BUTTONS ROW:
  [button] labeled "Get Suggestions"
  [prepend get_suggestions]
  Connect: button → prepend → node.script

  [jit.cellblock 4 1] ← displays the 4 suggestion buttons
  Connect: node.script "suggestions" outlet → jit.cellblock

GENERATE BUTTONS:
  [button] labeled "Drum Pattern"
  [prepend generate_drum_pattern]
  Connect: button → prepend → node.script

  [button] labeled "Melody"
  [prepend generate_melodic_pattern]
  Connect: button → prepend → node.script

  [button] labeled "Chords"
  [prepend generate_chord_pattern]
  Connect: button → prepend → node.script

MIDI OUTPUT:
  [js write_midi.js]   ← see Step 5 for this file
  Connect: node.script "midi_pattern" outlet → js write_midi.js

STATUS DISPLAY:
  [message]           ← shows status text
  Connect: node.script "status" outlet → message

---

## Step 4 — Create get_context.js

Create a new file called get_context.js in the same MINA Claude folder.
Paste this content:

```javascript
// get_context.js — reads Ableton session info for Max for Live
inlets = 1;
outlets = 1;

function bang() {
  var liveSet = new LiveAPI("live_set");
  var bpm = liveSet.get("tempo")[0];
  
  // Get selected track
  var view = new LiveAPI("live_set view");
  var selectedTrack = new LiveAPI(view.get("selected_track"));
  var trackName = selectedTrack.get("name")[0];
  
  // Check if it's a MIDI track
  var trackType = "midi";
  
  // Get devices on track
  var devices = [];
  var numDevices = selectedTrack.get("devices").length / 2;
  for (var i = 0; i < numDevices; i++) {
    var device = new LiveAPI("live_set view selected_track devices " + i);
    var devName = device.get("name")[0];
    devices.push(devName);
  }
  
  // Get clip slot length if clip exists
  var clipLength = 8; // default bars
  
  outlet(0, bpm, "A minor", trackName, trackType, devices.join(", "), clipLength);
}
```

---

## Step 5 — Create write_midi.js

Create write_midi.js in the same folder. Paste this:

```javascript
// write_midi.js — writes Claude's MIDI output into an Ableton clip
inlets = 1;
outlets = 1;

function anything(s) {
  try {
    var pattern = JSON.parse(s);
    var notes = pattern.notes;
    var bars = pattern.bars || 4;
    
    // Get the currently selected clip slot
    var view = new LiveAPI("live_set view");
    var selectedTrack = new LiveAPI(view.get("selected_track"));
    
    // Get highlighted clip slot
    var clipSlot = new LiveAPI(view.get("highlighted_clip_slot"));
    
    // Create clip if empty
    var hasClip = clipSlot.get("has_clip")[0];
    if (!hasClip) {
      clipSlot.call("create_clip", bars * 4); // bars * 4 beats
    }
    
    var clip = new LiveAPI(clipSlot.get("clip"));
    
    // Clear existing notes
    clip.call("remove_notes_extended", 0, 0, 128, bars * 4);
    
    // Build notes array for add_new_notes
    // Format: pitch, time(beats), duration(beats), velocity, mute
    var noteData = [];
    notes.forEach(function(n) {
      var timeBeat = n.step * 0.25; // 16th notes to beats
      noteData.push(n.pitch, timeBeat, n.duration, n.velocity, 0);
    });
    
    // Add notes
    clip.call.apply(clip, ["add_new_notes"].concat(noteData));
    
    outlet(0, "done");
    
  } catch(e) {
    post("write_midi error: " + e.message + "\n");
  }
}
```

---

## Step 6 — Save your device

1. In Max, go to File > Save As
2. Save it as "MINA Claude.amxd" inside your MINA Claude folder
3. Make sure all 3 files are in the same folder:
   - MINA Claude.amxd
   - mina_claude.js
   - get_context.js  
   - write_midi.js

---

## Step 7 — Load it in Ableton

1. Close Max
2. In Ableton's browser, navigate to User Library > Presets > MIDI Effects > Max MIDI Effect > MINA Claude
3. Drag "MINA Claude.amxd" onto any MIDI track
4. The device will appear at the bottom of Ableton
5. Paste your API key into the key field
6. Select a clip slot on the track
7. Hit "Get Suggestions" or "Drum Pattern" and watch it go

---

## How to use it

1. Load a Drum Rack on a MIDI track
2. Create an empty clip slot (click the empty square in Session View)
3. Click the MINA Claude device at the bottom
4. Hit "Get Suggestions" — 4 context-aware options appear
5. Hit "Drum Pattern" — Claude reads your BPM and generates an 8-bar groove
6. The MIDI notes appear instantly in your empty clip
7. Press play

For melodies: put the device on a synth track, hit "Melody"
For chords: same, hit "Chords"

---

## Troubleshooting

- "No API key": paste your sk-ant-... key into the text field and press Enter
- Notes not appearing: make sure a clip slot is selected (highlighted blue) before generating
- Script not loading: make sure mina_claude.js is in the exact same folder as the .amxd file
- Max console errors: open the Max console (Cmd+M in Max) to see what's happening
