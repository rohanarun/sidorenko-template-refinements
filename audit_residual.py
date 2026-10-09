"""Exact supplementary checks for the new model-derived follow-up arguments."""
import argparse
from collections import Counter,defaultdict
from fractions import Fraction as Q
from itertools import combinations
import json
from math import comb
from pathlib import Path
import re
import sympy as s

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--complex-source',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
text=a.complex_source.read_text().split('\\midrule',1)[1].split('\\bottomrule',1)[0]
rows=[re.findall(r'\d+',line) for line in text.splitlines() if '&' in line]
assert len(rows)==22 and all(len(row)==8 for row in rows)
faces=[tuple(map(int,row[1:4])) for row in rows];bits=[row[-1] for row in rows]
assert all(len(bit)==3 for bit in bits)
edges=defaultdict(list)
for j,f in enumerate(faces):
    for e in combinations(f,2):edges[e].append(j)
assert len(edges)==33 and all(len(js)==2 for js in edges.values())
separation={e:sum(x!=y for x,y in zip(bits[js[0]],bits[js[1]])) for e,js in edges.items()}
assert min(separation.values())>=1
eligible=[e for e,h in separation.items() if h==1]
deg=Counter(v for e in eligible for v in e)
caps=sorted((2*deg[v] for v in range(13)),reverse=True)
m=len(eligible);C=sum(comb(x,2) for x in caps)
coarse=m*m-2*m+C
# Convexity/majorization puts as much of a fixed sum as possible in the
# largest caps first. Independently check its integer values by convolution DP.
dp={0:0}
for cap in caps:
    nd={}
    for total,value in dp.items():
        for x in range(cap+1):
            nd[total+x]=max(nd.get(total+x,-1),value+comb(x,2))
    dp=nd

def greedy(total):
    result=0
    for cap in caps:
        x=min(total,cap);total-=x;result+=comb(x,2)
    assert total==0
    return result

assert all(greedy(t)==v for t,v in dp.items())
strata=[]
for k in range(2,2*m):
    local_bound=greedy(2*k+1)
    remainder=-k*k+2*m*k-2*m+local_bound
    strata.append({'span':k,'local_dimension_sum':2*k+1,'binomial_bound':local_bound,'remainder':remainder})
best=max(x['remainder'] for x in strata)
assert coarse/2<best
# Exhaust all relaxed defects as a separate exact arithmetic comparison.
all_best=max(Q(-k*k+2*m*k-2*m+v,total-2*k)
             for k in range(2,2*m) for total,v in dp.items() if total>2*k)
assert all_best==best


result={'eligible_edges':m,'eligible_degree_caps':caps,'sum_binomials':C,'coarse_remainder':coarse,'refined_remainder':best,'maximizing_spans':[x['span'] for x in strata if x['remainder']==best], 'strata':strata,'comparison_for_defect_at_least_two':str(Q(coarse,2))}
a.output.write_text(json.dumps(result,indent=2))
print('Exact residual audit:',coarse,'->',best)
