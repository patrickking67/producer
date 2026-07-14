# Security policy

## Reporting

Use GitHub private vulnerability reporting when available. Do not publish credentials, tokens, personal data, or exploit details in a public issue.

## Credential handling

Producer integrates with local and remote Model Context Protocol servers and can call the Anthropic API from Max for Live. Never commit API keys or OAuth tokens. Store credentials in supported environment or secret-management facilities and review every connector before granting access.

The committed MCP configurations contain server metadata only. OAuth consent and local credentials remain outside the repository.
