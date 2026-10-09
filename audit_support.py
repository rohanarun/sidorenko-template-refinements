"""Model-derived active-support refinement; exact independent DP audit.

The existing original-baseline certificate determines the allowed pair graph.
This script reconstructs its edges from faces and cut bits, then exhausts all
vertex supports and relaxed defect-one dimensions. It does not certify the
upstream analytic argument that supplies the counting exponent.
"""
import argparse
from collections import defaultdict
from functools import lru_cache
from itertools import combinations
import json
from math import comb
from pathlib import Path


@lru_cache(None)
def dimension_dp(caps):
    """Maximum sum binomial(x_i,2) at each total, with 2 <= x_i <= cap_i."""
    values = {0: 0}
    for cap in caps:
        new = {}
        for total, value in values.items():
            for x in range(2, cap + 1):
                new[total + x] = max(new.get(total + x, -1), value + comb(x, 2))
        values = new
    return values


def greedy(caps, total):
    remaining = total - 2 * len(caps)
    assert remaining >= 0
    values = []
    for cap in caps:
        extra = min(remaining, cap - 2)
        values.append(2 + extra)
        remaining -= extra
    assert remaining == 0
    return sum(comb(x, 2) for x in values), values


def audit(baseline):
    faces, bits = baseline["faces"], baseline["bits"]
    incidence = defaultdict(list)
    for i, face in enumerate(faces):
        for edge in combinations(sorted(face), 2):
            incidence[edge].append(i)
    assert all(len(f) == 2 for f in incidence.values())
    allowed = sorted(edge for edge, (i, j) in incidence.items()
                     if sum(a != b for a, b in zip(bits[i], bits[j])) == 1)
    n = baseline["points"]
    m_all = len(allowed)
    all_caps = [2 * sum(i in edge for edge in allowed) for i in range(n)]
    coarse = m_all * m_all - 2 * m_all + sum(comb(c, 2) for c in all_caps)
    cases = 0
    best = None
    maximizing = []
    supports_tested = 0
    for mask in range(1 << n):
        vertices = [i for i in range(n) if mask & (1 << i)]
        edges = [e for e in allowed if all(mask & (1 << i) for i in e)]
        degree = {i: sum(i in edge for edge in edges) for i in vertices}
        if not edges or any(degree[i] == 0 for i in vertices):
            continue
        supports_tested += 1
        m = len(edges)
        for k in range(2, 2 * m):
            caps = tuple(sorted((min(k, 2 * degree[i]) for i in vertices), reverse=True))
            total = 2 * k + 1
            if not 2 * len(vertices) <= total <= sum(caps):
                continue
            local, dims = greedy(caps, total)
            # A separate convolution computes the integer maximum; it does not
            # assume that the greedy/majorization argument is correct.
            assert dimension_dp(caps)[total] == local
            remainder = -k * k + 2 * m * k - 2 * m + local
            cases += 1
            record = {"support_mask": mask, "vertices": vertices, "edge_upper_bound": m,
                      "span": k, "caps": list(caps), "relaxed_local_dimensions": dims,
                      "local_binomial_sum": local, "remainder": remainder}
            if best is None or remainder > best:
                best, maximizing = remainder, [record]
            elif remainder == best:
                maximizing.append(record)
    assert coarse <= 2 * best
    return {"allowed_edges": [list(e) for e in allowed], "coarse_remainder": coarse,
            "all_support_masks": 1 << n, "supports_without_isolates": supports_tested,
            "relaxed_defect_one_cases": cases, "refined_remainder": best,
            "maximizers": maximizing, "independent_dp_checks_passed": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=Path(__file__).parent / "experiments/original-baseline.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(json.loads(args.baseline.read_text()))
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("refined_remainder", "relaxed_defect_one_cases", "independent_dp_checks_passed")}, indent=2))
