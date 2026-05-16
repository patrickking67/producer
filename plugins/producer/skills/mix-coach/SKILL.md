---
name: mix-coach
description: Mix and master moves for an advanced producer — gain staging, EQ + comp strategy, bus routing, sidechain, low-end glue, vocal pocket, reference matching, LUFS targets. Use when the user says "mix this", "how should I master this", "fix my low end", "vocals sit weird", "compare to reference", "/mix". House/EDM mix conventions by default.
argument-hint: "<what's wrong, or what you want dialed in>"
---

# Mix Coach

User is advanced. Give moves, not lectures.

## Inputs
Bounce / stems / screenshot / description / reference track. If audio, get loudness first:
```bash
ffmpeg -i "$FILE" -af "ebur128=peak=true" -f null -    # integrated LUFS, true peak
sox "$FILE" -n stat                                     # RMS, peak, DC
sox "$FILE" -n spectrogram -o spec.png                  # visual
```
Report integrated LUFS, true peak, and any clipping or DC offset before opining.

## Mix targets (house/EDM defaults)

| Target | Streaming master | Club / DJ master |
|---|---|---|
| Integrated LUFS | −14 to −12 | −9 to −7 |
| Short-term LUFS (drop) | −10 to −8 | −7 to −5 |
| True peak ceiling | −1.0 dBTP | −0.8 dBTP |
| Dynamic range (PLR) | 8–10 dB | 6–8 dB |

## Diagnostic order (run top-down)

1. **Gain staging** — peaks before master at −6 dBFS, no clipping on any track
2. **Mono compatibility** — sum to mono, listen. Is anything disappearing (wide stereo bass, decorrelated FX)?
3. **Low end** — kick + sub. Mono below 120 Hz (Utility → Width 0 below 120 via EQ Eight HP on the side band, or use Bass Mono). Sidechain depth: bass −5 to −8 dB at the kick hit.
4. **Mud sweep** — narrow bell cut on synths/pads at 200–400 Hz, −2 to −4 dB
5. **Mid-range crowding** — high-pass anything not needed below 200 Hz (pads at 250, plucks at 300)
6. **Harshness check** — 2–5 kHz with multiband or dynamic EQ on the master bus
7. **Air** — high shelf +1 to +2 dB at 12 kHz on the master, only if the mix can take it
8. **Stereo image** — kick + sub mono, mids slightly wide (80–100%), hats/cymbals wide (110–130%), FX/reverb full-width

## Bus structure (house/EDM template)

```
DRUMS (group)
  ├── Kick           (Glue, slow, 2 dB GR)
  ├── Sub            (mono, sidechain from kick)
  ├── Clap/snare     (parallel reverb)
  └── Hats/perc      (high-pass 300)
       → Glue Compressor on group, 2:1, 30 ms attack, auto release, ~1 dB GR

BASS (group, mono)        → sidechain from kick
SYNTHS (group)            → sidechain from kick (light)
VOCALS (group)            → parallel compression bus, de-ess at 6 kHz
FX                        → reverb/delay sends

MASTER BUS:
  EQ Eight (corrective) → Glue Comp (2:1, slow attack 30 ms, release auto, ~1 dB GR)
  → Multiband Dynamics (lite tame at 3–5 kHz) → Limiter (Pro, ceiling −1.0, lookahead 1.5 ms)
```

## Common fixes

| Problem | Move |
|---|---|
| Muddy low end | HP everything not bass/kick at 80–120 Hz, narrow cut at 250 on pads |
| Kick gets buried in drop | Sidechain bass harder (−8), bell boost +1.5 dB at 60 Hz on kick |
| Vocals sound thin | +2 dB shelf at 5 kHz, parallel compression bus 4:1 |
| Drop feels small | Add a low shelf +0.5 dB at 80 Hz on master, automate +0.5 dB master gain into the drop |
| Mix translates fine in headphones, dies in car | Mono-check; widen reverb returns; ensure kick is fully mono |
| Master limiter is pumping | Slow the Glue Comp attack to 30 ms, lower limiter input by 2 dB, raise it 0.5 dB at a time |
| Phasey when mono-summed | Check stereo bass; M/S the sub to mono < 120; flip phase on stereo synth layers and listen |

## Reference workflow

1. Pull reference via Spotify `search` / `fetch_tracks` or Apple Music search (or `get_currently_playing` if they're listening to it)
2. Drop both into Ableton, level-match by integrated LUFS (Utility → Gain to match)
3. A/B with **Ear** (don't trust eyes). Match: low-end weight, vocal pocket, drop "lift", stereo width, brightness
4. Note 3 specific differences. Fix the 1 biggest.

If a curated reference set would help, hand off to `reference-curator` to build a proper playlist.

## Connectors
- `search_live_manual` for any Live device parameter you cite (esp. Pro Limiter, Hybrid Reverb, Multiband Dynamics)
- Spotify + Apple Music for reference matching
- Splice `describe_a_sound` / `download_asset` if a layer is missing (a clap top, a missing high-end perc)
- Ableton MCP — `session-bridge` to actually drop / re-order devices on the master bus

## After
"Want me to (a) sketch a full master chain, (b) draft the mix moves bar-by-bar for the drop, (c) build a reference playlist for this track (`reference-curator`), or (d) prep stems for an external master (`stem-prep`)?"
