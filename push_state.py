#!/usr/bin/env python3
"""Push changed files under state/hermes/ to the state branch every ~2 min.
Skips: caches, logs >8MB, .env (secrets must never hit the branch)."""
import os, sys, time, base64, json, urllib.request, hashlib

REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
BRANCH = "state"
STATE_ROOT = os.environ["HERMES_HOME"]
INTERVAL = int(os.environ.get("STATE_PUSH_INTERVAL", "2"))
API = f"https://api.github.com/repos/{REPO}"

def gh(method, path, payload=None):
    req = urllib.request.Request(f"{API}/{path}", method=method,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Authorization": f"Bearer {TOKEN}",
                 "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")

SKIP_DIRS = {"__pycache__", ".cache", "node_modules", "request_dumps", "tmp"}
SKIP_FILES = {".env", "gateway.log"}
PUSHABLE_EXT = {".db", ".json", ".yaml", ".yml", ".md", ".txt", ".jsonl"}

def iter_files():
    for root, dirs, files in os.walk(STATE_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f in SKIP_FILES:
                continue
            if not any(f.endswith(e) for e in PUSHABLE_EXT):
                continue
            p = os.path.join(root, f)
            try:
                if os.path.getsize(p) > 8 * 1024 * 1024:
                    continue
                with open(p, "rb") as fh:
                    yield p, fh.read()
            except OSError:
                continue

def rel_of(p):
    return os.path.relpath(p, STATE_ROOT).replace(os.sep, "/")

def main():
    print(f"[pusher] watching {STATE_ROOT} → {BRANCH} every {INTERVAL}m")
    time.sleep(60)
    while True:
        try:
            pushed = 0
            for path, data in iter_files():
                rel = rel_of(path)
                digest = hashlib.sha256(data).hexdigest()
                hpath = f".state-hashes/{digest[:16]}.h"
                st, cur = gh("GET", f"contents/{hpath}?ref={BRANCH}")
                if st == 200:
                    continue  # unchanged since last push
                st, _ = gh("PUT", f"contents/state/hermes-home/{rel}",
                           {"message": f"state-sync: {rel}",
                            "content": base64.b64encode(data).decode(),
                            "branch": BRANCH})
                if st in (200, 201):
                    gh("PUT", f"contents/{hpath}",
                       {"message": f"hash: {digest[:12]}",
                        "content": base64.b64encode(digest.encode()).decode(),
                        "branch": BRANCH})
                    pushed += 1
            if pushed:
                print(f"[pusher] pushed {pushed} files")
        except Exception as e:
            print(f"[pusher] cycle error: {e}", file=sys.stderr)
        time.sleep(INTERVAL * 60)

if __name__ == "__main__":
    main()
