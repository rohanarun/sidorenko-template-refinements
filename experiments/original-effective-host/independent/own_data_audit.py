"""Own exact template, activation, all-map score and symbolic-size checks.

No imports or execution of the packet's checkers/generator or repository code.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd
from pathlib import Path
import hashlib, json, random, re

P=Path(__file__).resolve().parent.parent
C=json.loads((P/'recovered/certificate.json').read_text())
tpl,sc,pa=C['template'],C['scores'],C['parameters']

def connected(adj):
    seen={0}; todo=[0]
    for v in todo:
        for w in adj[v]:
            if w not in seen: seen.add(w);todo.append(w)
    return len(seen)==len(adj)

def template():
    auth=json.loads((P/'upstream-authentication.json').read_text())
    for record in auth:
        source=P/'upstream'/Path(record['path']).name
        data=source.read_bytes()
        assert hashlib.sha256(data).hexdigest()==record['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==record['git_blob_sha1']
    src=(P/'upstream/complex.tex').read_text()
    table=src.split('\\midrule',1)[1].split('\\bottomrule',1)[0]
    faces=[]; bits=[]
    for line in table.splitlines():
        cells=[x.strip() for x in line.split('&')]
        if len(cells)!=8: continue
        j=int(cells[0]); assert j==len(faces)
        faces.append(tuple(int(x) for x in cells[1:4]))
        bits.append(cells[-1][:3])
    lean=(P/'upstream/SidorenkoCounterexample.lean').read_text()
    block=lean.split('def faces',1)[1].split('abbrev PatternVertex',1)[0]
    lean_faces=[tuple(map(int,x.split(','))) for x in re.findall(r'\{([0-9,]+)\}',block)]
    assert faces==lean_faces and [list(x) for x in faces]==tpl['faces']
    assert bits==tpl['bits'] and len(faces)==22
    pf=defaultdict(list)
    for j,face in enumerate(faces):
        for e in combinations(face,2): pf[e].append(j)
    edges=sorted(pf); corners=sorted((i,j) for j,face in enumerate(faces) for i in face)
    assert len(edges)==33 and len(corners)==66 and all(len(pf[e])==2 for e in edges)
    assert [list(x) for x in edges]==tpl['point_edges']
    assert [list(x) for x in corners]==tpl['corners']
    rho=[sum(x!=y for x,y in zip(bits[pf[e][0]],bits[pf[e][1]]))-1 for e in edges]
    assert rho==tpl['rho_times_3'] and min(rho)>=0 and sum(rho)==6
    ei={e:k for k,e in enumerate(edges)};ci={c:k for k,c in enumerate(corners)}
    face_adj=[set() for _ in faces]; edge_adj=[set() for _ in edges]
    A=[[0]*33 for _ in edges]
    for e in edges:
        j,k=pf[e];face_adj[j].add(k);face_adj[k].add(j)
    for face in faces:
        ids=[ei[e] for e in combinations(face,2)]
        for a,b in combinations(ids,2):
            edge_adj[a].add(b);edge_adj[b].add(a)
            A[a][a]+=1;A[b][b]+=1;A[a][b]-=1;A[b][a]-=1
    assert connected(face_adj) and connected(edge_adj)
    for k,r in enumerate(rho): A[k][k]+=12*r
    assert A==tpl['A']
    source_orders=re.findall(r'^([123])&([01])&\$([0-9,]+)\$',src,re.M)
    assert len(source_orders)==6
    exposure=[]
    for bit,value,text in source_orders:
        order=list(map(int,text.split(','))); pos=2*(int(bit)-1)+int(value)
        assert order==tpl['exposure_orders'][pos]
        assert set(order)=={j for j in range(22) if bits[j][int(bit)-1]==value}
        old=set(faces[order[0]]);prev={order[0]};introduced=[]; shared=[]
        for j in order[1:]:
            new=set(faces[j])-old;assert len(new)==1
            ee=[e for e in combinations(faces[j],2) if any(k in prev for k in pf[e] if k!=j)]
            assert len(ee)==1
            shared.append(ee[0]);introduced.append(next(iter(new)))
            old.update(faces[j]);prev.add(j)
        assert len(old)==13 and introduced==tpl['exposure_new_points'][pos]
        same=[e for e in edges if all(bits[j][int(bit)-1]==value for j in pf[e])]
        assert sorted(shared)==sorted(same) and len(same)==10
        exposure.append(introduced)
    U=[sum(1<<ci[(i,j)] for i in e for j in pf[e]) for e in edges]
    M=[];GG=[]; adjacent=[]
    for i,j in corners:
        kk=[ei[tuple(sorted((i,w)))] for w in faces[j] if w!=i];a,b=kk
        assert U[a]&U[b]==1<<ci[(i,j)]
        M.append(U[a]|U[b]);GG.append(U[a]^U[b]);adjacent.append(kk)
    assert U==tpl['U_masks'] and M==tpl['M_masks'] and GG==tpl['Gamma_masks']
    for k,e in enumerate(edges):
        value=(1<<66)-1
        for i in e:
            for j in pf[e]: value&=M[ci[(i,j)]]
        assert value==U[k]
    # Reconstruct the inverse from the freshly reconstructed A using exact elimination.
    n=33; aa=[[F(x) for x in A[i]]+[F(i==j) for j in range(n)] for i in range(n)]
    for j in range(n):
        k=next(i for i in range(j,n) if aa[i][j]); aa[j],aa[k]=aa[k],aa[j]
        z=aa[j][j];aa[j]=[x/z for x in aa[j]]
        for i in range(n):
            if i==j:continue
            z=aa[i][j]
            if z:aa[i]=[x-z*y for x,y in zip(aa[i],aa[j])]
    den=1
    for row in aa:
        for x in row[n:]: den=den*x.denominator//gcd(den,x.denominator)
    NN=[[int(den*x) for x in row[n:]] for row in aa]
    assert den==tpl['tau']==821810346672 and NN==tpl['N']
    assert all(sum(A[i][k]*NN[k][j] for k in range(n))==den*int(i==j) for i in range(n) for j in range(n))
    bad=[row[:] for row in NN];bad[0][0]+=1
    mutated_entries=sum(sum(A[i][k]*bad[k][j] for k in range(n))!=den*int(i==j) for i in range(n) for j in range(n))
    assert mutated_entries>0
    bv=[12-x for x in rho];u=[sum(x*y for x,y in zip(row,bv)) for row in NN]
    hn=sum(x*y for x,y in zip(bv,u))
    first=[609*den-6*x for x in u]; second=[first[i]**2-36*hn*NN[i][i] for i in range(n)]
    assert u==tpl['u'] and hn==tpl['Hnum']==7702171993838184
    assert min(first)==tpl['minimum_first_margin']==327514878189744
    assert min(second)==tpl['minimum_square_margin']==419595924675382839454010976
    degrees=[sum(i in e for e in edges) for i in range(13)]
    allowed=[sum(i in e and rho[k]==0 for k,e in enumerate(edges)) for i in range(13)]
    assert max(degrees)==6 and allowed==tpl['allowed_degrees']
    assert sum(x*(2*x-1) for x in allowed)==468
    return faces,corners,U,M,GG,adjacent,{'pinned_full_files_hashed':len(auth),'matrix_product_entries':1089,'inverse_one_entry_mutation_detected_entries':mutated_entries,'strict_coordinate_margins':33,'tau':den,'first_margin':min(first),'square_margin':min(second),'support_intersections':33,'singleton_overlaps':66,'exposure_trees':6}

def activation(corners,U,M,GG,adjacent):
    # In a seven-coordinate chart, coordinate zero is M\Gamma.
    checked=0;first=0
    for sigma in [-1,1]:
        states=[(127,s,2+sigma*((-1)**(bin(s&126).count('1')))) for s in range(128)]
        states += [(126,s<<1,2*(2-sigma*((-1)**bin(s).count('1')))) for s in range(64)]
        assert sum(w for _,_,w in states)==512 and min(w for _,_,w in states)>0
        for union in range(128):
            diff=union
            while True:
                direct=sum(w*((-1)**bin(s&diff).count('1')) for support,s,w in states if union&~support==0)
                expected=0
                if union&~127==0: expected+=256*int(diff==0)+128*sigma*int(diff==126)
                if union&~126==0: expected+=256*int(diff==0)-128*sigma*int(diff==126)
                assert direct==expected,(sigma,union,diff)
                checked+=1
                if union and diff==union: assert direct==0;first+=1
                if diff==0: break
                diff=(diff-1)&union
    def mom(k,a,b,sigma):
        union=a|b;diff=a^b; value=F(0)
        if union&~M[k]==0:value+=F(1,2)*int(diff==0)+F(sigma,4)*int(diff==GG[k])
        if union&~GG[k]==0:value+=F(1,2)*int(diff==0)-F(sigma,4)*int(diff==GG[k])
        return value
    coeff=F(1)
    for k,c in enumerate(corners):
        a,b=adjacent[k];sigma=-1 if c==(0,0) else 1
        value=mom(k,U[a],U[b],sigma);assert value==F(sigma,4);coeff*=value
        # Mixture with the empty law scales this moment once, not per coordinate.
        for lam in [F(0),F(1,3),F(1)]:
            assert lam*value+(1-lam)*int(U[a]==U[b]==0)==lam*value
    assert coeff==-F(1,2**132)
    return {'compatible_union_difference_moments':checked,'nonempty_first_moments':first,'corner_overlap_moments':66,'identity_coefficient':str(coeff),'whole_law_thinning_checks':198}

def all_map_scores(faces,corners):
    neighbors=[[] for _ in range(35)]
    for i,j in corners:neighbors[i].append(13+j);neighbors[13+j].append(i)
    colors=[0]*13+[1]*22; vertex=[0]*35; pair=[[0]*22 for _ in range(13)]
    rounds=[];classes=[]
    for t in range(4):
        hist=[Counter(colors[w] for w in neighbors[v]) for v in range(35)]
        vs=[-sum(n*n for n in h.values()) for h in hist]
        ps=[[2*hist[i][colors[13+j]]+2*hist[13+j][colors[i]] for j in range(22)] for i in range(13)]
        weight=1856**(3-t)
        vertex=[x+weight*y for x,y in zip(vertex,vs)]
        pair=[[pair[i][j]+weight*ps[i][j] for j in range(22)] for i in range(13)]
        keys=[(colors[v],tuple(sorted(hist[v].items()))) for v in range(35)]
        palette={key:k for k,key in enumerate(sorted(set(keys)))}
        new=[palette[key] for key in keys]
        rounds.append((colors,hist,vs,ps,new));colors=new
        classes.append([len(set(colors[:13])),len(set(colors[13:]))])
    assert classes==sc['round_class_counts']==[[3,1],[3,7],[13,7],[13,22]]
    assert vertex==sc['vertex_scores'] and pair==sc['pair_scores']
    aa=[x-min(vertex[:13]) for x in vertex[:13]];bb=[x-min(vertex[13:]) for x in vertex[13:]]
    top=max(x for row in pair for x in row);ell=[[top-x for x in row] for row in pair]
    assert aa==sc['a'] and bb==sc['b'] and ell==sc['ell']
    eid=sum(aa)+sum(bb)-sum(ell[i][j] for i,j in corners)
    Bpin=13*max(aa)+22*max(bb)-eid
    assert eid==sc['E_id']==115295183886 and Bpin==sc['B_pin']==1548347298342
    rng=random.Random(16120261012); tested=0
    # Direct adversarial examples: every constant map, every single-vertex collision,
    # and random maps with unrestricted repetitions.
    maps=[([a]*13+[13+b]*22) for a in range(13) for b in range(22)]
    for v in range(35):
        for w in (range(13) if v<13 else range(13,35)):
            if w==v:continue
            f=list(range(35));f[v]=w;maps.append(f)
    maps += [[rng.randrange(13) for _ in range(13)]+[13+rng.randrange(22) for _ in range(22)] for _ in range(5000)]
    def score(f,vs,ps):return sum(vs[f[v]] for v in range(35))+sum(ps[f[i]][f[13+j]-13] for i,j in corners)
    ident=list(range(35));idscore=score(ident,vertex,pair);mingap=None
    for f in maps:
        gap=idscore-score(f,vertex,pair);assert gap>=1
        mingap=gap if mingap is None else min(mingap,gap);tested+=1
    identities=0
    for old,hist,vs,ps,new in rounds:
        groups=defaultdict(list)
        for v,c in enumerate(old):groups[c].append(v)
        for _ in range(1000):
            f=[rng.choice(groups[old[v]]) for v in range(35)]
            loss=score(ident,vs,ps)-score(f,vs,ps)
            squared=0
            for v in range(35):
                squared+=sum((hist[f[v]][c]-hist[v][c])**2 for c in set(hist[f[v]])|set(hist[v]))
            assert loss==squared
            identities+=1
    assert all(1856**k-1854*sum(1856**j for j in range(k))>=1 for k in range(4))
    assert 13**13*22**22<2**147
    return {'round_class_counts':classes,'score_identity_checks_with_repetitions':identities,'adversarial_type_maps':tested,'smallest_observed_nonidentity_gap':mingap,'all_type_pair_scores':286,'E_id':eid,'B_pin':Bpin,'ell_max':max(x for row in ell for x in row)}

def parameters(score):
    D=7296; bd=D*(D+1)//2
    z=280+2459*score['B_pin'];a0=14*z+28353;lam=a0+1
    jpow=6+2210+(32*D+2048)+a0
    jupper=jpow+7+13*256;qupper=1+6*jupper;fqupper=1+qupper
    scale=14*bd;S=924*bd;B=11+lam+S*fqupper
    atom=z+2181+9+2459*(sc['max_a']+sc['max_b'])+132*bd*fqupper
    coin=18+4918*score['ell_max']+42*bd*fqupper
    normal=bd*fqupper
    expected={'D':D,'r':D//2,'bD':bd,'C_power_of_two':32*D+2048,'Z':z,'epsilon_exponent':z+2181,'A0':a0,'Lambda':lam,'J_power_of_two':jpow,'J_log2_upper':jupper,'Q_log2_upper':qupper,'q_log2_upper':fqupper,'kernel_scale_exponent':scale,'kernel_gap_q_exponent':S,'fixed_host_log2_order':B,'fixed_gap_exponent':B-10,'ell_max':score['ell_max'],'source_atom_denominator_log2_upper':atom,'source_coin_denominator_log2_upper':coin,'source_normalizer_enumeration_log2_upper':normal}
    for k,v in expected.items():assert pa[k]==v,(k,pa[k],v)
    assert 2048-661==1387>1024 and 132-35==97 and 132-1==131
    assert 147+2178-2459==-134
    assert z==147+2459*score['B_pin']+133
    assert 6*jupper+1==qupper and 66<2**7 and 7297<2**13
    # Scalar assertions for the prime lemma use small exponents only.
    for k in range(16,200):
        assert (k+2)**2<=2**(k-4) and k+3<=2**(k-3)
    return expected

def hom_small(n,edge_mask,faces,pcount):
    adj=[[0]*n for _ in range(n)];bit=0
    for a,b in combinations(range(n),2):
        adj[a][b]=adj[b][a]=(edge_mask>>bit)&1;bit+=1
    direct=sum(all(adj[f[i]][f[pcount+j]] for j,face in enumerate(faces) for i in face) for f in product(range(n),repeat=pcount+len(faces)))
    factored=0
    for f in product(range(n),repeat=pcount):
        val=1
        for face in faces:val*=sum(all(adj[f[i]][v] for i in face) for v in range(n))
        factored+=val
    assert direct==factored
    return direct

def refinement_obstruction(faces):
    q=13;D=4
    def rank(rows):
        a=[[x%q for x in row] for row in rows];k=0
        for j in range(2*D):
            idx=next((i for i in range(k,len(a)) if a[i][j]),None)
            if idx is None:continue
            a[k],a[idx]=a[idx],a[k];z=pow(a[k][j],-1,q)
            a[k]=[x*z%q for x in a[k]]
            for i in range(len(a)):
                if i==k:continue
                z=a[i][j]
                if z:a[i]=[(x-z*y)%q for x,y in zip(a[i],a[k])]
            k+=1
            if k==len(a):break
        return k
    ee=[tuple(int(i==j) for i in range(8)) for j in range(4)]
    ff=[tuple(int(i==j+4) for i in range(8)) for j in range(4)]
    lag={1:ee,0:[ee[0],ee[1],ff[2],ff[3]],7:[ee[0],ff[1],ee[2],tuple(x+y for x,y in zip(ee[3],ff[3]))]}
    for v,lamb in zip((i for i in range(13) if i not in lag),range(2,12)):
        lag[v]=[tuple(x+lamb*y for x,y in zip(a,b)) for a,b in zip(ee,ff)]
    def omega(a,b):return sum(a[i]*b[D+i]-a[D+i]*b[i] for i in range(D))%q
    assert all(rank(rows)==D and all(omega(a,b)==0 for a,b in combinations(rows,2)) for rows in lag.values())
    edges=sorted({e for face in faces for e in combinations(face,2)})
    caps={e:2*D-rank(lag[e[0]]+lag[e[1]]) for e in edges}
    assert {e:v for e,v in caps.items() if v}=={(0,1):2,(1,7):2}
    assert all(2*D-rank(sum((lag[i] for i in face),[]))==0 for face in faces)
    assert 2*D-rank(lag[0]+lag[7])==1 and (0,7) not in edges
    full=(q*q-1)*(q*q-q);line_first=(q-1)*(q*q-q)
    pattern=full*line_first;all_bases=full*full;lower_divisor=F(3*q**4,8)**2
    assert F(pattern,all_bases)==F(1,q+1) and pattern<lower_divisor
    return {'q':q,'D':D,'all_pair_dimensions_checked':33,'common_zero_faces_checked':22,'full_bases_of_two_space':full,'bases_with_first_vector_in_specified_line':line_first,'one_family_pattern_count':pattern,'full_family_basis_count':all_bases,'proposed_per_pattern_lower_divisor':str(lower_divisor),'strict_span_defect':{'global_k':3,'endpoint_dimension_sum':7},'sharper_refinement_not_used_in_main_theorem':True}

if __name__=='__main__':
    faces,corners,U,M,GG,adjacent,t=template()
    s=all_map_scores(faces,corners)
    tests=0
    for mask in range(8):hom_small(3,mask,[(0,1,2),(0,1)],3);tests+=1
    # All 8192 point maps of the literal H to K2, with faces eliminated.
    k2=0
    for f in product(range(2),repeat=13):
        val=1
        for face in faces:val*=sum(all(f[i]!=v for i in face) for v in range(2))
        k2+=val
    assert k2==2
    out={'template_and_inverse':t,'activation':activation(corners,U,M,GG,adjacent),'pinning_scores':s,'symbolic_parameters':parameters(s),'all_map_host_checks':{'tiny_hosts_checked_two_ways':tests,'original_H_to_K2_hom_count':k2,'noninjective_point_maps_tested':8192},'unused_refinement_obstruction':refinement_obstruction(faces),'packet_programs_executed':False,'huge_field_prime_or_host_materialized':False}
    (P/'own-data-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
