# Site-specific recipes (verified working)

## xvideos.com

**Working sort (the only one that actually sorts by views):**
`https://www.xvideos.com/?k=<query>&sort=views` — note the trailing `s` in `views`. The homepage `?sort=view` (no `s`) is IGNORED — it returns recommendations, not rankings.

**Extract link+views from result page (metadata format, not views-count span):**
```python
import re, subprocess
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
r = subprocess.run(["curl","-sL","-A",UA,"https://www.xvideos.com/?k=porn&sort=views"], capture_output=True, text=True, timeout=90)
h = r.stdout
blocks = re.split(r'<div id="video_', h)
for b in blocks[1:]:
    l = re.search(r'href="(/video\.[^"]+)"', b)
    v = re.search(r'(\d[\d.,]*[KMkm]?)\s*(?:<span class="sprfluous">)?\s*Views', b, re.I)
    if l and v: print(v.group(1), l.group(1))
```
Handle `k`/`M` suffixes incl. decimals (`771.4k`).

**Watch page → direct stream (token-expiring):**
```bash
curl -sL -A "$UA" "https://www.xvideos.com/video.<slug>" | grep -oE 'https://[^"]*\.mp4[^"]*'
# then download WITH referer:
curl -sL -A "$UA" -H "Referer: https://www.xvideos.com/" -o out.mp4 "<url>"
```
The `?secure=...,<ts>` token expires — re-fetch the page for a fresh one.

**Real all-time top (verified 2026):** `https://www.xvideos.com/video.hetaccd3f4e/bratty_-_fucked_my_step_ter_in_our_parents_bed` — 438.7M views, ~39MB 360p, 11:56. (Second: Mia Khalifa video-game clip, 30.5M. The `tags/100-million-views` page is clickbait — real counts there were 30M max. `tags/most-viewed` tops out ~17M.)

## rule34.xxx

Works with plain curl + UA + Referer. No Cloudflare issue.
```bash
curl -sL -A "$UA" "https://rule34.xxx/index.php?page=post&s=view&id=<ID>" | grep -oE 'src="https://[^"]*\.mp4[^"]*"'
curl -sL -A "$UA" -e "https://rule34.xxx/" -o out.mp4 "<direct-url>"
```
Listing page `page=post&s=list&tags=...` gives IDs; check size first with `curl -sIL | grep -i content-length` before downloading (skip >~50MB for Telegram direct, gofile has no cap).

## PunishBang.com (BDSM/punishment, darker — full videos DOWNLOADABLE)

Videos list: `https://www.punishbang.com/videos/` → full URLs `https://www.punishbang.com/video/<id>/<slug>/`.

Watch page contains BOTH endpoints:
- **Full file**: `https://www.punishbang.com/get_file/1/<hash>/33000/<id>/<id>.mp4/` (with optional `?v-acctoken=...` — the tokenless URL WORKED for download).
- **Preview** (`*_small_preview.mp4`) — only 10s; do NOT deliver this as the video. The full file is what you want.

Download the tokenless full URL with UA + Referer: worked, 145MB / 10:08. The preview grab (305KB) was the user-corrected mistake.

## DaftPorn.com (open, unblocked)

Homepage `/` → 23+ links on `extreme-videos/`; watch page has a plain `<source src="https://www.daftporn.com/movies/<file>.mp4">`. Direct download, no token.

**VIEW COUNTS EXIST on the archive pages** (verified 2026): `https://www.daftporn.com/?p=archive&Categorie=<Cat>` renders each video as `DATE | Category | N views` (thousands-separated, no suffix, e.g. `456.140`). Categories that exist: Anal, Big cock, Caught, Compilation, Creampie, Dick, Drunk, Fucking, Handjob, Orgasm, Public, Sluts, Spying, Webcam, Weird, Wtf. Homepage `/`, `extreme-videos/`, `/videos/`, and watch pages show NO counts — that's why they looked statless at first. `toplist.php?id=N` returns empty (`<HTML></HTML>` — dead/blocked).

**Site-wide most-viewed (crawled all 15 categories):** `Lunatic-films-visit-at-hot-doctor.php` — **1,571,364 views** (2018/02/01, Spying). #2: `Interrupted-at-a-bad-moment.php` 1,265,288. #3: `African-big-cock-safari.php` 1,090,219.

**Crawl recipe:**
```python
import re, subprocess
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
cats = ["Anal","Big cock","Caught","Compilation","Creampie","Dick","Drunk","Fucking","Handjob","Orgasm","Public","Sluts","Spying","Webcam","Weird","Wtf"]
all_items = []
for cat in cats:
    h = subprocess.run(["curl","-sL","-A",UA,f"https://www.daftporn.com/?p=archive&Categorie={cat}"], capture_output=True, text=True, timeout=70).stdout
    blocks = re.findall(r'href="(https://www\.daftporn\.com/extreme-videos/[^"]+)"[^>]*>([^<]+)</a>.*?(\d{4}/\d{2}/\d{2})\s*\|\s*([^|]+)\|\s*([\d.,]+)\s*views', h, re.S)
    for b in blocks:
        all_items.append((float(b[4].replace(".","").replace(",","")), b[0], b[1], b[2], cat))
all_items.sort(key=lambda x: x[0], reverse=True)
```
Note views use `.` as thousands separator (`456.140` = 456,140) — strip dots BEFORE converting.

Page numbers: `/?p=page1..5`.

## Cloudflare-walled / member-gated (as of this session)

- darknessporn.com, heavy-r.com, perverttube.com — CF "Just a moment..." challenge; no working bypass found (clicking the human checkbox in browser didn't clear it).
- sicflics.com — full movies member-gated; the `v6.pop.php?id=` player redirects to join page. Only free `https://images.sicflics.com/image.recent/vids/sf-preview*.mp4` previews (~small).

## gofile.io upload

```bash
SERVER=$(curl -s https://api.gofile.io/servers | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['servers'][0]['name'])")
curl -s -F "file=@vid.mp4" "https://${SERVER}.gofile.io/contents/uploadfile" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['downloadPage'])"
```
Uploads are anonymous guest uploads; links persist server-side and survive local env wipes.

## Frame extraction

```bash
DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 in.mp4)   # float, e.g. 715.972278
echo $DUR   # never do arithmetic on it in bash
ffmpeg -y -v quiet -ss <literal-int> -i in.mp4 -frames:v 1 out.png
```
Random frame: `python3 -c "import random;print(random.randint(30, int(float('$DUR'))-30))"`
Seeking past the end yields an EMPTY png (`Output file is empty`) — clamp to dur-30.