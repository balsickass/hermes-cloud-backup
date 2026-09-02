# Hermes Cloud — full Hermes Agent on GitHub Actions, $0

Telegram bot: the gateway bot (@balsic_hermes_bot or whichever token is in
TG_BOT_TOKEN secret). Runs the FULL Hermes Agent (tools, memory, skills,
cron, dashboard-capable) as a messaging gateway — nothing local.

## How it works
- `cron 0 */5` → fresh Ubuntu runner every 5h.
- Installs Hermes Agent via the official installer.
- First boot: `bootstrap_profile.sh` writes config.yaml + .env (secrets
  injected from GitHub Secrets — never committed).
- `run_hermes.sh` runs `hermes gateway run` for 4h45m.
- `push_state.py` syncs the Hermes profile (state.db, memory, skills,
  sessions, config) to the `state` branch every ~2 min so every shift
  resumes where the last one ended.
- Restore step pulls the state branch back at boot.

## Secrets
- TG_BOT_TOKEN — Telegram bot token
- ROUTER_API_KEY — 9router key (Flash-lite)
- TELEGRAM_ALLOWED_USERS — comma-separated user IDs (Boss = 6592796294)

## Manual run
Actions tab → hermes-cloud → Run workflow.
