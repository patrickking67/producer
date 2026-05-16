---
name: sound-design
description: Patch recipes for Ableton stock instruments (Wavetable, Operator, Drift, Analog, Meld, Simpler, Sampler) and FX (EQ Eight, Glue, Hybrid Reverb, Echo, Roar, Spectral Resonator). Use when the user asks to "design a [sound]", "how do I make a [sound]", "sculpt a kick", "build a supersaw", "make a vocal chop", or names a target sound. Also pulls Splice samples when audio is faster than synthesis and Library presets when the user already owns the sound.
argument-hint: "<sound you want to design>"
---

# Sound Design

Recipes, not concepts. User is advanced — give parameters.

## Step 0 — Check the Library first
Before designing from scratch, call `library-browser` for the target sound. If the user already has a matching Wavetable / Operator / Drum Rack preset in their User Library or installed Packs, surface it ("you already own *Heavy Sub Bass* in `Bass/Wavetable`"). Then offer to either *use that* or *design fresh* — user picks.

## Output format

**Quick read** — one sentence: what we're making, which device, the one trick that makes it work.

**Build steps** — numbered list:
- **Step N — [action]**: device → parameter → value (and *why* in a half-sentence)

**FX chain** — top-down order, named devices, only the 1–2 parameters per device that you changed.

**Variants** — 2–3 quick mutations ("darker version: X"; "stab-y: Y").

**What to listen for** — 3 bullets: present / absent / failure mode + fix.

## Device cheat-sheets

**Wavetable**
- *Supersaw*: Osc 1 saw, Unison Classic, Voices 7, Detune 18, LP12 cutoff 8k res 10, Amp A 5 / D 200 / S 0 / R 200
- *Pluck*: short Amp env (A 0 D 250 S 0 R 200), Filter env +40 cutoff with D 200
- *Pad*: PWM or saw tables, A 800 R 1500, slow LFO sine 0.2 Hz → cutoff depth 15

**Operator (FM)**
- *FM bass*: Op A sine ratio 1 lvl 0 → Op B sine ratio 2 lvl −12 → Op C sine ratio 3.01 lvl −30. Algorithm 1. LP24 1.2 kHz, tracking 100.
- *Bell*: A → B with B at non-integer ratio (3.5, 7.07), short env, detune slightly
- *Reece*: 2–3 detuned saws → chorus → unison Op patch, slow LFO pitch wobble

**Drift / Analog**
- *Sub bass* (Drift): sine, octave −2, Glide 50, no filter, Saturator +3, Roar tube mode
- *303 acid* (Analog): single saw, self-osc LP24, env amount high, Accent + slide on. Write MIDI with overlapping notes.

**Meld**
- 2 engines, modulate one engine's morph with the other's amp env → evolving texture
- Risers: macro 1 from 0→100 over 16 bars + slow sine LFO at 0.0625 Hz

**Drum design (Drum Rack)**
- *House kick layered*: sub layer = Operator sine C1, pitch env C3→C1 over 50 ms; click layer = sampled 909 top HP'd at 80 Hz; Glue across rack 4:1 / 10 ms / auto / 2 dB GR
- *House clap*: tight clap + reverbed clap pitched +1 ST through 200 ms plate, panned ±15
- *Hat*: white noise → Auto Filter LP12 cutoff 9k res 15, A 0 D 30 R 0 (open hat R 180)

**Vocal chop**
- Simpler Slice mode by transient, MIDI to slices, Warp = Texture (weird) or Complex Pro (clean)
- Macro 1 → Transpose ±12 for chord chops
- Chain: EQ Eight (HP 200, LP 12k) → Chorus-Ensemble Classic 0.5 / 35% → Hybrid Reverb Ambient 25% wet → sidechain ducker

**Risers (3 layers)**
- Noise sweep: Operator noise → LP automated 200 Hz → 16 kHz
- Pitched sample: reversed snare pitched up 2 oct
- Tonal riser: Wavetable saw pitch automated up an octave
- Crossfade volumes: L1 first 4 bars / L2 next 2 / L3 final bar

**FX chain for "wide and modern"**
Saturator (Soft Sat, +2) → EQ Eight (HP 80, high shelf +1.5 @ 9k) → Hybrid Reverb (Plate 1.2 s, predelay 25, ducking on) → Echo (1/8 dotted, fb 35, HP 400 / LP 6k, ducking)

## Connectors
- `search_live_manual` before quoting parameters for Live 12 additions (Meld, Roar, new Drift, MPE)
- `search_push_manual` if user is sound-designing on Push
- **Splice** `describe_a_sound` + `prompt_to_stack` when audio is faster than synthesis ("give me a one-shot dark kick, 60 Hz fundamental") → `download_asset` to grab it
- `library-browser` for matching presets the user already owns
- `search_transcripts` for the Ableton tutorial that demos the technique
- Ableton MCP — `session-bridge` to load the device + apply parameters directly into Live

## After
"Want a variant, a complementary partner sound, or to load this straight into Live as a track?"
