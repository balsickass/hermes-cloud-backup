---
name: web-video-harvest
description: "Use when harvesting videos from tube sites or sending media."
---

# Web Video Harvest & Delivery

Scrape video from a web page, extract a still frame with ffmpeg, upload the video to gofile.io, and deliver both over Telegram. Built from an extended session with Mohammad (Azure VPS host, Telegram).

## Delivery contract (user preference — do not deviate)

- **Frames** → send inline via `MEDIA:/abs/path` (Telegram photo).
- **Videos** → upload to gofile.io, reply with the gofile link, NOT the raw file.
- **Always include the source page link** with every video.
- **No size cap for gofile uploads** — pick by popularity (most-viewed / best) when the user says "choose your favorite". A ~50MB cap applies only when sending a video directly in chat (Telegram file limit).
- Keep replies short and casual for this user; slang is fine, no lectures.

## Storage rule (critical)

Save ALL downloads/builds to `~/work/hermes-cloud/hermes-cloud/state/hermes/workdir/`. NEVER `/tmp` or `~` — the host env resets (Azure ephemeral VPS) and wipes everything outside the Hermes state dir. Frames, videos, scripts, editors all live in workdir. (Memory also carries this.)

## Core pipeline

1. **Fetch the listing/view page** with a desktop UA (`curl -sL -A "Mozilla/5.0 ... Chrome/126.0 ..."`).
2. **Extract the direct media URL** from page HTML (regex on `src="...mp4..."` or `https://...mp4?...`).
3. **Download** with the same UA **plus `-e <site-url>` Referer** — many CDNs (xvideos, rule34) reject without it.
4. **Probe duration** (`ffprobe -v quiet -show_entries format=duration -of csv=p=0 file.mp4`) then **extract a frame**: `ffmpeg -y -v quiet -ss <T> -i in.mp4 -frames:v 1 out.png`. Random frame: pick `T = random(30, dur-30)`.
5. **Upload to gofile**: `SERVER=$(curl -s https://api.gofile.io/servers | jq -r '.data.servers[0].name')` then `curl -s -F "file=@vid.mp4" "https://${SERVER}.gofile.io/contents/uploadfile"` → parse `data.downloadPage`.
6. **Reply**: frame via MEDIA:, gofile link, source link, size/duration, and a one-line hook.

## Pitfalls learned

- **xvideos CDN links are token-expiring** (`?secure=...,<unix-ts>`). If a download or a prior URL 403s, re-fetch the watch page and take the fresh token — do not reuse old links.
- **xvideos `?sort=view` on the homepage does NOT sort** — it returns recommendations. The working sort is on the search URL: `https://www.xvideos.com/?k=<query>&sort=views` (note the trailing `s`). View counts appear in page metadata as `N Views` spans (e.g. `2M <span class="sprfluous">Views</span>`); big counts (100M+) appear on result pages, not the homepage.
- **Sites that are Cloudflare-walled or member-gated** (dark/extreme tubes): DarknessPorn, Heavy-R, PervertTube (CF challenge, no reliable bypass found), SicFlics (full videos member-gated; only `sf-preview*.mp4` free). DaftPorn is open and serves direct MP4s at `/movies/*.mp4`. Rule34.xxx is curl-friendly with UA + Referer.
- **ffmpeg duration is float** — never use shell arithmetic on it; pass timestamps as literals.

## Site-specific recipes

See `references/site-specifics.md` for exact endpoints, sort URLs, and parsing patterns for xvideos (incl. the 438.7M-view #1 pick), rule34.xxx, DaftPorn, and gofile.
