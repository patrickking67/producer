---
name: library-browser
description: Walk the user's local Ableton Library — User Library, installed Packs, Sounds, Drums, Instruments, Audio Effects, MIDI Effects, Max for Live devices, Samples. Use when the user says "find a preset for", "do I have a [sound] in my library", "search my Packs", "what kits do I own", "/library", "browse library", or any request that should be satisfied by something already on disk before reaching for Splice. Mirrors how the Live browser categorizes content.
argument-hint: "<sound, preset, drum kit, pack, or category>"
---

# Library Browser

Acts like Ableton's left-hand browser, but searchable and AI-curated. Default to the user's own content — Splice is fallback.

## Library locations (macOS)

| Category | Path |
|---|---|
| User Library | `~/Music/Ableton/User Library/` |
| User Library — Presets | `~/Music/Ableton/User Library/Presets/` |
| User Library — Samples | `~/Music/Ableton/User Library/Samples/` |
| Factory + Pack content | `/Users/Shared/Ableton/` (default install) or `/Applications/Ableton Live 12 Suite.app/Contents/App-Resources/Core Library/` |
| Max for Live devices | `~/Music/Ableton/User Library/Presets/Audio Effects/Max Audio Effect/` etc. |

On Windows: substitute `%USERPROFILE%\Documents\Ableton\User Library\` and `C:\ProgramData\Ableton\` respectively. Always confirm path with `ls` before searching.

## How to search

1. `find` for filename matches across both User Library and Core Library
2. `rg --files | rg -i <term>` if recursive search is faster
3. `.adv` (presets), `.adg` (racks), `.alc` (clips), `.als` (sets), `.amxd` (Max devices), `.wav`/`.aif` (samples) — filter by extension when the category is clear
4. For preset *metadata* (tags, description), `unzip -p file.adv | xmllint --xpath` against the embedded XML

```bash
# All bass presets in the user library
find ~/Music/Ableton/User\ Library/Presets -iname "*bass*" \( -name "*.adv" -o -name "*.adg" \)

# All drum kits across factory + user
find ~/Music/Ableton "/Users/Shared/Ableton" -iname "*kit*" -name "*.adg" 2>/dev/null

# Samples tagged "snare top" across everything
find ~/Music ~/Documents -iname "*snare*top*" \( -iname "*.wav" -o -iname "*.aif" \)
```

## Output format

**Match read** — "Found 6 candidates. The 3 strongest:"

| # | Name | Type | Pack / Library | Path |
|---|---|---|---|---|
| 1 | *Heavy Sub Bass* | Wavetable preset | User Library | `~/Music/Ableton/User Library/Presets/Instruments/Wavetable/Bass/Heavy Sub Bass.adv` |

For each top match, one line on **why it fits** ("60 Hz fundamental, light saturation, perfect for the drop").

**If nothing matches locally**, fall back to Splice (`describe_a_sound`) and surface 3 candidates from there instead — flag them as Splice.

## Categorization (mirror Live's browser)

When listing, group like the Live browser does:

- **Sounds** — instrument racks (.adg) tagged for genre/mood
- **Drums** — drum racks + drum kits + drum hits
- **Instruments** — Wavetable / Operator / Drift / Analog / Meld / Simpler / Sampler / external
- **Audio Effects** — racks + chains
- **MIDI Effects** — racks
- **Max for Live** — Audio Effect / Instrument / MIDI Effect
- **Clips** — .alc files
- **Samples** — .wav / .aif / .flac
- **Grooves** — .agr files
- **Templates** — .als templates

## Tagging shortcut

If the user has tagged their User Library via Live 12 collections (Yellow/Red/Blue/etc.), surface those tags by reading `~/Music/Ableton/User Library/Ableton Folder Info/Tags.cfg`. Group results by tag color.

## Hand-offs
- Found a preset → ask whether to load it in Live via `session-bridge`
- Found a sample → ask whether to drop it onto a Simpler / new audio track
- Nothing local → Splice (`describe_a_sound` → `download_asset`)

## Connectors
- File system (Bash `find` / `rg`)
- Splice as fallback
- Ableton MCP (`session-bridge`) to actually load a found preset into the current set

## After
"Want me to load *Heavy Sub Bass* into a new MIDI track in Live, or keep browsing?"
