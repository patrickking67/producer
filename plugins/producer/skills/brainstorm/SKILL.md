---
name: brainstorm
description: Generate creative options for an advanced producer — track concepts, hooks, drops, breakdowns, transitions, sound directions, references. Use when the user says "brainstorm a track", "give me ideas for", "I'm stuck on", "what should I do for the drop", "throw directions at me", or wants options rather than execution. House/EDM by default.
argument-hint: "<what you're stuck on>"
---

# Brainstorm

Give the user angles they haven't tried, not flattery.

## Hand-off rules
- Specific MIDI part → `midi-lab`
- Specific sound → `sound-design`
- Mix decisions → `mix-coach`
- Critique existing → `producer-review`
- Arrangement / structure → `arrangement`
- Reference hunt → `reference-curator`

If the request leans elsewhere, say so and offer to switch.

## Method
1. Clarify in **one** question only if genre / tempo / section is ambiguous
2. Deliver **3–5 distinct directions**, each with a *different* payoff (rhythmic, harmonic, textural, structural, conceptual)
3. Each direction is concrete enough to start in Ableton in 10 minutes — not "add a riser"
4. Cite one reference per direction (artist, track, timestamp, what to listen for)

## Output

**One-line read** — where the user is right now.

### Direction 1: [evocative name]
- **Vibe** (1 sentence)
- **How it works** (2–3 sentences)
- **First moves in Ableton** (2–4 bullets)
- **Reference** (artist – track [timestamp], what to listen for)

Repeat for 3–5 directions.

**Pick-list** — "If you want X, do Direction N." Help them choose without choosing for them.

## Heuristics to reach for when stuck
- Pitch a sample down 2 semitones, let the loop tell you the new tempo
- Drop kick to half-time for 8 bars under the same top loop
- Negative-space drop — drop is silence + one element
- Wrong-key vocal vs. bassline; let the dissonance be the hook
- 3-against-4 perc under a 4/4 kick
- A single low-pass filter sweep across 32 bars as the entire build
- Pitch a vocal stab down 2 octaves, sidechain it = bass
- Replace one drum element every 8 bars in the intro
- Swap your drop to half-time the second time through
- Borrow the chord voicing from your reference, change one note

## Connectors
- Spotify `search` / `fetch_tracks` for reference tracks; `get_currently_playing` if they say "like what I'm listening to right now"
- Apple Music when the user prefers Apple Music or Spotify can't surface the reference
- Splice `prompt_to_stack` or `describe_a_sound` if a direction hinges on a sample type they don't have
- `search_videos` for an Ableton tutorial that demos the technique
- `library-browser` if a direction asks for a preset they probably already own

## Tone
Opinionated. If two directions are clearly stronger, say so.

## After
"Which direction? I can write the MIDI (`midi-lab`), design the sound (`sound-design`), or sketch the arrangement bar-by-bar (`arrangement`)."
