<p align="center">
  <img src="assets/producer-logo.svg" alt="Producer" width="320">
</p>

<p align="center">
  <strong>An Ableton Live production toolkit: chat-side and in-Live.</strong><br>
  Review tracks, brainstorm, write MIDI, design sounds, dial in mixes, browse your library, arrange, prep stems and releases, and drive Ableton Live directly.
</p>

<p align="center">
  <a href="https://github.com/patrickking67/producer/actions/workflows/ci.yml"><img src="https://github.com/patrickking67/producer/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/patrickking67/producer/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-black?style=flat-square" alt="MIT License"></a>
</p>

<p align="center">
  <a href="https://patrickking67.github.io/producer/"><strong>Website</strong></a> ·
  <a href="plugins/producer/">Plugin</a> ·
  <a href="max-for-live/">Max for Live device</a> ·
  <a href="plugins/producer/CONNECTORS.md">Connectors</a> ·
  <a href="examples/README.md">Workflow examples</a>
</p>

---

Created by **Patrick King**. MIT licensed.

This repo is a Claude Code **marketplace** that ships two surfaces of the same product:

| Component | What it is | Where it lives |
|---|---|---|
| **Producer** (Claude Code plugin) | 12 skills + 12 slash commands + 1 agent + 6 remote MCPs, with optional local Ableton control and the Ableton Knowledge desktop extension. Reviews, brainstorms, writes MIDI, designs sounds, mixes, browses your library, arranges, preps stems and releases, and drives Live directly. | [`plugins/producer/`](plugins/producer/) |
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

The marketplace manifest is at [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json). The 6 cloud MCPs (Splice, Spotify, Google Drive, Gmail, Google Calendar, Canva) OAuth on first use. Install the Ableton MCP separately: see [`plugins/producer/CONNECTORS.md`](plugins/producer/CONNECTORS.md#1-ableton-mcp).

Works in **Claude Code on the web** (cowork) and in the local CLI. Cloud MCPs OAuth on first use either way; the Ableton MCP only runs locally (it talks to Live over the Remote Script).

## Install (Producer for Live: the Max for Live device)

Follow the step-by-step in [`max-for-live/README.md`](max-for-live/README.md). You'll drop three JS files plus a `.amxd` patch into `~/Music/Ableton/User Library/Presets/MIDI Effects/Max MIDI Effect/Producer/`.

## What's in the Producer plugin

### 12 slash commands

| Command | Skill |
|---|---|
| `/review` | producer-review: peer-level teardown |
| `/brainstorm` | brainstorm: 3-5 directions with references |
| `/midi` | midi-lab: playable `.mid` from a prompt |
| `/sound` | sound-design: stock-device patch recipes + Splice |
| `/mix` | mix-coach: LUFS, sidechain, low-end glue |
| `/docs` | ableton-docs: Live / Push / Move / Note manuals + KB + videos |
| `/library` | library-browser: your Ableton Library + Packs, like Live's browser |
| `/arrange` | arrangement: bar-by-bar plan with an energy curve |
| `/reference` | reference-curator: Spotify playlists with BPM/key/LUFS |
| `/stems` | stem-prep: for mastering, remix, sync, DJ tools, live |
| `/release` | release-prep: master target, metadata, artwork, ISRC, schedule |
| `/session` | session-bridge: drive Live directly via the Ableton MCP |

### 1 agent

| Agent | Purpose |
|---|---|
| **ableton-engineer** | End-to-end multi-step tasks: "build me a tech house starter set", "prep this for release across streaming and Beatport", "compare my track to 5 references and write the mix moves". |

### 6 bundled MCP connectors

Auto-declared in [`.mcp.json`](plugins/producer/.mcp.json): **Splice**, **Spotify**, **Google Drive**, **Gmail**, **Google Calendar**, and **Canva**. Local Ableton control is configured separately so the committed repository contains remote HTTPS MCPs only. The **Ableton Knowledge** desktop extension adds manual, knowledge-base, and video lookups. Full breakdown in [CONNECTORS.md](plugins/producer/CONNECTORS.md).

## Repo layout

```
producer/
├── .claude-plugin/
│   └── marketplace.json          ← marketplace manifest
├── assets/
│   ├── producer-logo.svg         ← wordmark + mark (monochrome)
│   └── producer-mark.svg         ← icon only (square)
├── docs/                         ← GitHub Pages site (published as-is)
│   ├── index.html                ← landing page (Tailwind Play CDN)
│   ├── llms.txt                  ← same as the root llms.txt
│   └── og.png                    ← share image
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
│   └── producer.plugin           ← reproducible plugin bundle for manual install
├── scripts/
│   ├── check.sh                  ← npm run check
│   ├── check-repository.py       ← repository checks
│   └── package-plugin.py         ← npm run package
├── llms.txt
├── AGENTS.md                     ← agent and contributor guide
├── LICENSE
└── README.md
```

## Manual install (bundle)

If you'd rather sideload the zipped bundle instead of using the marketplace, grab [`dist/producer.plugin`](dist/producer.plugin) and drag it into Claude Code.

## See complete workflows

The [workflow examples](examples/README.md) show how Producer moves from a real production problem to concrete artifacts across arrangement, MIDI, sound design, mix decisions, and release preparation. Each example identifies the commands, expected outputs, and external connections involved.

## Development

Requirements: Python 3.11+, Node with npm, and the `claude` CLI (`npm install -g @anthropic-ai/claude-code@2.1.309`). The repository has no dependencies of its own.

```bash
npm run check     # manifests, frontmatter, bundle, site links, Max for Live scripts, strict plugin validation
npm run package   # rebuild dist/producer.plugin after changing plugins/producer/
npm run dev       # preview the site at http://127.0.0.1:4105
```

CI runs `npm run check` on every pull request and push to `main`. See [AGENTS.md](AGENTS.md) for the full guide and [CONTRIBUTING.md](CONTRIBUTING.md) for the pull request checklist.

## Deploy and releases

Merges to `main` run the check and publish `docs/` to [GitHub Pages](https://patrickking67.github.io/producer/). A `v*` tag that matches the plugin version runs the check and attaches the committed `dist/producer.plugin` to a GitHub release. See [CHANGELOG.md](CHANGELOG.md) for shipped changes.

## License

MIT. See [LICENSE](LICENSE).
