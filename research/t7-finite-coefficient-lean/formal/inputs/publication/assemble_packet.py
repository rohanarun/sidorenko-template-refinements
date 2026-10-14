"""Assemble local inert proof/evidence copies; never execute producer code.

Independently authored stdlib packaging script. Outputs are exclusive unless
already byte-identical, so a rerun cannot silently replace a prepared packet.
The theorem and final reviews are added after their exact wording is checked.
"""
from pathlib import Path
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEST = HERE / "proposed" / "experiments" / "t7-orbit"


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f"Refusing changed existing output: {path}")
        return
    temp = path.with_name(path.name + ".partial")
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


copies = [
    ("source-artifacts/l3-manuscript-transfer-20261010/template_transfer_proof.md",
     "dependencies/l3-template-transfer-proof.md",
     "2d286841535e86965dd1af937a85c65ae11ed73281184636ccc5375b3526cba4"),
    ("source-artifacts/round2-unindexed-20261011/task-04/files/orbit_transfer/orbit_transfer_theorem.md",
     "dependencies/task04-orbit-transfer-theorem.md",
     "9afd06cf6911763965e15b57a83805828c0c680e9a88ae2942a4bb63ef346362"),
    ("source-artifacts/round2-unindexed-20261011/task-11/round2-11-response.md",
     "dependencies/task11-response.md",
     "87944a5c592d904a1b79855e5bfc99d26a82e7cc07ec5f178daaec8743755914"),
    ("upstream/round2-independent-20261011/orbit-transfer/checks/check_t7.py",
     "checks/check_t7.py",
     "66e4b0490ac03e727019f1047e14a09bbfca4bf0d440e090238c5d793454919f"),
    ("upstream/round2-independent-20261011/orbit-transfer/inputs/t7-literals.json",
     "inputs/t7-literals.json",
     "583719581922454280d360875e7cb0ef0178477a5084a8b222da86744e0c7f7e"),
    ("upstream/round2-independent-20261011/orbit-transfer/checks/result.json",
     "evidence/original-result.json",
     "4bb7495f02e996b412cb3dc8e87d6cb974dbfc0c9e3c440bdaefebb948710710"),
    ("upstream/round2-independent-20261011/orbit-transfer/checks/execution-receipt.json",
     "evidence/original-execution-receipt.json",
     "af76dd63ea0b5f1680805b9311fa9fa97a3b7616c55f214a57e9180c627253fd"),
    ("upstream/round2-independent-20261011/orbit-transfer/INTEGRATION.txt",
     "reviews/integration.txt",
     "6e36dc193585633e5d1412db034fab0f8bc09dfadb153542089c8c47e2b61b43"),
    ("upstream/round2-independent-20261011/orbit-transfer-challenge/REVIEW.txt",
     "reviews/t7-specialization-challenge.txt",
     "750fdb190a57d9e23328ac0a4d29781cec3e3841646a53368c36b34f24febf29"),
    ("upstream/sidorenko/L3-manuscript-local-review.txt",
     "reviews/l3-local-review.txt",
     "a4305456c861bb646708ae813a9752a196a8d99e4104335bcf0c6632a1311fa5"),
    ("upstream/sidorenko/L3-manuscript-tail-review.txt",
     "reviews/l3-tail-review.txt",
     "2213a713bf2e8c247bda4a7a14c0eb2661dc6bcb6ba5edf1ba506507156e4eca"),
    ("upstream/sidorenko/L3-manuscript-global-review.txt",
     "reviews/l3-global-review.txt",
     "a8c7463b12b830afbe81d877a75e1804b32dbeed3a0417e567837ecfda43e57f"),
    ("upstream/sidorenko/t7-publication/source-comparison/REVIEW.txt",
     "reviews/source-comparison.txt",
     "e26587679421730a5e483aab13fc4d42848ccd441367a7f125fc1bcb71d8b9b9"),
]
for name in ("TASK04-REVIEW.txt", "TASK11-REVIEW.txt", "source-pins.json"):
    source = "upstream/round2-independent-20261011/orbit-transfer/" + name
    copies.append((source, "reviews/" + name, None))
for source, target in [
    ("review/BOUNDARY-REVIEW.txt", "reviews/acceptance-boundary.txt"),
    ("PUBLIC-NOVELTY-BOUNDARY.txt", "reviews/public-novelty-boundary.txt"),
]:
    copies.append((str((HERE / source).relative_to(ROOT)), target, None))

records = []
for source, target, expected in copies:
    data = (ROOT / source).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if expected is not None and digest != expected:
        raise RuntimeError(f"Source mutation: {source}")
    put(DEST / target, data)
    records.append({"original_workspace_path": source, "path": target,
                    "bytes": len(data), "sha256": digest,
                    "copied_without_modification": True})
put(DEST / "SOURCE-MANIFEST.json", (json.dumps({
    "schema_version": 1,
    "scope": "Exact inert source proofs, independent checker, literal inputs and historical reviews.",
    "files": records,
    "source_program_execution": False,
    "classification_archive_included": False,
    "note": "Original workspace paths in historical reviews are custody references, not portable dependencies. This manifest maps included exact bytes to portable paths."
}, indent=2) + "\n").encode())
print(json.dumps({"copied_files": len(records), "bytes": sum(x["bytes"] for x in records),
                  "portable_directory": str(DEST.relative_to(ROOT))}))
