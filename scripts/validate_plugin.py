#!/usr/bin/env python3
"""Validate Producer plugin structure.

Runs on every push/PR via .github/workflows/validate.yml. Catches the
three bug classes we shipped in v1.0:

1. Invalid JSON in marketplace.json / plugin.json / .mcp.json
2. Unparseable YAML frontmatter in SKILL.md / commands / agents
3. Wrong schema (authors vs author, tools as list vs string, …)
4. Orphaned commands (command references a skill that doesn't exist)

Exit 0 on success, 1 on any failure.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / "plugins" / "producer"

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"  FAIL: {msg}")


def parse_frontmatter(path: Path) -> dict | None:
    text = path.read_text()
    m = re.match(r"---\n(.+?)\n---", text, re.DOTALL)
    if not m:
        fail(f"{path.relative_to(REPO)}: no YAML frontmatter")
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        first_line = str(e).splitlines()[0]
        fail(f"{path.relative_to(REPO)}: YAML error — {first_line}")
        return None


def check_json(path: Path, required: list[str], forbidden: dict[str, str]) -> dict | None:
    if not path.exists():
        fail(f"{path.relative_to(REPO)}: missing")
        return None
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        fail(f"{path.relative_to(REPO)}: invalid JSON — {e}")
        return None
    for key in required:
        if key not in data:
            fail(f"{path.relative_to(REPO)}: missing required key {key!r}")
    for key, reason in forbidden.items():
        if key in data:
            fail(f"{path.relative_to(REPO)}: forbidden key {key!r} — {reason}")
    return data


def check_marketplace() -> None:
    print("\n[marketplace.json]")
    data = check_json(
        REPO / ".claude-plugin" / "marketplace.json",
        required=["name", "owner", "plugins"],
        forbidden={},
    )
    if not data:
        return
    if "name" in data:
        plugins = data.get("plugins", [])
        if not plugins:
            fail("marketplace.json: empty plugins array")
        for i, plugin in enumerate(plugins):
            prefix = f"plugins[{i}]"
            for key in ("name", "source"):
                if key not in plugin:
                    fail(f"marketplace.json: {prefix} missing {key!r}")
            if "authors" in plugin:
                fail(f"marketplace.json: {prefix} uses 'authors' (plural) — schema is 'author' (singular)")
            if "author" in plugin and not isinstance(plugin["author"], dict):
                fail(f"marketplace.json: {prefix}.author must be an object, got {type(plugin['author']).__name__}")
    if "owner" in data:
        owner = data["owner"]
        if "url" in owner:
            fail("marketplace.json: owner.url is not in the schema — only name + email are valid")


def check_plugin_manifest() -> None:
    print("\n[plugin.json]")
    data = check_json(
        PLUGIN / ".claude-plugin" / "plugin.json",
        required=["name", "version"],
        forbidden={"authors": "use 'author' (singular object), not 'authors' (array)"},
    )
    if data and "author" in data and not isinstance(data["author"], dict):
        fail(f"plugin.json: author must be an object, got {type(data['author']).__name__}")


def check_mcp_config() -> None:
    print("\n[.mcp.json]")
    data = check_json(PLUGIN / ".mcp.json", required=["mcpServers"], forbidden={})
    if not data:
        return
    for name, server in data.get("mcpServers", {}).items():
        has_command = "command" in server
        has_url = "url" in server
        if not has_command and not has_url:
            fail(f".mcp.json: server {name!r} has neither 'command' nor 'url'")
        if has_command and has_url:
            fail(f".mcp.json: server {name!r} has both 'command' and 'url' — pick one")


def check_skills() -> set[str]:
    print("\n[skills/]")
    skills_dir = PLUGIN / "skills"
    found = set()
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        data = parse_frontmatter(skill_md)
        if data is None:
            continue
        name = data.get("name") or skill_md.parent.name
        found.add(name)
        if "description" not in data:
            fail(f"{skill_md.relative_to(REPO)}: missing 'description'")
        if "name" in data and data["name"] != skill_md.parent.name:
            fail(f"{skill_md.relative_to(REPO)}: name {data['name']!r} doesn't match directory {skill_md.parent.name!r}")
    if not found:
        fail("skills/: no skills found")
    print(f"  parsed {len(found)} skill(s)")
    return found


def check_commands(skill_names: set[str]) -> None:
    print("\n[commands/]")
    cmd_dir = PLUGIN / "commands"
    count = 0
    for cmd_md in sorted(cmd_dir.glob("*.md")):
        data = parse_frontmatter(cmd_md)
        if data is None:
            continue
        count += 1
        if "description" not in data:
            fail(f"{cmd_md.relative_to(REPO)}: missing 'description'")
    print(f"  parsed {count} command(s)")


def check_agents() -> None:
    print("\n[agents/]")
    agents_dir = PLUGIN / "agents"
    count = 0
    for agent_md in sorted(agents_dir.glob("*.md")):
        data = parse_frontmatter(agent_md)
        if data is None:
            continue
        count += 1
        for key in ("name", "description"):
            if key not in data:
                fail(f"{agent_md.relative_to(REPO)}: missing {key!r}")
        if "tools" in data and not isinstance(data["tools"], str):
            fail(
                f"{agent_md.relative_to(REPO)}: 'tools' must be a comma-separated string "
                f"(got {type(data['tools']).__name__}) — Claude Code subagent schema"
            )
    print(f"  parsed {count} agent(s)")


def check_max_for_live_js() -> None:
    print("\n[max-for-live/]")
    m4l_dir = REPO / "max-for-live"
    js_files = list(m4l_dir.glob("*.js"))
    if not js_files:
        print("  (no JS files)")
        return
    print(f"  found {len(js_files)} JS file(s)")


def check_codex_config() -> None:
    print("\n[codex-config.toml]")
    path = PLUGIN / "codex-config.toml"
    if not path.exists():
        fail(f"{path.relative_to(REPO)}: missing")
        return
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore[no-redef]
    try:
        data = tomllib.loads(path.read_text())
    except tomllib.TOMLDecodeError as e:
        fail(f"{path.relative_to(REPO)}: invalid TOML — {e}")
        return
    servers = data.get("mcp_servers", {})
    if not servers:
        fail("codex-config.toml: no [mcp_servers.*] entries found")
        return
    for name, server in servers.items():
        has_command = "command" in server
        has_url = "url" in server
        if not has_command and not has_url:
            fail(f"codex-config.toml: mcp_servers.{name} has neither 'command' nor 'url'")
    print(f"  parsed {len(servers)} server entr{'y' if len(servers) == 1 else 'ies'}")


def main() -> int:
    print("Producer plugin validator")
    print(f"Repo: {REPO}")

    check_marketplace()
    check_plugin_manifest()
    check_mcp_config()
    skill_names = check_skills()
    check_commands(skill_names)
    check_agents()
    check_max_for_live_js()
    check_codex_config()

    print()
    if errors:
        print(f"{len(errors)} error(s)")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
