#!/usr/bin/env python3
"""Independent, bounded stdlib replay of literal T7 structural facts; v1.

This checker does not import or execute producer code. It does not evaluate
homomorphism densities or decide Sidorenko's property. Output is a JSON receipt.
"""
import hashlib
import itertools
import json
import platform
import resource
import sys
import time
from pathlib import Path

START = time.perf_counter()
HERE = Path(__file__).resolve().parent
FACES = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 4),
         (1, 3, 4), (2, 3, 5), (2, 4, 5), (3, 4, 6),
         (3, 5, 6), (4, 5, 6))
POINTS = tuple(range(7))
VERTICES = tuple(range(17))
EDGES = {(p, 7 + j) for j, f in enumerate(FACES) for p in f}
ADJ = {v: set() for v in VERTICES}
for a, b in EDGES:
    ADJ[a].add(b)
    ADJ[b].add(a)


def connected(vertices):
    vertices = set(vertices)
    if not vertices:
        return False
    todo = [next(iter(vertices))]
    seen = set(todo)
    while todo:
        for v in ADJ[todo.pop()] & vertices - seen:
            seen.add(v)
            todo.append(v)
    return seen == vertices


face_set = set(FACES)
assert len(EDGES) == 30 and connected(VERTICES)
degrees = [len(ADJ[p]) for p in POINTS]
assert degrees == [3, 4, 5, 6, 5, 4, 3]
assert all(len(ADJ[f]) == 3 for f in range(7, 17))

stellar = set(itertools.combinations(range(4), 3))
stellar_steps = []
for old, new in [((1, 2, 3), 4), ((2, 3, 4), 5), ((3, 4, 5), 6)]:
    assert old in stellar
    stellar.remove(old)
    added = [tuple(sorted((*pair, new))) for pair in itertools.combinations(old, 2)]
    stellar.update(added)
    stellar_steps.append({"removed_face": old, "inserted_point": new, "added_faces": added})
assert stellar == face_set

point_codegrees = {pair: len(ADJ[pair[0]] & ADJ[pair[1]])
                   for pair in itertools.combinations(POINTS, 2)}
face_codegrees = {pair: len(ADJ[pair[0]] & ADJ[pair[1]])
                  for pair in itertools.combinations(range(7, 17), 2)}
assert max(point_codegrees.values()) == max(face_codegrees.values()) == 2
tetrahedra = [q for q in itertools.combinations(POINTS, 4)
              if set(itertools.combinations(q, 3)) <= face_set]
assert tetrahedra == []
squares = []
for a, b in itertools.combinations(POINTS, 2):
    common = sorted(ADJ[a] & ADJ[b])
    if len(common) == 2:
        squares.append(frozenset((a, b, *common)))
assert len(squares) == 15
intersection_stats = {}
for first, second in itertools.combinations(squares, 2):
    overlap = first & second
    induced_edges = sum(a in overlap and b in overlap for a, b in EDGES)
    key = f"vertices={len(overlap)},edges={induced_edges}"
    intersection_stats[key] = intersection_stats.get(key, 0) + 1
    assert (len(overlap), induced_edges) in ((0, 0), (1, 0), (2, 1))

automorphisms = []
for perm in itertools.permutations(POINTS):
    if {tuple(sorted(perm[x] for x in f)) for f in FACES} == face_set:
        automorphisms.append(perm)
assert automorphisms == [POINTS, tuple(reversed(POINTS))]
reverse = tuple(reversed(POINTS))
fixed_points = [p for p in POINTS if reverse[p] == p]
fixed_faces = [f for f in FACES if tuple(sorted(reverse[p] for p in f)) == f]
assert fixed_points == [3] and fixed_faces == []
assert connected(set(VERTICES) - {3})

receipt = {
    "checker_version": "t7-positive-class-structural-screen-v1",
    "scope": "Independent standalone finite structural replay; not an auditable-runner receipt, not a Sidorenko-density test, not a complete decomposition search.",
    "supplied_code_executed": False,
    "input": {"points": POINTS, "faces": FACES, "source": "literal task specification"},
    "graph": {"vertices": 17, "edges": 30, "point_degrees": degrees, "face_degrees": [3] * 10},
    "stellar_steps": stellar_steps,
    "max_point_codegree": max(point_codegrees.values()),
    "max_face_codegree": max(face_codegrees.values()),
    "tetrahedron_face_sets": tetrahedra,
    "square_count": len(squares),
    "square_pair_intersections": intersection_stats,
    "point_automorphisms": automorphisms,
    "nonidentity_fixed_points": fixed_points,
    "nonidentity_fixed_faces": fixed_faces,
    "connected_after_removing_point3": True,
    "tree_arrangement_incidence_obstructions": {
        "tree_on_points": {"required": 20, "maximum_available": 12},
        "tree_on_faces": {"required": 23, "maximum_available": 18},
    },
    "enumeration_sizes": {"point_permutations": 5040, "point_quadruples": 35, "square_pairs": 105},
    "runtime": {"python": sys.version, "platform": platform.platform(),
                "elapsed_seconds": time.perf_counter() - START,
                "maxrss_raw": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "maxrss_unit": "bytes on macOS; KiB on Linux"},
    "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "result": "PASS: every asserted finite structural fact holds",
}
(HERE / "finite-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"result": receipt["result"], "elapsed_seconds": receipt["runtime"]["elapsed_seconds"],
                  "maxrss_raw": receipt["runtime"]["maxrss_raw"], "receipt": str(HERE / "finite-receipt.json")}))
