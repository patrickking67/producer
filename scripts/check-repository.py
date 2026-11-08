from html.parser import HTMLParser
import json
import re
from pathlib import Path
import subprocess
import sys
import tomllib


root = Path(__file__).resolve().parents[1]
errors = []


def load_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path.relative_to(root)}: {error}")
        return {}


marketplace = load_json(root / ".claude-plugin" / "marketplace.json")
plugin = load_json(root / "plugins" / "producer" / ".claude-plugin" / "plugin.json")
load_json(root / "plugins" / "producer" / ".mcp.json")

for required_file in (root / "examples" / "README.md", root / "CHANGELOG.md", root / ".github" / "workflows" / "release.yml"):
    if not required_file.exists():
        errors.append(f"missing required release asset: {required_file.relative_to(root)}")

packaged = subprocess.run(
    [sys.executable, str(root / "scripts" / "package-plugin.py"), "--check"],
    capture_output=True,
    text=True,
)
if packaged.returncode:
    errors.append(packaged.stdout.strip() or packaged.stderr.strip())

entry = (marketplace.get("plugins") or [{}])[0]
for field in ("name", "version", "homepage", "repository"):
    if entry.get(field) != plugin.get(field):
        errors.append(f"marketplace and plugin disagree on {field}")

for label, pattern, expected in (
    ("commands", "plugins/producer/commands/*.md", 12),
    ("skills", "plugins/producer/skills/*/SKILL.md", 12),
    ("agents", "plugins/producer/agents/*.md", 1),
):
    count = len(list(root.glob(pattern)))
    if count != expected:
        errors.append(f"expected {expected} {label}, found {count}")


def frontmatter_keys(path):
    """Return the top-level frontmatter keys and their inline values.

    claude plugin validate --strict parses the YAML itself; this only checks
    the keys this repository relies on.
    """
    text = path.read_text()
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append(f"{path.relative_to(root)}: missing frontmatter")
        return {}
    keys = {}
    for line in match.group(1).splitlines():
        found = re.match(r"([A-Za-z][\w-]*):\s*(.*)", line)
        if found:
            keys[found.group(1)] = found.group(2).strip()
    return keys


plugin_root = root / "plugins" / "producer"
for skill in sorted(plugin_root.glob("skills/*/SKILL.md")):
    keys = frontmatter_keys(skill)
    if keys and keys.get("name") != skill.parent.name:
        errors.append(f"{skill.relative_to(root)}: name must match its folder {skill.parent.name!r}")
    if keys and not keys.get("description"):
        errors.append(f"{skill.relative_to(root)}: missing description")

for command in sorted(plugin_root.glob("commands/*.md")):
    keys = frontmatter_keys(command)
    if keys and not keys.get("description"):
        errors.append(f"{command.relative_to(root)}: missing description")

for agent in sorted(plugin_root.glob("agents/*.md")):
    keys = frontmatter_keys(agent)
    for key in ("name", "description"):
        if keys and not keys.get(key):
            errors.append(f"{agent.relative_to(root)}: missing {key}")
    if "tools" in keys and not keys["tools"]:
        errors.append(f"{agent.relative_to(root)}: tools must be a comma-separated string, not a YAML list")

# The committed MCP config holds remote HTTPS servers only, and the Codex
# config must offer the same servers.
mcp_urls = set()
for name, server in (load_json(plugin_root / ".mcp.json").get("mcpServers") or {}).items():
    url = server.get("url", "")
    if "command" in server or not url.startswith("https://"):
        errors.append(f"plugins/producer/.mcp.json: {name} must be a remote https server")
    mcp_urls.add(url)

try:
    codex = tomllib.loads((plugin_root / "codex-config.toml").read_text())
except (OSError, tomllib.TOMLDecodeError) as error:
    errors.append(f"plugins/producer/codex-config.toml: {error}")
    codex = {}
codex_urls = {server.get("url", "") for server in (codex.get("mcp_servers") or {}).values()}
if codex_urls != mcp_urls:
    errors.append("plugins/producer/codex-config.toml and .mcp.json list different servers")


class LocalAssetParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for key in ("href", "src"):
            value = values.get(key, "")
            if not value or value.startswith(("http:", "https:", "#", "data:")):
                continue
            path = (root / "docs" / value.split("#", 1)[0].split("?", 1)[0]).resolve()
            if not path.exists():
                errors.append(f"docs/index.html: missing {value}")


parser = LocalAssetParser()
parser.feed((root / "docs" / "index.html").read_text())

for script in sorted((root / "max-for-live").glob("*.js")):
    result = subprocess.run(["node", "--check", str(script)], capture_output=True, text=True)
    if result.returncode:
        errors.append(f"{script.relative_to(root)}: {result.stderr.strip()}")

if (root / "CLAUDE.md").read_text().strip() != "@AGENTS.md":
    errors.append("CLAUDE.md must contain only @AGENTS.md")

# Walk only files git knows about, so worktrees under .worktrees/ or
# .claude/worktrees/ and other ignored folders are never scanned.
tracked = subprocess.run(
    ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
    cwd=root,
    capture_output=True,
    check=True,
).stdout.decode().split("\0")
repository_files = [root / name for name in tracked if name and (root / name).is_file()]

retired_repository = "patrickking67/" + "producer-plugin"
for path in repository_files:
    if "dist" in path.relative_to(root).parts:
        continue
    try:
        if retired_repository in path.read_text():
            errors.append(f"{path.relative_to(root)}: contains the retired repository slug")
    except UnicodeDecodeError:
        pass

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("Validated manifests, frontmatter, MCP configs, bundle, 12 commands, 12 skills, one agent, docs, and Max for Live scripts.")
