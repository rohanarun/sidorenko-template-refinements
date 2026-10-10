"""Model-derived overlap refinement of the sequential count; exact DP audit.

The sequential basis count bounds the nondirect remainder by -2m plus the
overlap of the two endpoint spans at every non-defect basis vector, plus the
defect terms.  The overlap at a pair is at most the number of earlier
globally dependent vectors at neighbouring pairs that nevertheless raised
the local span at the shared point (plus one for a second vector whose
partner was independent).  For a fixed order of the active pairs this script
exhausts every assignment of vector types by dynamic programming over those
per-point counts, keeping only the defect counts as further state.  Every
other consistency condition is dropped, which only enlarges the adversary's
choices, so the maximum found is an upper bound.  It does not certify the
upstream analytic argument that supplies the counting exponent.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path

VERTEX_SEQUENCE = [2, 1, 4, 3, 0, 9, 11, 10, 7, 6, 12, 8, 5]
MAX_TRACKED_DEFECT = 38


def allowed_pairs(baseline):
    faces, bits = baseline["faces"], baseline["bits"]
    incidence = defaultdict(list)
    for i, face in enumerate(faces):
        for edge in combinations(sorted(face), 2):
            incidence[edge].append(i)
    assert all(len(f) == 2 for f in incidence.values())
    return sorted(edge for edge, (i, j) in incidence.items()
                  if sum(a != b for a, b in zip(bits[i], bits[j])) == 1)


def star_order(pairs, sequence):
    pos = {v: t for t, v in enumerate(sequence)}
    return sorted(pairs, key=lambda e: (max(pos[e[0]], pos[e[1]]), min(pos[e[0]], pos[e[1]])))


def run_dp(order, n, max_defect):
    """Return the maximum relaxed remainder for each defect 1..max_defect."""
    vectors = [(e, s) for e in order for s in (0, 1)]
    m = len(order)
    last_use = {}
    for x, (e, _) in enumerate(vectors):
        for a in e:
            last_use[a] = x
    seen = {a: 0 for a in range(n)}          # N_a: earlier vectors at a
    live = []                                 # open points, in state-tuple order
    # state: (T-tuple, g of the previous vector, defect so far) -> best partial sum
    states = {((), 1, 0): 0}
    max_states = 0
    for x, ((i, j), second) in enumerate(vectors):
        for a in (i, j):
            if a not in live:
                live.append(a)
                states = {(T + (0,), g, d): v for (T, g, d), v in states.items()}
        pi_, pj_ = live.index(i), live.index(j)
        Ni, Nj = seen[i], seen[j]
        new = {}
        def push(key, value):
            if new.get(key, -1) < value:
                new[key] = value
        for (T, lastg, d), value in states.items():
            Ti, Tj = T[pi_], T[pj_]
            cap = Ti + Tj + (lastg if second else 0)
            term = min(Ni, Nj, cap)
            push((T, 1, d), value + term)                   # independent everywhere
            push((T, 0, d), value + term)                   # inside both endpoint spans
            if d + 1 <= max_defect:                         # inside one span, new at the other
                for side in (pi_, pj_):
                    T2 = list(T); T2[side] += 1
                    push((tuple(T2), 0, d + 1), value + Ni + Nj)
            if d + 2 <= max_defect:                         # inside the global span, new at both
                # at least ceil(d/2) earlier defect vectors are dependent, so w' <= x - ceil(d/2)
                T2 = list(T); T2[pi_] += 1; T2[pj_] += 1
                push((tuple(T2), 0, d + 2), value + (x - (d + 1) // 2) + Ni + Nj)
        states = new
        seen[i] += 1; seen[j] += 1
        for a in (i, j):
            if last_use[a] == x:
                k = live.index(a)
                live.pop(k)
                merged = {}
                for (T, g, d), v in states.items():
                    key = (T[:k] + T[k + 1:], g, d)
                    if merged.get(key, -1) < v:
                        merged[key] = v
                states = merged
        max_states = max(max_states, len(states))
    best = {}
    for (T, g, d), v in states.items():
        if d >= 1:
            best[d] = max(best.get(d, -10**9), v - 2 * m)
    return best, max_states


def tail_bound(pairs, n, d):
    """Averaging bound for defect d: R <= 178 + (23/2) n1 + (11 + 56 - n1 - n2) n2."""
    m = len(pairs)
    degrees = [sum(a in e for e in pairs) for a in range(n)]
    base = sum(x * x for x in degrees) - 3 * m
    excess = max(2 * degrees[a] + 2 * degrees[b] - 1 for a, b in pairs)
    best = None
    for n2 in range(0, d // 2 + 1):
        n1 = d - 2 * n2
        value = base + Q(excess, 2) * n1 + (Q(excess - 1, 2) + 2 * m - n1 - n2) * n2
        best = value if best is None else max(best, value)
    return best


def audit(baseline):
    pairs = allowed_pairs(baseline)
    n = baseline["points"]
    m = len(pairs)
    order = star_order(pairs, VERTEX_SEQUENCE)
    assert sorted(order) == pairs
    best, max_states = run_dp(order, n, MAX_TRACKED_DEFECT)
    ratios = {d: Q(best[d], d) for d in best}
    tracked = max(ratios.values())
    tail = max(tail_bound(pairs, n, d) / d for d in range(MAX_TRACKED_DEFECT + 1, 4 * m + 1))
    constant = max(tracked, tail)
    return {"allowed_pairs": [list(e) for e in pairs], "vertex_sequence": VERTEX_SEQUENCE,
            "pair_order": [list(e) for e in order], "max_tracked_defect": MAX_TRACKED_DEFECT,
            "best_remainder_by_defect": {str(d): best[d] for d in sorted(best)},
            "best_ratio_by_defect": {str(d): str(ratios[d]) for d in sorted(ratios)},
            "tracked_ratio_max": str(tracked), "untracked_defect_ratio_max": str(tail),
            "refined_constant": str(constant), "max_dp_states": max_states}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=Path(__file__).parent / "experiments/original-baseline.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(json.loads(args.baseline.read_text()))
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("best_remainder_by_defect", "tracked_ratio_max",
                                             "untracked_defect_ratio_max", "refined_constant", "max_dp_states")}, indent=2))
