---
name: stem-prep
description: Prep stems for collaboration, mastering engineer, remixer, DJ tools (Stem Separator / Serato Stems / Virtual DJ), or sync. Decides grouping, naming, bit depth, headroom, normalization, and consolidation. Use when the user says "export stems", "prep for mastering", "send stems to my engineer", "stems for a remix", "/stems", or names a recipient.
argument-hint: "<recipient / purpose>"
---

# Stem Prep

Stems are a contract. The recipient should be able to drop them on the timeline at 1.1.1 and hear the same record. Get this wrong and they bounce back.

## First — who's the recipient?

| Recipient | Stem grouping | Headroom | Format | Notes |
|---|---|---|---|---|
| **Mastering engineer** | Drums / Bass / Keys / Vox / FX (5–8 stems) | −6 dBFS true peak, no master bus FX | 24-bit / project SR (44.1 or 48) WAV | No limiter / no master comp / no master EQ |
| **Remixer** | Drums / Bass / Keys / Lead / Vox / Pad / FX (full breakdown) | −6 dBFS | 24-bit WAV | Include MIDI of melodic parts + acapella + project tempo + key |
| **DJ stems** (Serato / Virtual DJ) | Vocals / Drums / Bass / Other (exactly 4) | Whatever the final master is | 16- or 24-bit WAV / FLAC | These are *post-master* stems |
| **Sync / film** | Music (mix-) / Vocals / Drums + sub-stems | Same as remixer | 24-bit 48 kHz WAV (matches video) | Include instrumental, TV mix (vox under), and a-cappella |
| **Live performance / Ableton playback** | Per element + click track + ID track | −6 dBFS | 24-bit, **project SR** | All same length, all start at 1.1.1, include 4-bar count-in click |

If the recipient is unspecified, default to mastering grouping and ask.

## Standard checklist before bouncing

1. **Print everything in-the-box** — bounce VIs to audio, freeze automation, kill the master limiter/comp/EQ
2. **Headroom** — pull the master fader so the loudest hit is < −6 dBFS true peak. Don't touch individual track faders.
3. **Same start, same end** — every stem starts at 1.1.1 and ends at the same bar. Bake silence at the start if needed.
4. **Same length** — pad short stems with silence so they all match (drag-and-drop deployment for the recipient)
5. **Mono where appropriate** — Kick, Sub, often Bass = mono stems. Everything else stereo even if the source is mono.
6. **Naming convention** — `<artist>_<title>_<bpm>_<key>_<stem>.wav`, e.g. `mina_overnight_124_Am_drums.wav`. Number-prefix stems for sort order: `01_drums`, `02_bass`, `03_keys`...
7. **Tempo + key + bar count** — include in a `README.txt` alongside the stems
8. **Reference bounce** — also export the final mix (`00_reference.wav`) so the recipient knows the target

## File package structure

```
mina_overnight_124_Am_stems/
├── 00_reference_mix.wav
├── 01_drums.wav
├── 02_bass.wav
├── 03_keys.wav
├── 04_vox_lead.wav
├── 05_vox_harm.wav
├── 06_fx.wav
├── README.txt          ← tempo, key, bar count, total duration, plugin chain notes
└── midi/
    ├── 03_keys.mid
    └── 04_vox_lead_pitch.mid (if vox is tuned)
```

Zip the folder as `mina_overnight_124_Am_stems.zip`.

## In Ableton

If the Ableton MCP is connected, the export can be driven directly:
1. `session-bridge` → group all tracks by stem category
2. Solo each group + bounce to disk via Live's `Export Audio/Video` (Ableton MCP can trigger this)
3. Disable master FX chain *just for the bounce*, then re-enable

Otherwise, give the user a numbered checklist + screenshot guidance.

## Naming sanity check
After bounce, list the output folder. If any file:
- doesn't start with a number prefix
- has a space (replace with `_`)
- has uppercase that breaks Linux/cloud sync (lowercase the lot)
- has a different sample rate than the reference

…fix it before uploading.

## Delivery

After the package is ready:
- **Google Drive**: upload to `Producer/Stems/<artist>_<title>/`
- **Gmail**: optionally draft an email to the engineer / collaborator with the Drive link, the BPM/key, and the master target (streaming or club)
- **Google Calendar**: add a follow-up event for the expected return date

## Connectors
- Ableton MCP — drive the export
- Google Drive — upload
- Gmail — draft delivery email
- Google Calendar — schedule follow-up
- `search_live_manual` for Live's export dialog options if the user wants the menu walkthrough

## After
"Stems are at `<path>`, zipped at `<zip path>`. Want me to (a) upload to Drive, (b) draft the email to <recipient>, or (c) move on to mastering chain (`release-prep`)?"
