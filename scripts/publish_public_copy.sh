#!/usr/bin/env bash
# Build the public copy of this repository (D-066): a fresh clone with knowledge/pages.jsonl
# (full text of the organiser/publisher documents) removed from every master commit.
#
# Usage: scripts/publish_public_copy.sh DEST_DIR
#
# - Filters only refs/heads/master and the freeze-1 tag. The provenance branch never held
#   pages.jsonl, so it and its run/* tags keep their exact hashes (the provenance_commit in
#   every run manifest stays valid).
# - Deterministic: re-running on later commits gives the same new hashes for old commits,
#   so a later push is a fast-forward.
# - Writes DEST_DIR/.git/filter-repo/commit-map (old -> new master hashes; the code_sha in
#   run manifests is an old hash; docs/commit-map.txt is the committed copy).
# - Never pushes. Push by name from DEST_DIR: master, provenance, the freeze-1 tag
#   (never --all / --mirror / --tags; worktree-agent-* branches stay local).
set -euo pipefail

src="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
dest="${1:?usage: $0 DEST_DIR}"
[ -e "$dest" ] && { echo "refusing: $dest exists" >&2; exit 1; }

git clone -q --no-local --single-branch -b master "$src" "$dest"
cd "$dest"
git fetch -q origin provenance:provenance 'refs/tags/*:refs/tags/*'
git remote remove origin
uvx git-filter-repo --invert-paths --path knowledge/pages.jsonl \
  --preserve-commit-hashes --refs refs/heads/master refs/tags/freeze-1 --force >/dev/null

# Drop the clone's reflog so the old blobs become unreachable, then prune them.
git reflog expire --expire=now --all
git gc -q --prune=now

# Checks: no pages.jsonl path or blob (any version ever committed) left; provenance unchanged.
if git rev-list --objects --all | grep -q 'knowledge/pages.jsonl'; then
  echo "FAIL: pages.jsonl still reachable" >&2; exit 1
fi
for blob in $(git -C "$src" log --all --format= --raw --no-abbrev -- knowledge/pages.jsonl | awk '{print $4}' | sort -u); do
  case "$blob" in 0000000*) continue ;; esac
  if git cat-file -e "$blob" 2>/dev/null; then echo "FAIL: pages.jsonl blob $blob still in .git" >&2; exit 1; fi
done
[ "$(git rev-parse provenance)" = "$(git -C "$src" rev-parse provenance)" ] \
  || { echo "FAIL: provenance hash changed" >&2; exit 1; }
echo "OK: $dest (master $(git rev-parse --short master), provenance $(git rev-parse --short provenance))"
