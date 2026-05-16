# Connectors

The Producer plugin auto-declares 7 MCP servers in `.mcp.json`. Six are cloud HTTP MCPs that OAuth on first use; the Ableton MCP runs locally via `uvx`. The Ableton Knowledge desktop extension is recommended separately.

## All connectors at a glance

| Connector | Type | Required | Declared in `.mcp.json` | Used by |
|---|---|---|---|---|
| **Ableton** | stdio (local) | Recommended | Yes — `uvx ableton-mcp` | `session-bridge`, also called from `midi-lab`, `sound-design`, `mix-coach`, `arrangement`, `stem-prep`, `release-prep`, `library-browser`, `ableton-engineer` |
| **Splice** | HTTP (cloud) | Optional | Yes | `sound-design`, `producer-review`, `brainstorm`, `library-browser` (fallback) |
| **Spotify** | HTTP (cloud) | Optional | Yes | `reference-curator`, `brainstorm`, `producer-review`, `mix-coach`, `release-prep` |
| **Google Drive** | HTTP (cloud) | Optional | Yes | `stem-prep`, `release-prep`, `reference-curator`, `arrangement` |
| **Gmail** | HTTP (cloud) | Optional | Yes | `stem-prep`, `release-prep`, `reference-curator` |
| **Google Calendar** | HTTP (cloud) | Optional | Yes | `release-prep`, `ableton-engineer` |
| **Canva** | HTTP (cloud) | Optional | Yes | `release-prep`, `brainstorm` (artwork, moodboards) |

Plus one separate Desktop Extension recommended for Claude users:

| Extension | Type | Used by |
|---|---|---|
| **Ableton Knowledge** | Desktop Extension (Ableton) | `ableton-docs` — searches Live / Push / Move / Note manuals, knowledge base, video transcripts |

If a connector isn't authorized, the skills degrade gracefully: they tell you the gap and proceed with everything else.

## 1. Ableton MCP

**Server**: [`ableton-mcp`](https://github.com/ahujasid/ableton-mcp) by Siddharth Ahuja.

**Install** (one-time):
```bash
# 1. Install the server
uv tool install ableton-mcp
# (or: pipx install ableton-mcp)

# 2. Install the Live Remote Script
# Download AbletonMCP_Remote_Script/Ableton_MCP.py from the repo
# Copy to: ~/Music/Ableton/User Library/Remote Scripts/Ableton_MCP/
# (create the folder if it doesn't exist; the file must be at exactly Ableton_MCP/Ableton_MCP.py)

# 3. In Live → Preferences → Link/Tempo/MIDI:
#    Control Surface = "Ableton MCP"
#    Input = (none)
#    Output = (none)
```

**Tools used**: `get_session_info`, `get_track_info`, `create_midi_track`, `create_audio_track`, `set_tempo`, `load_instrument`, `load_effect`, `load_browser_item`, `get_browser_tree`, `get_browser_items_at_path`, `create_clip`, `add_notes_to_clip`, `fire_clip`, `stop_clip`, `set_clip_name`, `start_playback`, `stop_playback`.

## 2. Splice

**URL**: `https://mcp.splice.com/mcp`. OAuth on first use.

**Tools used**: `search` (Search Splice Sounds), `create_stack` (Create Stack from Sample), `download_asset` (Download Sound), `prompt_to_stack` (Generate Stack from Prompt), `share_stack`, `update_stack`.

**Skip if**: you don't have a Splice subscription, or you've already got the sample library you need locally.

## 3. Spotify

**URL**: `https://mcp-gateway-external-pilot.spotify.net/mcp`. OAuth on first use.

**Tools used**: `search`, `fetch_tracks` (audio features incl. BPM/key), `get_currently_playing`, `create_playlist`, `add_to_library`, `Remove_from_library`.

## 4. Google Drive

**URL**: `https://drivemcp.googleapis.com/mcp/v1`. OAuth on first use.

**Tools used**: `search_files`, `read_file_content`, `download_file_content`, `create_file`, `get_file_metadata`, `get_file_permissions`, `list_recent_files`. Upload stems, references, masters, save reference notes, share folders.

## 5. Gmail

**URL**: `https://gmailmcp.googleapis.com/mcp/v1`. OAuth on first use.

**Tools used**: `search_threads`, `get_thread`, `list_drafts`, `list_labels`, `create_draft`. The skills *draft* — you send. Never auto-send promo email.

## 6. Google Calendar

**URL**: `https://calendarmcp.googleapis.com/mcp/v1`. OAuth on first use.

**Tools used**: `list_calendars`, `list_events`, `get_event`, `create_event`, `update_event`, `delete_event`, `find_free_time`, `respond_to_event`. Used to create reminders for the release timeline (−28 / −21 / −14 / −7 / −1 / 0).

## 7. Canva

**URL**: `https://mcp.canva.com/mcp`. OAuth on first use.

**Tools used**: `search-designs`, `get-design`, `get-design-pages`, `get-design-content`, `search`, `fetch`, `import-design-from-url`. Used by `release-prep` to draft cover art templates and by `brainstorm` for visual moodboards.

## Bonus: Ableton Knowledge (Desktop Extension)

Not declared in `.mcp.json` because it's a Claude Desktop Extension, not an HTTP MCP. Strongly recommended for `ableton-docs` lookups.

**Install**: in Claude Desktop → Settings → Extensions → install "Ableton Knowledge" (developed by Ableton). Tools: `search_live_manual`, `search_push_manual`, `search_move_manual`, `search_note_manual`, `search_knowledge_base`, `search_videos`, `search_transcripts`, `get_ableton_knowledge_info`. Everything runs locally — no network calls.

## Install order

1. **Ableton MCP** first — it's the only one that takes setup work. Without it, `session-bridge` can't drive Live and the engineer agent can't do end-to-end runs.
2. **Drop the plugin into Claude Code** — the remaining 6 cloud MCPs are declared in `.mcp.json` and OAuth on first use.
3. **Authorize what you need.** Splice and Canva are skippable; Spotify / Drive / Gmail / Calendar unlock different workflows.
4. **Add Ableton Knowledge** in Claude Desktop if you want richer manual lookups.

## Use with Codex CLI

Codex doesn't have a plugin marketplace, but it does speak MCP — so the 7 connectors above (which carry most of the actual capability) all work in Codex too. The slash commands and skills are Claude Code-specific and don't port; in Codex you just describe what you want and Codex calls the MCPs directly.

Paste the contents of [`codex-config.toml`](codex-config.toml) into `~/.codex/config.toml` (or use `codex mcp add --url …` for each cloud MCP to let Codex run the OAuth flow). Requires Codex CLI with streamable HTTP MCP support.

## Routing rules the skills follow

| Question | First connector | Then |
|---|---|---|
| "How does [Live feature] work?" | Ableton Knowledge `search_live_manual` | `search_knowledge_base`, `search_videos` |
| "Find me a [sound]" | `library-browser` (local) | Splice (`search` / `prompt_to_stack`) if no local match |
| "What should this sound like?" | Spotify `search` | Spotify `fetch_tracks` for BPM/key |
| "Make me a reference playlist" | Spotify `create_playlist` | Drive (save notes) |
| "Send stems to my engineer" | `stem-prep` | Drive (upload) + Gmail (draft) |
| "Set up my release" | `release-prep` | Drive + Gmail + Calendar + Canva (artwork) |
| "Set BPM to 126 / add track / load preset" | `session-bridge` (Ableton MCP) | — |
| "Compare my track to a reference" | Spotify `get_currently_playing` or `search` | `mix-coach` |
| "Draft cover art / a release moodboard" | Canva `search-designs` / `import-design-from-url` | Drive (save) |
