from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
import zipfile


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

with zipfile.ZipFile(root / "dist" / "producer.plugin") as archive:
    packaged_manifest = json.loads(archive.read(".claude-plugin/plugin.json"))
    if packaged_manifest != plugin:
        errors.append("dist/producer.plugin does not match the source plugin manifest")

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

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("Validated manifests, 12 commands, 12 skills, one agent, docs, and Max for Live scripts.")
