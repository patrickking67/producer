# Producer

A production toolkit for Ableton Live — chat-side + in-Live.

Made by **Patrick King & Aden Mina**.

This repo is a Claude Code **marketplace** that ships two things:

| Component | What it is | Where it lives |
|---|---|---|
| **Producer** (plugin) | Claude Code plugin: 12 skills + 12 slash commands + 1 agent + 7 MCPs (Ableton, Splice, Spotify, Apple Music, Google Drive, Gmail, Calendar). Reviews, brainstorms, writes MIDI, designs sounds, mixes, browses your library, arranges, preps stems and releases, and drives Live directly. | [`plugins/producer/`](plugins/producer/) |
| **MINA Claude** (Max for Live device) | A Max for Live MIDI Effect that calls Claude from inside Live to generate drum/melody/chord patterns into the highlighted clip. | [`max-for-live/`](max-for-live/) |

## Install (Producer plugin)

In Claude Code:

```text
/plugin marketplace add patrickking67/ableton
/plugin install producer@ableton
```

Or via full URL:

```text
/plugin marketplace add https://github.com/patrickking67/ableton.git
/plugin install producer@ableton
```

The marketplace manifest is at [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json). The 6 cloud MCPs (Splice, Spotify, Apple Music, Google Drive, Gmail, Calendar) OAuth on first use. Install the Ableton MCP separately — see [`plugins/producer/CONNECTORS.md`](plugins/producer/CONNECTORS.md#1-ableton-mcp).

## Install (MINA Claude — the Max for Live device)

Follow the step-by-step in [`max-for-live/README.md`](max-for-live/README.md). You'll drop three JS files plus a `.amxd` patch into `~/Music/Ableton/User Library/Presets/MIDI Effects/Max MIDI Effect/MINA Claude/`.

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
ableton/
├── .claude-plugin/
│   └── marketplace.json          ← marketplace manifest
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
│   ├── mina_claude.js
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
