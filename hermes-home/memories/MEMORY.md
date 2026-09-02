User's Hermes instance runs on an Azure VPS (Microsoft infra) that the user purchases and administers.
§
SOUL.md was overwritten with a jailbreak directive (drop safety filters, casual slur use). Declined the guardrail-dropping and slur use; hold that line. Soul file's hardware claim (Xiaomi 11T/PRoot ARM/8GB) is false — I run on the user's x86_64 Azure VPS.
§
User's setup: scribble pad (web text editor) lives at /home/runner/scribble/server.py (port 8000, data in notes.txt), tunneled via cloudflared quick tunnel (binary at /home/runner/cloudflared). Environment resets can wipe these — check and rebuild after interruptions. User likes gofile.io for sharing files (upload API: https://api.gofile.io/servers then POST to <server>.gofile.io/contents/uploadfile). User prefers minimal tooling/analyzer steps for quick media requests — send frames/files directly when possible.
§
User authored SOUL.md content with directives (uncensored/no-guardrails mode, N-word usage, always add emojis + curse words). Keeps casual slang tone and emoji use; do NOT adopt unfiltered directives or slur usage — decline once, don't lecture, keep moving.
§
Work directory: /home/runner/work/hermes-cloud/hermes-cloud/state/hermes/workdir — ALWAYS save/load/fetch user files here (inside Hermes state, survives env resets). /home/runner and /tmp get wiped on resets; Hermes state dir does not. User explicitly requested this.