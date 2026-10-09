"""Exhaustive plantri enumeration with independent incidence color refinement.

Enumerates simple sphere triangulations; it does not establish minimality
among arbitrary Sidorenko counterexamples. Supply explicit size range.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess


def decode(line):
    ns, code = line.strip().split()
    n = int(ns)
    rotation = [[ord(c)-ord('a') for c in part] for part in code.split(',')]
    assert len(rotation) == n
    assert all(len(set(row)) == len(row) and u not in row for u,row in enumerate(rotation))
    for u,row in enumerate(rotation):
        for v in row:
            assert 0 <= v < n and u in rotation[v]
    darts = {(u,v) for u,row in enumerate(rotation) for v in row}
    faces = []
    while darts:
        start = min(darts)
        u,v = start
        face = []
        while True:
            assert (u,v) in darts
            darts.remove((u,v))
            face.append(u)
            w = rotation[v][(rotation[v].index(u)+1) % len(rotation[v])]
            u,v = v,w
            if (u,v) == start:
                break
        assert len(face) == 3 and len(set(face)) == 3
        faces.append(tuple(sorted(face)))
    faces = sorted(faces)
    assert len(set(faces)) == len(faces) == 2*n-4
    edge_counts = Counter(e for f in faces for e in combinations(f,2))
    assert len(edge_counts) == 3*n-6 and set(edge_counts.values()) == {2}
    return n, rotation, faces


def refine(n,faces):
    adj = [[] for _ in range(n+len(faces))]
    for i,f in enumerate(faces,n):
        for v in f:
            adj[i].append(v)
            adj[v].append(i)
    colors = [0]*n+[1]*len(faces)
    while True:
        signatures = [(colors[v],tuple(sorted(colors[w] for w in adj[v]))) for v in range(len(adj))]
        ids = {s:i for i,s in enumerate(sorted(set(signatures)))}
        new = [ids[s] for s in signatures]
        if len(set(new)) == len(set(colors)):
            return len(set(new)) == len(adj), sorted(Counter(new).values())
        colors = new


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plantri',type=Path,required=True)
    p.add_argument('--min-n',type=int,required=True)
    p.add_argument('--max-n',type=int,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    results=[]
    for n in range(a.min_n,a.max_n+1):
        command=[str(a.plantri.resolve()),'-a',str(n)]
        run=subprocess.run(command,check=True,capture_output=True,text=True)
        counts=Counter();candidates=[]
        for index,line in enumerate(run.stdout.splitlines()):
            m,rotation,faces=decode(line)
            assert m==n
            counts['all_simple_sphere_triangulations']+=1
            if max(map(len,rotation))>6:continue
            counts['maximum_degree_at_most_six']+=1
            discrete,classes=refine(n,faces)
            if discrete:
                counts['discrete_incidence_refinement']+=1
                candidates.append({'plantri_index':index,'ascii':line,'points':n,'faces':faces})
        item={'n':n,'counts':dict(counts),'generator_stderr':run.stderr,
              'output_sha256':hashlib.sha256(run.stdout.encode()).hexdigest()}
        results.append(item)
        (a.output/f'candidates-{n}.json').write_text(json.dumps(candidates,indent=2))
        (a.output/'summary.json').write_text(json.dumps(results,indent=2))
        print(json.dumps(item),flush=True)


if __name__=='__main__':main()
