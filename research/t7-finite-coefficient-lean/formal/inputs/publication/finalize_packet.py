"""Freeze and validate the prepared local T7 proposal; no remote operations.

This packaging script reads inert manuscripts/reviews, applies a generated
text patch in an isolated empty test directory, and compares exact bytes.
It neither runs mathematical source programs nor changes source worktrees.
"""
from pathlib import Path
import datetime
import difflib
import hashlib
import json
import os
import re
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TREE = HERE / "proposed"
BASE = "d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d"
OBJECTS = ROOT / "source-mirrors/sidorenko-template-refinements/objects.git"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(obj):
    return (json.dumps(obj, indent=2) + "\n").encode()


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f"Refusing changed output {path}")
        return
    temp = path.with_name(path.name + ".partial")
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


copies = [
    ("theorem.md", "t7-orbit-theorem.md"),
    ("DEPENDENCIES.txt", "experiments/t7-orbit/DEPENDENCIES.txt"),
    ("review/DRAFT-REVIEW.txt", "experiments/t7-orbit/reviews/exact-draft-review.txt"),
]
for name in ("REVIEW.md", "check_graph.py", "finite-receipt.json", "source-pins.json", "output-sha256.txt"):
    copies.append(("review/positive-class-screen/" + name,
                   "experiments/t7-orbit/reviews/positive-class-screen/" + name))
for src, dst in copies:
    put(TREE / dst, (HERE / src).read_bytes())

assert digest((HERE / "theorem.md").read_bytes()) == "a4996ac29fdc54e31f7ebb25bffe233fe4f4caa164d557ad9e7dd7fbd89fb960"
source_manifest = json.loads((TREE / "experiments/t7-orbit/SOURCE-MANIFEST.json").read_bytes())
for rec in source_manifest["files"]:
    p = TREE / "experiments/t7-orbit" / rec["path"]
    blob = p.read_bytes()
    assert len(blob) == rec["bytes"] and digest(blob) == rec["sha256"]
    assert blob == (ROOT / rec["original_workspace_path"]).read_bytes()

# Publication prose uses portable local links. Historical dependency and review
# source text deliberately preserves its original custody/link references.
listing = subprocess.run(["git", "--git-dir", str(OBJECTS), "ls-tree", "-r", "--name-only", BASE],
                         check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10).stdout.decode().splitlines()
link_checks = []
for name in ("README.md", "t7-orbit-theorem.md", "experiments/t7-orbit/README.md"):
    path = TREE / name
    for link in re.findall(r"\]\(([^\n)]+)\)", path.read_text()):
        if re.match(r"[a-z]+://", link) or link.startswith("#"):
            continue
        dest = (path.parent / link.split("#", 1)[0]).resolve()
        assert dest.is_relative_to(TREE.resolve()), (name, link)
        relative = str(dest.relative_to(TREE.resolve()))
        in_base = relative in listing or any(x.startswith(relative + "/") for x in listing)
        assert dest.is_file() or in_base, (name, link)
        link_checks.append({"from": name, "to": link,
                            "target": "proposed file" if dest.is_file() else "unchanged base repository"})

entries = []
for path in sorted(TREE.rglob("*")):
    if path.is_file():
        data = path.read_bytes()
        entries.append({"path": str(path.relative_to(TREE)), "bytes": len(data), "sha256": digest(data)})
put(HERE / "PROPOSED-MANIFEST.json", encoded({"base_commit": BASE, "files": entries}))

assert all(rec["path"] not in listing for rec in entries if rec["path"] != "README.md")
base_readme = subprocess.run(["git", "--git-dir", str(OBJECTS), "show", BASE + ":README.md"],
                             check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10).stdout
assert base_readme == (HERE / "validation/base-README.md").read_bytes()

chunks = []
for rec in entries:
    name = rec["path"]
    old = base_readme if name == "README.md" else b""
    new = (TREE / name).read_bytes()
    if old == new:
        raise RuntimeError("Unexpected unchanged proposed file")
    chunks.append(f"diff --git a/{name} b/{name}\n")
    if name != "README.md":
        chunks.append("new file mode 100644\n")
    for line in difflib.unified_diff(old.decode().splitlines(keepends=True),
                                    new.decode().splitlines(keepends=True),
                                    fromfile="a/" + name if old else "/dev/null",
                                    tofile="b/" + name):
        chunks.append(line)
        if not line.endswith("\n"):
            chunks.append("\n\\ No newline at end of file\n")
patch = "".join(chunks).encode()
put(HERE / "proposed.patch", patch)
with tempfile.TemporaryDirectory(prefix="t7-patch-", dir=HERE / "validation") as name:
    sandbox = Path(name)
    (sandbox / "README.md").write_bytes(base_readme)
    for args in (["--check"], []):
        subprocess.run(["git", "apply", "--whitespace=nowarn", *args, str(HERE / "proposed.patch")],
                       cwd=sandbox, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    assert sorted(str(p.relative_to(sandbox)) for p in sandbox.rglob("*") if p.is_file()) == sorted(x["path"] for x in entries)
    for rec in entries:
        assert (sandbox / rec["path"]).read_bytes() == (TREE / rec["path"]).read_bytes()

receipt = json.loads((HERE / "validation/portable-check-receipt.json").read_bytes())
assert receipt["status"] == "PASS" and receipt["stdout_matches_original_exactly"]
validation = {"status": "PASS", "base_commit": BASE, "patch_apply_check": True,
              "applied_file_bytes_equal_proposal": True, "files": len(entries),
              "copied_source_records_rehashed": len(source_manifest["files"]),
              "publication_prose_links_checked": link_checks,
              "finite_packaging_replay": receipt,
              "root_theorem_review": "Complete finite conditional proof read; no new finite-side defect found. Generic L3 analytics remain explicit supplied proof dependencies.",
              "no_source_worktree_changed": True, "no_remote_write": True,
              "no_formal_or_independent_human_validation": True}
put(HERE / "validation/packet-validation.json", encoded(validation))

archive = HERE / "t7-publication-packet.zip"
put(HERE / "ARCHIVE-README.txt", (
    "Focused local T7 review proposal; not published.\n"
    "Apply proposed.patch to rohanarun/sidorenko-template-refinements at " + BASE + ".\n"
    "proposed/ contains the changed files, not the unchanged full base repository.\n"
    "Read proposed/t7-orbit-theorem.md and proposed/experiments/t7-orbit/DEPENDENCIES.txt.\n"
    "The theorem is RL-conditional; the separate proposed unconditional corollary retains all supplied L3 analytics.\n"
    "PROPOSED-MANIFEST.json pins every changed file; validation/packet-validation.json records the checks.\n"
    "proposed-pr-title.txt and proposed-pr-body.md are drafts only. No external write was performed.\n"
).encode())
archive_files = [HERE / "PROPOSED-MANIFEST.json", HERE / "proposed.patch",
                 HERE / "ARCHIVE-README.txt",
                 HERE / "proposed-pr-title.txt", HERE / "proposed-pr-body.md",
                 HERE / "validation/packet-validation.json"]
archive_files += [TREE / rec["path"] for rec in entries]
if archive.exists():
    raise RuntimeError("Archive already frozen")
temporary = archive.with_suffix(".partial")
with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
    for path in sorted(archive_files):
        info = zipfile.ZipInfo(str(path.relative_to(HERE)), (2026, 10, 11, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        output.writestr(info, path.read_bytes())
os.replace(temporary, archive)
with zipfile.ZipFile(archive) as check:
    assert check.testzip() is None
    for path in archive_files:
        assert check.read(str(path.relative_to(HERE))) == path.read_bytes()

def pin(path):
    blob = path.read_bytes()
    return {"path": str(path.relative_to(HERE)), "bytes": len(blob), "sha256": digest(blob)}

delivery = {"status": "prepared_local_not_published", "base_commit": BASE,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "archive": pin(archive), "patch": pin(HERE / "proposed.patch"),
            "manifest": pin(HERE / "PROPOSED-MANIFEST.json"),
            "theorem": pin(HERE / "theorem.md"), "dependencies": pin(HERE / "DEPENDENCIES.txt"),
            "draft_review": pin(HERE / "review/DRAFT-REVIEW.txt"),
            "validation": pin(HERE / "validation/packet-validation.json"),
            "publication_files": len(entries), "publication_bytes": sum(x["bytes"] for x in entries),
            "claim_boundary": "Exact RL-conditional theorem; proposed source-dependent unconditional corollary if complete L3 analytics accepted. Finite arithmetic, proof review and publication are separate.",
            "unverified_census_included_as_evidence": False,
            "external_publication_authorized_by_prior_three_draft_approval": False,
            "remote_write": False}
put(HERE / "DELIVERY.json", encoded(delivery))
for path in [TREE / rec["path"] for rec in entries] + archive_files + [archive, HERE / "DELIVERY.json"]:
    path.chmod(0o444)
print(json.dumps(delivery, indent=2))
