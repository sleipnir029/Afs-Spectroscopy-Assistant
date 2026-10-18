"""Git provenance for pipeline runs (dulwich object API).

Each run becomes one commit on refs/heads/provenance (parent = previous provenance
commit) plus a tag-like ref refs/tags/run/<run_id>. Objects are written straight
into the object store, so the working tree, the index and the current branch are
never touched. A local copy is also written to runs/<run_id>/ (gitignored).
"""

from __future__ import annotations

import fcntl
import json
import threading
import time

from dulwich import porcelain
from dulwich.errors import NotGitRepository
from dulwich.object_store import iter_tree_contents
from dulwich.objects import Blob, Commit, Tree
from dulwich.repo import Repo

from afs_assistant import paths

PROVENANCE_REF = b"refs/heads/provenance"
AUTHOR = b"afs-assistant pipeline <pipeline@afs-assistant.local>"
# One provenance commit at a time: parallel runs would otherwise read the same parent and lose commits. The
# thread lock covers workers in one process; a flock on a file in the git dir covers parallel processes.
_RECORD_LOCK = threading.Lock()


def _tree(repo: Repo, files: dict[str, bytes]) -> bytes:
    """Build nested trees for {"dir/file": bytes}; returns the root tree id."""
    root: dict = {}
    for path, data in files.items():
        node = root
        parts = path.split("/")
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = data

    def write(node: dict) -> bytes:
        tree = Tree()
        for name, value in sorted(node.items()):
            if isinstance(value, dict):
                tree.add(name.encode(), 0o040000, write(value))
            else:
                blob = Blob.from_string(value)
                repo.object_store.add_object(blob)
                tree.add(name.encode(), 0o100644, blob.id)
        repo.object_store.add_object(tree)
        return tree.id

    return write(root)


def code_sha(repo_path=paths.ROOT) -> str:
    try:
        return Repo(str(repo_path)).head().decode()
    except (NotGitRepository, KeyError):
        return "unknown"


# Run results are written while a set runs; they are data, not code.
DIRTY_IGNORED = (b"outputs/",)


def code_dirty(repo_path=paths.ROOT) -> bool | None:
    """True if tracked files outside outputs/ differ from HEAD (staged or unstaged); None if not a repository.

    Read-only: untracked files are ignored and the index is not refreshed on disk.
    """
    try:
        st = porcelain.status(str(repo_path), untracked_files="no", optional_locks=False)
    except NotGitRepository:
        return None

    def counts(path) -> bool:
        raw = path if isinstance(path, bytes) else str(path).encode()
        return not raw.startswith(DIRTY_IGNORED)

    staged = [x for paths_ in st.staged.values() for x in paths_]
    return any(counts(x) for x in staged + list(st.unstaged))


def record(run_id: str, files: dict[str, str | bytes], message: str, repo_path=paths.ROOT) -> str:
    """Write files under runs/<run_id>/ locally and commit them on the provenance ref (thread-safe)."""
    lock_path = f"{Repo(str(repo_path)).controldir()}/afs-provenance.lock"
    with _RECORD_LOCK, open(lock_path, "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            return _record(run_id, files, message, repo_path)
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def _record(run_id: str, files: dict[str, str | bytes], message: str, repo_path) -> str:
    encoded = {k: v.encode("utf-8") if isinstance(v, str) else v for k, v in files.items()}
    local = paths.ROOT / "runs" / run_id if repo_path == paths.ROOT else repo_path / "runs" / run_id
    for name, data in encoded.items():
        target = local / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    repo = Repo(str(repo_path))
    try:
        parent = repo.refs[PROVENANCE_REF]
        parent_tree = repo[parent].tree
        existing = {}
        for entry in iter_tree_contents(repo.object_store, parent_tree):
            existing[entry.path.decode()] = repo[entry.sha].data
    except KeyError:
        parent, existing = None, {}
    for name, data in encoded.items():
        existing[f"runs/{run_id}/{name}"] = data

    commit = Commit()
    commit.tree = _tree(repo, existing)
    commit.parents = [parent] if parent else []
    commit.author = commit.committer = AUTHOR
    commit.author_time = commit.commit_time = int(time.time())
    commit.author_timezone = commit.commit_timezone = 0
    commit.encoding = b"UTF-8"
    commit.message = message.encode("utf-8")
    repo.object_store.add_object(commit)
    repo.refs[PROVENANCE_REF] = commit.id
    repo.refs[f"refs/tags/run/{run_id}".encode()] = commit.id
    return commit.id.decode()


def run_files(result_json: dict, markdown: str) -> dict[str, str]:
    m = result_json["manifest"]

    def dump(value) -> str:
        return json.dumps(value, indent=1, ensure_ascii=False)

    files = {
        "enquiry.txt": result_json["enquiry"] + "\n",
        "intake.json": dump(result_json["intake"]),
        "intake_removed.json": dump(result_json["intake_removed"]),
        "screening.json": dump(result_json["screening"]),
        "assessment_raw.json": dump(result_json["assessment_raw"]),
        "assessment.json": dump(result_json["assessment"]),
        "finalize.json": dump({"removed_citations": result_json["removed_citations"],
                               "finalize_changes": result_json["finalize_changes"],
                               "flagged": result_json["flagged"]}),
        "verification.json": dump(result_json["verification"]),
        "calls.json": dump(result_json["calls"]),
        "manifest.json": dump(m),
        "assessment.md": markdown,
    }
    if result_json.get("off_topic") is not None:      # stopped after the intake: nothing assessed
        for name in ("screening.json", "assessment_raw.json", "assessment.json", "finalize.json",
                     "verification.json"):
            del files[name]
        files["off_topic.json"] = dump(result_json["off_topic"])
    for rep in result_json["repairs"]:
        files[f"repair_round_{rep['round']}.json"] = dump(rep)
    if "external" in result_json:       # metadata, verified quotes and sha256 only; never fetched full text
        files["external.json"] = dump(result_json["external"])
    return files


def commit_message(result_json: dict) -> str:
    m = result_json["manifest"]
    v = m["verification"]
    verifier = ("not run (off-topic enquiry: stopped after the intake)" if v is None else
                f"{'pass' if v['passed'] else 'fail'} ({v['hard_failures']} hard, {v['soft_failures']} soft); "
                f"citations {v['citations_verified']}/{v['citations_total']}")
    return (f"run {m['run_id']}\n\n"
            f"Run-Id: {m['run_id']}\n"
            f"Models: {', '.join(m['models'])}\n"
            f"Code-SHA: {m.get('code_sha', 'unknown')}{' (dirty)' if m.get('code_dirty') else ''}\n"
            f"Prompt-SHA256-Assess: {m['prompt_sha256']['assess']}\n"
            f"Knowledge-SHA256: {m['knowledge_sha256']}\n"
            f"Verifier: {verifier}\n"
            f"Cost-USD: {m['cost_usd']}\n")
