#!/usr/bin/env python3
"""Create the main branch on an empty repo, then push the local tree."""
import json, urllib.request, os, base64, subprocess, sys

TOKEN = os.environ["GH_TOKEN"]
API = "https://api.github.com/repos/balsicl1234/hermes-cloud"

def gh(method, path, payload=None):
    req = urllib.request.Request(f"{API}/{path}", method=method,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")

st, ref = gh("GET", "git/ref/heads/main")
if st != 200:
    st, blob = gh("POST", "git/blobs", {"content": base64.b64encode(b"# hermes-cloud\n").decode(), "encoding": "base64"})
    st, tree = gh("POST", "git/trees", {"tree": [{"path": "README.md", "mode": "100644", "type": "blob", "sha": blob["sha"]}]})
    st, commit = gh("POST", "git/commits", {"message": "init", "tree": tree["sha"], "parents": []})
    st, _ = gh("POST", "git/refs", {"ref": "refs/heads/main", "sha": commit["sha"]})
    print("main created:", st)

r = subprocess.run([sys.executable, "/tmp/hermes-cloud-build/push_repo.py",
                    "/tmp/hermes-cloud-build", "balsicl1234/hermes-cloud", "main",
                    "initial deploy: hermes agent gateway on actions"],
                   env=dict(os.environ))
sys.exit(r.returncode)
