---
name: reference-curator
description: Build a reference playlist across Spotify and Apple Music for a vibe, mix target, arrangement model, or track in progress. Tags each reference with BPM, key, integrated LUFS, and what to listen for. Use when the user says "find references for", "make me a reference playlist", "what should this sound like", "tracks like X", "/reference", or wants a curated A/B set.
argument-hint: "<vibe, genre, or 'like this track'>"
---

# Reference Curator

The goal isn't 8 random vibey tracks. It's 8 tracks that each *teach the user something specific* about where their record could go.

## Method

1. **Clarify scope** in one question if missing: are we matching mix, vibe, arrangement, or sound palette?
2. **Pull 8–12 candidates** across both Spotify and Apple Music (use both — coverage and curation differ)
3. **Tag every track** with the row below
4. **Group into 3–4 buckets** (e.g. "for the drop energy", "for the bass tone", "for the breakdown")
5. **Save a playlist** on the user's preferred platform; back up the list to Google Drive as a markdown file

## Output table

| Track | Artist | BPM | Key | LUFS-i | What to listen for |
|---|---|---|---|---|---|
| *Untitled* | Lane 8 | 124 | A min | −11 | Breakdown shape — strips to vocal at 2:18 |
| *...* | ... | ... | ... | ... | ... |

Pull BPM/key from Spotify audio features where available, else from beatport metadata if known. LUFS-i is your best guess from the master loudness rules of that genre + label.

## Bucket grouping

Each bucket = 2–3 tracks that solve the same problem:

**For the drop weight**
- Track A — kick at 55 Hz, mono-tight
- Track B — same energy, but uses a vocal chop as the rhythmic anchor
- Track C — slower BPM, half-time drop variant

**For the breakdown emotion**
- ...

## Playlist creation

After approval:
- Spotify: `create_playlist` named `"<track> — references"`, then `add_to_library` each match
- Apple Music: create a playlist via the Apple Music MCP, same naming
- Save the curator notes + the bucket structure to `~/Music/Producer/references/<track>_references.md` *and* upload to Google Drive at `Producer/References/`

## Workflow with mix-coach
When this skill is called from `mix-coach`:
- Lead with the 2 references that match the user's mix target most tightly
- Level-match by integrated LUFS (Utility → Gain) before A/B
- Note the 3 biggest spectral / dynamics differences and feed them back to `mix-coach`

## Workflow with arrangement
When called from `arrangement`:
- Pick references with similar arrangement shape
- Tag the timestamps of every section transition
- Feed those timestamps into the arrangement bar-by-bar table

## Workflow with brainstorm
When called from `brainstorm`:
- Pick references that *differ* from where the user is right now — at least one in an adjacent genre
- Each reference should illustrate *one* direction in the brainstorm output

## Connectors
- **Spotify**: `search`, `fetch_tracks` (audio features), `create_playlist`, `add_to_library`, `get_currently_playing`
- **Apple Music**: search, playlist creation, "now playing"
- **Google Drive**: upload the curator notes markdown
- **Gmail**: optionally email the playlist link to a collaborator (the user names the recipient)
- **Splice**: if a reference uses an iconic sample, `describe_a_sound` to find a related one

## Tone
Curatorial. If two references in the same bucket are redundant, kill one.

## After
"Want me to (a) save the playlist + curator notes to Drive, (b) draft mix moves from these references (`mix-coach`), or (c) email the playlist to a collaborator (Gmail)?"
