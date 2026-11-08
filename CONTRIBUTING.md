# Contributing

Thanks for helping with Producer. Changes are small and reviewed in pull requests against `main`.

## Setup

You need `python3` (3.11 or newer), `node` with `npm`, and the `claude` CLI for strict manifest validation:

```bash
npm install -g @anthropic-ai/claude-code@2.1.309
git clone git@github.com:patrickking67/producer.git
cd producer
npm run check
```

The repository has no dependencies to install. `npm run dev` serves the site from `docs/` at http://127.0.0.1:4105.

To try the plugin from your checkout, load it for one session with `claude --plugin-dir ./plugins/producer`.

## Branches and commits

- Branch from `main` with a prefix: `feat/`, `fix/`, `docs/` or `chore/`.
- Use [Conventional Commits](https://www.conventionalcommits.org/): `feat(skills): add a groove skill`, `fix(site): ...`, `docs: ...`.
- One logical change per commit. Each commit should pass `npm run check`.

## Pull request checklist

- [ ] `npm run check` passes.
- [ ] `npm run package` run and `dist/producer.plugin` committed if anything under `plugins/producer/` changed.
- [ ] Marketplace and plugin manifests still agree, and the version is bumped in both if this is a release.
- [ ] README, site, `llms.txt` and counts updated if you added or removed a skill, command or agent.
- [ ] `CHANGELOG.md` has an entry under `[Unreleased]`.
- [ ] No credentials, tokens or personal data anywhere in the diff.

## Checks

`npm run check` is the same command CI runs. See [AGENTS.md](AGENTS.md#commands) for what it covers.
