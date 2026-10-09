"""Independent exact audit: plantri completeness + partition refinement + Held-Karp.

Does not import either proposal script or use floating point optimization.
The completeness claim depends on the specified plantri generator.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from math import gcd
from pathlib import Path
import re
import subprocess


def incidence_discrete(faces,n):
    size=n+len(faces)
    neighbors=[set() for _ in range(size)]
    for j,face in enumerate(faces,n):
        for v in face:
            neighbors[v].add(j);neighbors[j].add(v)
    blocks=[set(range(n)),set(range(n,size))]
    while True:
        refined=[]
        for block in blocks:
            groups={}
            for v in block:
                sig=tuple(len(neighbors[v]&b) for b in blocks)
                groups.setdefault(sig,set()).add(v)
            refined.extend(groups.values())
        if len(refined)==len(blocks):return len(blocks)==size
        blocks=refined


def parse_independently(line):
    ntext,code=line.split();n=int(ntext)
    rot=[tuple(ord(v)-97 for v in row) for row in code.split(',')]
    assert len(rot)==n
    # Recover each triangular face from a wedge in the rotation system.
    wedges=Counter()
    for v,row in enumerate(rot):
        assert len(set(row))==len(row) and v not in row
        for u,w in zip(row,row[1:]+row[:1]):
            assert v in rot[u] and w in rot[u]
            wedges[tuple(sorted((v,u,w)))]+=1
    assert set(wedges.values())=={3}
    faces=sorted(wedges)
    edge_counts=Counter(e for f in faces for e in combinations(f,2))
    assert len(faces)==2*n-4 and len(edge_counts)==3*n-6
    assert set(edge_counts.values())=={2}
    return n,rot,faces


def max_hamilton_weight(rot,weights):
    n=len(rot);unit=1
    for q in weights.values():unit=unit*q.denominator//gcd(unit,q.denominator)
    iw={e:int(q*unit) for e,q in weights.items()}
    # mask includes vertex zero. A state records maximum weight and count of
    # all paths to its endpoint, separately; no exposure-order filtering.
    table={(1,0):(0,1)}
    for mask in range(1,1<<n,2):
        for end in range(n):
            state=table.get((mask,end))
            if state is None:continue
            value,count=state
            for nxt in rot[end]:
                bit=1<<nxt
                if mask&bit:continue
                key=(mask|bit,nxt)
                val=value+iw.get(tuple(sorted((end,nxt))),0)
                old=table.get(key)
                table[key]=(val,count) if old is None else (max(val,old[0]),count+old[1])
    full=(1<<n)-1;best=None;count=0
    for end in rot[0]:
        if (full,end) not in table:continue
        val,c=table[full,end];count+=c
        val+=iw.get(tuple(sorted((0,end))),0)
        best=val if best is None else max(val,best)
    assert count%2==0
    return None if best is None else Fraction(best,unit),count//2


def verify_weight(rot,item):
    weights={tuple(e):Fraction(w) for e,w in item['edge_weights']}
    assert len(weights)==len(item['edge_weights'])
    assert all(u<v and v in rot[u] and w>=0 for (u,v),w in weights.items())
    assert sum(weights.values())==1
    best,count=max_hamilton_weight(rot,weights)
    assert count==item['hamilton_cycles']
    assert best==Fraction(item['exact_max_cycle_weight'])
    assert best<Fraction(1,3)
    return count,Fraction(1,3)-best


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plantri',type=Path,required=True)
    p.add_argument('--witnesses',type=Path,required=True)
    p.add_argument('--generator-source',type=Path,required=True)
    p.add_argument('--min-n',type=int,required=True)
    p.add_argument('--max-n',type=int,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    items=json.loads(a.witnesses.read_text())['results']
    witnesses={(v['n'],v['plantri_index']):v for v in items}
    assert len(witnesses)==len(items)
    results=[];checked=set();gaps=[];totalcycles=0;control=None
    for n in range(a.min_n,a.max_n+1):
        run=subprocess.run([str(a.plantri.resolve()),'-a',str(n)],capture_output=True,text=True,check=True)
        count=Counter()
        for index,line in enumerate(run.stdout.splitlines()):
            m,rot,faces=parse_independently(line);assert m==n
            count['all_triangulations']+=1
            if max(map(len,rot))>6:continue
            count['degree_eligible']+=1
            if not incidence_discrete(faces,n):continue
            count['discrete_refinement']+=1
            item=witnesses[n,index]
            cycles,gap=verify_weight(rot,item)
            totalcycles+=cycles;gaps.append(gap);checked.add((n,index))
            if control is None:control=(rot,item)
            count['exact_obstructions']+=1
        declared=int(re.search(r'(\d+) triangulations written',run.stderr).group(1))
        assert declared==count['all_triangulations']
        results.append(dict(n=n,counts=dict(count),generator_output_sha256=hashlib.sha256(run.stdout.encode()).hexdigest()))
    assert checked==set(witnesses)
    # A normalized weight on one edge has a Hamilton cycle attaining 1, so it
    # must not be accepted as a separating witness.
    rot,item=control
    bad=dict(item);bad['edge_weights']=[[item['edge_weights'][0][0],'1']]
    try:verify_weight(rot,bad)
    except AssertionError:pass
    else:raise AssertionError('Corrupted witness accepted')
    result={'scope':'Minimum 35 incidence vertices within the distinct-triple, two-occurrences, paired spanning-exposure, weighted-cut coverage and discrete-incidence-refinement template; relies on plantri enumeration.',
            'plantri_source_sha256':hashlib.sha256(a.generator_source.read_bytes()).hexdigest(),
            'sizes':results,'exact_obstructions':len(checked),'independent_hamilton_cycle_count':totalcycles,
            'minimum_separation_margin':str(min(gaps)),'negative_controls_rejected':1}
    a.output.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))


if __name__=='__main__':main()
