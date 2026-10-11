"""Bounded driver for the fully reviewed PR3 overlap DP; no publication action.

This file is a proposed local replay entrypoint, pending root source review.
The supplied audit module is hash-pinned and its CLI is never invoked.
"""
import hashlib
import json
from pathlib import Path
import runpy
import sys

PINS = {
    "audit_overlap.py": "ea039289878ed689fd4746f2710d8427c3355a970b2a42facd0c675e64b9a09f",
    "original-baseline.json": "5644bdbe73a51cf4aa2bc52ff1f0492263bae1785948bd9f359291453095d916",
    "overlap-expected.json": "903cddaa07d67f8787c4b629fed0a1d4549d19f4f6b230c6b135b8399ef66a04",
}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def verify_files(root):
    for name, expected in PINS.items():
        require(hashlib.sha256((root / name).read_bytes()).hexdigest() == expected,
                "Unreviewed or mutated bytes: " + name)


def main():
    require(__debug__, "Assertions must be enabled")
    require(len(sys.argv) == 2 and sys.argv[1] in ("5", "26"), "Only cap5/cap26 are reviewed")
    cap = int(sys.argv[1])
    root = Path(__file__).resolve().parent
    verify_files(root)
    baseline = json.loads((root / "original-baseline.json").read_bytes())
    producer = json.loads((root / "overlap-expected.json").read_bytes())
    ns = runpy.run_path(str(root / "audit_overlap.py"), run_name="_reviewed_overlap")
    pairs = ns["allowed_pairs"](baseline)
    order = ns["star_order"](pairs, ns["VERTEX_SEQUENCE"])
    require([list(e) for e in pairs] == producer["allowed_pairs"], "Allowed-pair mismatch")
    require([list(e) for e in order] == producer["pair_order"], "Order mismatch")
    require(len(pairs) == 28 and baseline["points"] == 13, "Wrong finite graph")
    best, max_states = ns["run_dp"](order, baseline["points"], cap)
    expected = {d: producer["best_remainder_by_defect"][str(d)] for d in range(1, cap + 1)}
    require(best == expected, "Fresh DP maxima differ from saved prefix")
    require(all(best[d] + 28 <= 33 * d for d in range(1, cap + 1)), "Proposed corrected finite bound fails")
    verify_files(root)
    print(json.dumps({
        "driver_version": "pr3-reviewed-cap-driver-1.0",
        "source_sha256": PINS["audit_overlap.py"],
        "baseline_sha256": PINS["original-baseline.json"],
        "producer_expected_sha256": PINS["overlap-expected.json"],
        "max_defect": cap,
        "best_remainder_by_defect": {str(d): best[d] for d in sorted(best)},
        "max_dp_states_after_forgetting": max_states,
        "saved_table_prefix_matches": True,
        "repaired_bound_33d_for_replayed_defects": True,
        "support_uniform_claim_verified_by_this_run": False,
        "scope": "Full-support relaxed DP through the stated defect cap only; support completion and analytic counting need their separate proofs.",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
