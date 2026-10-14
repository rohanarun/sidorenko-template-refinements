"""Independent small-field stress audit; imports no supplied programs.

All instantiated fields are F_3. The theorem's field/order stay symbolic.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json

Q = 3
HERE = Path(__file__).resolve().parent.parent

def rr(rows, n):
    a = [[x % Q for x in r] for r in rows]
    k = 0
    for j in range(n):
        p = next((i for i in range(k, len(a)) if a[i][j]), None)
        if p is None: continue
        a[k], a[p] = a[p], a[k]
        z = pow(a[k][j], -1, Q)
        a[k] = [(x*z) % Q for x in a[k]]
        for i in range(len(a)):
            if i != k and a[i][j]:
                z = a[i][j]
                a[i] = [(x-z*y) % Q for x,y in zip(a[i],a[k])]
        k += 1
        if k == len(a): break
    return tuple(tuple(r) for r in a[:k])

def spaces(n, k):
    for piv in combinations(range(n), k):
        cells = [(i,j) for i in range(k) for j in range(piv[i]+1,n) if j not in piv]
        for values in product(range(Q), repeat=len(cells)):
            a = [[int(j == piv[i]) for j in range(n)] for i in range(k)]
            for (i,j),v in zip(cells,values): a[i][j] = v
            yield tuple(tuple(r) for r in a)

def omega(a,b):
    d = len(a)//2
    return sum(a[i]*b[d+i]-a[d+i]*b[i] for i in range(d)) % Q

def annihilator(rows,n):
    a=rr(rows,n); piv=[next(i for i,x in enumerate(r) if x) for r in a]
    out=[]
    for j in range(n):
        if j in piv: continue
        x=[int(i==j) for i in range(n)]
        for r,p in zip(a,piv): x[p]=(-r[j]) % Q
        out.append(tuple(x))
    return rr(out,n)

def pop(x): return bin(x).count('1')
def b(x): return x*(x+1)//2

def full_gain(dimension,c,h):
    r=dimension//2; d=dimension-c; s=[x-c for x in h]
    possible=[]
    if min(s)<0 or sum(s)>d: return None
    for u in range(min(c,r)+1):
        rp=r-u; delta=2*u-c
        if not 0<=rp<=d: continue
        assert delta==d-2*rp
        for p in product(*(range(x+1) for x in s)):
            t=[s[i]-p[i] for i in range(3)]
            if any(t[i]>p[i]+delta for i in range(3)): continue
            P=sum(p)
            for v in range(min(p)+delta+1):
                w=(d-3*delta)//2-P+v
                if w<0: continue
                g=(r+c+1)*u-2*u*u+sum(b(x) for x in s)-delta*P-sum(x*x for x in p)-v*w-sum(b(x) for x in t)+b(v)
                possible.append(g)
    return max(possible) if possible else None

def orbit_and_planted():
    d=2
    lag=[x for x in spaces(4,2) if omega(x[0],x[1])==0]
    assert len(lag)==40
    ids={x:i for i,x in enumerate(lag)}
    vectors=list(product(range(Q),repeat=4)); vid={v:i for i,v in enumerate(vectors)}
    masks=[]
    for rows in lag:
        mask=0
        for coeff in product(range(Q),repeat=2):
            x=tuple(sum(coeff[k]*rows[k][j] for k in range(2)) % Q for j in range(4))
            mask|=1<<vid[x]
        masks.append(mask)
    dims={1:0,3:1,9:2}
    cap=[[dims[pop(x&y)] for y in masks] for x in masks]
    neighbors=[sum(1<<j for j in range(40) if cap[i][j]==1) for i in range(40)]
    assert {pop(x) for x in neighbors}=={12}
    perms=[]
    for (v,) in spaces(4,1):
        perm=[]
        for rows in lag:
            tr=[tuple((x[j]+omega(x,v)*v[j]) % Q for j in range(4)) for x in rows]
            perm.append(ids[rr(tr,4)])
        assert len(set(perm))==40
        perms.append(perm)
    def profile(a,b_,c_):
        common=dims[pop(masks[a]&masks[b_]&masks[c_])]
        return (common,cap[b_][c_],cap[c_][a],cap[a][b_])
    visited=bytearray(40**3); rows=[]; profiles=defaultdict(list)
    planted_mass=F(0)
    gain_cache={}
    for seed in range(40**3):
        if visited[seed]: continue
        a,tail=divmod(seed,1600); b_,c_=divmod(tail,40)
        pr=profile(a,b_,c_); centers=pop(neighbors[a]&neighbors[b_]&neighbors[c_])
        queue=[seed]; visited[seed]=1
        for code in queue:
            aa,t=divmod(code,1600);bb,cc=divmod(t,40)
            assert profile(aa,bb,cc)==pr
            assert pop(neighbors[aa]&neighbors[bb]&neighbors[cc])==centers
            for p in perms:
                k=1600*p[aa]+40*p[bb]+p[cc]
                if not visited[k]: visited[k]=1;queue.append(k)
        c,*h=pr; cost=3*c+sum(b(x-c) for x in h)
        mass=F(len(queue),40**3)
        assert mass>=F(1,2**17*3**cost)
        factor=F(centers*40**2,12**3)
        g=full_gain(2,c,h)
        if g is None: assert centers==0
        else: assert factor<=2**49*3**5*F(3)**g
        planted_mass+=mass*factor
        row={'profile':pr,'size':len(queue),'cost':cost,'center_count':centers,'gain':g,'planted_factor':str(factor)}
        rows.append(row); profiles[pr].append(row)
    assert all(visited) and planted_mass==1
    for pr,os in profiles.items():
        c,*h=pr; z=2-c-sum(x-c for x in h)
        assert len(os)==(2 if z else 1),(pr,z,len(os))
        assert sum(F(x['size'],40**3) for x in os)<=128*F(3)**(-os[0]['cost'])
    # Verify all actual reduced tuples for planting at one fixed center.
    center=0; near=[i for i in range(40) if cap[i][center]==1]; tuples=Counter()
    def basis(mask): return rr([vectors[i] for i in range(81) if mask>>i&1],4)
    for abc in product(near,repeat=3):
        c,*h=profile(*abc); common=masks[abc[0]]&masks[abc[1]]&masks[abc[2]]
        C=basis(common); u=dims[pop(common&masks[center])]
        R=[rr(list(basis(masks[i]&masks[center]))+list(C),4) for i in abc]
        p=[]
        for j,k in [(1,2),(2,0),(0,1)]:
            p.append(len(R[j])+len(R[k])-len(rr(list(R[j])+list(R[k]),4))-c)
        t=[h[i]-c-p[i] for i in range(3)]
        delta=2*u-c; v=2-len(rr([x for s in R for x in s],4))
        w=(2-c-3*delta)//2-sum(p)+v
        assert 0<=u<=min(c,1) and 0<=1-u<=2-c
        assert all(0<=t[i]<=p[i]+delta and 0<=v<=p[i]+delta for i in range(3))
        assert sum(p)+sum(t)<=2-c and w>=0
        tuples[(c,u,tuple(p),tuple(t),v)]+=1
    return {'q':3,'D':2,'lagrangians':40,'ordered_triples':40**3,'symplectic_transvection_generators':len(perms),'individual_orbits':len(rows),'profiles':len(profiles),'actual_planted_tuples':12**3,'distinct_planted_tuples':len(tuples),'orbits':rows}

def difference_image():
    lines=list(spaces(3,1)); assert len(lines)==13
    checked=0; profiles=Counter(); lift_checks=0
    for abc in product(range(13),repeat=3):
        if abc[0]==abc[1]==abc[2]: continue
        R=[lines[x] for x in abc]
        A=[annihilator(x,3) for x in R]
        V=annihilator([r[0] for r in R],3)
        targets=[]; forms=[]; qs=[]
        for j,k in [(1,2),(2,0),(0,1)]:
            qq=annihilator(list(R[j])+list(R[k]),3);qs.append(qq)
            for x,y in combinations(range(len(qq)+1),2):
                y-=1  # Enumerate (0,0),(0,1),(1,1) for a two-space.
                row=[0]*9
                for idx,sgn in [(j,1),(k,-1)]:
                    piv=[next(i for i,a in enumerate(r) if a) for r in A[idx]]
                    v1=[qq[x][p] for p in piv];v2=[qq[y][p] for p in piv]
                    coeff=[v1[0]*v2[0],v1[0]*v2[1]+v1[1]*v2[0],v1[1]*v2[1]]
                    for t,val in enumerate(coeff): row[3*idx+t]=sgn*val % Q
                targets.append(row)
        expected=sum(b(len(x)) for x in qs)-b(len(V))
        assert len(rr(targets,9))==expected,(abc,expected)
        profiles[(tuple(map(len,qs)),len(V),expected)]+=1
        # One independently chosen lift triple for each subspace triple.
        ff=[(abc[0]+2*abc[1]+t*abc[2]+t*t+1)%Q for t in range(9)]
        lifts=[]
        for i in range(3):
            mat=[[ff[3*i],ff[3*i+1]],[ff[3*i+1],ff[3*i+2]]]
            piv=[next(j for j,x in enumerate(row) if x) for row in A[i]]
            rows=[tuple(R[i][0])+(0,0,0)]
            for k,zeta in enumerate(A[i]):
                y=[0]*3
                for t,p in enumerate(piv): y[p]=mat[k][t]
                rows.append(tuple(y)+tuple(zeta))
            rows=rr(rows,6);assert len(rows)==3
            assert all(omega(x,y)==0 for x,y in combinations(rows,2))
            lifts.append(rows)
        offset=0
        for i,(j,k) in enumerate([(1,2),(2,0),(0,1)]):
            nn=len(qs[i]); vals=[sum(a*z for a,z in zip(row,ff))%Q for row in targets[offset:offset+b(nn)]]
            offset+=b(nn);mat=[[0]*nn for _ in range(nn)]; pos=0
            for x in range(nn):
                for y in range(x,nn): mat[x][y]=mat[y][x]=vals[pos];pos+=1
            null=nn-len(rr(mat,nn))
            p=int(abc[j]==abc[k]); actual=6-len(rr(list(lifts[j])+list(lifts[k]),6))
            assert actual==p+null,(abc,i,actual,p,null)
            lift_checks+=1
        checked+=1
    return {'q':3,'ambient_center_dimension':3,'common_zero_center_line_triples':checked,'cyclic_image_rank_profiles':[[list(a),v,rank,count] for (a,v,rank),count in sorted(profiles.items())],'pair_exact_sequences_checked':lift_checks}

def det(a): return (a[0]*a[2]-a[1]*a[1])%Q
def inv(a):
    z=pow(det(a),-1,Q);return (a[2]*z%Q,-a[1]*z%Q,a[0]*z%Q)
def sub(a,b_): return tuple((x-y)%Q for x,y in zip(a,b_))
def rank_sign(a):
    if not any(a): return 0,1
    if det(a): return 2,1 if det(a)==1 else -1
    v=a[0] or a[2]
    assert v
    return 1,1 if v==1 else -1

def half_rank_centers():
    mats=list(product(range(3),repeat=3)); counts=Counter(rank_sign(x) for x in mats)
    assert counts[(1,1)]==counts[(1,-1)]==4
    lines=[x[0] for x in spaces(2,1)]
    triples=0; signs_checked=0
    c0=-1
    for B0,B1 in product(mats,repeat=2):
        if not det(B0) or not det(B1) or not det(sub(B1,B0)): continue
        L=sub(inv(B0),inv(B1));QQ=inv(B0)
        assert det(L)
        eta=[rank_sign(B0)[1],rank_sign(B1)[1],rank_sign(sub(B1,B0))[1]]
        for signs in product([-1,1],repeat=3):
            actual=sum(rank_sign(A)==(1,signs[0]) and rank_sign(sub(A,B0))==(1,signs[1]) and rank_sign(sub(A,B1))==(1,signs[2]) for A in mats)
            matches=(eta==[c0*signs[0]*signs[1],c0*signs[0]*signs[2],c0*signs[1]*signs[2]])
            predicted=0
            if matches:
                assert rank_sign(L)[1]==c0
                for x,y in lines:
                    iso=(L[0]*x*x+2*L[1]*x*y+L[2]*y*y)%Q
                    val=(QQ[0]*x*x+2*QQ[1]*x*y+QQ[2]*y*y)%Q
                    if iso==0 and val and (1 if val==1 else -1)==signs[0]: predicted+=1
            assert actual==predicted,(B0,B1,signs,actual,predicted)
            signs_checked+=1
        triples+=1
    return {'q':3,'D':2,'symmetric_matrices':27,'rank_sign_counts':[[list(k),v] for k,v in sorted(counts.items())],'translated_transverse_triples':triples,'signed_center_counts':signs_checked}

if __name__=='__main__':
    out={'ordered_orbits_and_planted':orbit_and_planted(),'correlated_difference_image':difference_image(),'half_rank_centers':half_rank_centers(),'huge_field_or_host_materialized':False}
    (HERE/'own-geometry-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:{a:b_ for a,b_ in v.items() if a not in ['orbits','cyclic_image_rank_profiles']} if isinstance(v,dict) else v for k,v in out.items()},indent=2))
