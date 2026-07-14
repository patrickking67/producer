# Architecture

Producer has two coordinated surfaces.

- The marketplace plugin provides 12 portable skills, 12 slash commands, one task agent, and connector configuration for music-production workflows.
- Producer for Live uses Max for Live JavaScript to read session context and write generated MIDI into Ableton Live.

The static site under `docs/` documents both surfaces and is deployed through GitHub Pages. `.claude-plugin/marketplace.json` is the marketplace entrypoint. `plugins/producer/.claude-plugin/plugin.json` is the plugin manifest.

Connector access is intentionally external to the plugin package. OAuth and local Ableton connectivity are configured by each user and no credentials belong in the repository.
