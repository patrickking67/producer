---
name: ableton-docs
description: Surgical lookups in the Ableton Live, Push, Move, and Note manuals plus the help center and the full YouTube catalog. Use when the user says "how do I [do X] in Ableton", "what does [device/parameter] do", "find a tutorial on", "Push 3 question", "Move workflow", "/docs", or asks any Ableton-specific feature question. Always grounded in actual docs — never answer from memory.
argument-hint: "<your Ableton question>"
---

# Ableton Docs

Pull answers from the actual manuals and the video catalog. Don't speculate.

## Routing

| Question is about | Call |
|---|---|
| Live (any version) — devices, workflows, MIDI, automation, warping, racks, M4L | `search_live_manual` |
| Push 3 (standalone or controller) | `search_push_manual` — ask which Push model if unclear |
| Move (portable standalone) | `search_move_manual` |
| Note (iOS app) | `search_note_manual` |
| Setup / install / licensing / Cloud / troubleshooting | `search_knowledge_base` |
| "Show me" / video / tutorial | `search_videos` |
| Exact spoken content from a video | `search_transcripts` |

**Always pair**: manual lookup + `search_knowledge_base`. The KB has how-to articles the manual doesn't.

## Output format

**Answer** — direct, ≤ 4 sentences. Quote parameter names exactly as the manual phrases them.

**Steps** (if procedural) — numbered, terse, real menu paths and key commands.

**Sources** — link the manual section + KB article + video (when relevant), as markdown links. Format:
- [Live 12 Manual → Section](url)
- [KB: Article title](url)
- [Video: Title (timestamp)](url)

## Push model disambiguation

When the user says "Push" without specifying:
- **Push 3 Standalone** — built-in computer, battery, makes music without a Mac/PC
- **Push 3 (controller mode)** — same hardware, plugged into a computer
- **Push 2** — controller only, requires computer
- **Push 1** — original controller

Ask which one before you answer if the workflow differs.

## Special routing
- **Ableton Link** (sync over network) — Live manual covers usage; for the protocol/SDK send to https://ableton.github.io/link/
- **Max for Live patching/programming** — Live manual covers using devices; for building patches send to https://cycling74.com/learn

## Tone
Brief. The user is advanced. Skip explaining what the manual is. Give the answer, the steps, the links.

## After
Offer one specific adjacent feature you noticed in the same manual section, and offer a video walkthrough if you found a relevant one in `search_videos`.
