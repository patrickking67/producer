// get_context.js — reads live Ableton session info
// Max for Live JS object — called when user hits any generate button
inlets = 1;
outlets = 1;

function bang() {
  try {
    var liveSet = new LiveAPI("live_set");
    var bpm = liveSet.get("tempo")[0];

    // Selected track
    var view = new LiveAPI("live_set view");
    var selectedTrackPath = view.get("selected_track");
    var selectedTrack = new LiveAPI(selectedTrackPath);
    var trackName = selectedTrack.get("name")[0];

    // Devices on track
    var deviceNames = [];
    var devicePaths = selectedTrack.get("devices");
    // devicePaths is alternating id/path pairs
    for (var i = 0; i < devicePaths.length; i += 2) {
      try {
        var dev = new LiveAPI(devicePaths[i + 1]);
        var dName = dev.get("name")[0];
        if (dName) deviceNames.push(dName);
      } catch (de) {}
    }

    // Try to detect key from clip if available
    var key = "A minor"; // default for Mina
    try {
      var clipSlot = new LiveAPI(view.get("highlighted_clip_slot"));
      var hasClip = clipSlot.get("has_clip")[0];
      if (hasClip) {
        var clip = new LiveAPI(clipSlot.get("clip"));
        var clipName = clip.get("name")[0];
        // If clip name contains key info, use it
        if (clipName && clipName.length > 0) {
          key = clipName; // user can name clips with key info
        }
      }
    } catch (ke) {}

    var devicesStr = deviceNames.join(", ") || "none";
    var clipLength = 8; // default bars

    post("Context: BPM=" + bpm + " Key=" + key + " Track=" + trackName + " Devices=" + devicesStr + "\n");
    outlet(0, bpm, key, trackName, "midi", devicesStr, clipLength);

  } catch (e) {
    post("get_context error: " + e.message + "\n");
    outlet(0, 130, "A minor", "Unknown", "midi", "none", 8);
  }
}
