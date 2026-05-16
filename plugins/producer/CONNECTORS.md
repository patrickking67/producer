# Connectors

The Producer plugin uses 7 MCP servers. Six are auto-declared in `.mcp.json` and OAuth on first use. One — the Ableton MCP — runs locally via `uvx`.

## All connectors at a glance

| Connector | Type | Required | Declared in `.mcp.json` | Used by |
|---|---|---|---|---|
| **Ableton** | stdio (local) | Recommended | Yes — `uvx ableton-mcp` | `session-bridge`, also called from `midi-lab`, `sound-design`, `mix-coach`, `arrangement`, `stem-prep`, `release-prep`, `library-browser`, `ableton-engineer` |
| **Splice** | HTTP (cloud) | Optional | Yes | `sound-design`, `producer-review`, `brainstorm`, `library-browser` (fallback) |
| **Spotify** | HTTP (cloud) | Optional | Yes | `reference-curator`, `brainstorm`, `producer-review`, `mix-coach`, `release-prep` |
| **Apple Music** | stdio (local) | Optional | Yes — `npx @kazuph/mcp-apple-music` | `reference-curator`, `brainstorm`, `release-prep` |
| **Google Drive** | HTTP (cloud) | Optional | Yes | `stem-prep`, `release-prep`, `reference-curator`, `arrangement` |
| **Gmail** | HTTP (cloud) | Optional | Yes | `stem-prep`, `release-prep`, `reference-curator` |
| **Google Calendar** | HTTP (cloud) | Optional | Yes | `release-prep`, `ableton-engineer` |

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

**Tools used**: `describe_a_sound`, `prompt_to_stack`, `create_stack`, `share_stack`, `download_asset`.

**Skip if**: you don't have a Splice subscription, or you've already got the sample library you need locally.

## 3. Spotify

**URL**: `https://mcp-gateway-external-pilot.spotify.net/mcp`. OAuth on first use.

**Tools used**: `search`, `fetch_tracks` (audio features incl. BPM/key), `get_currently_playing`, `create_playlist`, `add_to_library`.

## 4. Apple Music

**Server**: [`@kazuph/mcp-apple-music`](https://www.npmjs.com/package/@kazuph/mcp-apple-music) — controls the local Apple Music app via AppleScript (macOS only).

**Install**: nothing; `npx` pulls it on first use. macOS will prompt to allow Claude Code to control Music.app the first time.

**Tools used**: search the local library + Apple Music catalog, create playlists, currently playing, play/pause.

**Skip if**: you're on Windows/Linux or only use Spotify.

## 5. Google Drive

**URL**: `https://mcp.google.com/drive`. OAuth on first use.

**Tools used**: upload files (stems, references, masters), create folders, share folders / files with collaborators.

## 6. Gmail

**URL**: `https://mcp.google.com/gmail`. OAuth on first use.

**Tools used**: draft messages (label sends, DJ promo, mastering hand-offs).

The skills *draft* — you send. Never auto-send promo email.

## 7. Google Calendar

**URL**: `https://mcp.google.com/calendar`. OAuth on first use.

**Tools used**: create events with reminders for the release timeline (−28 / −21 / −14 / −7 / −1 / 0).

## Install order

1. **Ableton MCP** first — it's the only one that takes setup work. Without it, `session-bridge` can't drive Live and the engineer agent can't do end-to-end runs.
2. **Drop the plugin into Claude Code** — the remaining 6 MCPs are declared in `.mcp.json` and OAuth on first use.
3. **Authorize what you need.** Splice and Apple Music are skippable; the rest unlock different workflows.

## Routing rules the skills follow

| Question | First connector | Then |
|---|---|---|
| "How does [Live feature] work?" | `search_live_manual` | `search_knowledge_base`, `search_videos` |
| "Find me a [sound]" | `library-browser` (local) | Splice (`describe_a_sound`) if no local match |
| "What should this sound like?" | Spotify `search` | Apple Music search |
| "Make me a reference playlist" | Spotify + Apple Music | Drive (save notes) |
| "Send stems to my engineer" | `stem-prep` | Drive (upload) + Gmail (draft) |
| "Set up my release" | `release-prep` | Drive + Gmail + Calendar |
| "Set BPM to 126 / add track / load preset" | `session-bridge` (Ableton MCP) | — |
| "Compare my track to a reference" | Spotify `get_currently_playing` or `search` | `mix-coach` |
