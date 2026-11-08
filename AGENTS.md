# Repository instructions

Producer is an Ableton Live production toolkit distributed as a Claude Code marketplace plugin and a Max for Live device, with a static site on GitHub Pages.

## Stack

- Plugin: Markdown skills, commands and one agent with YAML frontmatter, JSON manifests, `.mcp.json` with remote HTTPS servers only.
- Max for Live: plain JavaScript run by Max (`max-for-live/*.js`). No build step.
- Site: one static `docs/index.html` using the Tailwind Play CDN (pinned). No build step.
- Tooling: Python 3.11+ and bash scripts, Node for `node --check`, and the `claude` CLI for strict manifest validation. `package.json` only names scripts and has no dependencies.

## Layout

| Path | What it is |
|---|---|
| `.claude-plugin/marketplace.json` | Marketplace manifest. Must agree with the plugin manifest on name, version, homepage and repository. |
| `plugins/producer/` | The plugin: `.claude-plugin/plugin.json`, `.mcp.json`, `codex-config.toml`, `skills/`, `commands/`, `agents/`, `CONNECTORS.md`. |
| `dist/producer.plugin` | Reproducible zip of `plugins/producer/`. Generated, but committed so it can be sideloaded. |
| `max-for-live/` | Device scripts and setup guide. |
| `docs/` | GitHub Pages site. Everything in it is published, including `docs/llms.txt` and `docs/og.png`. |
| `llms.txt` | Same content as `docs/llms.txt`. |
| `examples/` | Workflow examples linked from the site and README. |
| `scripts/` | `check.sh`, `check-repository.py`, `package-plugin.py`. |

## Commands

Requirements: `python3` (3.11+), `node`, `npm`, and the `claude` CLI (`npm install -g @anthropic-ai/claude-code@2.1.309`, the version CI pins). There is nothing to install for the repo itself.

```bash
npm run check     # everything CI runs; must pass before any commit
npm run package   # rebuild dist/producer.plugin after any change under plugins/producer/
npm run dev       # serve docs/ at http://127.0.0.1:4105 (also .claude/launch.json "producer-site")
```

`npm run check` runs `scripts/check.sh`, which runs:

1. `python3 scripts/check-repository.py`: manifests agree, skill names match folders, skills, commands and the agent have descriptions, agent `tools` is a comma-separated string, `.mcp.json` holds only remote https servers and matches `codex-config.toml`, `dist/producer.plugin` is byte-identical to a fresh build, exactly 12 commands, 12 skills and one agent, local links in `docs/index.html` resolve, `node --check` on the Max for Live scripts, `CLAUDE.md` is exactly `@AGENTS.md`, `llms.txt` copies match, and no em dashes or retired repository slug in tracked text.
2. `claude plugin validate --strict .` for the marketplace.
3. `claude plugin validate --strict plugins/producer` for the plugin manifest and component frontmatter.

There is no separate lint, typecheck or test suite; the check above is the test.

## Conventions

- Keep the marketplace and plugin manifests aligned. Bump `version` in both and in `CHANGELOG.md` together.
- Components load from the default `skills/`, `commands/` and `agents/` folders. Do not add `skills`, `commands` or `agents` keys to `plugin.json`; the `agents` key rejects directories.
- Adding or removing a skill, command or agent changes the counts in `check-repository.py`, the README, the site and `llms.txt`. Update all of them.
- Any change under `plugins/producer/` needs `npm run package` and the rebuilt `dist/producer.plugin` in the same commit.
- Use the canonical repository name `producer` in every install command and URL.
- Plain, short writing. No em dashes, no emojis. ISO dates.
- Conventional Commits, one logical change per commit, branch names `feat/`, `fix/`, `docs/`, `chore/`.

## Safety

- Never commit credentials, OAuth tokens, API keys, `.env` files, local settings or user-local agent state. Connector auth happens on the user's machine.
- `.mcp.json` and `codex-config.toml` hold remote https servers only. Local servers such as the Ableton MCP are documented in `CONNECTORS.md`, not committed.
- Do not edit `dist/producer.plugin` by hand.
- Do not change GitHub settings, Pages configuration, secrets or branch protection.

## Shipping

- Open a pull request against `main`. CI runs `npm run check`.
- Merging to `main` runs `pages.yml`: the same check, then publishes `docs/` to https://patrickking67.github.io/producer/.
- A release is a `v*` tag on `main` (for example `v1.0.1`) matching the manifest version. `release.yml` runs the check, confirms the tag matches the version and attaches the committed `dist/producer.plugin` to a GitHub release.

## Definition of done

- `npm run check` passes locally.
- `dist/producer.plugin` rebuilt if plugin content changed.
- Site checked with `npm run dev` at 375px and desktop if `docs/` changed.
- README, site, `llms.txt` and `CHANGELOG.md` (`[Unreleased]`) match the change.
