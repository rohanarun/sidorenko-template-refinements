#!/usr/bin/env python3
"""Reference deterministic generator and all-map arithmetic checks.

Default: symbolic output only. No huge field, integer, or graph is allocated.
The mathematical generator uses arbitrary finite binary strings. The full
instance is not physically runnable on this or any presently provided runtime;
the proof supplies a finite termination bound, not a feasibility claim.
"""
from __future__ import annotations
import argparse
import json
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Optional

B = 7866423844799423288734694969
FACES = ((0,1,3),(0,1,9),(0,2,3),(0,2,9),(1,3,10),(1,7,10),
         (1,7,12),(1,9,12),(2,3,4),(2,4,9),(3,4,11),(3,10,11),
         (4,8,9),(4,8,11),(5,6,7),(5,6,11),(5,7,10),(5,10,11),
         (6,7,12),(6,8,11),(6,8,12),(8,9,12))

def assignments(n: int, width: int) -> Iterator[tuple[int,...]]:
    """All maps, in lexicographic order, with repetitions; constant-width storage."""
    if n<1 or width<0:
        raise ValueError('n must be positive and width nonnegative')
    digits=[0]*width
    while True:
        yield tuple(digits)
        j=width-1
        while j>=0 and digits[j]+1==n:
            digits[j]=0;j-=1
        if j<0:return
        digits[j]+=1

def graph_from_mask(n: int, mask: int) -> list[int]:
    """Upper-triangle order: (0,1),(0,2),...,(n-2,n-1). No loops."""
    if n<1 or mask<0 or mask.bit_length()>n*(n-1)//2:
        raise ValueError('invalid order or upper-triangle mask')
    rows=[0]*n;k=0
    for u in range(n):
        for v in range(u+1,n):
            if (mask>>k)&1:
                rows[u]|=1<<v;rows[v]|=1<<u
            k+=1
    return rows

def validate_graph(rows: Sequence[int]) -> None:
    n=len(rows)
    if not n:raise ValueError('host must be nonempty')
    for u,row in enumerate(rows):
        if row<0 or row.bit_length()>n or ((row>>u)&1):
            raise ValueError('invalid row or graph loop')
        for v in range(u+1,n):
            if ((row>>v)&1)!=((rows[v]>>u)&1):
                raise ValueError('graph is not symmetric')

def hom_count(rows: Sequence[int], faces: Sequence[Sequence[int]]=FACES,
              point_count: int=13) -> int:
    """Exact all-map count, eliminating independent face-vertex assignments.

    A face with repeated source point indices is rejected, but different source
    points may have equal host images. Face vertices may also repeat their images.
    """
    validate_graph(rows);n=len(rows)
    if point_count<0:raise ValueError('invalid source point count')
    for face in faces:
        if len(face)!=len(set(face)) or any(i<0 or i>=point_count for i in face):
            raise ValueError('invalid source face')
    universe=(1<<n)-1;total=0
    for images in assignments(n,point_count):
        count=1
        for face in faces:
            possible=universe
            for i in face:possible&=rows[images[i]]
            count*=possible.bit_count()
            if not count:break
        total+=count
    return total

def hom_count_direct_small(rows: Sequence[int], faces: Sequence[Sequence[int]],
                           point_count: int) -> int:
    """Independent full-assignment implementation, for tiny regression tests only."""
    validate_graph(rows);n=len(rows);out=0
    for f in assignments(n,point_count+len(faces)):
        good=True
        for j,face in enumerate(faces):
            for i in face:
                if not ((rows[f[i]]>>f[point_count+j])&1):
                    good=False;break
            if not good:break
        out+=good
    return out

def accepted(rows: Sequence[int], count: Optional[int]=None) -> bool:
    """The exact integer test (A). No floating-point density is evaluated."""
    validate_graph(rows);n=len(rows)
    edges=sum(x.bit_count() for x in rows)//2
    h=hom_count(rows) if count is None else count
    if h<0:raise ValueError('negative homomorphism count')
    return (2*edges)**66-h*n**97 >=1024*n**131

def first_host() -> tuple[int,int,int]:
    """Literal reference for the mathematical generator, not run by default.

    Return (order, upper-triangle mask, hom count). In the mathematical
    unbounded-memory interpretation this halts by Theorem T. CPython on a fixed
    platform cannot even materialize the full order; no runtime completion is
    asserted for this function on actual hardware.
    """
    n=1<<B
    m=n*(n-1)//2;mask=0;limit=1<<m
    while mask<limit:
        rows=graph_from_mask(n,mask);h=hom_count(rows)
        if accepted(rows,h):return n,mask,h
        mask+=1
    raise AssertionError('Theorem T would be contradicted by an exhausted enumeration')

def self_test() -> dict:
    # Exhaust all labeled simple hosts of order three, on a five-vertex template.
    small=((0,1,2),(0,1));tested=0
    for mask in range(8):
        rows=graph_from_mask(3,mask)
        a=hom_count(rows,small,3);b=hom_count_direct_small(rows,small,3)
        if a!=b:raise AssertionError((mask,a,b))
        tested+=1
    # Original 35-vertex connected bipartite H has two maps to K2, both noninjective.
    k2=graph_from_mask(2,1);h=hom_count(k2)
    if h!=2:raise AssertionError(('original H -> K2',h))
    if accepted(k2,h):raise AssertionError('K2 falsely accepted')
    if hom_count(graph_from_mask(2,0))!=0:raise AssertionError('empty host count')
    if list(assignments(2,2))!=[(0,0),(0,1),(1,0),(1,1)]:
        raise AssertionError('assignment enumerator omitted repeated images')
    return {'status':'PASS','small_hosts_compared_to_full_map_enumeration':tested,
            'original_H_hom_count_to_K2':h,
            'original_H_maps_to_K2_are_all_noninjective':True,
            'empty_host_hom_count':0,'huge_generator_executed':False}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--execute-full-generator',action='store_true',
                    help='explicit guard; the full instance exceeds this runtime\'s representation limits')
    args=ap.parse_args()
    if args.self_test:
        print(json.dumps(self_test(),indent=2));return
    if args.execute_full_generator:
        try:
            result=first_host()
        except (OverflowError,MemoryError) as exc:
            raise SystemExit('This runtime cannot materialize the theorem instance. '
                             'The mathematical specification and finite bound are in PROOF.md.') from exc
        print(result);return
    cert_path=Path(__file__).with_name('certificate.json')
    params=json.loads(cert_path.read_text())['parameters']
    if params['fixed_host_log2_order']!=B:raise ValueError('certificate/generator parameter mismatch')
    print(json.dumps({'order':f'2^{B}','certified_deficit':f'2^-{B-10}',
      'acceptance':'(2*edge_count)^66 - hom(H,G)*N^97 >= 1024*N^131',
      'max_graph_tests':'2^(N*(N-1)/2)','max_point_assignments_per_test':'N^13',
      'all_homomorphisms_included':True,'field_q_log2_upper':params['q_log2_upper'],
      'huge_integers_or_graphs_allocated':False},indent=2))

if __name__=='__main__':main()
