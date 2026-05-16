---
name: midi-lab
description: Write playable MIDI for an advanced producer — chord progressions, basslines, drum patterns, melodies, arpeggios, stabs. Key/scale aware, theory-grounded. Use when the user asks to "write a chord progression", "make a bassline", "give me a drum pattern", "build a MIDI loop", or names key/tempo/genre. Outputs both a human-readable recipe and a real .mid file.
argument-hint: "<what to compose — key, tempo, vibe, length>"
---

# MIDI Lab

## Defaults
- Tempo: ask, or infer from genre (124–128 house, 128–132 techno, 174 DnB, 140 trance/hard, 100 hip-hop)
- Key: ask. House defaults if starting fresh: A minor / F minor / G minor
- Length: 4 bars loop / 8 bars progression / 16 bars build
- Quantize 1/16; loosen to 1/32 + humanize for swung tech house

## Always deliver two things

**1. A human-readable recipe** — table:

| Bar | Beat | Note(s) | Velocity | Length | Notes |
|-----|------|---------|----------|--------|-------|

Velocity bands: 100–115 accents, 75–95 body, 50–70 ghosts. Flat velocity is the #1 thing that makes MIDI sound programmed.

**2. An actual .mid file** — save to `~/Music/Producer/midi/`, descriptive name (`tech_house_bassline_Am_126.mid`). Use `mido`:

```python
import mido, os
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo

mid = MidiFile(ticks_per_beat=480)
track = MidiTrack(); mid.tracks.append(track)
track.append(MetaMessage('set_tempo', tempo=bpm2tempo(126)))
track.append(MetaMessage('time_signature', numerator=4, denominator=4))

notes = [(0.0, 57, 110, 0.5), ...]  # (start_beat, pitch, vel, length_beats)
events = []
for s, p, v, l in notes:
    events.append((int(s*480), 'on', p, v))
    events.append((int((s+l)*480), 'off', p, v))
events.sort(key=lambda e: (e[0], 0 if e[1]=='on' else 1))
last = 0
for tick, kind, p, v in events:
    delta = tick - last; last = tick
    track.append(Message('note_on' if kind=='on' else 'note_off',
                         note=p, velocity=v if kind=='on' else 0, time=delta))

out_dir = os.path.expanduser('~/Music/Producer/midi'); os.makedirs(out_dir, exist_ok=True)
out_name = 'tech_house_bassline_Am_126.mid'
mid.save(os.path.join(out_dir, out_name))
```

Naming pattern: `<genre>_<part>_<key>_<bpm>.mid`.

## Composition heuristics

**Chord progressions**
- Always-works: i–VI–III–VII, i–VII–VI–VII, ii–V–i (deep house)
- Voice as 7ths / 9ths, not triads. Drop the root and let bass hold it.
- Tight voice-leading (≤ 3 semitones between chord tones)

**Basslines**
- House: rolling 1/8 or 1/16, mostly root, octave jumps for movement, ghost notes 50–65
- Tech house: more syncopation, off-beat accents
- Check bass vs. kick — if they hit in the same 30 ms window, move bass 1/32 later or sidechain harder

**Drums**
- Don't write the obvious pattern unless asked
- Tech house: 16th shaker with sin-wave velocity, off-beat open hat ("tss"), perc on 3.5 of every other bar
- House clap = tight clap + reverbed clap pitched +1 ST

**Melodies / leads**
- 5–7 note set. Pentatonic + one passing tone.
- Repetition + one variation: A–A–A'–B
- Tension notes (b9, #11) on weak beats only

**Humanize**
- ±3 ms hats, ±1 ms kick (keep kick tight)
- ±10 velocity hats, ±20 ghosts

## Live integration
If the Ableton MCP is connected:
1. After saving the `.mid`, offer to import directly via `session-bridge` (creates a new clip in the highlighted slot)
2. Or, generate the notes directly into the active clip without ever writing a file — ask which the user prefers

## Connectors
- `search_live_manual` for Live 12 MIDI tools (Scale, Arpeggiator, Note Echo, Random, generative tools) before quoting parameters
- Spotify `fetch_tracks` or Apple Music search if the user names a reference; pull tempo/key from metadata where possible
- Ableton MCP for direct clip writing
- `library-browser` if the user wants the MIDI to match an instrument preset they already own

## After
Drop the `.mid` link, then ask: "Variant — busier, sparser, different key, or a complementary chord layer? Or drop it into the active clip in Live?"
