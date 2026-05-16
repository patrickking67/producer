---
name: producer-review
description: Peer-level teardown of a track, loop, or arrangement. Use when the user says "review my track", "critique this", "is this drop working", "be honest about this", or shares a bounce / stems / arrangement screenshot. House/EDM defaults. Returns prioritized fixes, not encouragement.
argument-hint: "<bounce, screenshot, .als, or description>"
---

# Producer Review

User is an advanced producer. Skip basics. No flattery.

## Inputs
Bounce, stems, screenshot of arrangement or device chain, `.als` (`gunzip -c set.als > set.xml`), reference track, or written description. If audio file, get loudness stats first:
```bash
ffprobe -hide_banner "$FILE"
ffmpeg -i "$FILE" -af "ebur128=peak=true" -f null -
sox "$FILE" -n stat
sox "$FILE" -n spectrogram -o spec.png
```

If the Ableton MCP is connected and the user is asking about their current session, pull live state through `session-bridge` instead of asking for a bounce.

## Review across these dimensions — lead with the two weakest
1. **Arrangement & energy curve** — section lengths, where energy stalls or peaks too early
2. **Groove** — kick/clap pocket, ghost notes, swing %, hat doing more than 16th-filler
3. **Low end** — kick + sub relationship, mono below 120 Hz, sidechain shape, sub key
4. **Sound palette** — dated / generic / over-processed sounds, is there one signature element
5. **Mix translation** — small-speaker test, 200–400 Hz mud, 2–5 kHz harshness
6. **Tension & release** — risers, drops, silence, are listeners earned in
7. **Hook / lead** — memorable in first 4 bars, doing one thing well or three things badly
8. **Genre fit vs. signature** — DJ-set ready *and* identifiable as you

## Output

**Headline** — two sentences. Biggest weakness + biggest strength to protect.

**Prioritized fixes** — 5–8 numbered items, highest impact first. Each:
- Verb-first action ("Cut", "Replace", "Sidechain")
- Where (bar, section, track, freq range)
- Why (in producer language)
- How in Ableton (specific device + parameters — e.g. "Glue Comp on drum bus, 4:1, 10 ms attack, auto release, 2 dB GR")

**References** — 2–3 tracks that solve the problem. Artist, track, timestamp, what to listen for. Pull from Spotify (`search` / `fetch_tracks`) or Apple Music if useful.

**What's working** — 3 bullets of things to *not* change.

## Connectors
- `search_live_manual` to verify any device parameter you cite
- Spotify `search` + `fetch_tracks` and Apple Music search for reference matches
- Ableton `search_videos` if a tutorial would land the fix better than text
- Splice `describe_a_sound` if a missing element needs a real sample
- Ableton MCP (`get_session_info`, `get_track_info`) for live session diagnostics
- Google Drive — if the bounce was shared via a Drive link, fetch it directly

## House/EDM defaults (if genre unspecified)
- BPM by genre: 120–128 house, 124–128 tech house, 128–132 techno, 174 DnB
- Mono kick + sub, sidechain bass and pads
- Drops at 32 or 64 bars
- Master targets: −8 to −6 LUFS short-term in the drop; integrated −9 to −7 club / −14 streaming

## After
Ask: "Want me to (a) write MIDI for the weakest section (`midi-lab`), (b) sketch a sound-design recipe for the element that's not landing (`sound-design`), (c) draft mix moves bar-by-bar (`mix-coach`), or (d) re-arrange the section that's losing energy (`arrangement`)?"
