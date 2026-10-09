"""Independent checks for the two feasible objects at the minimum order."""
import argparse
import importlib.util
import json
from pathlib import Path
from verify_minimality import parse_independently, incidence_discrete, verify_weight

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--candidates',type=Path,required=True)
p.add_argument('--results',type=Path,required=True)
p.add_argument('--finite-checker',type=Path,required=True)
p.add_argument('--original',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
spec=importlib.util.spec_from_file_location('finite_checker',a.finite_checker)
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)

def canonical(d):
    n=d['points'];faces=d['faces'];adj=[set() for _ in range(n+len(faces))]
    for j,f in enumerate(faces,n):
        for v in f:adj[j].add(v);adj[v].add(j)
    colors=[0]*n+[1]*len(faces)
    for _ in adj:
        sig=[(colors[v],tuple(sorted(colors[w] for w in adj[v]))) for v in range(len(adj))]
        ids={t:i for i,t in enumerate(sorted(set(sig)))}
        nxt=[ids[t] for t in sig]
        if len(set(nxt))==len(adj):
            return sorted((min(nxt[v],nxt[w]),max(nxt[v],nxt[w])) for v in range(len(adj)) for w in adj[v] if v<w)
        assert len(set(nxt))>len(set(colors))
        colors=nxt
    raise AssertionError('Refinement not discrete')

original=canonical(json.loads(a.original.read_text()))
results={i['plantri_index']:i for i in json.loads(a.results.read_text())['results']}
obstructions=0;cycles=0;feasible=[];seen=set()
for c in json.loads(a.candidates.read_text()):
    n,rot,faces=parse_independently(c['ascii'])
    assert faces==[tuple(f) for f in c['faces']]
    assert incidence_discrete(faces,n)
    index=c['plantri_index'];seen.add(index);r=results[index]
    if r['status']=='exact_infeasibility_witness':
        count,_=verify_weight(rot,r);obstructions+=1;cycles+=count
    else:
        assert r['status']=='exact_feasible_candidate'
        certificate=a.results.parent/f'candidate-{n}-{index}.json'
        d=json.loads(certificate.read_text())
        assert d['faces']==c['faces']
        proof=checker.check(d)
        feasible.append({'plantri_index':index,'finite_checks':proof,'isomorphic_to_original':canonical(d)==original})
assert seen==set(results)
a.output.write_text(json.dumps({'obstructions':obstructions,'independent_cycle_count':cycles,'feasible':feasible},indent=2))
print(a.output.read_text())
