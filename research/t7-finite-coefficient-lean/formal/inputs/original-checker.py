"""Independent exact finite witness check, authored in the review lane.

Only JSON literal data are loaded. No producer program is imported.
This does not certify the rank-layer limit or the unavailable full census.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "inputs/t7-literals.json"
EXPECTED = "583719581922454280d360875e7cb0ef0178477a5084a8b222da86744e0c7f7e"
assert hashlib.sha256(INPUT.read_bytes()).hexdigest() == EXPECTED
data = json.loads(INPUT.read_text())
faces = [frozenset(x) for x in data["faces"]]
n, f = 7, len(faces)

def graph_of_faces(n, faces):
    adj = [set() for _ in range(n + len(faces))]
    for j, face in enumerate(faces):
        for i in face:
            adj[i].add(n+j)
            adj[n+j].add(i)
    return adj

def refine(n, adj):
    colors = [int(v >= n) for v in range(len(adj))]
    sizes = [len(set(colors))]
    for _ in range(len(adj)):
        signatures = [(colors[u], tuple(sorted(colors[v] for v in adj[u])))
                      for u in range(len(adj))]
        names = {x: i for i, x in enumerate(sorted(set(signatures)))}
        new = [names[x] for x in signatures]
        sizes.append(len(set(new)))
        if len(set(new)) == len(set(colors)):
            return new, sizes
        colors = new
    raise ValueError("refinement did not stabilize")

inc = {}
for j, face in enumerate(faces):
    for e in combinations(sorted(face), 2):
        inc.setdefault(e, []).append(j)
assert len(inc) == 15 and all(len(js) == 2 for js in inc.values())
assert set(inc) == {(i, j) for i in range(n) for j in range(i+1, n) if j-i <= 3}
stellar = {frozenset(x) for x in combinations(range(4), 3)}
for v, face in [(4, (1,2,3)), (5, (2,3,4)), (6, (3,4,5))]:
    assert frozenset(face) in stellar
    stellar.remove(frozenset(face))
    stellar.update(frozenset((*e, v)) for e in combinations(face, 2))
assert stellar == set(faces)
coverage = Counter()
for cycle, sides in zip(data["cycles"], data["exposures"]):
    assert sorted(cycle) == list(range(n))
    edges = {tuple(sorted((cycle[t], cycle[(t+1) % n]))) for t in range(n)}
    assert edges <= set(inc) and len(edges) == n
    coverage.update(edges)
    assert sorted(sides[0]+sides[1]) == list(range(f))
    for side in sides:
        seen, old_edges = set(), set()
        face_edge_counts = Counter()
        for t, j in enumerate(side):
            tri = faces[j]
            if t:
                assert len(tri-seen) == 1 and tuple(sorted(tri & seen)) in old_edges
            seen |= tri
            es = list(combinations(sorted(tri), 2))
            old_edges.update(es)
            face_edge_counts.update(es)
        assert seen == set(range(n))
        assert {e for e, count in face_edge_counts.items() if count == 1} == edges
assert set(coverage) == set(inc) and min(coverage.values()) == 1
assert {e for e, c in coverage.items() if c == 3} == {(0,1), (5,6)}
assert {e for e, c in coverage.items() if c == 2} == {(0,2), (4,6)}
adj = graph_of_faces(n, faces)
colors, rounds = refine(n, adj)
point_cells = sorted(sorted(i for i in range(n) if colors[i] == c)
                     for c in set(colors[:n]))
face_cells = sorted(sorted(j for j in range(f) if colors[n+j] == c)
                    for c in set(colors[n:]))
assert point_cells == [[0,6], [1,5], [2,4], [3]]
assert face_cells == [[0,9], [1,8], [2,7], [3,6], [4,5]]
domains = [[a for a in range(n) if colors[a] == colors[i]] for i in range(n)]
valid, count, noninjective = [], 0, 0
for a in product(*domains):
    count += 1
    assert count <= data["limits"]["stable_point_maps"]
    noninjective += len(set(a)) < n
    face_domains = [[b for b in range(f) if colors[n+b] == colors[n+j]
                     and {a[i] for i in face} <= faces[b]]
                    for j, face in enumerate(faces)]
    if all(face_domains):
        assert all(len(d) == 1 for d in face_domains)
        valid.append({"points": list(a), "faces": [d[0] for d in face_domains]})
assert count == 64 and noninjective == 56
assert valid == [{"points": list(range(n)), "faces": list(range(f))},
                 {"points": list(reversed(range(n))), "faces": list(reversed(range(f)))}]
corners = {(i,j) for j, face in enumerate(faces) for i in face}
U = {e: {(i,j) for i in e for j in js} for e, js in inc.items()}
at = {c: [e for e in inc if c in U[e]] for c in corners}
assert all(len(es) == 2 for es in at.values())
M = {c: U[es[0]] | U[es[1]] for c, es in at.items()}
Delta = {c: U[es[0]] ^ U[es[1]] for c, es in at.items()}
assert all(len(M[c]) == 7 and len(Delta[c]) == 6 for c in corners)
assert all(U[es[0]] & U[es[1]] == {c} for c, es in at.items())
assert all(set.intersection(*(M[c] for c in U[e])) == U[e] for e in inc)
def moment(c, a, b):
    union, diff = a | b, a ^ b
    sigma = -1 if c == (0,0) else 1
    return ((F(1,2)*(int(not diff)+sigma*F(1,2)*int(diff == Delta[c]))
             if union <= M[c] else 0)
            +(F(1,2)*(int(not diff)-sigma*F(1,2)*int(diff == Delta[c]))
              if union <= Delta[c] else 0))
canonical_products = []
for auto in valid:
    pmap, fmap = auto["points"], auto["faces"]
    value = F(1)
    for i, j in sorted(corners):
        e, h = at[(i,j)]
        labels = [U[tuple(sorted(pmap[x] for x in edge))] for edge in (e,h)]
        value *= moment((pmap[i], fmap[j]), *labels)
    assert value == -F(1, 4**30)
    canonical_products.append(str(value))
degrees = [len(adj[i]) for i in range(n)]
hist = [Counter(degrees[i] for i in face) for face in faces]
norm = lambda h: sum(x*x for x in h.values())
assert sum(x*x for x in degrees) == 136 and sum(map(norm, hist)) == 34
assert sorted(Counter(map(norm, hist)).items()) == [(3,8), (5,2)]
local_max = max(2*sum(h[d] for d in ds)-norm(h)
                for h in hist for ds in product((3,4,5,6), repeat=3))
assert local_max == 7
pair_max = max(74*degrees[a]+2*h[degrees[a]] for a in range(n) for h in hist)
assert pair_max == 446 and 37*136+34 == 5066
assert n**n * f**f < 2**54 and 54+450-564 == -60
assert 5066-30*446 == -8314
folds = []
for case in data["smaller"]:
    sf = [frozenset(x) for x in case["faces"]]
    a = case["point_map"]; b = case["face_map"]; sn = case["n"]
    sa = graph_of_faces(sn, sf); sc, _ = refine(sn, sa)
    mapping = a + [sn+j for j in b]
    assert len(set(mapping)) < len(mapping)
    assert all(sc[u] == sc[mapping[u]] for u in range(len(sa)))
    assert all(mapping[v] in sa[mapping[u]] for u in range(len(sa)) for v in sa[u])
    folds.append(case["name"])
simplices = [frozenset((i,)) for i in range(n)] + [frozenset(e) for e in inc] + faces
fixed = {x for x in simplices if frozenset(6-i for i in x) == x}
assert fixed == {frozenset((3,)), frozenset((2,4))}
remaining = set(simplices)-fixed
reached = {next(iter(remaining))}
while True:
    newer = reached | {y for y in remaining for x in reached if x < y or y < x}
    if newer == reached:
        break
    reached = newer
assert reached == remaining and len(reached) == 30
dual = [{j for js in inc.values() if i in js for j in js if i != j} for i in range(f)]
diameter = 0
for start in range(f):
    dist = {start: 0}; queue = [start]
    for u in queue:
        for w in dual[u]:
            if w not in dist:
                dist[w] = dist[u]+1; queue.append(w)
    assert len(dist) == f
    diameter = max(diameter, max(dist.values()))
Ma = 4104*f*(diameter+1)**2
Ca = 12*Ma*Ma+2*Ma
threshold = max(Ma+2*f*Ca, 15*15+20*15, 11)
even_D = 2*(threshold//2+1)
print(json.dumps({"status":"PASS","input_sha256":EXPECTED,
 "source_response_sha256":data["source_response_sha256"],
 "n":n,"f":f,"point_edges":len(inc),"incidence_edges":len(corners),
 "stellar_construction_matches":True,"coverage":{str(e):str(F(c,3)) for e,c in sorted(coverage.items())},
 "exposure_orders_checked":6,"refinement_cell_counts":rounds,
 "point_cells":point_cells,"face_cells":face_cells,
 "stable_point_maps_checked":count,"noninjective_point_maps_checked":noninjective,
 "all_stable_endomorphisms":valid,"support_intersections_checked":len(inc),
 "canonical_orbit_label_products":canonical_products,
 "canonical_product_scope":"The full-sum uniqueness is a conventional support proof, not brute force.",
 "score_values":{"sum_degree_squares":136,"sum_histogram_squares":34,"max_local_error":local_max,
 "Qmax":5066,"max_pair_score":pair_max,"beta_log2":564,"normalized_lower_map_bound_exponent":-60},
 "smaller_folds_checked":folds,"barycentric_fixed_set":[sorted(s) for s in sorted(fixed,key=lambda s:(len(s),sorted(s)))],
 "nonfixed_barycentric_vertices_connected":len(reached),
 "dual_diameter":diameter,"L3_M":Ma,"L3_C":Ca,"L3_B":525,
 "sufficient_fixed_even_D":even_D,
 "limits":data["limits"],
 "not_verified":["full n<=12 census","producer standalone certificate","analytic rank-layer theorem by computation","numerical prime/kernel/host"]},indent=2))
