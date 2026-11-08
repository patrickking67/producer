# Security policy

## Supported versions

| Version | Supported |
|---|---|
| 1.x (latest on `main`) | Yes |
| Older | No |

## Reporting a vulnerability

Report privately through GitHub security advisories:
https://github.com/patrickking67/producer/security/advisories/new

Do not open a public issue, and do not include credentials, tokens or personal data in a report. Include the file or component, steps to reproduce and the impact you expect.

Expect an acknowledgement within 7 days and an assessment within 30 days. Fixes ship in a new release and are noted in `CHANGELOG.md`.

## Scope

In scope:

- The plugin under `plugins/producer/`: manifests, skills, commands, the agent and the committed MCP configuration.
- The Max for Live scripts under `max-for-live/`.
- The site under `docs/` and the repository workflows.

Out of scope: the third-party MCP servers Producer connects to (Splice, Spotify, Google, Canva, the Ableton MCP), Ableton Live, Claude Code and the Anthropic API. Report those to their maintainers.

## Credential handling

Producer integrates with local and remote Model Context Protocol servers and can call the Anthropic API from Max for Live. Never commit API keys or OAuth tokens. Store credentials in supported environment or secret-management facilities and review every connector before granting access.

The committed MCP configurations contain server metadata only. OAuth consent and local credentials remain outside the repository.
