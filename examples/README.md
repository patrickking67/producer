# Producer workflow examples

These examples show how Producer turns an open-ended music production problem into concrete, reviewable output. They are designed to be run one step at a time so the artist stays in control.

## Build a tech house starter set

**Brief:** Create a playable 126 BPM starter set in F minor with drums, bass, a breakdown idea, and a clear six-minute structure.

```text
/brainstorm Give me four directions for a dark 126 BPM tech house track in F minor.
/midi Write a four-bar swung bassline for direction two.
/sound Build a stock-device bass patch that leaves room for a 60 Hz kick.
/arrange Turn the loop into a six-minute club arrangement with an energy curve.
/session Set the tempo, create the MIDI tracks, and place the first clips.
```

**Output:** Creative directions, a MIDI file, a repeatable device recipe, a bar-by-bar arrangement, and an initialized Live session. The `/session` step requires the local Ableton MCP.

## Diagnose a weak drop

**Brief:** The drop works in headphones but loses impact in a car.

```text
/review Tear down the drop with focus on low-end contrast and transition energy.
/reference Find five comparable releases and summarize their low-end balance.
/mix Give me an ordered set of moves using stock Ableton devices.
/session Inspect the kick and bass tracks, then apply only the approved gain changes.
```

**Output:** A prioritized diagnosis, reference set, measurable mix moves, and optional session changes that remain explicit and reversible.

## Prepare a track for mastering

**Brief:** Deliver organized stems and context for an external mastering engineer.

```text
/review Flag arrangement, clipping, phase, and headroom issues before export.
/mix Set final pre-master targets and an A/B checklist.
/stems Define stem groups, naming, tails, sample rate, bit depth, and export order.
```

**Output:** A preflight report, target levels, export matrix, and handoff checklist.

## Plan a release without losing the music

**Brief:** Prepare a finished single for a digital release and a small promotion cycle.

```text
/release Build the release checklist, metadata sheet, artwork brief, and schedule.
/reference Create a short playlist that communicates the track's market position.
/library identify alternate mixes and source files that belong in the archive.
```

**Output:** Release metadata, artwork direction, distribution checklist, schedule, reference playlist, and an archive inventory. Connected services require their documented OAuth setup.
