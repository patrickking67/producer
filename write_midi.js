// write_midi.js — writes Claude's MIDI output into the selected Ableton clip
// Max for Live JS object
inlets = 1;
outlets = 1;

function anything() {
  // Reconstruct full JSON string from all arguments
  var args = [];
  for (var i = 0; i < arguments.length; i++) {
    args.push(arguments[i]);
  }
  var s = args.join(" ");
  parseAndWrite(s);
}

function parseAndWrite(s) {
  try {
    var pattern = JSON.parse(s);
    var notes = pattern.notes;
    var bars = pattern.bars || 4;

    if (!notes || notes.length === 0) {
      post("No notes in pattern\n");
      return;
    }

    // Get selected track and clip slot
    var view = new LiveAPI("live_set view");
    var clipSlotPath = view.get("highlighted_clip_slot");

    if (!clipSlotPath || clipSlotPath.length === 0) {
      post("No clip slot selected — click an empty slot first\n");
      outlet(0, "error: select a clip slot first");
      return;
    }

    var clipSlot = new LiveAPI(clipSlotPath);
    var hasClip = clipSlot.get("has_clip")[0];

    // Create clip if slot is empty
    if (!hasClip) {
      var lengthInBeats = bars * 4;
      clipSlot.call("create_clip", lengthInBeats);
      post("Created new clip: " + lengthInBeats + " beats\n");
    }

    // Get the clip
    var clipPath = clipSlot.get("clip");
    var clip = new LiveAPI(clipPath);

    // Remove all existing notes
    var totalBeats = bars * 4;
    clip.call("remove_notes_extended", 0, 0, 128, totalBeats);

    // Prepare notes for add_new_notes
    // add_new_notes takes: notes_count, then for each note: pitch time duration velocity mute
    var noteCount = notes.length;
    var addArgs = ["add_new_notes", noteCount];

    notes.forEach(function(n) {
      var pitch = Math.max(0, Math.min(127, Math.round(n.pitch)));
      var timeBeat = n.step * 0.25; // convert 16th steps to beats
      var duration = Math.max(0.05, n.duration);
      var velocity = Math.max(1, Math.min(127, Math.round(n.velocity)));
      var mute = 0;
      addArgs.push(pitch, timeBeat, duration, velocity, mute);
    });

    clip.call.apply(clip, addArgs);

    post("Wrote " + noteCount + " notes into clip\n");
    outlet(0, "done: " + noteCount + " notes written");

  } catch (e) {
    post("write_midi error: " + e.message + "\n");
    outlet(0, "error: " + e.message);
  }
}
