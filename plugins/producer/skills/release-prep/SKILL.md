---
name: release-prep
description: Release-day prep — master target, distribution metadata, artwork specs, ISRC, label deliverables, promo plan, schedule. Use when the user says "I'm releasing this", "prep this for distribution", "what does Distrokid / Spotify for Artists / Beatport need", "/release", "master for streaming", "mastering checklist", or is shipping a track. Defaults to electronic-music release workflow.
argument-hint: "<track title, label, release date>"
---

# Release Prep

A release is a checklist. Miss an item and the label or DSP bounces it back two days before drop.

## Phase 0 — Decide the target

Ask in one question if not given:
- **Streaming-only** (Spotify / Apple / Tidal): master to −14 to −12 LUFS-i, −1.0 dBTP
- **Club / DJ-first** (Beatport / Traxsource): master to −9 to −7 LUFS-i, −0.8 dBTP
- **Both**: deliver two masters with the same artistic intent, different loudness

## Phase 1 — Final master checklist

- [ ] Integrated LUFS hits target ±0.5 dB
- [ ] True peak ≤ ceiling, no inter-sample peaks (check with `ffmpeg ebur128=peak=true`)
- [ ] Mono compatibility — bass and sub mono < 120 Hz
- [ ] No DC offset (`sox stat` → DC offset 0.000)
- [ ] No clicks at start/end (top + tail with fade-in / fade-out < 30 ms each)
- [ ] Fade-out length is musical (last bar plus reverb tail, not abrupt)
- [ ] 24-bit / project SR WAV master + 16-bit / 44.1 dithered for CD-quality
- [ ] Clean 30-second preview clip for socials (best 30 s of the drop)
- [ ] Instrumental version (vocal-out) if vocals exist
- [ ] Radio edit < 3:30 if a radio plan exists

## Phase 2 — Metadata package

Required for every DSP / distributor:

| Field | Value |
|---|---|
| Title |  |
| Artist (primary) |  |
| Artist (featured) |  |
| Remixer |  |
| Label |  |
| Catalog # |  |
| Genre / Subgenre | (Beatport list — get exact spelling) |
| BPM | (one decimal, e.g. 124.0) |
| Key | (Camelot + Western — e.g. 8A / A minor) |
| Composer (publishing) | (legal name) |
| Producer | (credited name) |
| Mix engineer |  |
| Mastering engineer |  |
| ISRC | (label assigns; or distributor auto-generates) |
| UPC / EAN | (distributor) |
| P-line | (© 2026 Label Name) |
| C-line | (© 2026 Label Name) |
| Release date |  |
| Pre-save date |  |
| Language of lyrics |  |
| Explicit | yes / no / clean |
| Spotify Canvas | 1080×1920 mp4, 3–8 sec |
| Spotify Artist bio updated | yes/no |

Save this metadata sheet as `~/Music/Producer/releases/<title>_metadata.md` and upload to Google Drive at `Producer/Releases/<title>/`.

## Phase 3 — Artwork specs

| Where | Spec |
|---|---|
| DSPs (universal) | 3000×3000 px, RGB, JPG or PNG, < 10 MB |
| Beatport | 1400×1400 min, square |
| Spotify Canvas | 1080×1920 vertical video, 3–8 s, MP4 |
| Apple Music motion artwork | 1080×1080 or 1920×1080, < 100 MB, MP4 |
| Instagram square | 1080×1080 |
| Instagram story / reel | 1080×1920 |
| YouTube thumbnail | 1280×720 |

Verify the master artwork is **300 dpi, RGB (not CMYK), no transparency, embedded color profile**. Run `identify -verbose artwork.jpg | rg -i "(geometry|colorspace|profile)"` to confirm.

## Phase 4 — Promo plan + schedule

Use Google Calendar to lock the timeline:
- **Release date −28** — final master locked, sent to label
- **Release date −21** — distributor upload, pre-save link live
- **Release date −14** — first promo post + Canvas live
- **Release date −7** — second promo post, DJ promo pool live, Beatport pre-order
- **Release date −1** — final post, story countdown
- **Release date 0** — release day post, story link, "out now" everywhere
- **Release date +7** — first-week analytics screenshot post

Create those as recurring calendar events with reminders the day before each one.

## Phase 5 — Distribution & promo

Distribution platforms to consider (electronic-music releases):
- **Beatport / Traxsource** — DJ-first, often via label
- **Spotify / Apple Music / Tidal / Amazon** — via DistroKid, Symphonic, Stem, Amuse, label
- **SoundCloud Premier** — for SC monetization
- **Bandcamp** — direct-to-fan, highest margin
- **DJ pools** — DMS, Direct Music Service, Beatport Promo, etc. (for industry DJs)

Promo email drafts (Gmail):
- Tastemaker DJs (with private SoundCloud / WeTransfer link, BPM, key, release date)
- Radio (BBC R1 Dance, Rinse, etc.)
- Blog editors

For each draft, lead with the *one sentence* that makes this record different, then the BPM/key/drop date, then the private link.

## Connectors
- **Google Drive** — upload final master + metadata + artwork
- **Gmail** — draft promo / label / engineer emails
- **Google Calendar** — schedule the −28 / −21 / −14 / −7 / −1 / 0 milestones
- **Spotify** — `create_playlist` for the pre-save playlist and a "Inspired By" companion playlist
- **Canva** — `search-designs` / `import-design-from-url` for cover art templates and motion / lyric video assets
- Ableton MCP — drive the final master export

## After
"Want me to (a) schedule the full release timeline in Calendar, (b) draft promo emails for the top 10 DJs (Gmail), (c) build a pre-save companion playlist on Spotify, (d) draft cover art templates in Canva, or (e) double-check the final master against the LUFS target (`mix-coach`)?"
