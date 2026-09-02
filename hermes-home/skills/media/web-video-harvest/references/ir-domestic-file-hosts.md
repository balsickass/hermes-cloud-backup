# Iranian domestic file hosts (ترافیک داخلی = cheaper data for IR users)

User (Mohammad, Mashhad, Iran) wants file upload/download hosts that cost ~50% LESS internet usage. The mechanism: Iranian ISPs (MCI/Hamrah-e Aval, Shatel, etc.) bill **domestic/national traffic** (`ترافیک داخلی`) at roughly half the international rate, so any file service **hosted inside Iran** makes uploads/downloads count as national traffic — literally the cheaper lane. Verified via web_search + live curl (HTTP 200 checks) 2026-09.

## Shortlist (Iranian-hosted, free tiers)

1. **files.ir** — best overall. Paid-ish but homepage states "بدون محدودیت برای کاربران ایرانی" (no limits for Iranian users); free signup at my.files.ir/register; direct links, chunk upload. Trusted by Top universities (Sharif, Tehran, Amirkabir) + Digikala — legit infra. Workspaces/subscriptions for teams; free tier has some caps.
2. **uploadkon.ir** — fastest to use: drag & drop, **no account**, free up to **10GB per file**, permanent direct links, Iranian servers.
3. **my.uupload.ir** — direct-link file host; explicitly advertises "ترافیک داخلی" (domestic traffic) and unlimited bandwidth; free tier + paid subscriptions for heavy users.
4. **imgurl.ir** — small files only (~250MB cap), permanent links.

## What to tell the user

- No Iranian host is truly "unlimited forever free" like gofile.io anonymous guests — free tiers cap at 10GB/file (uploadkon), storage per account, etc. Honest framing: **files.ir + uploadkon.ir combo** = free uploads + Iranian hosting = ~half the traffic cost vs gofile for data-billed plans.
- For Telegram delivery workflow: still send frames inline + gofile for videos (the delivery contract), but mention these as the cheaper alternative when the user's data plan matters.
- These were NOT used for an actual upload this session — honest note: verified reachable + feature claims from their pages, not a real file transfer. Test-upload first before promising a link.

## Pitfall

- Generic web_search in English or with "melli internet" returns unrelated stuff (website builders, filtering news). Search in Persian: `سایت آپلود فایل ایرانی ترافیک داخلی رایگان نامحدود` or `آپلود فایل رایگان نامحدود دانلود ترافیک ملی`. The term that unlocks the right results is **ترافیک داخلی / ترافیک ملی**.
