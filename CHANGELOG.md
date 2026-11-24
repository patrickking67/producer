# Changelog

All notable changes to Producer are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Plugin icon and a privacy policy page (`docs/privacy.html`) with `privacyPolicyUrl` in `plugin.json`, which clears both plugin directory warnings.
- `set_model` message for the Max for Live device, and a 60 second request timeout.
- `npm run check`, one command for everything CI runs, and `npm run dev` to preview the site on port 4105.
- CI workflow that runs the check on every pull request and push to `main`, with a pinned validator CLI.
- Strict marketplace and plugin validation in the check.
- Checks for skill, command and agent frontmatter, remote-only MCP servers, matching Codex config, matching `llms.txt` copies and em dashes.
- `llms.txt` at the site root and the repository root.
- Share image, canonical URL and theme metadata for the site.
- `CONTRIBUTING.md`, issue forms, a pull request template, CODEOWNERS, Dependabot for GitHub Actions, `.editorconfig` and `.gitattributes`.
- Complete production workflow examples with expected outputs.
- Automated plugin packaging for versioned GitHub releases.

### Changed

- Site redesign: hand-written `docs/index.html` and `docs/site.css` replace the Tailwind Play CDN and the scroll-reveal script. The page now loads no third-party code and no JavaScript, supports light and dark through `prefers-color-scheme`, and has a session-view clip grid and a MIDI clip illustration in place of the grid background.
- `dist/producer.plugin` is now built reproducibly, and the check fails if it differs from a fresh build of `plugins/producer/`.
- Releases ship the committed bundle and refuse a tag that does not match the plugin version.
- Site: skip link, main landmark, visible focus, a mobile nav, content visible without scripts, pinned Tailwind CDN and fewer looping animations.
- Renamed the repository from `producer-plugin` to `producer` and updated installation links.

### Fixed

- The Max for Live device defaulted to `claude-sonnet-4-5`. It now defaults to `claude-sonnet-5-5`, and its prompt no longer names a specific producer.
- `plugin.json` no longer sets `agents` to a directory, which strict validation rejects. Components load from their default folders.
- The site described `/reference` as using Apple Music. It uses Spotify.

## [1.0.0] - 2026-05-16

### Added

- Producer plugin with 12 skills, 12 slash commands, the `ableton-engineer` agent and six remote MCP connectors (Splice, Spotify, Google Drive, Gmail, Google Calendar, Canva).
- Producer for Live, a Max for Live MIDI effect that generates patterns into the highlighted clip.
- Marketplace manifest so `/plugin marketplace add patrickking67/producer` works.
- GitHub Pages site and deploy workflow.
- Codex CLI connector config.

### Fixed

- Plugin install failures from invalid agent frontmatter and manifest author fields.
