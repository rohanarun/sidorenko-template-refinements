#!/usr/bin/env python3
"""Offline exact checker. Python 3 standard library only; no field construction.

Default inputs are the accompanying template_data.json and certificates.json.
Optional --candidate-source/--complex-source compare the transcribed literals
with local copies of the pinned repository files. No repository code is run.
"""
from __future__ import annotations
if not __debug__:
    raise RuntimeError("Run this certifier without Python -O or -OO: assertions must be enabled.")
import argparse
import json
import re
from collections import Counter, deque
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

# Sparse polynomials over Q: equality checks below are symbolic, not evaluations.
NAMES = ('c','d','z','v','p0','p1','p2','t0','t1','t2','P','T','x','y','M','D')
NVAR = len(NAMES)
ZERO_MON = (0,) * NVAR
class Poly:
    def __init__(self, value=0):
        self.a = dict(value) if isinstance(value, dict) else ({ZERO_MON:F(value)} if value else {})
        self.a = {m:F(a) for m,a in self.a.items() if a}
    @staticmethod
    def cast(x): return x if isinstance(x, Poly) else Poly(x)
    def __add__(self, other):
        other = self.cast(other); ans=dict(self.a)
        for m,a in other.a.items(): ans[m]=ans.get(m,F(0))+a
        return Poly(ans)
    __radd__=__add__
    def __neg__(self): return Poly({m:-a for m,a in self.a.items()})
    def __sub__(self, other): return self + (-self.cast(other))
    def __rsub__(self, other): return self.cast(other) - self
    def __mul__(self, other):
        other=self.cast(other); ans={}
        for m,a in self.a.items():
            for n,b in other.a.items():
                k=tuple(x+y for x,y in zip(m,n)); ans[k]=ans.get(k,F(0))+a*b
        return Poly(ans)
    __rmul__=__mul__
    def __truediv__(self, other): return self * (F(1)/F(other))
    def __pow__(self, n):
        assert isinstance(n,int) and n>=0
        ans=Poly(1)
        for _ in range(n): ans=ans*self
        return ans
    def deriv(self, name):
        i=NAMES.index(name); ans={}
        for m,a in self.a.items():
            if m[i]:
                n=list(m);n[i]-=1;ans[tuple(n)]=a*m[i]
        return Poly(ans)
    def subst(self, name, value):
        i=NAMES.index(name); value=self.cast(value); ans=Poly()
        for m,a in self.a.items():
            n=list(m); power=n[i]; n[i]=0
            ans=ans+Poly({tuple(n):a})*(value**power)
        return ans

def var(name):
    m=[0]*NVAR;m[NAMES.index(name)]=1
    return Poly({tuple(m):F(1)})

def same(a,b,label):
    assert not (Poly.cast(a)-b).a, 'Failed polynomial identity: '+label

def check_symbolic():
    c,d,z,v=map(var,('c','d','z','v'))
    pp=[var('p'+str(i)) for i in range(3)];tt=[var('t'+str(i)) for i in range(3)]
    P0=sum(pp);T0=sum(tt);nn=[2*p-t for p,t in zip(pp,tt)]
    w=(d-3*z)/2-P0+v
    slack=(c*(d+z-1)-z*(d+2)+2*z*z)/4
    slack+=sum(n*(n-1)/6+z*p-c*(p+t)/6 for n,p,t in zip(nn,pp,tt))
    slack+=v*w-v*(v+1)/2
    quad=(c*(d+z)-z*d+2*z*z)/4
    quad+=sum(n*n/6+z*p-c*(p+t)/6 for n,p,t in zip(nn,pp,tt))
    quad+=v*((d-3*z)/2-P0)+v*v/2
    loss=c/4+z/2+(2*P0-T0)/6+v/2
    same(slack,quad-loss,'source slack = Q - linear loss')
    Hface=3*c+P0+T0
    same(Hface/2-loss,c/4+(c-z)+2*T0/3+(P0/3+z-v)/2,'linear envelope')
    S0=3*c*(c-1)/4+sum(n*n+(c-1)*n+3*c*p for n,p in zip(nn,pp))/6
    same(slack,S0+(c-z)*(d-3*c-2*z+2-4*P0)/4
         +v*(d-3*z-2*P0+v-1)/2,'common-mode decomposition')
    same(S0,(c-1)*(5*c+1)/8+sum((n+(c-1)/2)**2 for n in nn)/6+c*P0/2,
         'integer-base completing squares')
    # The coincident triple has negative local slack, for every even D.
    same(slack.subst('d',0).subst('z',0).subst('v',0)
         .subst('p0',0).subst('p1',0).subst('p2',0)
         .subst('t0',0).subst('t1',0).subst('t2',0),-c/4,'coincident negative slack')
    P,T,x,y,M,D=map(var,('P','T','x','y','M','D'))
    same((d+z)/4-(P+T)/6,(d+3*z)/12+(d-P-T)/6,'coefficient of c')
    F1=3*z*z/4+(2*P-T)**2/18+(5*P-T)*z/6-(P/3+z)**2/2
    F2=3*z*z/4+(2*P-T)**2/18+(5*P-T)*z/6-(P-T+3*z)**2/8
    H1=F1-(P+T)**2/72; H2=F2-(P+T)**2/72
    same(H1.deriv('T'),(T-3*P-2*z)/12,'positive branch derivative')
    same(H2.deriv('T').deriv('T'),-F(1,6),'positive branch concavity')
    for H in (H1,H2):
        same(H.subst('T',P/3+z),(4*P+3*z)*(4*P+9*z)/216,'positive breakpoint')
    same(H2.subst('T',P+3*z),z*(4*P+15*z)/24,'positive endpoint')
    G1=y*y/4+(2*x-T)*y/3+(2*x-T)**2/18-(x/3)**2/2
    G2=y*y/4+(2*x-T)*y/3+(2*x-T)**2/18-(x-T)**2/8
    I1=G1-(x+3*y+T)**2/72;I2=G2-(x+3*y+T)**2/72
    same(I1.deriv('T'),(T-3*x-5*y)/12,'negative branch derivative')
    same(I2.deriv('T').deriv('T'),-F(1,6),'negative branch concavity')
    for I in (I1,I2):
        same(I.subst('T',x/3),(16*x*x+96*x*y+27*y*y)/216,'negative breakpoint')
    same(I2.subst('T',x),y*(4*x+3*y)/24,'negative endpoint')
    ss=[pp[i]+tt[i] for i in range(3)]
    same(2*sum(ss)**2-sum((ss[i]-ss[j])**2 for i,j in combinations(range(3),2)),
         6*sum(ss[i]*ss[j] for i,j in combinations(range(3),2)),'triangle energy envelope')
    same((D-4*c-2*z+2-4*P)-(D-12*M+6*c+2),
         2*(c-z)+4*(3*(M-c)-P),'positive kappa coefficient')
    same((D-c-3*z-2*P+v-1)-(D-6*M+2*c+v-1),
         3*(c-z)+2*(3*(M-c)-P),'positive v coefficient')
    print('PASS symbolic identities, both scalar branches, and common-mode certificates')

def connected(adj, subset=None):
    subset=set(range(len(adj))) if subset is None else set(subset)
    if not subset:return True
    todo=[min(subset)];seen=set(todo)
    for i in todo:
        for j in sorted(adj[i]):
            if j in subset and j not in seen:seen.add(j);todo.append(j)
    return seen==subset

def face_structure(faces):
    assert len(faces)==22 and len(set(faces))==22
    assert all(tuple(sorted(set(f)))==f and len(f)==3 for f in faces)
    ef={}
    for j,f in enumerate(faces):
        for e in combinations(f,2):ef.setdefault(e,[]).append(j)
    assert len(ef)==33 and all(len(js)==2 for js in ef.values())
    dual=[set() for _ in faces]
    for j,k in ef.values():dual[j].add(k);dual[k].add(j)
    assert connected(dual)
    assert set().union(*map(set,faces))==set(range(13))
    degrees=[sum(i in e for e in ef) for i in range(13)]
    assert max(degrees)==6
    # Every vertex link is a single cycle, and Euler characteristic is 2.
    for i in range(13):
        link={}
        for f in faces:
            if i in f:
                a,b=[v for v in f if v!=i]
                link.setdefault(a,set()).add(b);link.setdefault(b,set()).add(a)
        assert all(len(neis)==2 for neis in link.values())
        todo=[min(link)];seen=set(todo)
        for a in todo:
            for b in link[a]:
                if b not in seen:seen.add(b);todo.append(b)
        assert seen==set(link)
    assert 13-33+22==2
    return ef,dual,degrees

def verify_cut(faces,ef,cycle_edges):
    assert len(cycle_edges)==13
    adj=[set() for _ in faces]
    for e,(j,k) in ef.items():
        if e not in cycle_edges:adj[j].add(k);adj[k].add(j)
    unseen=set(range(22));parts=[]
    while unseen:
        start=min(unseen);order=[start];seen={start}
        for j in order:
            for k in sorted(adj[j]):
                if k not in seen:seen.add(k);order.append(k)
        unseen-=seen;parts.append(seen)
        assert len(order)==11
        assert sum(len(adj[j]) for j in order)==20
        exposed=set(faces[order[0]])
        for j in order[1:]:
            assert len(set(faces[j])-exposed)==1
            exposed.update(faces[j])
        assert exposed==set(range(13))
    assert len(parts)==2
    assert {e for e,(j,k) in ef.items() if (j in parts[0])!=(k in parts[0])}==cycle_edges

def compare_literals(data,args):
    if args.candidate_source:
        source=json.loads(args.candidate_source.read_text())
        d=data['candidate_49243']
        assert source['faces']==d['faces']
        assert [(r['cycle'],F(r['weight'])) for r in source['cuts']]==[(r['cycle'],F(r['weight'])) for r in d['cycles']]
    if args.complex_source:
        text=args.complex_source.read_text()
        parsed={}
        pat=r'^\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*\d+\s*&\s*\d+\s*&\s*\d+\s*&\s*([01]{3})\\\\'
        for m in re.finditer(pat,text,re.M):parsed[int(m[1])]=([int(m[k]) for k in (2,3,4)],m[5])
        assert len(parsed)==22
        assert [parsed[i][0] for i in range(22)]==data['original']['faces']
        assert [parsed[i][1] for i in range(22)]==data['original']['bits']

def check_template(name,data,cert):
    faces=[tuple(f) for f in data['faces']]
    ef,dual,degrees=face_structure(faces);edges=sorted(ef)
    a={e:F(0) for e in edges}
    if 'bits' in data:
        bits=data['bits'];assert len(bits)==22
        for k in range(3):
            cut={e for e,(j,l) in ef.items() if bits[j][k]!=bits[l][k]}
            verify_cut(faces,ef,cut)
            for e in cut:a[e]+=F(1,3)
        ncuts=3
    else:
        assert len(data['cycles'])==20
        assert sum(F(c['weight']) for c in data['cycles'])==1
        for item in data['cycles']:
            cyc=item['cycle'];wt=F(item['weight']);assert wt>0
            assert sorted(cyc)==list(range(13))
            cut={tuple(sorted((cyc[j],cyc[(j+1)%13]))) for j in range(13)}
            assert cut<=set(edges)
            verify_cut(faces,ef,cut)
            for e in cut:a[e]+=wt
        ncuts=20
    assert sum(a.values())==13 and min(a.values())>=F(1,3)
    assert all(sum(a[e] for e in edges if i in e)==2 for i in range(13))
    assert all((3*a[e]).denominator==1 for e in edges)
    excess=[a[e]-F(1,3) for e in edges]
    assert sum(excess)==2
    assert cert['edge_order']==[list(e) for e in edges]
    assert list(map(F,cert['coverage']))==[a[e] for e in edges]
    d=[int(3*w) for w in excess]; assert sorted(v for v in d if v)==[1,1,1,1,2]
    # A=144K=L+12 diag(d). Connected edge graph plus positive anchors => SPD.
    size=len(edges);A=[[0]*size for _ in range(size)];edgeadj=[set() for _ in edges]
    for face in faces:
        ix=[edges.index(e) for e in combinations(face,2)]
        for i,j in combinations(ix,2):
            A[i][i]+=1;A[j][j]+=1;A[i][j]-=1;A[j][i]-=1
            edgeadj[i].add(j);edgeadj[j].add(i)
    assert connected(edgeadj)
    for i in range(size):A[i][i]+=12*d[i]
    N=cert['adjugate'];tau=cert['denominator']
    assert isinstance(tau,int) and tau>0
    assert len(N)==size and all(len(row)==size for row in N)
    assert all(isinstance(x,int) for row in N for x in row)
    assert all(N[i][j]==N[j][i] for i in range(size) for j in range(size))
    for i in range(size):
        for j in range(size):
            assert sum(A[i][k]*N[k][j] for k in range(size))==(tau if i==j else 0)
    b=[12-x for x in d];u=[sum(N[i][j]*b[j] for j in range(size)) for i in range(size)]
    Hnum=sum(b[i]*u[i] for i in range(size));assert Hnum>0
    B=cert['strict_bound_B'];margins=[]
    for i in range(size):
        z=B*tau-6*u[i];margin=z*z-36*Hnum*N[i][i]
        assert z>0 and margin>0
        margins.append(margin)
    M=B-1;D=12*M
    assert (cert['M'],cert['D'])==(M,D) and D%2==0 and D>=12
    allowed=[e for e in edges if a[e]==F(1,3)]
    ds=[sum(i in e for e in allowed) for i in range(13)]
    allowedadj=[set() for _ in range(13)]
    for i,j in allowed:allowedadj[i].add(j);allowedadj[j].add(i)
    assert connected(allowedadj) and len(allowed)==28
    base=sum(t*t for t in ds)-3*len(allowed)
    r1=base+11;r2=F(base,2)+33
    assert D>=r1 and D>=2*r2-r1
    assert (r1,r2)==(cert['nondirect_remainder'],F(cert['higher_defect_ratio']))
    assert cert['singular_prefactor_power_of_two']==22*D+2450
    assert cert['matrix_singular_prefactor_power_of_two']==22*D+2683
    # No exponent-sized power, finite field, host, or kernel is constructed.
    print(f'PASS {name}: cuts={ncuts}; 33x33 integer inverse certificate; B={B}, M<={M}, even D={D}')
    print(f'  allowed degrees={ds}; nondirect remainder={r1}; higher-defect ratio={r2}')
    print(f'  unsigned error <= 2^{22*D+2450} ({D+1})^231 q^(-1/6), q>=3')
    print(f'  signed-chart singular error <= 2^{22*D+2683} ({D+1})^231 q^(-1/6), q>=2D')
    return {'template':name,'M':M,'D':D,'non_direct_saving':D-r1,'min_certificate_margin':str(min(margins))}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--candidate-source',type=Path)
    parser.add_argument('--complex-source',type=Path)
    args=parser.parse_args()
    data=json.loads((args.directory/'template_data.json').read_text())
    certs=json.loads((args.directory/'certificates.json').read_text())
    compare_literals(data,args)
    check_symbolic()
    result=[check_template(name,data[name],certs['templates'][name]) for name in ('original','candidate_49243')]
    print('PASS all-D proof certificates and both finite input certificates; no bounded-D sweep')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
