"""New exact checks for the newly recovered pentagonal/hexagonal examples.

Example JSON is independently generated from the formulas below. No downloaded program is imported or executed.
The universal sign/flag and reflection proofs are separate written arguments.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
import hashlib
import json
from pathlib import Path

DATA = None
OUT = Path.cwd()

def features(n, faces, point_map, face_map):
    u = [0] * n
    v = [0] * len(faces)
    w = [0] * (n * len(faces))
    for a in point_map:
        u[a] += 1
    for b in face_map:
        v[b] += 1
    for j, f in enumerate(faces):
        for i in f:
            w[point_map[i] * len(faces) + face_map[j]] += 1
    return u + v + w

def check(ell):
    file = DATA / ('bipyramid_%d_certificate.json' % ell)
    raw = file.read_bytes()
    d = json.loads(raw)
    n = ell + 2
    faces = [tuple(sorted((apex, i, (i+1) % ell)))
             for apex in (ell, ell+1) for i in range(ell)]
    assert d['faces'] == [list(f) for f in faces] and d['n'] == n
    assert Fraction(*d['theta']) == Fraction(1, 2)
    edges = sorted(set(e for f in faces for e in combinations(f, 2)))
    edge_index = {e:i for i,e in enumerate(edges)}
    corners = [(i,j) for j,f in enumerate(faces) for i in f]
    U = {e:frozenset((i,j) for j,f in enumerate(faces) if set(e) <= set(f) for i in e)
         for e in edges}
    local_edges = {(i,j):[e for e in combinations(f,2) if i in e]
                   for j,f in enumerate(faces) for i in f}
    M = {c:U[es[0]] | U[es[1]] for c,es in local_edges.items()}
    D = {c:U[es[0]] ^ U[es[1]] for c,es in local_edges.items()}
    assert all(len(M[c]) == 7 and len(D[c]) == 6 for c in corners)
    assert all((U[e] <= M[c]) == (c in U[e]) for e in edges for c in corners)
    coverage = Counter()
    assert sum(Fraction(*x['weight']) for x in d['cycles']) == 1
    for atom in d['cycles']:
        cycle = atom['cycle']
        assert set(cycle) == set(range(n)) and len(cycle) == n
        for a,b in zip(cycle,cycle[1:]+cycle[:1]):
            e = tuple(sorted((a,b)))
            assert e in edge_index
            coverage[e] += Fraction(*atom['weight'])
    assert all(coverage[e] == (Fraction(ell-2,ell) if max(e) < ell else Fraction(2,ell))
               and coverage[e] >= Fraction(1,3) for e in edges)

    face_set = set(faces)
    autos = [a for a in permutations(range(n))
             if {tuple(sorted(a[i] for i in f)) for f in faces} == face_set]
    g = len(autos)
    assert g == 4 * ell
    fi = {f:j for j,f in enumerate(faces)}
    auto_faces = [[fi[tuple(sorted(a[i] for i in f))] for f in faces] for a in autos]
    identity = features(n,faces,list(range(n)),list(range(len(faces))))
    plus = features(n,faces,d['fold_plus_points'],d['fold_plus_faces'])
    minus = features(n,faces,d['fold_minus_points'],d['fold_minus_faces'])
    assert [a+b for a,b in zip(plus,minus)] == [2*a for a in identity]
    orbit_sizes = []
    terms = {}
    negative = tuple(d['negative_corner'])
    for kind in ['reflection','fold_plus','fold_minus']:
        pm, fm = d[kind+'_points'], d[kind+'_faces']
        assert all(pm[i] in faces[fm[j]] for i,j in corners)
        maps = {(tuple(pm[a[i]] for i in range(n)), tuple(fm[b[j]] for j in range(len(faces))))
                for a,b in zip(autos,auto_faces)}
        if kind.startswith('fold'):
            assert len(maps) == g // 2
            orbit_sizes.append(len(maps))
        labels = {e:U[tuple(sorted(pm[i] for i in e))] for e in edges}
        product = Fraction(1)
        for c,es in local_edges.items():
            target = (pm[c[0]],fm[c[1]])
            a,b = labels[es[0]],labels[es[1]]
            q,r = a|b,a^b
            sign = -1 if target == negative else 1
            value = (Fraction(1,2) * (q <= M[target]) * ((not r) + sign*Fraction(1,2)*(r == D[target]))
                     + Fraction(1,2) * (q <= D[target]) * ((not r) - sign*Fraction(1,2)*(r == D[target])))
            product *= value
        expected = Fraction(1,4) ** len(corners) * (-1 if kind == 'reflection' else 1)
        assert product == expected
        terms[kind] = str(product)

    # Medial edges connect the two point edges at each corner. Gray enumeration
    # changes one spin and updates only its four incident medial edges.
    neighbors = [[] for _ in edges]
    for es in local_edges.values():
        a,b = [edge_index[e] for e in es]
        neighbors[a].append(b)
        neighbors[b].append(a)
    assert all(len(z) == 4 for z in neighbors)
    hist = Counter({0:1})
    state = 0
    cut = 0
    for index in range(1,1 << len(edges)):
        low = index & -index
        flipped = low.bit_length()-1
        bit = (state >> flipped) & 1
        before = sum(bit != ((state >> j) & 1) for j in neighbors[flipped])
        cut += 4-2*before
        state ^= 1 << flipped
        assert cut % 2 == 0
        hist[cut] += 1
    coefficient = 63 + 32 * Fraction(1,2) ** len(corners) * sum(
        count * Fraction(1,2) ** boundary for boundary,count in hist.items())
    reported = json.loads((DATA/'exact_report.json').read_text())['examples'][str(ell)]
    assert {str(k):v for k,v in sorted(hist.items())} == reported['constant_spin_oracle']['cut_histogram']
    assert coefficient == Fraction(reported['constant_spin_oracle']['coefficient'])
    return {'ring':ell,'source_SHA256':hashlib.sha256(raw).hexdigest(),
            'automorphisms':g,'fold_orbit_sizes':orbit_sizes,'feature_midpoint':True,
            'coverage_min':str(min(coverage.values())),'canonical_single_terms':terms,
            'spin_states':1 << len(edges),'constant_coefficient':str(coefficient),
            'histogram':dict(sorted(hist.items())),'complete_global_polynomial_enumerated':False}


def make_example_data(ell):
    n = ell + 2
    faces = [sorted((apex,i,(i+1)%ell)) for apex in (ell,ell+1) for i in range(ell)]
    cycles = []
    for plus in range(ell):
        for minus in range(ell):
            if plus == minus:
                continue
            cycle = []
            for i in range(ell):
                cycle.append(i)
                if i == plus:
                    cycle.append(ell)
                if i == minus:
                    cycle.append(ell+1)
            cycles.append({'cycle':cycle,'weight':[1,ell*(ell-1)]})
    return {'format':'reflection-fold-v1','ring_size':ell,'n':n,'faces':faces,
            'boundary_cycle':list(range(ell)),
            'plus_faces':list(range(ell)),'minus_faces':list(range(ell,2*ell)),
            'reflection_points':list(range(ell))+[ell+1,ell],
            'reflection_faces':list(range(ell,2*ell))+list(range(ell)),
            'fold_plus_points':list(range(ell))+[ell,ell],
            'fold_plus_faces':list(range(ell))+list(range(ell)),
            'fold_minus_points':list(range(ell))+[ell+1,ell+1],
            'fold_minus_faces':list(range(ell,2*ell))+list(range(ell,2*ell)),
            'cycles':cycles,'theta':[1,2],'negative_corner':[ell,0]}

EXPECTATIONS = {'examples': {'5': {'constant_spin_oracle': {'cut_histogram': {'0': 2, '4': 30, '6': 80, '8': 580, '10': 1744, '12': 4780, '14': 8560, '16': 9050, '18': 6000, '20': 1942}, 'coefficient': '1108307726537083/17592186044416'}}, '6': {'constant_spin_oracle': {'cut_histogram': {'0': 2, '4': 36, '6': 96, '8': 846, '10': 2688, '12': 10424, '14': 25920, '16': 53118, '18': 66688, '20': 61668, '22': 31584, '24': 9074}, 'coefficient': '1134907106239454873/18014398509481984'}}}}

if __name__ == '__main__':
    import argparse
    import tempfile
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',default='replay-result.json')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='reflection-example-') as td:
        DATA = Path(td)
        for ell in (5,6):
            (DATA/('bipyramid_%d_certificate.json'%ell)).write_text(json.dumps(make_example_data(ell)))
        (DATA/'exact_report.json').write_text(json.dumps(EXPECTATIONS))
        checks = [check(5),check(6)]
    result = {'status':'PASS','examples':checks,
              'inputs':'Generated independently from ring/apex and cycle formulas',
              'complete_global_polynomial_enumerated':False,
              'finite_checker_proves_universal_theorem':False}
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
