#!/usr/bin/env python3
"""Build the balsicl1234/hermes-cloud repo: files are written by separate
write_file steps; this script pushes the whole directory tree to GitHub.
Usage: python3 push_repo.py <local-dir> <owner/repo> <branch> <msg>"""
import sys, os, base64, json, urllib.request

LOCAL, REPO, BRANCH, MSG = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
TOKEN = os.environ["GH_TOKEN"]
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

# 1. get base commit of branch (create orphan-ish if missing)
st, ref = gh("GET", f"git/ref/heads/{BRANCH}")
if st == 200:
    base_sha = ref["object"]["sha"]
    _, base_obj = gh("GET", f"git/commits/{base_sha}")
    base_tree = base_obj["tree"]["sha"]
else:
    base_sha, base_tree = None, None

# 2. collect local files
blobs = []
for root, dirs, files in os.walk(LOCAL):
    dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
    for f in files:
        p = os.path.join(root, f)
        rel = os.path.relpath(p, LOCAL).replace(os.sep, "/")
        with open(p, "rb") as fh:
            data = fh.read()
        if len(data) > 900_000:
            print(f"skip large: {rel}")
            continue
        st, blob = gh("POST", "git/blobs",
                      {"content": base64.b64encode(data).decode(), "encoding": "base64"})
        if st not in (200, 201):
            print(f"blob FAIL {rel}: {st} {blob}")
            sys.exit(1)
        blobs.append({"path": rel, "mode": "100644", "type": "blob", "sha": blob["sha"]})

# 3. create tree (with base_tree so unchanged files persist)
tree_payload = {"tree": blobs}
if base_tree:
    tree_payload["base_tree"] = base_tree
st, tree = gh("POST", "git/trees", tree_payload)
if st not in (200, 201):
    print("tree FAIL:", st, json.dumps(tree)[:300]); sys.exit(1)

# 4. commit
commit_payload = {"message": MSG, "tree": tree["sha"], "parents": ([base_sha] if base_sha else [])}
st, commit = gh("POST", "git/commits", commit_payload)
if st not in (200, 201):
    print("commit FAIL:", st, json.dumps(commit)[:300]); sys.exit(1)

# 5. point branch at it
if base_sha:
    st, _ = gh("POST", f"git/refs/heads/{BRANCH}", {"sha": commit["sha"], "force": True})
else:
    st, _ = gh("POST", "git/refs", {"ref": f"refs/heads/{BRANCH}", "sha": commit["sha"]})
print("PUSHED" if st in (200, 201) else f"REF FAIL {st}", commit["sha"][:8], f"({len(blobs)} files)")
