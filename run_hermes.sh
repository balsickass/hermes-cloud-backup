#!/usr/bin/env bash
# Boot the Hermes gateway with a self-healing profile.
# - if state/hermes/config.yaml is missing → write fresh cloud profile
# - run gateway in foreground for $RUN_MINUTES
set -u
HERMES="$HOME/.local/bin/hermes"
export HERMES_HOME="${HERMES_HOME:-$PWD/state/hermes}"
mkdir -p "$HERMES_HOME"

# ---- first-boot profile bootstrap ----
if [ ! -f "$HERMES_HOME/config.yaml" ]; then
  echo "[boot] no profile found → generating cloud config"
  bash "$(dirname "$0")/bootstrap_profile.sh"
fi

# ---- run ----
echo "[boot] gateway starting (window: ${RUN_MINUTES:-285}m)"
timeout "${RUN_MINUTES:-285}m" "$HERMES" gateway run 2>&1 | tee -a "$HERMES_HOME/gateway.log"
EXIT=$?
echo "[boot] gateway window ended (exit=$EXIT) — exiting cleanly for next cron"
exit 0
