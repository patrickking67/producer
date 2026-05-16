<p align="center">
  <img src="assets/producer-logo.svg" alt="Producer" width="320">
</p>

<p align="center">
  <strong>An Ableton Live production toolkit — chat-side and in-Live.</strong><br>
  Review tracks, brainstorm, write MIDI, design sounds, dial in mixes, browse your library, arrange, prep stems and releases — and drive Ableton Live directly.
</p>

<p align="center">
  <a href="https://github.com/patrickking67/producer/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-black?style=flat-square" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-plugin-black?style=flat-square" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/Ableton%20Live-12-black?style=flat-square" alt="Ableton Live 12">
  <img src="https://img.shields.io/badge/Max%20for%20Live-device-black?style=flat-square" alt="Max for Live">
</p>

<p align="center">
  <a href="https://patrickking67.github.io/producer/"><strong>Website</strong></a> ·
  <a href="plugins/producer/">Plugin</a> ·
  <a href="max-for-live/">Max for Live device</a> ·
  <a href="plugins/producer/CONNECTORS.md">Connectors</a>
</p>

---

Created by **Patrick King** for **Aden Mina** (producer) to use.

This repo is a Claude Code **marketplace** that ships two surfaces of the same product:

| Component | What it is | Where it lives |
|---|---|---|
| **Producer** (Claude Code plugin) | 12 skills + 12 slash commands + 1 agent + 7 MCPs (Ableton, Splice, Spotify, Apple Music, Google Drive, Gmail, Calendar). Reviews, brainstorms, writes MIDI, designs sounds, mixes, browses your library, arranges, preps stems and releases, and drives Live directly. | [`plugins/producer/`](plugins/producer/) |
| **Producer for Live** (Max for Live device) | A Max for Live MIDI Effect that calls the Claude API from inside Live to generate drum/melody/chord patterns into the highlighted clip. | [`max-for-live/`](max-for-live/) |

## Install (Producer plugin)

In Claude Code:

```text
/plugin marketplace add patrickking67/producer
/plugin install producer@producer
```

Or via full URL:

```text
/plugin marketplace add https://github.com/patrickking67/producer.git
/plugin install producer@producer
```

The marketplace manifest is at [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json). The 6 cloud MCPs (Splice, Spotify, Apple Music, Google Drive, Gmail, Calendar) OAuth on first use. Install the Ableton MCP separately — see [`plugins/producer/CONNECTORS.md`](plugins/producer/CONNECTORS.md#1-ableton-mcp).

Works in **Claude Code on the web** (cowork) and in the local CLI. Cloud MCPs OAuth on first use either way; the Ableton MCP only runs locally (it talks to Live over the Remote Script).

## Install (Producer for Live — the Max for Live device)

Follow the step-by-step in [`max-for-live/README.md`](max-for-live/README.md). You'll drop three JS files plus a `.amxd` patch into `~/Music/Ableton/User Library/Presets/MIDI Effects/Max MIDI Effect/Producer/`.

## What's in the Producer plugin

### 12 slash commands

| Command | Skill |
|---|---|
| `/review` | producer-review — peer-level teardown |
| `/brainstorm` | brainstorm — 3–5 directions with references |
| `/midi` | midi-lab — playable `.mid` from a prompt |
| `/sound` | sound-design — stock-device patch recipes + Splice |
| `/mix` | mix-coach — LUFS, sidechain, low-end glue |
| `/docs` | ableton-docs — Live / Push / Move / Note manuals + KB + videos |
| `/library` | library-browser — your Ableton Library + Packs, like Live's browser |
| `/arrange` | arrangement — bar-by-bar plan with an energy curve |
| `/reference` | reference-curator — Spotify + Apple Music playlists with BPM/key/LUFS |
| `/stems` | stem-prep — for mastering, remix, sync, DJ tools, live |
| `/release` | release-prep — master target, metadata, artwork, ISRC, schedule |
| `/session` | session-bridge — drive Live directly via the Ableton MCP |

### 1 agent

| Agent | Purpose |
|---|---|
| **ableton-engineer** | End-to-end multi-step tasks: "build me a tech house starter set", "prep this for release across streaming and Beatport", "compare my track to 5 references and write the mix moves". |

### 7 MCP connectors

Auto-declared in [`.mcp.json`](plugins/producer/.mcp.json): **Ableton**, **Splice**, **Spotify**, **Apple Music**, **Google Drive**, **Gmail**, **Google Calendar**. Full breakdown in [CONNECTORS.md](plugins/producer/CONNECTORS.md).

## Repo layout

```
producer/
├── .claude-plugin/
│   └── marketplace.json          ← marketplace manifest
├── assets/
│   ├── producer-logo.svg         ← wordmark + mark (monochrome)
│   └── producer-mark.svg         ← icon only (square)
├── docs/
│   └── index.html                ← GitHub Pages landing site (Tailwind)
├── plugins/
│   └── producer/                 ← the plugin
│       ├── .claude-plugin/plugin.json
│       ├── .mcp.json
│       ├── README.md
│       ├── CONNECTORS.md
│       ├── commands/             ← 12 slash commands
│       ├── skills/               ← 12 skills
│       └── agents/               ← ableton-engineer
├── max-for-live/                 ← the .amxd device files
│   ├── README.md
│   ├── producer.js
│   ├── get_context.js
│   └── write_midi.js
├── dist/
│   └── producer.plugin           ← zipped plugin bundle for manual install
├── LICENSE
└── README.md
```

## Manual install (bundle)

If you'd rather sideload the zipped bundle instead of using the marketplace, grab [`dist/producer.plugin`](dist/producer.plugin) and drag it into Claude Code.

## License

MIT — see [LICENSE](LICENSE).
