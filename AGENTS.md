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

Keep marketplace and plugin manifests aligned. Use the canonical repository name `producer` in every installation command and URL. Do not commit credentials, local settings, or user-local agent state.
