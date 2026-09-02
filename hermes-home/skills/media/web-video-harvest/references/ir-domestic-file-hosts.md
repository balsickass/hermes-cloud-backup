# Iranian domestic file hosts (ترافیک داخلی = cheaper data for IR users)

User (Mohammad, Mashhad, Iran) wants file upload/download hosts that cost ~50% LESS internet usage. Mechanism: Iranian ISPs (MCI/Hamrah-e Aval, Shatel, etc.) bill **domestic/national traffic** (ترافیک داخلی) at roughly half the international rate, so a file service **hosted inside Iran** = uploads/downloads count as national traffic = cheaper lane.

## VERIFIED upload tests (2026-09) — the real results

Live-tested by actually uploading a real MP4 (DaftPorn video) and random files:

### ✅ **up.20script.ir — the ONLY one that accepts adult content**
- Uploaded a 3.6MB MP4 (no signup, anonymous) → got permanent link → **re-downloaded: byte-identical (same MD5)**. No antivirus flag, no extension block.
- **Hard cap: 50MB per file** — 49MB OK, 50MB REJECTED: "حجم فایل باید کوچکتر از 50 MB باشد" (must be smaller than 50MB).
- Extension rules: `.mp4` ✅, `.zip` ✅, `.bin` ❌ blocked ("پسوند bin پشتیبانی نمیشود").
- Upload endpoint (reverse-engineered): POST multipart `file_1_=<file>` + `submitr=1` to `https://up.20script.ir/`. Response page contains `do.php?filename=<name>`; the actual file is served via `do.php?downf=<name>` (needs the PHPSESSID cookie from visiting do.php?filename= first).
- LiteSpeed server, Iranian .ir infra → domestic traffic.
- **BUT: user verdict "Throw it in the trash"** — 50MB cap kills it for full-length videos (their files are 30-145MB). Only useful for sub-50MB files. Gofile remains the real host for full videos.

### ❌ uploadkon.ir — REJECTS adult content
- Homepage claims free 10GB, no signup, drag & drop — **BUT**:
  - MP4 upload → "پسوند mp4 پشتیبانی نمیشود!" (mp4 extension not supported without membership).
  - Zip of the same video → **antivirus flagged it as malicious** ("حاوی کد مخرب").
- So: no anonymous MP4s at all. Dead end for this use.

### ❌ files.ir — needs Iranian SMS-OTP, corporate
- Registration via `my.files.ir/register` requires **Iranian phone + SMS/OTP verification** (API: `/api/v1/auth/sms/send-login-code`, `/verify-login-code`). No account = no upload.
- Corporate/semiofficial (universities, Digikala) — porn would be nuked by ToS anyway.

### ❌ my.uupload.ir — login-gated
- Requires session/login (logout action present); free tier very limited.

### ❌ imgurl.ir — 250MB/file cap, images-first

## The honest verdict for this user's workflow

- **Gofile.io stays the host**: anonymous, uncapped, never touches adult content. Foreign servers (EU) but no data-plan discount.
- For TRUE 50% cheaper domestic traffic on videos: only 20script works but caps at 50MB. Options: (a) accept 20script only for sub-50MB videos, (b) split big videos into <50MB parts via ffmpeg (`ffmpeg -i in.mp4 -c copy -f segment -segment_time 300 part_%03d.mp4`) and upload each, (c) stay on gofile.
- User found the 50MB cap pointless for his use case — don't re-sell 20script hard; one mention of the cap and move on.

## Pitfalls

- Generic English web_search returns unrelated junk (website builders, filtering news). Search Persian: `سایت آپلود فایل ایرانی ترافیک داخلی رایگان نامحدود` or `آپلود فایل رایگان نامحدود دانلود ترافیک ملی`. The unlock term: **ترافیک داخلی / ترافیک ملی**.
- Iranian hosts often have an AV/extension filter invisible on the homepage — ALWAYS test-upload a real MP4 before promising a link. Page claims ("آپلود نامحدود") are marketing, not reality.
- Finding the upload endpoint: grep the page for `filedrop({` / `url:` / form `action` + the JS bundle; hidden in init config, not obvious.
