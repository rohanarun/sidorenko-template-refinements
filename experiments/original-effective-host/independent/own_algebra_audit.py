"""Independent rational algebra and relaxed-domain stress checks.

The evaluations for identities use unisolvent sets for the stated polynomial
degree; domain signs are separately examined in the written audit.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json

P=Path(__file__).resolve().parent.parent
def b(x):return x*(x+1)/2

def degree_two_nodes(n):
    yield [F(0)]*n
    for j in range(n):
        for v in [1,2]:
            x=[F(0)]*n;x[j]=F(v);yield x
    for i,j in combinations(range(n),2):
        x=[F(0)]*n;x[i]=x[j]=F(1);yield x

def quadratic_identities():
    count=0;names=None
    for x in degree_two_nodes(11):
        c,d,z,p0,p1,p2,t0,t1,t2,v,M=x
        pp=[p0,p1,p2];tt=[t0,t1,t2];ss=[p+t for p,t in zip(pp,tt)]
        PS=sum(pp);TS=sum(tt);D=c+d;r=D/2;u=(c+z)/2
        w=(d-3*z)/2-PS+v;nn=[2*p-t for p,t in zip(pp,tt)]
        beta=((D+1)*c+sum(b(s) for s in ss))/2-sum(b(c+s) for s in ss)/6
        gain=(r+c+1)*u-2*u*u+sum(b(s) for s in ss)-z*PS-sum(p*p for p in pp)-v*w-sum(b(t) for t in tt)+b(v)
        S=(c*(d+z-1)-z*(d+2)+2*z*z)/4+sum(n*(n-1)/6+z*p-c*s/6 for n,p,s in zip(nn,pp,ss))+v*w-b(v)
        L=c/4+z/2+(2*PS-TS)/6+v/2
        Q=(c*(d+z)-z*d+2*z*z)/4+sum(n*n/6+z*p-c*s/6 for n,p,s in zip(nn,pp,ss))+v*((d-3*z)/2-PS)+v*v/2
        k=(c-z)/2;S0=3*c*(c-1)/4+sum(n*n+(c-1)*n+3*c*p for n,p in zip(nn,pp))/6
        checks={
          'gain_minus_slack':beta-gain-S,
          'homogeneous_and_linear_parts':S-Q+L,
          'mode_removal':S-S0-k*(d-3*c-2*z+2-4*PS)/2-v*(d-3*z-2*PS+v-1)/2,
          'completed_square':S0-(c-1)*(5*c+1)/8-sum((n+(c-1)/2)**2 for n in nn)/6-c*PS/2,
          'linear_loss':(3*c+PS+TS)/2-L-(c/4+c-z+2*TS/3+(PS/3+z-v)/2),
          'pair_energy':2*(PS+TS)**2-sum((a-b_)**2 for a,b_ in combinations(ss,2))-6*sum(a*b_ for a,b_ in combinations(ss,2)),
          'center_common_gain':3*(b(r)-b(r-u))-u*d-b(u)-((r+c+1)*u-2*u*u),
          'first_bracket':(d-3*c-2*z+2-4*PS)-(D-12*M+6*c+2)-2*(c-z)-4*(3*(M-c)-PS),
          'second_bracket':(d-3*z-2*PS+v-1)-(D-6*M+2*c+v-1)-3*(c-z)-2*(3*(M-c)-PS),
          'subspace_count_exponent':(d-v)*v-3*((d-z)/2)*v+(d-v)*PS-sum(p*p for p in pp)-2*((d-v)-(d-z)/2)*PS+z*PS+sum(p*p for p in pp)+v*w,
        }
        assert all(y==0 for y in checks.values()),(x,checks)
        names=list(checks);count+=len(checks)
    return names,count

def regional_identities():
    count=0
    for aa,yy,t in product(map(F,range(4)),repeat=3):
        # Positive delta, both branches after c=delta.
        P0=aa;z=yy;bb=P0/3+z;ee=P0+3*z;ell=ee-bb
        hb=(4*P0+3*z)*(4*P0+9*z)/216;he=z*(4*P0+15*z)/24
        R=t;T=bb-R
        H1=3*z*z/4+(2*P0-T)**2/18+(5*P0-T)*z/6-(P0/3+z)**2/2-(P0+T)**2/72
        assert H1==hb+R*(16*P0/3+2*z+R)/24
        T=t
        H2=3*z*z/4+(2*P0-T)**2/18+(5*P0-T)*z/6-((P0-T+3*z)/2)**2/2-(P0+T)**2/72
        assert ell*H2==(ee-T)*hb+(T-bb)*he+ell*(T-bb)*(ee-T)/12
        # Negative delta, after P=x+3y,c=y,d=P+T.
        xx=aa;y=yy;bb=xx/3;ee=xx;ell=ee-bb
        hb=(16*xx*xx+96*xx*y+27*y*y)/216;he=y*(4*xx+3*y)/24
        R=t;T=bb-R
        H1=y*y/4+(2*xx-T)*y/3+(2*xx-T)**2/18-(xx/3)**2/2-(xx+3*y+T)**2/72
        assert H1==hb+R*(16*xx/3+10*y+R)/24
        T=t
        H2=y*y/4+(2*xx-T)*y/3+(2*xx-T)**2/18-((xx-T)/2)**2/2-(xx+3*y+T)**2/72
        assert ell*H2==(ee-T)*hb+(T-bb)*he+ell*(T-bb)*(ee-T)/12
        count+=4
    for c,d,s0,s1,s2 in degree_two_nodes(5):
        beta=((c+d+1)*c+b(s0)+b(s1)+b(s2))/2-(b(c+s0)+b(c+s1)+b(c+s2))/6
        rhs=b(c+s0)/3+b(c)/6+(b(s1)+b(s2))/3
        assert beta-rhs==c*(3*d-3*s0-s1-s2)/6;count+=1
    for k in map(F,range(3)):
        assert b(2*k)/3-b(k)==k*(k-1)/6
        assert b(2*k+1)/3-b(k)==(k+1)*(k+2)/6;count+=2
    for x in map(F,range(5)):
        assert (1+5*x)*(1-x/2)**3-(1+x/6)==x*(F(10,3)-F(27,4)*x+F(29,8)*x*x-F(5,8)*x**3)
        assert (1+4*x)*(1-x/2)**2-(1+x/6)==x*(F(17,6)-F(15,4)*x+x*x)
        assert 1-(1-3*x)*(1+x)**3==6*x*x+8*x**3+3*x**4
        assert 1-(1-2*x)*(1+x)**2==3*x*x+2*x**3;count+=4
    return count

def integer_domain():
    all_counts={};minimum=0
    for D in [2,4,6,8,10]:
        r=D//2;count=0
        for c in range(D+1):
            d=D-c
            for u in range(min(c,r)+1):
                rp=r-u;z=2*u-c
                if not 0<=rp<=d:continue
                options=[(p,t) for p in range(d+1) for t in range(d-p+1) if t<=p+z]
                for rows in product(options,repeat=3):
                    pp=[a for a,_ in rows];tt=[a for _,a in rows]
                    ss=[p+t for p,t in rows];h=[c+s for s in ss]
                    PS=sum(pp);TS=sum(tt)
                    if PS+TS>d:continue
                    for v in range(min(pp)+z+1):
                        w=(d-3*z)//2-PS+v
                        if w<0:continue
                        bi=lambda x:x*(x+1)//2
                        cost=(D+1)*c+sum(bi(s) for s in ss)
                        gain=(r+c+1)*u-2*u*u+sum(bi(s) for s in ss)-z*PS-sum(p*p for p in pp)-v*w-sum(bi(t) for t in tt)+bi(v)
                        sixS=3*cost-sum(bi(a) for a in h)-6*gain
                        twelveQ=2*sixS+3*c+6*z+4*PS-2*TS+6*v
                        assert 6*twelveQ>=(PS+TS)**2
                        dif=sum((a-b_)**2 for a,b_ in combinations(h,2))
                        assert 24*sixS>=dif-72*sum(h)
                        if D>=12*max(h):assert sixS>=0
                        minimum=min(minimum,sixS);count+=1
        all_counts[str(D)]=count
    # The manuscript explicitly excludes this real, nonintegral counterprofile.
    nn=[F(1,2)]*3;PS=TS=F(3,2)
    S=sum(n*(n-1)/6 for n in nn);E=F(1);delta=22*S+E
    assert S==F(-1,8)
    assert delta==F(-7,4)
    return {'fully_enumerated_relaxed_integer_tuples_by_D':all_counts,'total_tuples':sum(all_counts.values()),'minimum_six_times_local_slack_at_small_D':minimum,'real_noninteger_counterprofile_global_delta':str(delta)}

if __name__=='__main__':
    names,count=quadratic_identities()
    out={'degree_two_identity_names':names,'degree_two_unisolvent_evaluations':count,'regional_and_other_identity_evaluations':regional_identities(),'domain_stress':integer_domain(),'universal_inequality_signs_certified_by_finite_sweep':False}
    (P/'own-algebra-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
