"""Propose LP witnesses, then certify Hamilton-cycle obstructions exactly."""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--search-module',type=Path,required=True)
p.add_argument('--candidates',type=Path,nargs='+',required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args();a.output.mkdir(exist_ok=True,parents=True)
spec=importlib.util.spec_from_file_location('prior_search',a.search_module)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
summary=[]
for name in a.candidates:
    for obj in json.loads(name.read_text()):
        n=obj['points'];faces=tuple(tuple(f) for f in obj['faces'])
        st=module.structure(faces);cycles=module.cuts(faces,st);edges=list(st[1])
        item={'n':n,'plantri_index':obj['plantri_index'],'hamilton_cycles':len(cycles)}
        A=np.array([[int(c['mask']>>i&1) for i in range(len(edges))] for c in cycles],dtype=float)
        if not cycles:
            item['status']='no_hamilton_cycles'
        else:
            # Normalize nonnegative edge weights to sum one. Every admissible
            # mixture would have expected weighted coverage at least one third.
            c=np.zeros(len(edges)+1);c[-1]=1
            res=linprog(c,A_ub=np.column_stack([A,-np.ones(len(cycles))]),b_ub=np.zeros(len(cycles)),A_eq=[list(np.ones(len(edges)))+[0]],b_eq=[1],bounds=[(0,None)]*(len(edges)+1),method='highs')
            assert res.success,res.message
            ys=[Q(float(x)).limit_denominator(1000000) for x in res.x[:-1]]
            total=sum(ys);ys=[x/total for x in ys]
            worst=max(sum(ys[i] for i in range(len(edges)) if cy['mask']>>i&1) for cy in cycles)
            item.update(exact_max_cycle_weight=str(worst),exact_required_weight='1/3',edge_weights=[[list(e),str(y)] for e,y in zip(edges,ys) if y])
            if min(ys)>=0 and worst<Q(1,3):
                item['status']='exact_infeasibility_witness'
            else:
                # A failed obstruction is not proof of feasibility.
                primal=linprog(np.zeros(len(cycles)),A_ub=-A.T,b_ub=-np.ones(len(edges))/3,A_eq=[np.ones(len(cycles))],b_eq=[1],bounds=(0,None),method='highs')
                item['status']='requires_primal_verification' if primal.success else 'unresolved'
                if primal.success:
                    weights=[Q(float(x)).limit_denominator(1000000) for x in primal.x];weights=[w/sum(weights) for w in weights]
                    cover=[sum(w for w,cy in zip(weights,cycles) if cy['mask']>>i&1) for i in range(len(edges))]
                    if min(weights)>=0 and min(cover)>=Q(1,3) and max(cover)>Q(1,3):
                        item['status']='exact_feasible_candidate'
                        candidate=dict(points=n,faces=faces,cuts=[dict(cy,weight=str(w)) for cy,w in zip(cycles,weights) if w])
                        (a.output/f'candidate-{n}-{obj["plantri_index"]}.json').write_text(json.dumps(candidate,indent=2))
        summary.append(item)
        (a.output/'summary.json').write_text(json.dumps({'search_module_sha256':hashlib.sha256(a.search_module.read_bytes()).hexdigest(),'results':summary},indent=2))
        print(json.dumps(item),flush=True)
