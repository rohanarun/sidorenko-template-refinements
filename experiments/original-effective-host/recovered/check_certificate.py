#!/usr/bin/env python3
"""Exact finite checks for the original Sidorenko template.

This is newly written, standard-library-only code. It never downloads, imports,
or executes repository code, and never constructs the large field or host.
The universal inequalities are proved in PROOF.md, not inferred from sampling.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import gcd, lcm
from pathlib import Path
import hashlib
import json
import re
import zipfile

FACES = [[0,1,3],[0,1,9],[0,2,3],[0,2,9],[1,3,10],[1,7,10],
         [1,7,12],[1,9,12],[2,3,4],[2,4,9],[3,4,11],[3,10,11],
         [4,8,9],[4,8,11],[5,6,7],[5,6,11],[5,7,10],[5,10,11],
         [6,7,12],[6,8,11],[6,8,12],[8,9,12]]
BITS = ['000','010','001','110','001','000','100','110','101','100',
        '111','101','101','011','000','110','010','111','001','010','011','111']
ORDERS = [[0,1,2,4,5,16,14,18,20,19,13], [3,9,8,10,11,17,15,12,21,7,6],
          [0,2,8,9,12,4,11,5,6,18,14], [1,3,7,21,20,19,13,10,15,17,16],
          [0,1,3,9,7,6,5,16,14,15,19], [2,8,10,11,4,17,13,12,21,20,18]]
EXPECTED = dict(tau=821810346672, Hnum=7702171993838184,
    first_margin=327514878189744, square_margin=419595924675382839454010976,
    max_a=127937502468, max_b=20679552, E_id=115295183886,
    B_pin=1548347298342, Z=3807386006623258, A0=53303404092753965)

def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)

class Poly:
    """Sparse rational polynomials; monomials are sorted (variable,power) pairs."""
    def __init__(self, x=0):
        if isinstance(x, Poly): self.a=dict(x.a)
        elif isinstance(x, dict): self.a={m:F(v) for m,v in x.items() if v}
        else: self.a={():F(x)} if x else {}
    @staticmethod
    def var(s): return Poly({((s,1),):F(1)})
    def __add__(self, other):
        out=dict(self.a)
        for m,c in Poly(other).a.items(): out[m]=out.get(m,F(0))+c
        return Poly(out)
    __radd__=__add__
    def __neg__(self): return Poly({m:-c for m,c in self.a.items()})
    def __sub__(self, other): return self+-Poly(other)
    def __rsub__(self, other): return Poly(other)+-self
    def __mul__(self, other):
        out=defaultdict(F)
        for m,c in self.a.items():
            for n,d in Poly(other).a.items():
                e=Counter(dict(m)); e.update(dict(n))
                out[tuple(sorted(e.items()))]+=c*d
        return Poly(out)
    __rmul__=__mul__
    def __truediv__(self, other): return self*F(1,other)
    def __pow__(self, k):
        require(isinstance(k,int) and k>=0,'invalid polynomial power')
        out=Poly(1)
        for _ in range(k): out=out*self
        return out
    def sub(self, substitutions):
        out=Poly(0)
        for m,c in self.a.items():
            term=Poly(c)
            for s,k in m: term*=Poly(substitutions.get(s,Poly.var(s)))**k
            out+=term
        return out

def polynomial_checks():
    V=Poly.var
    c,d,z,v=map(V,['c','d','delta','v'])
    p=[V('p'+str(i)) for i in range(3)]
    t=[V('t'+str(i)) for i in range(3)]
    P,T=sum(p),sum(t); s=[p[i]+t[i] for i in range(3)]
    b=lambda x:x*(x+1)/2
    D=d+c; r=D/2; u=(z+c)/2; w=(d-3*z)/2-P+v
    beta=((D+1)*c+sum(b(x) for x in s))/2-sum(b(c+x) for x in s)/6
    gain=(r+c+1)*u-2*u*u+sum(b(x) for x in s)-z*P-sum(x*x for x in p)-v*w-sum(b(x) for x in t)+b(v)
    S=(c*(d+z-1)-z*(d+2)+2*z*z)/4+sum((2*p[i]-t[i])*(2*p[i]-t[i]-1)/6+z*p[i]-c*s[i]/6 for i in range(3))+v*w-b(v)
    L=c/4+z/2+(2*P-T)/6+v/2
    Q=(c*(d+z)-z*d+2*z*z)/4+sum((2*p[i]-t[i])**2/6+z*p[i]-c*s[i]/6 for i in range(3))+v*((d-3*z)/2-P)+v*v/2
    k=(c-z)/2; nn=[2*p[i]-t[i] for i in range(3)]
    S0=3*c*(c-1)/4+sum(nn[i]**2+(c-1)*nn[i]+3*c*p[i] for i in range(3))/6
    identities={
      'source_gain_to_exact_slack':beta-gain-S,
      'quadratic_linear_split':S-Q+L,
      'mode_removal':S-S0-k*(d-3*c-2*z+2-4*P)/2-v*(d-3*z-2*P+v-1)/2,
      'S0_square_completion':S0-(c-1)*(5*c+1)/8-sum((a+(c-1)/2)**2 for a in nn)/6-c*P/2,
      'linear_loss':(3*c+P+T)/2-L-(c/4+c-z+2*T/3+(P/3+z-v)/2),
      'edge_energy':2*(P+T)**2-sum((s[i]-s[j])**2 for i,j in combinations(range(3),2))-6*sum(s[i]*s[j] for i,j in combinations(range(3),2)),
      'common_gain':3*(b(r)-b(r-u))-u*(D-c)-b(u)-((r+c+1)*u-2*u*u),
    }
    M=V('M')
    identities['first_mode_bracket']=(d-3*c-2*z+2-4*P)-(D-12*M+6*c+2)-(2*(c-z)+4*(3*(M-c)-P))
    identities['second_mode_bracket']=(d-3*z-2*P+v-1)-(D-6*M+2*c+v-1)-(3*(c-z)+2*(3*(M-c)-P))
    a,x,y,R=map(V,['a','x','y','R'])
    z=V('delta'); T=V('T')
    bp=a/3+z; ep=a+3*z; ell=ep-bp
    Hp1=3*z*z/4+(2*a-T)**2/18+(5*a-T)*z/6-(a/3+z)**2/2-(a+T)**2/72
    Hp2=3*z*z/4+(2*a-T)**2/18+(5*a-T)*z/6-((a-T+3*z)/2)**2/2-(a+T)**2/72
    hbp=(4*a+3*z)*(4*a+9*z)/216; hep=z*(4*a+15*z)/24
    identities['positive_delta_first_interval']=Hp1.sub({'T':bp-R})-hbp-R*(16*a/3+2*z+R)/24
    identities['positive_delta_chord']=ell*Hp2-(ep-T)*hbp-(T-bp)*hep-ell*(T-bp)*(ep-T)/12
    bm=x/3; em=x; ellm=em-bm
    Hm1=y*y/4+(2*x-T)*y/3+(2*x-T)**2/18-(x/3)**2/2-(x+3*y+T)**2/72
    Hm2=y*y/4+(2*x-T)*y/3+(2*x-T)**2/18-((x-T)/2)**2/2-(x+3*y+T)**2/72
    hbm=(16*x*x+96*x*y+27*y*y)/216; hem=y*(4*x+3*y)/24
    identities['negative_delta_first_interval']=Hm1.sub({'T':bm-R})-hbm-R*(16*x/3+10*y+R)/24
    identities['negative_delta_chord']=ellm*Hm2-(em-T)*hbm-(T-bm)*hem-ellm*(T-bm)*(em-T)/12
    h,k=V('h'),V('k')
    identities['two_active_even']=b(2*k)/3-b(k)-k*(k-1)/6
    identities['two_active_odd']=b(2*k+1)/3-b(k)-(k+1)*(k+2)/6
    # Lower-activity beta inequality, with s0 the largest reduced pair dimension.
    c,d=V('c'),V('d'); ss=[V('s'+str(i)) for i in range(3)]
    bet=((c+d+1)*c+sum(b(x) for x in ss))/2-sum(b(c+x) for x in ss)/6
    rhs=b(c+ss[0])/3+b(c)/6+(b(ss[1])+b(ss[2]))/3
    # Expanded difference is nonnegative because d >= sum(ss), c>=0.
    identities['lower_activity_beta']=bet-rhs-c*(3*d-3*ss[0]-ss[1]-ss[2])/6
    for name,expr in identities.items():
        require(not expr.a, f'polynomial identity failed: {name}: {expr.a}')
    return sorted(identities)

def inverse(a):
    n=len(a)
    rows=[[F(x) for x in a[i]]+[F(i==j) for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot=next((i for i in range(col,n) if rows[i][col]),None)
        require(pivot is not None,'singular energy matrix')
        rows[col],rows[pivot]=rows[pivot],rows[col]
        scale=rows[col][col]; rows[col]=[x/scale for x in rows[col]]
        for i in range(n):
            if i!=col and rows[i][col]:
                fac=rows[i][col]; rows[i]=[x-fac*y for x,y in zip(rows[i],rows[col])]
    return [row[n:] for row in rows]

def template_checks():
    require(len(FACES)==22 and len(set(map(tuple,FACES)))==22,'face count')
    edge_faces=defaultdict(list)
    for j,f in enumerate(FACES):
        require(len(f)==3 and f==sorted(set(f)),'invalid face')
        for e in combinations(f,2): edge_faces[e].append(j)
    edges=sorted(edge_faces)
    require(len(edges)==33 and all(len(v)==2 for v in edge_faces.values()),'pair multiplicities')
    ei={e:i for i,e in enumerate(edges)}
    rho3=[]
    for e in edges:
        j,k=edge_faces[e]; rho3.append(sum(a!=b for a,b in zip(BITS[j],BITS[k]))-1)
    require(min(rho3)>=0 and sum(rho3)==6,'coverage/excess')
    lap=[[0]*33 for _ in range(33)]
    for f in FACES:
        face_edges=[ei[e] for e in combinations(f,2)]
        for a,b in combinations(face_edges,2):
            lap[a][a]+=1;lap[b][b]+=1;lap[a][b]-=1;lap[b][a]-=1
    seen={0}
    while True:
        new=seen|{j for i in seen for j in range(33) if i!=j and lap[i][j]}
        if new==seen: break
        seen=new
    require(len(seen)==33,'disconnected coordinate Laplacian')
    exposure=[]
    for index,order in enumerate(ORDERS):
        bit,value=divmod(index,2)
        require(set(order)=={j for j in range(22) if int(BITS[j][bit])==value},'exposure class')
        old=set(FACES[order[0]]); previous=[set(FACES[order[0]])]; added=[]
        for j in order[1:]:
            f=set(FACES[j]);new=f-old
            require(len(new)==1 and any(len(f&g)==2 for g in previous),'invalid fresh-point exposure')
            old|=f;previous.append(f);added.append(next(iter(new)))
        require(old==set(range(13)) and len(order)==11,'exposure coverage')
        exposure.append(added)
    degrees=[sum(i in e for e in edges) for i in range(13)]
    require(max(degrees)==6,'joint-sign degree bound')
    allowed=[e for e,a in zip(edges,rho3) if not a]
    deg0=[sum(i in e for e in allowed) for i in range(13)]
    require(len(allowed)==28 and sum((2*x)*(2*x-1)//2 for x in deg0)==468,'nondirect count cap')
    corners=sorted((i,j) for j,f in enumerate(FACES) for i in f)
    ci={c:k for k,c in enumerate(corners)}
    U=[]
    for e in edges:
        U.append(sum(1<<ci[(i,j)] for i in e for j in edge_faces[e]))
    M={};Gamma={};corner_edge_indices={}
    for corner in corners:
        i,j=corner
        idx=[ei[tuple(sorted((i,k)))] for k in FACES[j] if k!=i]
        a,b=idx; require((U[a]&U[b])==1<<ci[corner],'corner overlap')
        M[corner]=U[a]|U[b];Gamma[corner]=U[a]^U[b]
        require(M[corner].bit_count()==7 and Gamma[corner].bit_count()==6,'activation sizes')
        corner_edge_indices[corner]=idx
    for k,e in enumerate(edges):
        inter=(1<<66)-1
        for c in corners:
            if U[k]&(1<<ci[c]): inter&=M[c]
        require(inter==U[k],f'identity support forcing: {e}')
    a=[[lap[i][j]+(12*rho3[i] if i==j else 0) for j in range(33)] for i in range(33)]
    inv=inverse(a); tau=lcm(*(x.denominator for row in inv for x in row))
    N=[[int(x*tau) for x in row] for row in inv]
    require(tau==EXPECTED['tau'],'energy denominator differs')
    verify_inverse(a,N,tau)
    bvec=[12-x for x in rho3]
    u=[sum(x*y for x,y in zip(row,bvec)) for row in N]
    Hnum=sum(x*y for x,y in zip(bvec,u))
    margin1=[609*tau-6*x for x in u]
    margin2=[margin1[i]**2-36*Hnum*N[i][i] for i in range(33)]
    require(Hnum==EXPECTED['Hnum'] and min(margin1)==EXPECTED['first_margin'] and min(margin2)==EXPECTED['square_margin'],'coordinate certificate mismatch')
    require(min(margin1)>0 and min(margin2)>0,'coordinate bound not strict')
    return dict(faces=FACES,bits=BITS,exposure_orders=ORDERS,exposure_new_points=exposure,
                point_edges=[list(e) for e in edges],rho_times_3=rho3,point_degrees=degrees,
                allowed_degrees=deg0,corners=[list(c) for c in corners],
                U_masks=U,M_masks=[M[c] for c in corners],Gamma_masks=[Gamma[c] for c in corners],
                A=a,N=N,tau=tau,bvec=bvec,u=u,Hnum=Hnum,
                minimum_first_margin=min(margin1),minimum_square_margin=min(margin2))

def verify_inverse(A,N,tau):
    require(len(A)==len(N)==33 and tau>0,'inverse dimensions')
    require(all(len(row)==33 for row in N),'inverse row dimensions')
    require(all(N[i][j]==N[j][i] for i in range(33) for j in range(33)),'inverse not symmetric')
    for i in range(33):
        for j in range(33):
            require(sum(A[i][k]*N[k][j] for k in range(33))==(tau if i==j else 0),'AN != tau I')

def scores():
    adj=[[] for _ in range(35)]
    for j,f in enumerate(FACES):
        for i in f: adj[i].append(13+j);adj[13+j].append(i)
    colors=[0]*13+[1]*22; vs=[0]*35; ps=[[0]*22 for _ in range(13)]
    histories=[]
    for r in range(4):
        nc=max(colors)+1
        hist=[[sum(colors[w]==k for w in adj[v]) for k in range(nc)] for v in range(35)]
        weight=1856**(3-r)
        for v in range(35): vs[v]-=weight*sum(t*t for t in hist[v])
        for i in range(13):
            for j in range(22): ps[i][j]+=weight*2*(hist[i][colors[13+j]]+hist[13+j][colors[i]])
        sig=[(colors[v],tuple(hist[v])) for v in range(35)]
        canon={s:k for k,s in enumerate(sorted(set(sig)))};colors=[canon[s] for s in sig]
        histories.append([len(set(colors[:13])),len(set(colors[13:]))])
    require(histories==[[3,1],[3,7],[13,7],[13,22]],'refinement histories')
    aa=[x-min(vs[:13]) for x in vs[:13]]; bb=[x-min(vs[13:]) for x in vs[13:]]
    mx=max(x for row in ps for x in row); ell=[[mx-x for x in row] for row in ps]
    Eid=sum(aa)+sum(bb)-sum(ell[i][j] for j,f in enumerate(FACES) for i in f)
    Bpin=13*max(aa)+22*max(bb)-Eid
    computed=dict(max_a=max(aa),max_b=max(bb),E_id=Eid,B_pin=Bpin)
    require(all(computed[k]==EXPECTED[k] for k in computed),'pinning exponent data')
    require(13**13*22**22<2**147,'all-maps count bound')
    # A first failing refinement round has score loss >=1. Later losses cannot undo it.
    for k in range(4): require(1856**k-1854*sum(1856**j for j in range(k))>=1,'lexicographic dominance')
    return dict(vertex_scores=vs,pair_scores=ps,a=aa,b=bb,ell=ell,round_class_counts=histories,**computed)

def activation_checks():
    M=127;G=126;U=15;V=113;count=0
    for sigma in [-1,1]:
        dist=[]
        for neg in range(128):
            parity=(-1)**((neg&G).bit_count())
            dist.append((M,neg,F(2+sigma*parity,512)))
        for mask in range(64):
            neg=mask<<1;parity=(-1)**neg.bit_count()
            dist.append((G,neg,F(2-sigma*parity,256)))
        require(sum(w for _,_,w in dist)==1 and all(w>0 for _,_,w in dist),'activation probability law')
        # Compute both branch Fourier transforms directly from the enumerated probabilities.
        fm=[sum(w*((-1)**((neg&R).bit_count())) for S,neg,w in dist if S==M) for R in range(128)]
        fg=[sum(w*((-1)**((neg&R).bit_count())) for S,neg,w in dist if S==G) for R in range(128)]
        for R in range(128):
            require(fm[R]==F(R==0,2)+F(sigma*(R==G),4),'full-branch Fourier transform')
        for R in range(128):
            if not R&1: require(fg[R]==F(R==0,2)-F(sigma*(R==G),4),'punctured-branch Fourier transform')
        for A in range(1,128):
            actual=fm[A]+(fg[A] if A&G==A else 0)
            require(actual==0,'nonempty first moment');count+=1
        for Q in range(128):
            R=Q
            while True:
                actual=fm[R]+(fg[R] if Q&G==Q else 0)
                formula=F(R==0,2)+F(sigma*(R==G),4)
                if Q&G==Q: formula+=F(R==0,2)-F(sigma*(R==G),4)
                require(actual==formula,'overlap moment identity');count+=1
                if R==0:break
                R=(R-1)&Q
        Q=U|V;R=U^V
        actual=sum(w*((-1)**((neg&R).bit_count())) for S,neg,w in dist if Q&S==Q)
        require(actual==F(sigma,4),'identity signed corner factor')
    return count

def parameters(sc):
    D=7296;r=D//2;bD=D*(D+1)//2
    Z=280+2459*sc['B_pin']; A0=14*Z+28353; Lambda=A0+1
    require(Z==EXPECTED['Z'] and A0==EXPECTED['A0'],'margin exponents')
    EJ=A0+241071; EQ=6*EJ+1; Fq=EQ+1
    S=66*14*bD; B=11+Lambda+S*Fq
    ell_max=max(max(row) for row in sc['ell'])
    L_atom=Z+2181+9+2459*(sc['max_a']+sc['max_b'])+132*bD*Fq
    L_coin=18+4918*ell_max+42*bD*Fq
    require(12*608==D and D%2==r%2==0,'dimension/reversal')
    require(14*bD==372672384 and S==24596377344,'scaling exponents')
    # Exponent domination in the rank-layer estimate, both terms separately <= C_D/2.
    require((22*D+1421)+(165*13)+1 <= 32*D+2048,'tail constant envelope')
    require(170+13+1<=32*D+2048,'transverse constant envelope')
    require(2**11>1322 and 2**11-661>1024,'fixed host margin')
    return dict(D=D,r=r,bD=bD,C_power_of_two=32*D+2048,C_polynomial_power=256,
                A_D_power_of_two=D+47,A_D_polynomial_power=5,Z=Z,epsilon_exponent=Z+2181,
                A0=A0,Lambda=Lambda,rank_error_exponent_denominator=6,
                H_coordinate_power_of_two=2210,J_power_of_two=A0+6+2210+32*D+2048,
                J_multiplier=66,J_polynomial_base=D+1,J_polynomial_power=256,
                Q_addend=16*D,J_log2_upper=EJ,Q_log2_upper=EQ,q_log2_upper=Fq,
                kernel_scale_exponent=14*bD,kernel_gap_q_exponent=S,
                fixed_host_log2_order=B,fixed_gap_exponent=B-10,
                ell_max=ell_max,source_atom_denominator_log2_upper=L_atom,
                source_coin_denominator_log2_upper=L_coin,
                source_normalizer_enumeration_log2_upper=bD*Fq,
                fixed_host_acceptance='(2*edges)^66 - hom(H,G)*N^97 >= 1024*N^131')

def archive_audit(path):
    raw=Path(path).read_bytes();z=zipfile.ZipFile(Path(path));manifest=json.loads(z.read('MANIFEST.json'))
    seen=[]
    for f in manifest['files']:
        b=z.read(f['archive_path'])
        require(len(b)==f['bytes'],'archive length mismatch')
        require(hashlib.sha256(b).hexdigest()==f['sha256'],'archive sha256 mismatch')
        blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        require(blob==f['git_blob_sha1'],'archive git blob mismatch')
        if f.get('expected_git_blob_sha1'):require(blob==f['expected_git_blob_sha1'],'archive expected blob mismatch')
        seen.append(f['archive_path'])
    matches=[name for name in z.namelist() if any(k in name.lower() for k in ['sidorenko','/161.','template-refinements'])]
    return dict(sha256=hashlib.sha256(raw).hexdigest(),zip_entries=len(z.namelist()),
                manifest_entries_checked=len(seen),group_counts=manifest['counts'],sidorenko_entries=matches)


def rank_mod(rows, prime):
    """Rank of a small row matrix by exact elimination in a prime field."""
    if not rows:
        return 0
    a = [[int(x) % prime for x in row] for row in rows]
    width = len(a[0])
    require(all(len(row) == width for row in a), 'ragged matrix')
    rank = 0
    for col in range(width):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], -1, prime)
        a[rank] = [(x * inv) % prime for x in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][col]:
                factor = a[i][col]
                a[i] = [(x - factor*y) % prime for x,y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def refinement_obstruction_checks(tc):
    """Small realizable configuration; it is not a small Sidorenko host."""
    q = 13
    D = 4
    e = [[int(i == j) for j in range(2*D)] for i in range(D)]
    f = [[int(i+D == j) for j in range(2*D)] for i in range(D)]
    add = lambda x,y: [(a+b) % q for a,b in zip(x,y)]
    spaces = {1: e, 0: [e[0], e[1], f[2], f[3]],
              7: [e[0], f[1], e[2], add(e[3],f[3])]}
    for i, lam in zip([i for i in range(13) if i not in spaces], range(2,12)):
        spaces[i] = [[(a + lam*b) % q for a,b in zip(e[t],f[t])] for t in range(D)]
    def symplectic(x,y):
        return sum(x[t]*y[D+t] - x[D+t]*y[t] for t in range(D)) % q
    for i, rows in spaces.items():
        require(rank_mod(rows,q) == D, 'Lagrangian dimension')
        require(all(symplectic(x,y) == 0 for x in rows for y in rows), 'isotropy')
    intersections = {}
    for i,j in combinations(range(13),2):
        dim = 2*D - rank_mod(spaces[i]+spaces[j],q)
        expected = {(0,1):2,(1,7):2,(0,7):1}.get((i,j),0)
        require(dim == expected, 'explicit pair intersection')
        intersections[(i,j)] = dim
    edge_set = {tuple(e) for e in tc['point_edges']}
    require((0,7) not in edge_set, 'extra intersection must be off the point graph')
    rho = {tuple(e): (sum(a != b for a,b in zip(BITS[js[0]], BITS[js[1]]))-1)
           for e in edge_set
           for js in [[j for j, face in enumerate(FACES) if set(e).issubset(face)]]}
    require(rho[(0,1)] == rho[(1,7)] == 0, 'example uses positive-excess edge')
    # A transverse pair in every face forces its common intersection to vanish.
    require(all(any(intersections[tuple(sorted(pair))] == 0
                    for pair in combinations(face,2)) for face in FACES), 'common-zero faces')
    H01, H17 = [e[0],e[1]], [e[0],e[2]]
    require(rank_mod(H01+H17,q) == 3, 'global span dimension')
    require(rank_mod(H01,q) + rank_mod(H01+H17,q) + rank_mod(H17,q) == 7,
            'strict local span defect')
    # Count bases directly in their two coordinates, not via a downloaded enumerator.
    results=[]
    for prime in (3,13):
        bases = 0
        selected = 0
        for a in range(prime):
            for b in range(prime):
                for c in range(prime):
                    for d in range(prime):
                        if (a*d-b*c) % prime:
                            bases += 1
                            if b == 0:  # first vector is in the fixed shared line
                                selected += 1
        require(bases == (prime**2-1)*(prime**2-prime), 'basis enumeration')
        require(selected == (prime-1)*(prime**2-prime), 'selected basis enumeration')
        require(F(selected,bases) == F(1,prime+1), 'pattern basis proportion')
        results.append(dict(q=prime,bases_per_space=bases,selected_second_bases=selected,
                            pattern_bases=bases*selected,full_family_bases=bases*bases,
                            proportion='1/'+str(prime+1)))
    q13=results[1]
    divisor = F(3,8)**2 * 13**8
    require(q13['pattern_bases'] < divisor, 'even source lower multiplicity fails per pattern')
    return dict(status='PASS',geometric_q=q,geometric_D=D,
                positive_point_graph_intersections=[[0,1,2],[1,7,2]],
                extra_nonedge_intersection=[0,7,1],common_dimensions_all_zero=True,
                global_span=3,sum_local_spans=7,basis_counts=results,
                source_lower_divisor_q13_numerator=divisor.numerator,
                source_lower_divisor_q13_denominator=divisor.denominator,
                scope='multiplicity inference obstruction, not refutation of the repaired numerical 189 bound')


def source_literal_check(path, kind):
    raw=Path(path).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    expected={'complex':'178b0e9da21867a727ea847dae8e537b9d719a70',
              'comparator':'3f4fa1074f812e2e823350ea50ff1a786e4a1927'}[kind]
    require(blob==expected,'optional source differs from immutable Git blob')
    text=raw.decode('utf-8')
    if kind=='complex':
        rows=re.findall(r'(?m)^\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&[^\n]*?&\s*([01]{3})\\',text)
        rows=sorted(rows,key=lambda x:int(x[0]))
        require([int(x[0]) for x in rows]==list(range(22)),'source table parse')
        require([[int(x[1]),int(x[2]),int(x[3])] for x in rows]==FACES,'source faces differ')
        require([x[4] for x in rows]==BITS,'source bits differ')
    else:
        block=text.split('def faces',1)[1].split('abbrev PatternVertex',1)[0]
        rows=re.findall(r'\{([0-9,]+)\}',block)
        require([[int(v) for v in x.split(',')] for x in rows]==FACES,'comparator faces differ')
    return {'git_blob_sha1':blob,'literal_comparison':'PASS'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write',action='store_true',help='write the reconstructed small certificates')
    ap.add_argument('--archive',type=Path,help='optional audit of the original upload')
    ap.add_argument('--complex-source',type=Path,help='optional pinned complex.tex literal comparison')
    ap.add_argument('--comparator-source',type=Path,help='optional pinned comparator literal comparison')
    args=ap.parse_args();here=Path(__file__).resolve().parent
    tc=template_checks();sc=scores();ids=polynomial_checks();act=activation_checks();par=parameters(sc)
    cert=dict(template=tc,scores=sc,parameters=par)
    if args.write:
        (here/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
        (here/'template.json').write_text(json.dumps({k:tc[k] for k in ['faces','bits','point_edges','corners','exposure_orders']},indent=2)+'\n')
    elif (here/'certificate.json').exists():
        saved=json.loads((here/'certificate.json').read_text())
        require(saved==cert,'saved certificate differs from independent reconstruction')
    # Deliberately corrupt an inverse entry: the exact matrix identity must reject it.
    bad=[row[:] for row in tc['N']];bad[0][0]+=1
    try:verify_inverse(tc['A'],bad,tc['tau'])
    except ValueError:inverse_mutation=True
    else:raise ValueError('inverse mutation was not detected')
    obstruction=refinement_obstruction_checks(tc)
    report=dict(status='PASS',scope='finite data and exact algebra only; universal proofs are in PROOF.md',
        counts=dict(points=13,faces=22,incidences=66,point_edges=33,exposure_orders=6,
                    matrix_entries=1089,coordinate_bounds=33,activation_identities=act,polynomial_identities=len(ids)),
        polynomial_identities=ids,inverse_mutation_rejected=inverse_mutation,
        refinement_obstruction=obstruction,parameters=par)
    if args.archive:report['archive_audit']=archive_audit(args.archive)
    if args.complex_source:report['complex_source_comparison']=source_literal_check(args.complex_source, 'complex')
    if args.comparator_source:report['comparator_source_comparison']=source_literal_check(args.comparator_source, 'comparator')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
