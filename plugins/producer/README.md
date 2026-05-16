# Producer — Ableton companion plugin

A Claude Code plugin for advanced Ableton Live producers. Tuned for house and EDM, works for any genre.

Made by **Patrick King & Aden Mina**.

> Review tracks, brainstorm, write MIDI, design sounds, dial in mixes, browse your library, arrange bar-by-bar, prep stems and releases, and drive Live directly — all from the chat box.

## Install

### From the marketplace (recommended)

In Claude Code:
```
/plugin marketplace add patrickking67/ableton
/plugin install producer@ableton
```

That's it. The 6 cloud MCPs (Splice, Spotify, Apple Music, Google Drive, Gmail, Calendar) will OAuth on first use. Install the Ableton MCP separately — see [CONNECTORS.md](CONNECTORS.md#1-ableton-mcp).

### From this repo

```
/plugin marketplace add https://github.com/patrickking67/ableton.git
/plugin install producer@ableton
```

## Slash commands

| Command | Skill | What it does |
|---|---|---|
| `/review` | `producer-review` | Peer-level teardown of a track / loop / arrangement |
| `/brainstorm` | `brainstorm` | 3–5 distinct creative directions, each with a reference |
| `/midi` | `midi-lab` | Chord progressions, basslines, drum patterns, melodies → `.mid` file |
| `/sound` | `sound-design` | Patch recipes for stock Ableton devices + Splice fallback |
| `/mix` | `mix-coach` | Mix and master moves — LUFS, sidechain, low-end glue, references |
| `/docs` | `ableton-docs` | Surgical lookups in Live / Push / Move / Note manuals + KB + videos |
| `/library` | `library-browser` | Browse your User Library + installed Packs like Live's left-hand browser |
| `/arrange` | `arrangement` | Bar-by-bar arrangement coach — energy curve, section moves |
| `/reference` | `reference-curator` | Build a reference playlist across Spotify + Apple Music |
| `/stems` | `stem-prep` | Prep stems for mastering, remix, sync, DJ tools, live |
| `/release` | `release-prep` | Master target, metadata, artwork, ISRC, release-day schedule |
| `/session` | `session-bridge` | Drive Ableton Live directly — create tracks, load presets, fire clips |

Skills also auto-trigger from natural language — "review my track", "write a bassline", "what should this sound like" — no slash needed.

## Agent

| Agent | When |
|---|---|
| `ableton-engineer` | End-to-end multi-step tasks: "build me a tech house starter set", "prep this for release across streaming and Beatport", "compare my track to 5 references and write the mix moves". Reads session state, calls the right skills in order, files artifacts, returns a one-paragraph status. |

## Connectors (7 MCP servers)

| Connector | Used for |
|---|---|
| **Ableton** (local) | Drive Live directly — tempo, tracks, devices, clips, locators |
| **Splice** (cloud) | Sample discovery, stack building, downloads |
| **Spotify** (cloud) | References, audio features (BPM/key), playlists |
| **Apple Music** (local stdio) | References, playlists for Apple Music users |
| **Google Drive** (cloud) | Upload stems, masters, reference notes, release packages |
| **Gmail** (cloud) | Draft promo / label / mastering hand-off emails |
| **Google Calendar** (cloud) | Schedule release-day timeline |

Full reference: [CONNECTORS.md](CONNECTORS.md).

## Quick taste

```
> /brainstorm I'm stuck on the second drop of my tech house track in F minor at 126
> /midi 4-bar tech house bassline in F minor, 126 bpm, dark, swung
> /sound make me a Drum Rack kick — punchy 60 Hz, like Innervisions
> /library find me a Wavetable pad preset for a moody breakdown
> /arrange draft the full 6-minute arrangement for the loop I just imported
> /reference build me 10 references for a Beatport-bound tech house EP
> /mix my drop dies in the car
> /stems prep stems for my mastering engineer
> /release prep this for a Beatport release on July 25
> /session set BPM to 126, create 4 MIDI tracks, load my favourite drum rack on track 1
```

Or just describe what you want — "make me a 4-bar bassline in F minor, drop it into the active clip" — and it'll route to the right skill.

## Defaults

- BPM by genre: 120–128 house, 124–128 tech house, 128–132 techno, 174 DnB, 140 trance, 100 hip-hop
- Master targets: −9 to −7 LUFS club, −14 to −12 LUFS streaming, true peak −1.0 dBTP
- Keys when starting fresh: A minor / F minor / G minor
- Drop length: 32 bars; intros/outros: 16–32; full track 5–7 minutes

Override anything explicitly and the plugin follows you.

## License

MIT. See [`../../LICENSE`](../../LICENSE).
