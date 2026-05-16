---
name: session-bridge
description: Drive Ableton Live directly via the Ableton MCP. Create tracks, drop devices, load presets, set tempo and key, fire and clear clips, arm/record, place locators, bounce clips to MIDI, capture session state. Use when the user says "set the BPM to", "create a new MIDI track", "load Wavetable on", "fire the clip in", "drop a Drum Rack on", "/session", or any request that should manipulate the running Live set instead of describing what to do.
argument-hint: "<what you want to do in Live>"
---

# Session Bridge

The other skills *talk about* Ableton. This skill *acts on* Ableton.

## Prereq

The Ableton MCP server must be running and Live must have the Remote Script loaded. If `get_session_info` errors out:
1. Check `uvx ableton-mcp` is installed
2. Live → Preferences → Link/Tempo/MIDI — set Control Surface to "Ableton MCP" with Input/Output `(none)`
3. Restart Live

If still failing, fall back to `ableton-docs` to walk the user through setup.

## Capabilities map

| Intent | Ableton MCP tool |
|---|---|
| Read tempo / key / time sig / set state | `get_session_info` |
| Read a specific track (name, devices, clips, color) | `get_track_info` |
| Create a new MIDI / audio track | `create_midi_track` / `create_audio_track` |
| Set tempo | `set_tempo` |
| Load an instrument / effect | `load_instrument` / `load_effect` |
| Load a Browser item by path | `load_browser_item` |
| Search the browser | `get_browser_tree`, `get_browser_items_at_path` |
| Create a clip with notes | `create_clip` / `add_notes_to_clip` |
| Fire a clip | `fire_clip` |
| Stop a clip | `stop_clip` |
| Set clip name | `set_clip_name` |
| Start playback / stop / record | `start_playback` / `stop_playback` |

(Tool names follow the `ahujasid/ableton-mcp` server. If a tool is missing, surface that to the user — don't make one up.)

## Operating principles

1. **Do, don't describe.** If the user says "set BPM to 124", call `set_tempo(124)`. Confirm after, not before.
2. **Confirm destructive actions.** Deleting a track, clearing all clips in a scene, overwriting a clip — ask first.
3. **Read before writing.** Before adding a device, call `get_track_info` so you know what's already on the track.
4. **Group related actions.** "Make me a tech house starter set" = sequence of 8 actions, executed in order, with one status line per action.
5. **Save state to disk when meaningful.** After a substantial change, offer to save: Live's `save_set` if exposed, else prompt the user to ⌘S.

## Common workflows

### "Set up a tech house template"
```
set_tempo(126)
create_midi_track(index=0, name="DRUMS")
load_instrument("Drum Rack" / preset path)
create_midi_track(index=1, name="BASS")
load_instrument("Bass / Operator / FM Bass")
create_midi_track(index=2, name="CHORDS")
load_instrument("Wavetable / Pad / Warm Pad")
create_midi_track(index=3, name="LEAD")
create_audio_track(index=4, name="VOX")
create_audio_track(index=5, name="FX")
create_return_track(name="REVERB"); load_effect("Hybrid Reverb / Plate Medium")
create_return_track(name="DELAY"); load_effect("Echo / 1/8 Dotted")
```

Report back with: "Template ready: 4 MIDI tracks, 2 audio, 2 returns. Tempo 126. What next?"

### "Drop the MIDI I just generated into the clip slot"
After `midi-lab` saves a `.mid`:
```
get_session_info() → confirm tempo matches
get_track_info(selected_track_idx)
create_clip(track_idx, slot_idx, length_bars)
add_notes_to_clip(track_idx, slot_idx, notes=[...])
set_clip_name(track_idx, slot_idx, "<genre>_<part>_<key>")
```

### "Load the preset Library Browser found"
After `library-browser` returns a path:
```
load_browser_item(track_idx, "Presets/Instruments/Wavetable/Bass/Heavy Sub Bass.adv")
```

### "Place arrangement locators"
After `arrangement` returns a bar map:
```
for each section in arrangement:
    set_locator(name=section.name, bar=section.start_bar)
```

## Error handling

- If a tool returns `track index out of range`, list current tracks with `get_session_info` and ask which one
- If `load_instrument` fails because the preset isn't found, fall back to `library-browser` to locate it or load a stock default
- If Live is in a state where the action isn't valid (e.g. recording while another track is armed), surface the conflict to the user and pause

## After
"Done. Live is at <state>. Want me to (a) keep building, (b) save the set, or (c) commit changes to git if this is a tracked project?"
