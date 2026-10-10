"""Model-derived sequential-basis refinement; exact independent audit.

The nondirect residual count is redone one basis vector at a time, as in the
original direct-case argument.  Each vector is orthogonal to both endpoint
spans, which cancels the containment cross terms, and the defect counts the
vectors that raise a local span without raising the global span.  This script
reconstructs the allowed pair graph from the saved original faces and cut bits
and exhausts the relaxed strata of that bound.  It does not certify the
upstream analytic argument that supplies the counting exponent.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
import json
from math import comb
from pathlib import Path


def phi(degree, x):
    """Bound on the sum of earlier local dimensions seen at a vertex of the
    given active degree whose final local dimension is x."""
    return comb(x, 2) + (2 * degree - x) * x


@lru_cache(None)
def phi_dp(items):
    """items: tuple of (degree, cap).  Max sum phi over totals, 2 <= x <= cap."""
    values = {0: 0}
    for degree, cap in items:
        new = {}
        for total, value in values.items():
            for x in range(2, cap + 1):
                new[total + x] = max(new.get(total + x, -1), value + phi(degree, x))
        values = new
    return values


def phi_greedy(items, total):
    """Concave allocation: start at two, add units by largest marginal gain.
    Independent of the convolution; ties are broken arbitrarily and do not
    affect the value because each marginal sequence is nonincreasing."""
    xs = [2] * len(items)
    remaining = total - 2 * len(items)
    assert remaining >= 0
    while remaining:
        best = None
        for t, (degree, cap) in enumerate(items):
            if xs[t] < cap:
                gain = phi(degree, xs[t] + 1) - phi(degree, xs[t])
                if best is None or gain > best[0]:
                    best = (gain, t)
        assert best is not None
        xs[best[1]] += 1
        remaining -= 1
    return sum(phi(d, x) for (d, _), x in zip(items, xs))


def connected(vertices, edges):
    seen = {vertices[0]}
    frontier = [vertices[0]]
    while frontier:
        v = frontier.pop()
        for a, b in edges:
            for x, y in ((a, b), (b, a)):
                if x == v and y not in seen:
                    seen.add(y)
                    frontier.append(y)
    return seen == set(vertices)


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
    degree_all = [sum(i in edge for edge in allowed) for i in range(n)]
    assert connected(list(range(n)), allowed)

    # Per-vertex concavity bound and its maximizers.
    for degree in set(degree_all):
        peak = degree * (2 * degree - 1)
        for x in range(0, 2 * degree + 1):
            assert phi(degree, x) <= peak
            assert (phi(degree, x) == peak) == (x in (2 * degree - 1, 2 * degree))
    vertex_total = sum(d * (2 * d - 1) for d in degree_all)
    base = Q(vertex_total, 2) - 2 * m_all
    assert base == sum(d * d for d in degree_all) - 3 * m_all
    # Adding an edge whose endpoints have degrees a, b changes
    # sum(deg^2) - 3m by 2a + 2b - 1; the full connected graph maximizes it.
    for (a, b) in allowed:
        assert 2 * degree_all[a] + 2 * degree_all[b] - 1 > 0
    excess = max(2 * degree_all[a] + 2 * degree_all[b] - 1 for a, b in allowed)
    closed_form = int(base + Q(excess, 2))

    # Exhaust relaxed defect-one strata over all supports and spans.
    best = None
    maximizers = []
    cases = 0
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
            items = tuple(sorted(((degree[i], min(k, 2 * degree[i])) for i in vertices), reverse=True))
            total = 2 * k + 1
            if not 2 * len(vertices) <= total <= sum(cap for _, cap in items):
                continue
            table = phi_dp(items)
            local = table[total]
            assert phi_greedy(items, total) == local
            # The defect vector lies at one active pair; its endpoints see at
            # most k_i + k_j - 1 earlier local dimensions.
            pair_excess = max(min(k, 2 * degree[a]) + min(k, 2 * degree[b]) - 1 for a, b in edges)
            remainder = int(Q(local + pair_excess, 2)) - 2 * m
            cases += 1
            record = {"support_mask": mask, "vertices": vertices, "active_pairs": m, "span": k,
                      "local_phi_sum": local, "pair_excess": pair_excess, "remainder": remainder}
            if best is None or remainder > best:
                best, maximizers = remainder, [record]
            elif remainder == best:
                maximizers.append(record)
    assert best == closed_form

    # Defects at least two: each defect unit costs at most (k + 11) when the
    # vector is new at both endpoints and at most excess/2 otherwise.
    ratio = Q(0)
    for d in range(2, 4 * m_all + 1):
        for two in range(0, d // 2 + 1):
            one = d - 2 * two
            for k in range(2, 2 * m_all):
                value = base + Q(excess, 2) * one + (k + Q(excess - 1, 2)) * two
                ratio = max(ratio, value / d)
    assert ratio <= best
    return {"allowed_edges": [list(e) for e in allowed], "allowed_degrees": degree_all,
            "vertex_bound_sum": vertex_total, "base_remainder": str(base), "pair_excess_max": excess,
            "closed_form_remainder": closed_form, "all_support_masks": 1 << n,
            "supports_without_isolates": supports_tested, "relaxed_defect_one_cases": cases,
            "refined_remainder": best, "maximizers": maximizers,
            "higher_defect_ratio_max": str(ratio), "independent_greedy_checks_passed": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=Path(__file__).parent / "experiments/original-baseline.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(json.loads(args.baseline.read_text()))
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("closed_form_remainder", "refined_remainder",
                                             "relaxed_defect_one_cases", "higher_defect_ratio_max")}, indent=2))
