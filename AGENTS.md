# Repository instructions

Producer is an Ableton Live production toolkit distributed as a Claude Code marketplace plugin and a Max for Live device.

## Repository structure

- `plugins/producer/`: plugin manifest, skills, commands, agent, and connector references.
- `max-for-live/`: device scripts and setup guide.
- `docs/`: GitHub Pages website.
- `dist/producer.plugin`: packaged release bundle.

## Verification

```bash
python3 scripts/check-repository.py
bash scripts/package-plugin.sh
```

`check-repository.py` needs `node` (it runs `node --check` on the Max for Live scripts). It checks that the marketplace and plugin manifests agree, that `dist/producer.plugin` holds the same manifest, that there are exactly 12 commands, 12 skills and one agent, that local links in `docs/index.html` resolve, and that `CLAUDE.md` is exactly `@AGENTS.md`. Put shared instructions here, not in `CLAUDE.md`.

`package-plugin.sh` rebuilds `dist/producer.plugin` from `plugins/producer/`. The zip bytes change on every run, so only commit the bundle when plugin content changed.

## Deploys

- Every push to `main` runs `pages.yml`, which validates the repo and publishes `docs/` to GitHub Pages.
- Pushing a `v*` tag runs `release.yml`, which repackages the plugin and creates a GitHub release with `dist/producer.plugin`. Bump the version in both manifests and `CHANGELOG.md` first.

Keep marketplace and plugin manifests aligned. Use the canonical repository name `producer` in every installation command and URL. Do not commit credentials, local settings, or user-local agent state.
