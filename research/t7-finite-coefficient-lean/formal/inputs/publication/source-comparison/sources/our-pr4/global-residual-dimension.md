# Rank-layer dimensions 7296 and 7644 from global edge energy

**Authorship and review.** GPT-6 Pro developed this improvement and supplied the proof, exact certificates, and original checker in research Task 9. Codex prepared this publication version, independently reviewed the conventional argument and checker, and replayed the unchanged checker with source comparisons and two mutation controls. This is an independent follow-up to the credited source authors below, not an official OpenAI publication or a formal proof-assistant result.

The proof is complete for the new energy and residual implications relative to the explicitly retained geometric and transverse inputs. [Exact certificates and verification evidence](experiments/global-residual-energy/) accompany it.

## Completed result and scope

For the original 13-point/22-face template, the residue lemma holds for every even **D >= 7296**. For the literal candidate `candidate-13-49243.json`, with its published distribution of twenty Hamiltonian cuts, it holds for every even **D >= 7644**. The respective all-D bounds on a nonsaving profile are **M <= 608** and **M <= 637**.

Here "nonsaving" means `Delta = Ccal - sum_j g_j <= 0`, with the source's selected pointwise gain exponents. At the stated dimensions every such profile has `c_j=0`, `h_e in {0,2}`, `Ecal=0`, and `sum_j g_j = (2/3) sum_e b(h_e)`. This includes every activity pattern, every lower-activity face, and independently selected local maximizing tuples sharing the prescribed edge dimensions.

This replaces both the worst-path propagation estimate and the quadratic-remainder/common-mode elimination step. It does not merely substitute a new D in the predecessor theorem. It is a strengthening of the specified proof, not a claim of mathematical priority.

This note uses the immutable public sources below. It makes no global novelty or minimum-dimension claim. It does not depend on the unmerged proposal to reduce the residual constant to 28; the support-uniform residual constants used here remain 189 and 197.

## Immutable sources and retained inputs

All OpenAI source paths below are under commit
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, directory
`preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/`.

* [tail.tex](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/tail.tex), blob `dc11e07a592e70d3a13e3a005c72378c88edc351`: equations `eq:global-cost`, `eq:tail-total-slack`, `eq:tail-feasible`, `eq:slack`, `eq:tail-quadratic`, `eq:tail-linear-loss`, `eq:tail-scalar-quadratic`; lemmas `lem:tail-lower-active`, `lem:tail-span`, `lem:tail-residual-counts`.
* [planted.tex](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/planted.tex), blob `e1a4636e66361dae0f5918e1245950060535a83c`: the planted density/orbit ratio, `lem:planted-subspace-cost`, `eq:planted-nullity-cost`, `prop:planted-gain`, `lem:two-active-gain`.
* [orbits.tex](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/orbits.tex), blob `7da7ee247b4be60c3baf545a2e0f78309a667ee0`: exact finite-product counts and `eq:orbits-explicit-lower-bound`.
* [complex.tex](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/complex.tex), blob `178b0e9da21867a727ea847dae8e537b9d719a70`: literal original face table and bit cuts.
* [transverse.tex](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/transverse.tex), blob `d4991976e630f117c8d85a7e22deb60643a2450d`: `prop:transverse-limit`, even D >= 12, and its O_D(q^(-1/2)) proof. This is a retained analytic input, not independently re-proved here.

The refinement sources are at commit `d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d`:

* [proof.tex](https://github.com/rohanarun/sidorenko-template-refinements/blob/d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d/proof.tex), blob `66fc5eb655e6471df0c266c986c0ab47d943fe0f`: Hamiltonian/exposure reduction and the sequential residual accounting. Its stated attribution is an independent AI-generated research draft prepared with Codex, not an official OpenAI publication.
* [candidate-13-49243.json](https://github.com/rohanarun/sidorenko-template-refinements/blob/d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d/experiments/order-13-cuts/candidate-13-49243.json), blob `7d33c2ad101e4aedc57ea1eb2baab5db0c6f6778`: literal candidate faces, cycles, and rational weights.

No generator-completeness claim or template-minimum theorem is needed here.

## 1. Definitions and the theorem

Write b(t)=t(t+1)/2. Each edge of the point graph belongs to two faces. The coverage a_e is the probability that a random admissible Hamiltonian cut crosses e. Assume a_e>=1/3 and put rho_e=a_e-1/3. For a sphere template, sum_e rho_e=2.

For the profile h_e=dim(L_i intersect L_k), c_j=dim(intersection of the three point Lagrangians), let

    C_j = (D+1)c_j + sum_l b(h_l-c_j),
    Ccal = (1/2)[sum_j C_j - sum_e (1-a_e)b(h_e)],
    beta_j = C_j/2 - (1/6)sum_{e in j} b(h_e),
    S_j = beta_j-g_j,
    Ecal = (1/2)sum_e rho_e b(h_e).

Profiles whose actual three-active tuple domain is empty have zero face factor and are omitted, as in the retained source. For other profiles the selected gain is the source maximum over its finite, q-independent actual tuple union, or a valid upper bound over the stated necessary integer relaxation. In particular, delta=2u-c with integral 0<=u<=c, and all dimension/parity constraints are retained.

Thus, exactly,

    Delta := Ccal-sum_j g_j = sum_j S_j+Ecal.                 (1)

The global cost formula extends to rational cut distributions: for each cut, the complete profile event is contained in both class events. Take their probability bounds to the power 1/2, then a weighted geometric mean over cuts. Each face is counted once before the factor 1/2 and an edge is internal with probability 1-a_e. There is no independence assertion between cut classes.

Let L_triangle be the graph Laplacian on vertex set E, with an edge between two point-pairs whenever they belong to the same triangular face. More explicitly,

    h^T L_triangle h = sum_j sum_{e<e', e,e' in j} (h_e-h_e')^2.

Set

    K = L_triangle/144 + diag(rho_e)/4,
    ell_e = 1-rho_e/4,
    z = K^{-1}ell,  H = ell^T K^{-1}ell.                    (2)

The connected face-dual graph makes this edge graph connected. Nonnegative rho with positive total implies that K is positive definite.

**Theorem.** For every even D and every tuple allowed by the source's necessary dimension inequalities, on every activity pattern,

    Delta >= h^T K h - ell^T h.                            (3)

Consequently a nonsaving profile satisfies

    h_e <= (z_e + sqrt(H (K^{-1})_ee))/2.                   (4)

Suppose an integer B strictly exceeds every right-hand side in (4). If D is even and D>=12(B-1), every nonsaving profile satisfies

    c_j=0 for every face;
    h_e in {0,2} for every edge;
    Ecal=0;
    sum_j g_j=(2/3)sum_e b(h_e).                            (5)

The certificate below proves B=609 for the original template and B=638 for candidate 49243.

## 2. A sharper scalar quadratic estimate, valid for all D

On a three-active face use the source variables

    d=D-c,  delta=2u-c,  s_l=p_l+t_l,
    P=sum_l p_l, T=sum_l t_l,
    w=(d-3delta)/2-P+v.

The relaxed constraints used are

    c>=|delta|; P+T<=d; p_l,t_l,v>=0;
    t_l,v<=p_l+delta; w>=0.                                 (6)

Actual tuples satisfy these, but sufficiency for realizability is not asserted. The source gives S=Q-L, where

    Q=[c(d+delta)-delta d+2delta^2]/4
      +sum_l[(2p_l-t_l)^2/6+delta p_l-c(p_l+t_l)/6]
      +v[(d-3delta)/2-P]+v^2/2,
    L=c/4+delta/2+(2P-T)/6+v/2.                             (7)

We prove the directionally sharper estimate

    Q >= (P+T)^2/72.                                       (8)

This is not claimed to dominate every component of the old 1/342 coercivity statement. It is substantially stronger in precisely the P+T direction needed for propagation. Its coefficient is sharp on the relaxed domain: c=delta=v=0, p_l=t_l=a for all l, and d>=6a give equality.

Here is the complete rational certificate. Completing the v-square and applying Cauchy-Schwarz to the three (2p_l-t_l) gives the source scalar lower bound

    Q >= [c(d+delta)-delta d+2delta^2]/4
         +(2P-T)^2/18+delta P-c(P+T)/6-v0^2/2,
    v0=min(P/3+delta, (P-T+3delta)/2).                       (9)

Indeed a=(P-(d-3delta)/2)_+ obeys a<=v and a<=v0, and the v-expression is at least -a^2/2. The coefficient of c in (9) is

    (d+delta)/4-(P+T)/6
      =(d+3delta)/12+(d-P-T)/6>=0.

Replace c by |delta|, which decreases the right side.

For delta>=0, the resulting function of T is

    F(T)=3delta^2/4+(2P-T)^2/18+(5P-T)delta/6
          -(1/2)min(P/3+delta,(P-T+3delta)/2)^2,
    0<=T<=P+3delta.

Subtract (P+T)^2/72. On the first interval, ending at T=P/3+delta, its derivative is (T-3P-2delta)/12<=0. On the second interval its second derivative is -1/6, so its minimum is at an endpoint. The two endpoint differences are exactly

    at T=P/3+delta: (4P+3delta)(4P+9delta)/216 >=0;
    at T=P+3delta:  delta(4P+15delta)/24 >=0.                (10)

For delta=-y<0 put x=P-3y>=0, so 0<=T<=x. The coefficient of d after replacing c by y is y/2. Replacing d by P+T decreases the bound and leaves

    G(T)=y^2/4+(2x-T)y/3+(2x-T)^2/18
          -(1/2)min(x/3,(x-T)/2)^2.

Subtract (x+3y+T)^2/72. Its first-interval derivative is (T-3x-5y)/12<=0 and its second-interval second derivative is -1/6. Its breakpoint and endpoint values are

    at T=x/3: (16x^2+96xy+27y^2)/216 >=0;
    at T=x:   y(4x+3y)/24 >=0.                             (11)

This proves (8), including degenerate intervals. The four polynomial identities and the derivative/concavity identities are checked symbolically by the accompanying standard-library checker.

## 3. Global coupling instead of propagation along a worst path

There is an exact nonnegative certificate for the linear loss:

    (3c+P+T)/2-L
       =c/4+(c-delta)+2T/3+(P/3+delta-v)/2 >=0.             (12)

Thus L<=sum_{e in j}h_e/2. Also, with s_l=p_l+t_l>=0,

    2(P+T)^2-sum_{l<k}(s_l-s_k)^2
       =6 sum_{l<k}s_l s_k >=0.                            (13)

Since h_l=c+s_l, (8), (12), and (13) imply

    S_j >= (1/144)sum_{e<e', e,e' in j}(h_e-h_e')^2
               -(1/2)sum_{e in j}h_e.                     (14)

Every lower-activity face satisfies the same inequality. The source's lower-activity lemma gives S_j>=h_max^2/24-h_max/12 and S_j>=0. Meanwhile the sum of the three squared differences is at most 2h_max^2, and sum h_e>=h_max. Hence the difference between this lower bound and the right side of (14) is at least h_max^2/36+5h_max/12>=0.

Summing (14) counts each edge twice. Keeping the full excess term, including its linear part, proves (3):

    Ecal=(1/4)sum_e rho_e(h_e^2+h_e).

No local slack was assumed nonnegative here. In particular, fully coincident triples still have S=-D/4; the checker verifies this symbolic specialization.

If Delta<=0, then h^T K h<=ell^T h. Completing the square gives

    (h-z/2)^T K(h-z/2)<=H/4.

Cauchy-Schwarz in the K inner product proves (4). In this last step we permit every real vector h in the ellipsoid, discarding integrality and nonnegativity. This enlarges the domain and therefore gives a valid upper bound. No simultaneous realizability of the local maximizing tuples is used anywhere.

## 4. Exact positive-mode removal; no quadratic remainder box

Let kappa=c-u=(c-delta)/2, a nonnegative integer, and n_l=2p_l-t_l. Define

    S0=3c(c-1)/4+(1/6)sum_l[n_l^2+(c-1)n_l+3c p_l].

The exact identity replacing `S=Ad+R` followed by `|R|<=C_*` is

    S=S0
       +(kappa/2)[d-3c-2delta+2-4P]
       +(v/2)[d-3delta-2P+v-1].                            (15)

For a profile with M=max h_e, we have P<=3(M-c). With d=D-c, the bracketed terms obey

    d-3c-2delta+2-4P >= D-12M+6c+2,
    d-3delta-2P+v-1 >= D-6M+2c+v-1.                        (16)

The differences between the two sides of these inequalities are respectively

    2(c-delta)+4[3(M-c)-P],
    3(c-delta)+2[3(M-c)-P],

so (16) is also a symbolic nonnegative certificate.

The base expression S0 is nonnegative on every feasible integer tuple; S0 itself need not be integer-valued:

* For c>=2,

      S0=(c-1)(5c+1)/8
          +(1/6)sum_l[n_l+(c-1)/2]^2+(c/2)P >0.

* For c=1, S0=sum_l(n_l^2+3p_l)/6>=0, with equality precisely when all p_l=t_l=0.
* For c=0, necessarily delta=0, and t_l<=p_l. Thus n_l>=p_l>=0 is integral, and S0=sum_l n_l(n_l-1)/6>=0. Equality gives exactly (p_l,t_l)=(0,0) or (1,1) independently for the three opposite pairs.

If D>=12M, the kappa bracket in (15) is strictly positive. If v>0, the v bracket is also strictly positive, since v is an integer and M>=1. When M=0 all these variables are zero. Thus S>=S0>=0, strictly if kappa>0 or v>0. Lower-activity slacks are nonnegative by their source lemma.

Under Delta<=0, every slack and Ecal must now vanish. Therefore every three-active face has kappa=v=0, hence u=c and delta=c. A c=1 equality face has every edge dimension one. Across such an edge, a neighboring face cannot be a lower-activity equality face or a c=0 three-active equality face; it must also have c=1. Dual connectivity would give h_e=1 everywhere. But then Ecal=(1/2)sum rho_e=1, a contradiction. This excludes the last positive common mode.

On lower-activity equality faces the source lemma gives c=0 and either all edge dimensions zero or exactly one dimension two. The latter case requires two active incidences at that pair's endpoints. With zero or one active incidence, only the all-zero case is possible. The preceding three-active classification gives c=0 and each h_e in {0,2}. These are all cases, proving (5), including

    sum_j g_j=sum_j beta_j=(2/3)sum_e b(h_e).

## 5. Exact template and matrix certificates

The accompanying [template_data.json](experiments/global-residual-energy/template_data.json) contains only literal original faces/bits and candidate faces/cycles/weights. The original artifact reports that discovery did not execute repository programs; the later independent replay executed the reviewed supplied checker and parsed the pinned repository literals as data. The checker verifies every supplied cut by deleting its crossing edges in the dual graph, finding two 11-face trees, and constructing exposures adding one new point at every step. It also checks that every edge occurs twice, the vertex links are cycles, the Euler characteristic is two, both relevant graphs are connected, all vertex coverages sum to two, and all coverages are at least 1/3.

Both templates have exactly five edges of positive excess:

    original:
      rho(0,2)=2/3;
      rho(4,8)=rho(5,6)=rho(5,10)=rho(7,12)=1/3.

    candidate 49243:
      rho(10,11)=2/3;
      rho(0,5)=rho(5,6)=rho(6,7)=rho(8,9)=1/3.

All other excesses vanish. Define d_e=3rho_e, b_e=12-d_e and the integer matrix

    A=144K=L_triangle+12 diag(d_e).

For each template the supplied symmetric integer matrix N and positive integer tau satisfy

    A N = tau I.                                          (17)

Thus A^{-1}=N/tau, certified without numerical inversion. Let u=Nb and Hnum=b^T N b. For every one of the 33 coordinates, the checker verifies

    B tau-6u_e >0,
    (B tau-6u_e)^2 >36 Hnum N_ee.                          (18)

Equations (17)-(18) are exact rational certificates that B exceeds every coordinate bound in (4). The matrices are positive definite for the structural reason already proved, not on the strength of floating eigenvalues.

| Template | tau | B | integer M bound | sufficient even D |
|---|---:|---:|---:|---:|
| Original | 795067664967842660352 | 609 | 608 | 7296 |
| Candidate 49243 | 763747485816821907456 | 638 | 637 | 7644 |

The minimum positive integer margins in the second inequality of (18) are respectively

    392731950442990003623245857651838268217491456
    245352450284876763812602384886045741313687552.

The full N matrices, not just these scalar checksums, are supplied. The certificates do not assert optimality of these B or D values.

## 6. Strict saving, sequential residuals, and ordered bases

The new proof does not change the probability cost or the selected gains. Every g_j is an integer, and 3a_e is an integer for both literal cut distributions. Thus

    6 Ccal is an integer; Delta>0 implies Delta>=1/6.        (19)

This is the original strict exponent-saving lattice, not the denominator 144 appearing in the energy relaxation. The large denominators of the candidate cut weights do not enter (19); its aggregate edge coverages have denominator three.

For residual profiles Ecal=0 forces h_e=0 at each positive-excess edge. Both allowed graphs have 28 edges. Their active-degree caps, in point order, are

    original:  (3,6,3,6,4,2,4,4,4,6,4,6,4),
    candidate: (4,6,6,6,6,2,2,4,4,4,3,3,6).

Let m be the number of active two-spaces, k their total span dimension, k_i their endpoint span dimensions, and d_span=sum k_i-2k. The source strict span inequality gives d_span>=1 for a nondirect family.

For the sequential count, choose an ordered basis of each two-space and record each vector's type (g,l_i,l_j), together with its earlier span dimensions w',v'_i,v'_j and pi=dim(V'_i intersect V'_j). There are five types. The respective upper bounds on vector choices are

    (1,1,1): q^(2D-v'_i-v'_j+pi),
    (0,0,0): q^pi,
    (0,0,1): q^(v'_i), and symmetrically for (0,1,0),
    (0,1,1): q^(w').

Use the corrected ordered-basis counting order:

    number of families
      = [sum over all complete basis patterns
            (number of ordered lists in that pattern)] / |GL_2(q)|^m.

A fixed pattern need not contain every ordered basis of a family. Full basis multiplicity is used only after the pattern sum. The same equality holds for the containment-weighted count because the containment weight is basis-invariant.

After adding the endpoint containment exponents and the residual gain 2m, the source accounting gives -D*d_span+R with

    R=-2m+sum_{111,000} pi
           +sum_{001,010}(v'_i+v'_j)
           +sum_{011}(w'+v'_i+v'_j).                       (20)

At each endpoint of active degree delta_i,

    sum_x v'_i(x) <= binom(k_i,2)+(2delta_i-k_i)k_i
                     <=delta_i(2delta_i-1).

Write B0=sum_i delta_i^2-3m. For any nonempty subgraph of the connected allowed graph, B0 is at most its value on the full allowed graph. To see this, extend the subgraph along connected paths: an added edge with current endpoint degrees a,b increases B0 by 2a+2b-1, positive whenever at least one endpoint is already nonisolated. Complete such a connected spanning extension and then add remaining edges. The empty case has B0=0 and is harmless.

The full values are 178 and 186. If d_span=1, there is one one-sided defect vector. Averaging pi<=(v'_i+v'_j)/2 gives

    R <= B0+(k_i+k_j-1)/2 <= B0+23/2.

R is an integer. Thus the two remainders are **189** and **197**, respectively. The candidate remainder is not 189.

For d_span=n1+2n2>=2, (20) gives

    R <= B0+(23/2)n1+(k+11)n2,
    k<=2m-1<=55,
    R/d_span <= B0/2+33.

These ratios are 122 and 126. At the chosen dimensions this proves uniform nondirect bounds q^(-D+189) and q^(-D+197). Their savings are 7107 and 7447. Direct residuals save q^(-m), as in the source direct count, and hence at least q^(-1) in the singular stratum.

## 7. Explicit singular-tail constants and what they do not certify

The following are deliberately conservative prefactors, obtained from the retained geometric counts. They are additional quantitative consequences, not a claim that every downstream effective-witness constant has been audited.

For q>=3, finite products satisfy

    1/2 <= product_{j=1}^n (1-q^(-j)) <=1,
    1 <= product_{j=1}^n (1+q^(-j)) <=2.

Consequently Gaussian coefficients, after their leading q-power is removed, lie in [1,2]. Normalized containment probabilities lie in [1/2,1], isotropic-space counts in [1,4], and pair probabilities in [1/2,2].

The source common-space and pair-space formulas give a profile upper prefactor 4*32=128. The explicit individual-orbit lower bound gives

    P(actual ordered orbit) >= 2^(-D-13) q^(-C_j).

Its factors are: at least 2^(-3) for the normalized common-space count, at least 2^(-4) for the pair-space count with endpoint containments, at least 2^(-3) for avoidance, and at least 2^(-D-3) for the residual orbit. This remains valid when the residual dimension is zero.

The planted numerator has upper prefactor at most 2^23 per dimension tuple: 2^9 for common-space/center/normalization factors, 2^11 for the subspace selection, and 2^3 for the simultaneous nullity bound. For the subspace selection, the four factors are 2 (span), 2^3 (three span containments), 2^4 (direct pair decomposition), and 2^3 (three pair containments). There are at most (D+1)^8 tuples. Dividing by the individual orbit lower bound shows that

    G_D := 2^(D+40)(D+1)^8

is an upper prefactor for every face's chosen gain, including lower activity. In the two-active case, the direct pair-planted count gives at most 16(D+1), which is smaller.

A class exposure has 11 faces. Its root costs at most 128 and each subsequent conditional completion at most 256, so the full-profile prefactor is at most 2^87, also for the weighted cut distribution. There are at most (D+1)^55 profiles.

For the residual count, at most 56 basis vectors are present. A complete pattern can be specified by one of five types and four dimensions in {0,...,56} for each vector. Therefore the number of patterns is at most

    [5*57^4]^56 < 2^1512.

Since |GL_2(q)|>=q^4/2, division after summation costs at most 2^28. Summing over at most 2^28 active pair sets gives the nondirect prefactor 2^1568. Direct residuals have prefactor at most 2^56 after this active-set sum.

Thus, for any fixed activity pattern, the unsigned Lagrangian singular contribution is at most

    G_D^22 [ 2^87(D+1)^55 q^(-1/6)
              +2^56 q^(-1)
              +2^1568 q^(-D+R_*) ],                       (21)

where R_*=189 or 197. At the certified dimensions, this is at most

    K_sing(D) q^(-1/6),
    K_sing(D)=2^(22D+2450)(D+1)^231,  q>=3.                 (22)

Specifically,

    original:  2^162962 * 7297^231 * q^(-1/6),
    candidate: 2^170618 * 7645^231 * q^(-1/6).

For the signed symmetric-matrix singular contribution, q>=2D is sufficient for the following comparison. The signed rank-r mass is at least q^(-b(r))/4: the principal-minor induction gives a nonsingular symmetric r-form of each sign with probability at least (1-r/q)/2. The Lagrangian pair mass is at most 2q^(-b(r)), so each of the at most 66 incidence normalizers contributes a comparison factor at most 8. Conditioning 35 Lagrangians into the matrix chart costs at most 2^35. Hence the extra comparison factor is at most 2^233, and

    K_matrix-sing(D)=2^(22D+2683)(D+1)^231.                 (23)

The two coefficients of the power of two in (23) are 163195 and 170851. To make the signed singular error at most any rational epsilon>0, it is sufficient to use an odd prime satisfying

    q >= max(2D, [K_matrix-sing(D)/epsilon]^6).              (24)

These are symbolic integer/rational bounds. No such prime, finite field, or kernel is instantiated.

The transverse source calculation has the separate threshold even D>=12 and gives an O_D(q^(-1/2)) error; its joint-sign proof uses the point-degree bound six. Both templates pass those combinatorial requirements. Thus the new dimensions remove the dimension bottleneck in the rank-layer argument, with the other analytic inputs retained. The full error has the form

    T_D q^(-1/2) + K_matrix-sing(D) q^(-1/6).

A numerical value of the transverse prefactor T_D, the negative-kernel/pinning margin, and downstream rationalization/host bounds are not certified here. Formula (24) is therefore a quantitative singular-tail certificate, not a fully improved effective Sidorenko witness.

## 8. Verification status, computation limits, and replay

The all-domain inequalities, equality classification, basis aggregation, and geometric prefactors are conventional mathematical arguments. The finite checker verifies the polynomial identities and literal certificates supporting them; it is not a formal proof assistant for these arguments or the retained source theorems.

GPT-6 Pro supplied the checker and certificates. After complete static source review, Codex independently executed those unchanged bytes with both optional comparisons to the immutable original/candidate source literals. The full 1,164-byte output matched the supplied expectation exactly. Both 33-by-33 inverse certificates, all 66 strict coordinate inequalities, 23 fixed cuts, and symbolic identities passed. [Verification records](experiments/global-residual-energy/verification.json) distinguish this replay from the original author's reported discovery run.

The canonical finite receipt is `a44eb64cb5cb69e4aaf9c81f16a2f26bb827113b5cbd8e5e2f929ee980458fa5`. Changing one diagonal inverse-certificate entry by +1 was rejected at the inverse equation (receipt `bf0a5a5b569be06f9c6548f7aa65aa5731e7e001dda24af6136bc4af7b0ca82b`). Changing the original strict bound B from 609 to 1 was rejected at the strict coordinate inequality (receipt `61bf5ed1644db9c0e41117f9ba96a7e7bad39a8089453a69375841112e016d68`). These controls detect the tested corruptions; they are not a completeness claim for the checker.

The legitimate replay took 0.114 seconds orchestration wall time and 27,082,752 bytes peak RSS. A subsequent resume reused its durable receipt without another attempt. No D-sized allocation, bounded-D sweep, template search, finite field, prime, kernel, or host was constructed.

From the repository root, run the standalone standard-library checker with assertions enabled:

```sh
python3 -I -B experiments/global-residual-energy/check_global_residual.py
```

Optional source binding to the candidate already in this repository and an exact local copy of the pinned OpenAI `complex.tex`:

```sh
python3 -I -B experiments/global-residual-energy/check_global_residual.py \
  --candidate-source experiments/order-13-cuts/candidate-13-49243.json \
  --complex-source /path/to/pinned/complex.tex
```

The checker makes no network requests, writes no files, and does not execute repository modules. It refuses optimized Python (`-O`/`-OO`). It is deliberately a standalone addition; the existing full enumeration runner and its network/compiler requirements are unchanged. The output's phrase "all-D proof certificates" means finite symbolic identities supporting the separate universal proof, not formal verification.

## Dependency ledger and stopping boundary

| Step | Status | Depends on |
|---|---|---|
| Rational cut coverages/exposure | Exact finite certification, with weighted averaging proved | Literal tables/cycles/weights |
| Source exact slack and local gains | Retained geometric input; algebra rechecked | `planted.tex`, `tail.tex`, actual tuples or necessary relaxation |
| Q >= (P+T)^2/72 | Proved for all D | Scalar completion, four rational endpoint identities |
| Global anchored energy inequality | Proved for all D | Previous row; exact loss envelope; all lower-activity faces |
| M<=608 / M<=637 | Exact rational certificate | Two explicit SPD matrices; AN=tau I; coordinate inequalities |
| Mode removal at D>=12M | Proved uniformly | Exact decomposition (15), integer S0 classification |
| c=0 and h in {0,2}, all activity cases | Proved uniformly | Previous rows; dual connectivity; total excess two |
| Saving lattice 1/6 | Preserved and checked | Integer gains and aggregate coverage denominator three |
| Nondirect residual 189 / 197 | Proved via corrected basis aggregation and degree caps | Source span/accounting identities; literal allowed graphs |
| Explicit unsigned/signed singular prefactors | Proved envelopes from retained counts | Exact products, orbit lower bound, planted numerator, full pattern sum |
| Transverse rank-layer error | Retained analytic input | Source even-D>=12 local/sign estimates, max point degree six |
| Complete effective negative witness | Not certified here | Still needs transverse prefactor and downstream negative-margin/pinning/rationalization bounds |

**Strongest completed result:** the full residue classification and quantitative singular-tail bound are certified at D=7296 for the original template and D=7644 for candidate 49243, replacing the specified propagation and common-mode bottlenecks. The stopping boundary is the rank-layer dimension and singular-error interface; no giant witness or host is built.
