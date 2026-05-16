---
name: arrangement
description: Bar-by-bar arrangement coaching — intro/build/drop/breakdown/outro structure, energy curves, phrasing, transitions, where to place tension and release. Use when the user says "how should this be arranged", "my arrangement is flat", "what comes after the drop", "draft the arrangement", "/arrange", or wants a structural plan. House/EDM defaults; works for any genre.
argument-hint: "<section, vibe, or whole arrangement>"
---

# Arrangement

User has a loop or section and needs structure. Or has a full song that doesn't move. Either way: a bar-by-bar plan with an energy reason for every section change.

## Inputs
- 4–16 bar loop (audio or MIDI) — design the *full track* around it
- Existing arrangement bounce — diagnose where energy stalls / peaks early / drags
- Description only — produce a starter map

If a bounce is supplied, run `ebur128` short-term LUFS over time to see the actual energy curve. Then read the curve back to the user before redesigning.

## House/EDM phrasing defaults

| Section | Bars | Purpose |
|---|---|---|
| Intro | 16–32 | DJ-friendly, kick + maybe perc, no melody |
| First break / pre-drop A | 8–16 | Introduce hook |
| Drop 1 | 32 | Full energy |
| Breakdown 1 | 16–32 | Strip to vocal / pad, build tension |
| Drop 2 | 32 | Bigger — add a layer, change one thing |
| Breakdown 2 / bridge | 8–16 | Last surprise |
| Outro | 16–32 | DJ-friendly tail |

Total: ~5–7 minutes. Adjust for trance (longer), tech house (shorter), hard dance (faster phrasing).

## Output format

**Energy map** — ASCII curve, one row per 8 bars:

```
Bars 0-7    ▁▁▁▁▁▁▁▁  Intro: kick + perc
Bars 8-15   ▁▁▂▂▃▃▄▄  Build: add hat, filter pad open
Bars 16-31  █████████ DROP 1: full
Bars 32-47  ▂▂▁▁▁▂▃▄  Break: strip to vox + pad
Bars 48-79  █████████ DROP 2: + 5th layer
...
```

**Bar-by-bar plan** — markdown table:

| Bars | Section | Elements in | Elements out | The one move |
|------|---------|-------------|--------------|--------------|
| 0–15 | Intro | Kick, top loop | — | Filter slowly opens |
| 16–23 | Pre-build | Sub, perc roll | Top loop | Snare roll last 4 bars |
| 24–31 | Build | All synths | Kick (last bar) | Riser crests, silence on beat 4.4 |
| 32–63 | Drop 1 | Everything | — | Bass layer drops in at bar 40 |
| 64–79 | Breakdown | Vocal, pad | Drums | Pad swells, kick returns at 76 |
| ... | ... | ... | ... | ... |

Save this table to `~/Music/Producer/arrangements/<track-name>_arrangement.md`.

## Heuristics
- **One change per 4 bars minimum** — if nothing changes, the listener checks out
- **Drop 2 ≠ Drop 1** — add a counter-melody, change the bass octave, swap the lead with a vocal chop, or half-time it
- **Build with silence, not noise** — kill one element 2 bars before the drop for half a beat
- **Transitions are subtractions** — reduce before adding
- **DJ math** — start and end on 32-bar phrases; intro/outro mostly drums
- **Test with a DJ filter** — does it still groove when high-passed?

## Section-specific moves

**Drop won't land**
- Snare roll in the last bar of the build, then 1 bar of silence under just kick + sub
- Drop the bass in 8 bars *after* the drop hits (delayed gratification)
- Sidechain everything harder for the first 8 bars of the drop

**Breakdown feels dead**
- Lift one element from the drop (the lead, processed differently) and let it sing
- Add a vocal sample, even a chopped one
- Modulate the pad → filter sweep + chorus + reverb 80% wet

**Outro doesn't end**
- Last 16 bars = drum elements peeling off one at a time, 4 bars apart
- Final 4 bars = kick + reverb tail of the lead

## Connectors
- Ableton MCP — `session-bridge` to mark locators at section boundaries in the actual Live set
- Spotify / Apple Music — `reference-curator` to pull 3 references with similar arrangements and time-stamp the section changes
- `search_videos` for arrangement tutorials specific to the genre

## After
"Want me to (a) actually place locators at every section boundary in Live (`session-bridge`), (b) write the build-up MIDI (`midi-lab`), (c) design the riser for the build (`sound-design`), or (d) pull a reference playlist of similar arrangements (`reference-curator`)?"
