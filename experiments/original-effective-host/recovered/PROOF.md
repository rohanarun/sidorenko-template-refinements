# An effective finite Sidorenko counterexample for the original 35-vertex pattern

## The result and its acceptance boundary

Let `H` be the incidence graph of the 22 triples in §1, with the 13 point vertices and 22 face vertices treated as disjoint. For a simple graph `G` on `n` vertices, use

\[
p(G)=\frac{2|E(G)|}{n^2},\qquad
 t(H,G)=\frac{\operatorname{hom}(H,G)}{n^{35}}.
\]

**Every edge-preserving map is counted, including every noninjective map.** Put

\[
\boxed{B=7866423844799423288734694969,\qquad N=2^B.}
\]

**Theorem.** There is a nonempty finite simple graph `G` on exactly `N` vertices for which

\[
\boxed{p(G)^{66}-t(H,G)\ \ge\ 2^{10-B}=1024/N>0.}\tag{T}
\]

The following is a deterministic finite generator for such a graph: enumerate the labeled simple graphs on `N` vertices in binary upper-triangle order, and return the first one satisfying

\[
\boxed{(2|E(G)|)^{66}-\operatorname{hom}(H,G)N^{97}
       \ \ge\ 1024N^{131}.}\tag{A}
\]

It stops after at most `2^{binom(N,2)}` graph tests. Each test can count **all** homomorphisms by at most `N^13` point-label assignments, with 22 common-neighborhood cardinalities per assignment. The proof of termination is the explicit source-kernel construction below, not an assumed existence theorem or an unbounded search assertion.

A sharper parameterized statement is also proved. Set

\[
\begin{gathered}
D=7296,\quad r=3648,\quad b(s)=s(s+1)/2,\\
C_D=2^{235520}7297^{256},\quad
Z=3807386006623258,\quad m_0=2^{-Z},\\
\varepsilon=2^{-(Z+2181)},\quad
A_0=53303404092753965,\quad\alpha=2^{-A_0},\\
\Lambda=A_0+1=53303404092753966,\quad\Gamma=2^{-\Lambda},\\
H_c=66\,2^{2210},\quad
J_q=66\,7297^{256}2^{53303404092991701},\\
Q_0=116736+J_q^6.
\end{gathered}\tag{P}
\]

For **every odd prime `q>Q_0`**, the construction gives a rational symmetric kernel `U` on a finite rational probability space, with

\[
0\le U\le1,\qquad \mu=\mathbb EU=q^{-372672384},
\]
\[
\boxed{\mu^{66}-t(H,U)\ge
\Delta_q:=2^{-53303404092753966}q^{-24596377344}.}\tag{K}
\]

For each integer `n>=1322/Delta_q`, a finite simple host of order `n` has deficit at least `Delta_q/2`. The completely fixed version (T) follows from a proved prime search in `(Q_0,2Q_0)` and explicit exponent inequalities.

This is a conventional mathematical proof with an exact finite-data certificate. It is **not** a claim that a host adjacency list, the field, its complete kernel, or a Lean proof of this quantitative theorem was materialized. The earlier residual-classification admission condition is discharged in §§4–5; no research hypothesis about rank layers, pinning negativity, moment identities, or finite-host existence is retained. Finite checks certify the literal arithmetic; the universal statements are justified by the proofs, not extrapolated from tests.

## Provenance, attribution, and source coverage

The construction and original graph are from the OpenAI manuscript at commit
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. The relevant source labels are listed in §15 and `source-pins.json`. The refinement source is `rohanarun/sidorenko-template-refinements` at `d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d`; it is a research draft, not the original publication. No priority claim is made here.

Two recovered predecessor documents, `certificate(1).md` and `global_energy_adversarial_review.md`, supplied the proposed quantitative composition and energy route. They were treated as untrusted evidence. Their mathematical interfaces are reconstructed below; their programs were not run. The present small checker was written anew. In particular, a predecessor's conditional conclusion is not itself used to establish (T).

The uploaded `public-research-sources-20261011(3).zip` has SHA-256
`0fdb243cadcf1a85028f1126dd92f0c2707137a9f160c018e5d5908dbedd0ee3`.
Its 389 manifest entries passed independent length, SHA-256, and Git-blob consistency checks. It contains **none** of the Sidorenko manuscript sections, comparator, or refinement files. Its 17 OpenAI files concern integer multiplication. The required Sidorenko text was instead recovered through read-only GitHub calls at the immutable pins. Manifest consistency is not a mathematical certification or independent authentication of unrelated source claims.

The actual comparator is `lean/ComparatorChallenges/SidorenkoCounterexample.lean`. Its graph and all-map density definitions match §1. Its `main` declaration is a challenge stub containing `sorry`; the adjacent JSON names `OAI.Combinatorics.Sidorenko.RandomHost` as the solution module. Neither the stub nor an axiom allowlist is used as proof here. The full source Lean solution closure was not audited or compiled.

Family 161 is the subject of this result. No arithmetic cost assertion in Family 109's finite-alphabet multitape model or Family 130's exact-arithmetic RAM model is inferred from it.

## 1. The literal graph and finite combinatorics

The faces, in order `j=0,...,21`, are

```
(0,1,3)   (0,1,9)   (0,2,3)   (0,2,9)
(1,3,10)  (1,7,10)  (1,7,12)  (1,9,12)
(2,3,4)   (2,4,9)   (3,4,11)  (3,10,11)
(4,8,9)   (4,8,11)  (5,6,7)   (5,6,11)
(5,7,10)  (5,10,11) (6,7,12)  (6,8,11)
(6,8,12)  (8,9,12).
```

The corresponding bit strings are

```
000 010 001 110 001 000 100 110 101 100 111
101 101 011 000 110 010 111 001 010 011 111.
```

Write `I={0,...,12}`, `J={0,...,21}`, `C={(i,j):i belongs to face j}`. The incidence graph has vertex set `I disjoint-union J` and edge set `C`; its 66 edges are not the 33 edges of the auxiliary point graph. Let `E` be those 33 unordered point pairs. Each belongs to exactly two faces. The graph joining faces sharing a point pair is connected, as is the graph on the 33 point pairs that joins the three pairs in each face into a triangle. Point degrees are at most six.

For `e` with incident faces `j,k`, put

\[
a_e=\operatorname{Hamming}(\mathrm{bits}_j,\mathrm{bits}_k)/3,
\qquad\rho_e=a_e-1/3.
\]

All `rho_e>=0`, and the only nonzero values are

\[
\rho_{02}=2/3,\qquad
\rho_{48}=\rho_{56}=\rho_{5,10}=\rho_{7,12}=1/3.
\tag{1.1}
\]

Thus `sum rho_e=2`. There are 28 zero-excess pairs; their point degrees are

\[
(3,6,3,6,4,2,4,4,4,6,4,6,4),\qquad
\sum_i\binom{2d_i}{2}=468.\tag{1.2}
\]

Each bit position has two classes of eleven faces. The following orders start with three points and then introduce precisely one new point per face, sharing a pair with an earlier face:

```
bit 1, 0: 0 1 2 4 5 16 14 18 20 19 13
bit 1, 1: 3 9 8 10 11 17 15 12 21 7 6
bit 2, 0: 0 2 8 9 12 4 11 5 6 18 14
bit 2, 1: 1 3 7 21 20 19 13 10 15 17 16
bit 3, 0: 0 1 3 9 7 6 5 16 14 15 19
bit 3, 1: 2 8 10 11 4 17 13 12 21 20 18.
```

All of these are finite assertions verified directly from the displayed triples. `check_certificate.py` rebuilds the pair table, connectivity, coverage, all six fresh-point orders, and every support used later. Optional immutable-blob comparisons are supported with `--complex-source` and `--comparator-source`; these read local source text as data only.

## 2. Elementary finite-field counts, with constants

Throughout §§2–7, `q` is an odd prime. A symmetric form's sign is the quadratic character of the determinant on its nondegenerate quotient by its radical. The zero-dimensional determinant is one. We distinguish the signed matrix-layer mass `p_xi` from the Lagrangian pair mass `pi_{D,r}`.

### 2.1 Finite products and symmetric forms

For every finite initial product and `q>=3`,

\[
\frac12\le\prod_{j=1}^n(1-q^{-j})\le1,
\qquad1\le\prod_{j=1}^n(1+q^{-j})\le2.\tag{2.1}
\]

For the first inequality, expand successively or use `product(1-x_j)>=1-sum x_j`, with `sum q^{-j}<1/(q-1)<=1/2`. For the second, expansion bounds the product by `sum_{k>=0}(sum q^{-j})^k<=2`. Factoring powers in the ordered-basis formula gives

\[
{n\brack t}_q=
\prod_{a=0}^{t-1}\frac{q^n-q^a}{q^t-q^a},\qquad
1\le {n\brack t}_q q^{-t(n-t)}\le2.\tag{2.2}
\]

The lower bound follows termwise after writing the numerator exponents as `n-t+j>=j`. Also

\[
\tfrac12q^{n^2}\le |\mathrm{GL}_n(q)|
=q^{n^2}\prod_{j=1}^n(1-q^{-j})\le q^{n^2}.\tag{2.3}
\]

For a uniform symmetric `n`-form, `n>=1`, Schur-complement induction gives

\[
\Pr(\text{singular})\le n/q,
\quad
\left|\Pr(\text{nonsingular of sign }\xi)-\tfrac12\right|
\le n/(2q).\tag{2.4}
\]

Indeed, when the leading `(n-1)`-minor is invertible, the final Schur scalar is uniform. It vanishes with probability `1/q`, and each nonzero character has probability `(q-1)/(2q)`. The exceptional minor has probability at most `(n-1)/q`. Applying these bounds above and below yields (2.4), starting with the empty minor.

A prescribed radical `t`-space imposes `nt-binom(t,2)` independent zero coefficients. Summing over prospective radical spaces and using (2.2) proves

\[
\Pr(\operatorname{nullity}Z\ge t)\le2q^{-b(t)}.\tag{2.5}
\]

Every rank-`k` symmetric matrix with image a fixed `k`-space with basis matrix `P` is uniquely `PRP^T`, with `R` a nonsingular symmetric `k`-matrix. A left inverse of `P` proves existence and uniqueness; the induced nondegenerate quotient has the sign of `R`. Thus the signed rank count is exactly a Gaussian coefficient times the count of nonsingular forms on a `k`-space. In particular, for `D=2r`,

\[
p_\xi={D\brack r}_q q^{b(r)-b(D)}
       \Pr(Z_r\text{ nonsingular of sign }\xi).\tag{2.6}
\]

This is an exact normalization identity, not an assumed moment formula.

### 2.2 Lagrangians and the matrix chart

In a symplectic `2n`-space let

\[
L_n=\prod_{j=1}^n(q^j+1),\quad
\vartheta_n(t)=L_{n-t}/L_n,\quad
I_n(t)=(L_n/L_{n-t}){n\brack t}_q.\tag{2.7}
\]

These count Lagrangians, give containment probabilities for a fixed isotropic `t`-space, and count isotropic `t`-spaces, respectively. For completeness, count pairs consisting of a line and a containing Lagrangian. Reduction by that line gives
`L_n(q^n-1)=(q^{2n}-1)L_{n-1}`. This proves the product starting from `L_0=1`. Reduction by an isotropic `t`-space is a bijection to the Lagrangians of its symplectic quotient. Double-counting `(t-space,Lagrangian)` proves `I_n(t)`.

For a fixed Lagrangian `A`, choose its intersection `h`-space with `B`; after quotienting, `B` is a symmetric graph transverse to the image of `A`. This gives

\[
\pi_{n,h}={n\brack h}_q q^{b(n-h)}/L_n,
\qquad \tfrac12q^{-b(h)}\le\pi_{n,h}\le2q^{-b(h)},\tag{2.8}
\]
\[
\tfrac12q^{-nt+\binom t2}\le\vartheta_n(t)
\le q^{-nt+\binom t2}.\tag{2.9}
\]

A symplectic basis of the common space and a dual basis of the transverse quotient show that ordered pairs with the same intersection dimension form one orbit. Symplectic basis extension follows by choosing dual vectors and correcting their mutual alternating products by half of the resulting skew matrix; the odd-characteristic hypothesis permits division by two.

Graphs `Gamma_X={(x,Xx)}` of symmetric `D`-matrices form a chart of mass

\[
\beta_D=q^{b(D)}/L_D\ge1/2,
\qquad\dim(\Gamma_X\cap\Gamma_Y)=D-\operatorname{rank}(X-Y).
\tag{2.10}
\]

For independent Lagrangians use the unsigned normalized kernel

\[
J(L,Y)=\frac{\mathbf1_{\{\dim(L\cap Y)=r\}}}{\pi_{D,r}}.
\]

For independent matrices use

\[
K_\xi(Z)=\frac{\mathbf1_{\{\operatorname{rank}Z=r,
                       \operatorname{sign}Z=\xi\}}}{p_\xi}.
\]

Each kernel has mean one in either variable when the other is fixed. For `q>=16D`, (2.6) gives `p_xi>=q^{-b(r)}/8`; (2.8) then gives `pi_{D,r}/p_xi<=16`. For every nonnegative integrand in the 35 variables, dropping signs and conditioning all variables into the chart yields the comparison multiplier

\[
\beta_D^{-35}\prod_{\kappa\in B}\pi_{D,r}/p_{\xi_\kappa}
\le2^{35}16^{66}=2^{299}.\tag{2.11}
\]

There is no boundedness assumption on that nonnegative integrand. This matters for the singular tail.

### 2.3 Every individual ordered triple orbit

For a Lagrangian triple write `c` for the common dimension, `h_i` for opposite pair dimensions, `s_i=h_i-c`, `d=D-c`, `a=sum s_i`, `z=d-a`, and

\[
C=(D+1)c+\sum_i b(s_i).\tag{2.12}
\]

After common-space reduction the three pair spaces `H_i` are mutually orthogonal and in direct sum: a relation among them puts each summand in the zero common intersection. In particular `a<=d`.

Choosing the common space, the direct-sum pair spaces, and the required containments has exact weighted count

\[
I_D(c)\vartheta_D(c)^3\,
I_d(a)\frac{|\mathrm{GL}_a|}{\prod_i|\mathrm{GL}_{s_i}|}
\prod_i\vartheta_d(a-s_i).\tag{2.13}
\]

Its exponent is `-C`. The common group has normalized upper bound 4; the remaining group has upper bound 32. Ignoring exactness proves the profile upper bound `128q^{-C}`. Pair transitivity and (2.8) give, conditional on any specified older pair of dimension `h`, the fresh-third completion upper bound

\[
256q^{-C+b(h)}.\tag{2.14}
\]

A profile upper bound is not an individual-orbit lower bound. We establish the latter separately. For a common-zero triple, choose inside `L_i` a space `Q_i` paired perfectly with `H_i`. Then `H_i+Q_i` is a nondegenerate symplectic block. Each triple member contains a Lagrangian of that block, and its projection into the block lies in that contained Lagrangian. Hence all three members actually split across the block. The other pair spaces lie in its orthogonal complement. Repeating leaves a transverse triple in dimension `2z`. Its ordered orbit is determined by the congruence class of a nonsingular symmetric `z`-form. Conversely, isometries of these residual triples extend across the pair blocks and common-space quotient. There are no uncounted extension invariants.

For a specified residual form orbit `O_F`, the probability of that ordered residual triple orbit is

\[
q^{b(z)}|O_F|/L_z^2.\tag{2.15}
\]

An isometry of a nonsingular symmetric `z`-form is determined by the images of an orthogonal basis with prescribed nonzero norms. In a remaining nondegenerate `k`-space there are at most `2q^{k-1}` vectors of a prescribed norm, by fixing all but one diagonal coordinate. Therefore
`|Isom(F)|<=2^z q^{z(z-1)/2}`. Orbit-stabilizer and (2.3) imply that (2.15) is at least `2^{-z-3}`. When `z=0` the exact probability is one, so the same bound remains valid.

To preserve exact intersections when lifting this estimate, put `H_*=direct_sum H_i` and `A_i=direct_sum_{j!=i}H_j`. Under the three separate containments `A_i subset L_i`, require separately `L_i intersect H_*=A_i`. Its failure probability is at most

\[
\frac{q^{s_i}-1}{q-1}\frac1{q^{z+s_i}+1}<\frac12.
\tag{2.16}
\]

These separate events preserve independence. Each reduction to `H_*^perp/H_*` is uniform: extend any symplectic quotient automorphism by the identity on `H_*` and a dual space. Conditional invariance and transitivity prove uniformity, separately for each sample. A prescribed transverse residual orbit then forces the original pair intersections to be exact: a common vector reduces to zero, hence lies in `H_*`, where the avoidance conditions identify it with the prescribed pair space. The chosen common and pair spaces are consequently unique for each successful triple; there is no multiplicity loss in this lower bound.

The normalized common and pair factors in (2.13) are bounded below by `2^-4` and `2^-5`; (2.16) costs at most `2^-3`, and the residual orbit costs `2^{-z-3}`. Thus **every occurring individual ordered orbit** obeys

\[
\boxed{\Pr(O)\ge2^{-D-15}q^{-C}.}\tag{2.17}
\]

This deliberately loose constant is uniform in the orbit, profile, and odd prime.

## 3. The planted face bound on an explicit finite domain

### 3.1 Domain and selected gain

For a face with all three incidences active use integer variables

\[
\begin{gathered}
0\le u\le\min(c,r),\quad r'=r-u,\quad0\le r'\le d,\quad
\delta=2u-c=d-2r',\\
p_i,t_i\ge0,\quad p_i+t_i=s_i,\quad P=\sum p_i,\quad T=\sum t_i,
\quad P+T\le d,\\
0\le t_i\le p_i+\delta,\quad0\le v\le p_i+\delta,\quad
w=(d-3\delta)/2-P+v\ge0.
\end{gathered}\tag{3.1}
\]

Define `g_j` to be the maximum on this finite integer domain of

\[
(r+c+1)u-2u^2+\sum_i b(s_i)
-\delta P-\sum_i p_i^2-vw-\sum_i b(t_i)+b(v).
\tag{3.2}
\]

An empty domain means that the face factor is zero and the profile can be omitted. With two active incidences use `g_j=b(floor(h/2))`, where `h` is their actual pair dimension. With at most one active incidence use `g_j=0`.

This domain is larger than the manuscript's union of actually realized tuples. We prove everything below on this larger domain; no transfer from a smaller-domain classification is assumed. The maximum is independent of `q`. The entries counted below are all at most `D`, so at most `(D+1)^5` choices of `u,p_1,p_2,p_3,v` suffice; the `t_i` are then determined.

### 3.2 Density, subspaces, and correlated lift differences

Choose a uniform center `Y` and then independent `L_i` conditioned separately on `dim(L_i intersect Y)=r`. The resulting planted density against independent triples is exactly `E_Y product_i J(L_i,Y)`. It is constant on each ordered orbit and equals its planted mass divided by its independent mass. Thus (2.17), not a dimensional-profile average, is the denominator needed for a pointwise bound.

Fix a prospective actual common space `C_0` and put `u=dim(C_0 intersect Y)`. Choosing a prospective contained `u`-space gives center cost at most

\[
2q^{-u(D-c)-b(u)}.\tag{3.3}
\]

In the common-space quotient there is the exact identity

\[
(L_i/C_0)\cap Y'
=((L_i\cap Y)+C_0)/C_0,
\quad
Y'=((Y\cap C_0^\perp)+C_0)/C_0.\tag{3.4}
\]

A representative in the left side can be chosen in `Y intersect C_0^perp`; since `C_0 subset L_i`, membership modulo `C_0` is equivalent to actual membership in `L_i`. The kernel is `C_0 intersect Y`. Therefore the reduced incidence dimension is exactly `r-u`, not an extra condition on unknown lifts.

Before imposing mutual intersections, the reduced intersections `R_i=L_i' intersect Y'` are independent uniform `r'`-spaces. Their common intersection must be zero in an actual common-zero quotient. Let `p_i=dim(R_j intersect R_k)` and `v=d-dim(sum R_i)`. Their pair spaces are in direct sum. The three pair-relation spaces in the kernel of the summation map from the external direct sum of the `R_i` have total dimension `P`; this proves `w>=0`.

Choose a prospective span of dimension `n=d-v`, put all three `R_i` in it, choose and decompose the prospective pair-space sum, and require the pair containments in each `R_i`. Applying (2.2)–(2.3) to these four operations gives multiplier at most

\[
2\cdot4^3\cdot(2\cdot8)\cdot4^3=2^{17}
\]

and exponent

\[
nv-3r'v+nP-\sum_i p_i^2-2(n-r')P
=-\delta P-\sum_i p_i^2-vw.\tag{3.5}
\]

Containments not dimensionally possible contribute zero. Dropping exactness at these steps only enlarges the count.

For `A_i=R_i^circ subset (Y')^*`, every remaining Lagrangian lift is uniquely specified by a symmetric form `F_i` on `A_i`:

\[
L'(R_i,F_i)=\{(y,\zeta):\zeta\in A_i,
\ \beta(y)=F_i(\zeta,\beta)\text{ for all }\beta\in A_i\}.
\tag{3.6}
\]

The kernel of projection is `R_i`, its image is `A_i`, and isotropy is precisely symmetry of `F_i`. There are exactly `q^{b(d-r')}` lifts; the three forms are independent uniform before the mutual profile is imposed.

Let `Q_i=A_j intersect A_k` and use cyclic differences

\[
D_1=(F_2-F_3)|_{Q_1},\quad
D_2=(F_3-F_1)|_{Q_2},\quad
D_3=(F_1-F_2)|_{Q_3}.
\]

A simultaneous lift exists precisely when the two prescribed classes agree on the common annihilator. This proves the exact sequence

\[
0\longrightarrow R_j\cap R_k
\longrightarrow L_j'\cap L_k'
\longrightarrow\operatorname{rad}D_i\longrightarrow0.\tag{3.7}
\]

Consequently the additional intersection dimension is `t_i=nullity D_i` and `dim Q_i=p_i+delta`. If `V=A_1 intersect A_2 intersect A_3`, then `dim V=v`, and the exact image of the cyclic-difference map is

\[
\{(D_1,D_2,D_3): D_1|_V+D_2|_V+D_3|_V=0\}.\tag{3.8}
\]

To prove sufficiency, prescribe `F_1|V=0`, `F_2|V=-D_3|V`, `F_3|V=D_2|V`. On each `Q_i` extend the positive term arbitrarily and set the negative term by subtraction. Each `F_i` receives two prescriptions agreeing on their intersection `V`. Split that intersection from two complements and choose their mixed block arbitrarily; this extends the two prescriptions to one symmetric form on `A_i`. No additional relation between three ambient subspaces obstructs these separate extensions. The map summing restrictions onto `V` is surjective, so (3.8) has codimension `b(v)`.

Uniform forms push forward to uniform measure on this image. Equivalently, independent target difference forms are conditioned on an event of probability `q^{-b(v)}`. Applying (2.5) before that conditioning gives the full simultaneous-nullity bound

\[
2^3q^{-\sum_i b(t_i)+b(v)}.\tag{3.9}
\]

The `b(v)` loss is explicitly paid. The three difference forms are **not** declared independent.

### 3.3 Constants and lower-activity cases

The numerator ledger, before division by (2.17), is

| Operation | Multiplier | Exponent |
|---|---:|---|
| Common space and three containments | `2^2` | `-(D+1)c` |
| Center/common intersection | `2` | `-u(D-c)-b(u)` |
| Three reduced incidences and planted normalizers | `2^9` | `3[b(r)-b(r-u)]` |
| Three center subspaces with pair/span data | `2^17` | `-delta P-sum p_i^2-vw` |
| Correlated lift nullities | `2^3` | `-sum b(t_i)+b(v)` |

Every multiplier follows from (2.1)–(2.9); for example the three normalized pair ratios cost at most `4^3<=2^9`. The common/center exponent simplifies exactly to `(r+c+1)u-2u^2`. Dividing the total `2^32` numerator multiplier by (2.17) and summing the at most `(D+1)^5` tuples proves

\[
\boxed{\mathbb E_Y\prod_{i\in A_j}J(L_i,Y)
\le A_D q^{g_j},\qquad
A_D=2^{D+47}(D+1)^5.}\tag{3.10}
\]

For two active incidences, the two center `r`-spaces have intersection `p` with probability at most `2^3q^{-p^2}`. One uniform symmetric form on a `p`-space has nullity `t=h-p` at cost at most `2q^{-b(t)}`. Dividing by the pair mass in (2.8) and summing at most `D+1` values costs at most `2^6(D+1)`, below `A_D`. The exponent is

\[
b(h)-p^2-b(h-p).
\]

Its difference at consecutive `p` is `h-3p-1<0` for `p>=ceil(h/2)`. At `p=ceil(h/2)` its value is `b(floor(h/2))`, proving the stated gain. Zero or one active incidence has exact factor one by normalization. Thus (3.10) is uniform over every activity subset, including lower-activity faces.

## 4. A universal energy inequality on the relaxed gain domain

For a full point profile and arbitrary activity subset define

\[
\begin{split}
C_j&=(D+1)c_j+\sum_{e\subset j}b(h_e-c_j),\\
\mathcal C&=\frac12\left(\sum_j C_j-\sum_e(1-a_e)b(h_e)\right),\\
\beta_j&=C_j/2-\tfrac16\sum_{e\subset j}b(h_e),\quad
S_j=\beta_j-g_j,\\
\mathcal E&=\tfrac12\sum_e\rho_e b(h_e),\quad
\Delta=\mathcal C-\sum_jg_j=\sum_jS_j+\mathcal E.
\end{split}\tag{4.1}
\]

The gains are exactly the maxima on (3.1), not gains restricted to geometrically realizable tuples. Every compatible local tuple may be selected independently for an upper bound. No simultaneous geometric realizability of maximizing tuples is asserted or needed.

### 4.1 Exact local slack and a four-region quadratic proof

For a three-active face, substitution of (3.2) into (4.1) gives

\[
S=\frac{c(d+\delta-1)-\delta(d+2)+2\delta^2}{4}
+\sum_i\left[\frac{(2p_i-t_i)(2p_i-t_i-1)}6
+\delta p_i-\frac c6(p_i+t_i)\right]+vw-b(v).
\tag{4.2}
\]

Write `S=Q-L`, with `Q` its homogeneous quadratic part and

\[
L=c/4+\delta/2+(2P-T)/6+v/2.
\]

**Quadratic lemma.** On the entire real domain underlying (3.1),

\[
\boxed{Q\ge(P+T)^2/72.}\tag{4.3}
\]

This is a universal inequality, not a finite dimension sweep. Here is a positive certificate covering its full domain. Put

\[
a_*=\left(P-\frac{d-3\delta}{2}\right)_+.
\]

The `v`-quadratic is at least `-a_*^2/2`. From `w>=0`, `v<=p_i+delta`, and `d>=P+T`,

\[
a_*\le v\le P/3+\delta,\qquad
 a_*\le(P-T+3\delta)/2.
\]

Both right sides are nonnegative. Cauchy–Schwarz on the three numbers `2p_i-t_i` therefore gives

\[
Q\ge\frac{c(d+\delta)-\delta d+2\delta^2}{4}
+\frac{(2P-T)^2}{18}+\delta P-\frac{c(P+T)}6
-\frac12\min\left(P/3+\delta,(P-T+3\delta)/2\right)^2.
\tag{4.4}
\]

The coefficient of `c` equals

\[
(d+\delta)/4-(P+T)/6=(d+3\delta)/12+(d-P-T)/6\ge0,
\]

because `T<=P+3delta` implies `d+3delta>=2T`. Replacing `c` by `|delta|` is consequently in the correct lower-bound direction.

For `delta>=0` subtract `(P+T)^2/72` from the resulting lower bound, calling it `H_+(T)`. Its interval is `0<=T<=e=P+3delta`, with breakpoint `b=P/3+delta`. The endpoint values are

\[
H_b=(4P+3\delta)(4P+9\delta)/216,
\qquad H_e=\delta(4P+15\delta)/24.
\]

On the first interval put `R=b-T`. Exact expansion gives

\[
H_+(b-R)=H_b+R(16P/3+2\delta+R)/24\ge0.\tag{4.5}
\]

On the second interval, with `ell=e-b`, exact expansion gives

\[
\ell H_+(T)=(e-T)H_b+(T-b)H_e
              +\ell(T-b)(e-T)/12\ge0.\tag{4.6}
\]

If `ell=0`, then `P=delta=0` and the claim is immediate.

For `delta=-y<0` put `x=P-3y>=0`; now `0<=T<=x`. After setting `c=y`, the coefficient of `d` is `y/2`, so replacing `d` by `P+T` again lowers the bound. The resulting expression before subtraction is

\[
y^2/4+(2x-T)y/3+(2x-T)^2/18
-\tfrac12\min(x/3,(x-T)/2)^2.
\]

Subtract `(x+3y+T)^2/72` and call this `H_-(T)`. Here `b=x/3`, `e=x`, and

\[
H_b=(16x^2+96xy+27y^2)/216,
\qquad H_e=y(4x+3y)/24.
\]

For `R=b-T`,

\[
H_-(b-R)=H_b+R(16x/3+10y+R)/24\ge0.\tag{4.7}
\]

The second interval has exactly the chord identity (4.6) with these endpoints. If `x=0`, its sole value is `y^2/8`. Every factor in the four regional identities is nonnegative on its stated region. This proves (4.3). The sparse-polynomial checker verifies the identities coefficientwise over the rationals; their inequality signs are established by the displayed domain argument.

### 4.2 The loss estimate, including all lower-activity faces

Two exact identities give

\[
\frac{3c+P+T}{2}-L
=c/4+(c-\delta)+2T/3+(P/3+\delta-v)/2\ge0,
\tag{4.8}
\]
\[
2(P+T)^2-\sum_{i<k}(s_i-s_k)^2
=6\sum_{i<k}s_i s_k\ge0.\tag{4.9}
\]

Since `h_i=c+s_i`, (4.3), (4.8), and (4.9) imply on a three-active face

\[
S_j\ge\frac1{144}\sum_{e<e',\ e,e'\subset j}(h_e-h_{e'})^2
              -\frac12\sum_{e\subset j}h_e.\tag{4.10}
\]

For fewer active incidences, choose `s_0=max s_i` and `h=c+s_0=max h_i`. Direct subtraction gives the useful exact identity

\[
\beta-\left[\frac{b(h)}3+\frac{b(c)}6
                  +\frac{b(s_1)+b(s_2)}3\right]
=\frac c6(3d-3s_0-s_1-s_2)\ge0.\tag{4.11}
\]

The last sign uses `d>=s_0+s_1+s_2`. For integer `h`,

\[
\frac{b(h)}3-b(\lfloor h/2\rfloor)
=\begin{cases}k(k-1)/6,&h=2k,\\(k+1)(k+2)/6,&h=2k+1.
\end{cases}\tag{4.12}
\]

It is nonnegative, with zeros only at `h=0,2`. Also
`b(floor(h/2))<=h(h+2)/8`. Thus every lower-activity face has

\[
S_j\ge0,\qquad S_j\ge h^2/24-h/12.\tag{4.13}
\]

Because its squared pair differences sum to at most `2h^2` and its pair dimensions sum to at least `h`, (4.13) implies (4.10) for these faces too. Equality `S_j=0` is possible only with `c=0` and either all pair dimensions zero, or exactly one pair dimension two whose endpoints are exactly the two active incidences. With zero or one active incidence only the all-zero alternative is possible. This follows from the positive terms in (4.11)–(4.12); when the gain is zero, the dimension-two alternative has strictly positive beta.

### 4.3 Anchored edge energy and the exact rational ellipsoid

Let `L_triangle` be the 33-by-33 Laplacian with one triangle on the three pair coordinates in each face. Set

\[
K=L_\triangle/144+\operatorname{diag}(\rho)/4,
\qquad\lambda_e=1-\rho_e/4.
\]

Every pair appears in two faces. Summing (4.10) and retaining both terms of `rho_e b(h_e)/2` gives

\[
\boxed{\Delta\ge h^TKh-\lambda^Th.}\tag{4.14}
\]

The Laplacian is connected and its only null vectors are constants. The nonzero diagonal anchors from (1.1) eliminate those constants. Thus `K` is positive definite.

Let `z=K^{-1}lambda` and `H=lambda^T K^{-1}lambda`. If `Delta<=0`, completing the square and applying Cauchy–Schwarz in the `K` inner product gives

\[
(h-z/2)^TK(h-z/2)\le H/4,
\qquad h_e\le\tfrac12[z_e+\sqrt{H(K^{-1})_{ee}}].\tag{4.15}
\]

This bounds an enlarged ellipsoid; it does not presume simultaneous realization of its coordinate extrema.

Here is the exact certificate for the original template. Order the 33 pairs lexicographically, put `d_e=3rho_e`, `bvec_e=12-d_e`, and

\[
A=144K=L_\triangle+12\operatorname{diag}(d).
\]

The symmetric integer matrix `N` in `certificate.json` satisfies

\[
AN=\tau I,\qquad\tau=821810346672.
\tag{4.16}
\]

For `u=N bvec` and `Hnum=bvec^T N bvec`, the exact integer values are

\[
Hnum=7702171993838184,
\]
\[
\min_e(609\tau-6u_e)=327514878189744>0,
\]
\[
\min_e\{(609\tau-6u_e)^2-36Hnum\,N_{ee}\}
=419595924675382839454010976>0.\tag{4.17}
\]

The right side of (4.15) is `6(u_e+sqrt(Hnum N_ee))/tau`; (4.17) makes it strictly less than 609. Every integer nonsaving profile therefore obeys

\[
\boxed{M:=\max_eh_e\le608.}\tag{4.18}
\]

All 1,089 matrix-product entries and all 33 strict inequalities are checked with integer/rational arithmetic. The inverse is independently reconstructed from the literal graph, rather than accepted from a predecessor's matrix. A one-entry corruption is rejected.

## 5. Removing the common mode and classifying every nonsaving profile

Put `kappa=(c-delta)/2=c-u`, `n_i=2p_i-t_i`, and

\[
S_0=3c(c-1)/4+\tfrac16\sum_i[n_i^2+(c-1)n_i+3cp_i].
\]

Expanding (4.2) gives the exact identity

\[
S=S_0+\frac\kappa2[d-3c-2\delta+2-4P]
       +\frac v2[d-3\delta-2P+v-1].\tag{5.1}
\]

Since `p_i<=s_i<=M-c` and `delta<=c`, the brackets are at least

\[
D-12M+6c+2,\qquad D-6M+2c+v-1.\tag{5.2}
\]

The differences between the actual brackets and these bounds are respectively
`2(c-delta)+4[3(M-c)-P]` and `3(c-delta)+2[3(M-c)-P]`, both nonnegative. At `D>=12M`, the first bracket is strictly positive; the second is strictly positive whenever `v>0`, since then `M>=1`.

For `c>=2`,

\[
S_0=\frac{(c-1)(5c+1)}8+\tfrac16\sum_i(n_i+(c-1)/2)^2+cP/2>0.
\tag{5.3}
\]

For `c=1`, `S_0=sum(n_i^2+3p_i)/6`; equality forces every `p_i=t_i=0`. For `c=0`, feasibility gives `delta=0` and `t_i<=p_i`, hence the **integers** `n_i>=p_i>=0` obey

\[
S_0=\tfrac16\sum_i n_i(n_i-1)\ge0.
\]

The zero cases are exactly `(p_i,t_i)=(0,0)` or `(1,1)` for each `i`.

Now suppose `D>=7296=12*608` is even and `Delta<=0`. By (4.18), `D>=12M`. Every local slack is nonnegative by (5.1)–(5.3) and (4.13), as is `E`. Their sum is `Delta<=0`, so all vanish. Three-active faces have `kappa=v=0`. A zero-slack face with `c=1` has all three `h_e=1`. Its neighbor across any such pair must also be a three-active `c=1` equality face, because all other equality cases have pair dimensions zero or two. Connected face adjacency propagates this to every face and pair. But then `E=(sum rho_e)/2=1`, a contradiction.

Consequently, for **every activity pattern and every nonempty relaxed-gain profile**, the nonsaving locus is exactly constrained by

\[
\boxed{c_j=0,\quad h_e\in\{0,2\},\quad\mathcal E=0,
\quad S_j=0,\quad\Delta=0,
\quad\sum_jg_j=\tfrac23\sum_e b(h_e).}\tag{5.4}
\]

The last identity follows from `c_j=0`, `beta_j=sum_{e subset j}b(h_e)/3`, and the two occurrences of every pair. Positive-excess pairs have dimension zero. This proves the previously unadmitted residual classification on the **same enlarged integer domain** as the quantitative planted bound. It is not a retained assumption.

Integrality is essential. As an adversarial check, put `h_e=1`, `c_j=delta=u=v=0`, and `p_i=t_i=1/2` on every face. For any even `D>=12` this satisfies the real relaxation, but gives `S_j=-1/8`, `E=1`, and `Delta=-7/4`. This is a real relaxed counterprofile, not realizable dimension data and not a counterexample to (5.4). Continuous quadratic optimization cannot replace the integer equality argument.

## 6. Quantitative transverse estimates and the signed rank-layer model

For an activity subset `B subset C` and prescribed signs define

\[
R_D(B,\xi;q)=\mathbb E\prod_{(i,j)\in B}K_{\xi_{ij}}(X_i-Y_j).
\]

For a point pair `e={v,w}` on faces `j,l` set

\[
U_e=\{(v,j),(w,j),(v,l),(w,l)\},
\]

and define the integrated parity model

\[
P(B,\xi)=\prod_{e:U_e\subseteq B}
       \left(1+\prod_{\kappa\in U_e}\xi_\kappa\right),
\qquad0\le P\le2^{33}.\tag{6.1}
\]

### 6.1 Restriction-sign concentration with an explicit error

Assume `q>=16D`. For a family of `M` distinct `r`-subspaces and a uniform symmetric form `Q`, let `f_xi(Q)` be the fraction on which the restriction is nonsingular of sign `xi`. Two distinct restrictions overlap precisely in their common subspace `T`, of dimension at most `r-1`. Conditional on its nonsingular form, their remaining Schur complements are independent uniform forms of positive size. By (2.4), the centered second moment is bounded by

\[
\mathbb E(f_\xi-1/2)^2
\le\frac1{4M}+\frac{r-1}{4q}+\frac{r^2}{4q^2}
\le\frac1{4M}+D/q.\tag{6.2}
\]

The diagonal contribution is `1/(4M)`; the common-block singular event costs at most `(r-1)/(4q)`. Conditioning `Q`, or both `Q` and `Q-L`, nonsingular divides a nonnegative error expectation by at most `1-2D/q>=7/8`. Thus, for `q>=16D` and `M>=q`,

\[
\mathbb E[|f_\xi-1/2|\mid\text{that conditioning}]
\le2Dq^{-1/2},\tag{6.3}
\]

uniformly in fixed `L`. No further conditioning on determinant-sign matches is made.

### 6.2 Half-rank center parametrization and normalization

If `B` is nonsingular of size `2r` and `A` has rank `r`, then

\[
\operatorname{rank}(B-A)=r\quad\Longleftrightarrow\quad AB^{-1}A=A.
\tag{6.4}
\]

For the forward implication, the two rank-`r` images span the whole space and are complementary; `AB^{-1}` is their projection. Conversely it is an idempotent of rank `r`, so its complementary idempotent has rank `r`. Writing `A` and `A-B` in basis matrices of their complementary images and taking determinants gives the sign condition

\[
\chi(\det B)=c_0\xi_1\xi_2,
\qquad c_0=\chi((-1)^r).\tag{6.5}
\]

We also need the number of maximal isotropic `r`-spaces of a split nonsingular symmetric `2r`-form. A nonsingular symmetric form diagonalizes in odd characteristic. The sets of values of `ax^2` and `t-by^2` each have `(q+1)/2` elements, so meet; hence every nonsingular form of dimension at least three has a nonzero isotropic vector. Splitting off hyperbolic planes leaves anisotropic dimension at most two. In dimension two, `ax^2+by^2` is isotropic precisely when `chi(-ab)=1`. It follows that the `2r`-form is split precisely when its determinant sign is `c_0`; equivalently, it has an isotropic `r`-space.

In split coordinates `(x,y)`, there are `(q^r-1)(q^{r-1}+1)` nonzero isotropic vectors. Count incidences between their lines and maximal isotropic subspaces, reducing by a line. The recurrence yields

\[
N_r=\prod_{a=0}^{r-1}(1+q^a)
=2q^{r(r-1)/2}\prod_{a=1}^{r-1}(1+q^{-a}).\tag{6.6}
\]

This counts **both** isotropic families. For `r>1`, it is at least `q`.

On a transverse point triple put
`B_0=X_1-X_2`, `B_1=X_1-X_3`, `Q=B_0^{-1}`, `L=B_0^{-1}-B_1^{-1}`. Write a prospective center difference as `A=PRP^T`. Applying (6.4) twice shows that centers correspond bijectively to maximal `L`-isotropic `r`-spaces on which `Q` restricts nonsingularly, with

\[
P^TLP=0,\qquad R=(P^TQP)^{-1}.\tag{6.7}
\]

All three pair-sign matches force `L` split, and the sign of `Q|U` determines the remaining center sign. Thus the exact normalized factor on matches is

\[
F_3=A_3 f_{\xi_1},\qquad
 A_3=\frac{q^{-b(D)}N_r}{p_{\xi_1}p_{\xi_2}p_{\xi_3}};
\]

off matches it is zero. Its model is `8` on matches and zero otherwise. Given fixed nonsingular `L` and transversality, `Q` is uniform subject exactly to `Q,Q-L` nonsingular: inversion of the initially independent uniform pair `B_0,B_1` gives a bijection with such `Q`. This justifies applying (6.3) with the matching indicator kept **inside** the expectation.

With two active incidences the same argument uses all `r`-subspaces, with

\[
A_2=\frac{q^{-b(D)}{D\brack r}_q}{p_{\xi_1}p_{\xi_2}},
\]

and model value `2` on the one pair-sign match. Zero or one active incidence has factor one.

For explicit bounds put `x=D/q<=1/16`. The normalized Gaussian coefficient and product in (6.6) lie in `[1,1+x/6]`: (2.1)'s geometric-sum argument bounds each by `1+1/(q-2)<=1+D/(6q)`. By (2.4)–(2.6),

\[
1-x/2\le u_\xi:=2q^{b(r)}p_\xi\le1+x.
\]

The powers of `q` in `A_3,A_2` cancel. It follows that

\[
16(1-3x)\le A_3\le16(1+5x),\quad |A_3-16|\le80x,
\]
\[
4(1-2x)\le A_2\le4(1+4x),\quad |A_2-4|\le16x.\tag{6.8}
\]

For the first upper bound, `(1+5x)(1-x/2)^3-(1+x/6)` divided by `x` is
`10/3-(27/4)x+(29/8)x^2-(5/8)x^3>0` on `[0,1/16]`. For the second it is `17/6-(15/4)x+x^2>0`. The lower bounds follow by expanding the corresponding reciprocal-product inequalities. In particular `F_3<=21` and `F_2<=5`. Combining with (6.3) gives the convenient uniform envelope

\[
0\le F_j\le128\quad\text{on its transverse event},\qquad
\mathbb E[\mathbf1_{\mathcal T_j}|F_j-G_j|]
\le128Dq^{-1/2}.\tag{6.9}
\]

### 6.3 Joint determinant signs, not merely marginal balance

For point pairs put `eta_e=chi(det(X_i-X_k))`; its orientation is immaterial because `D` is even. Fix a nonempty subset of selected pairs and a vertex incident with `s` selected pairs, `1<=s<=6`. Set `n=D-1`. Conditional on its lower-right minor, the `s` difference minors are independent uniform symmetric `n`-matrices.

For independent unrestricted symmetric `Q_l`, each nonzero linear combination is uniform, so (2.5) gives

\[
\Pr\{\exists t\ne0:\operatorname{rank}(\sum_l t_lQ_l)\le s\}
\le2q^{s-b(n-s)}\le2q^{-9}.\tag{6.10}
\]

Conditioning all of them nonsingular costs at most `8/5`, since `s n/q<=6D/q<=3/8`. Inversion preserves the independent uniform nonsingular laws. Therefore the event that all difference minors are nonsingular and every nonzero combination of their inverses has rank at least `s+1` fails with probability at most

\[
6D/q+4q^{-9}.\tag{6.11}
\]

Only now freeze all entries except the central off-diagonal vector `z`. It remains uniform. Each selected determinant is a fixed nonzero minor determinant times

\[
a_i-a_k-(z-z_k)^TM_k^{-1}(z-z_k).
\]

Every nonzero joint Fourier frequency has quadratic rank at least `s+1`. For an odd-characteristic quadratic polynomial with quadratic matrix `A`, differencing gives

\[
|\mathbb E_z\psi(z^TAz+\ell^Tz+c)|^2
\le\Pr_u(Au=0)=q^{-\operatorname{rank}A}.
\]

Indeed, after translating by `u`, the average over `z` vanishes unless `Au=0`. Parseval and Cauchy–Schwarz therefore give total variation at most `q^{-1/2}/2` between the `s` quadratic evaluations and the uniform law on `F_q^s`. The product of their quadratic characters has uniform mean zero. All other selected determinant-sign factors are fixed and bounded by one. Thus every nonempty subset sign moment has absolute value at most

\[
q^{-1/2}+6D/q+4q^{-9}.\tag{6.12}
\]

Replace zero edge signs by `+1`. This changes a subset moment by at most `33D/q`. Walsh inversion on the 33-sign cube, applied to all nonempty subset moments, yields

\[
\operatorname{TV}(\widetilde\eta,\mathrm{Unif}\{\pm1\}^{33})
\le2^{39}Dq^{-1/2}.\tag{6.13}
\]

This proves a joint bound despite shared point matrices; no independent-sign premise was assumed.

### 6.4 Assembling the weighted rank-layer estimate

Given point matrices, centers are independent. On global transversality, telescope the product of 22 local factors in (6.9). This costs less than `2^159 Dq^{-1/2}`. The bounded model is at most `8^22=2^66`; removing the transverse indicator costs at most `33*2^66 D/q`. Replacing the joint determinant-sign law by independent signs via (6.13) costs at most `2^106 Dq^{-1/2}`. Their sum is below `2^170 Dq^{-1/2}`.

For each pair, averaging its two face factors over one independent sign yields `1` unless all four corners are active, and otherwise yields `1+product of the four incidence signs`. The two `c_0` factors cancel. This is exactly (6.1).

For the nontransverse contribution, use the nonnegative chart comparison (2.11), followed by the planted bound (3.10) conditional on the point Lagrangians. Define

\[
\mathfrak T_D(q;B)=
\mathbb E_L\left[\mathbf1_{\{\exists e:h_e>0\}}q^{\sum_jg_j}\right],
\]

with zero weight on an empty local domain. We have proved, for every even `D>=12`, every odd prime `q>=16D`, and **every** activity/sign pattern,

\[
\boxed{|R_D-P|\le2^{170}Dq^{-1/2}
              +2^{299}A_D^{22}\mathfrak T_D(q;B).}\tag{6.14}
\]

This weighted inequality itself has no residual-classification assumption.

## 7. The singular tail: profile saving and a robust span count

### 7.1 Profile probability and its lattice saving

For each of the six exposure orders in §1, bound its first face by `128q^{-C_j}` and every fresh-point completion by (2.14). Conditioning is on **all** earlier point variables; the fresh one remains independent and uniform. The resulting class-event bound has multiplier
`128*256^10=2^87`.

The full profile event is contained in every class event. Take the geometric mean of the six upper bounds. Each face occurs three times; each pair's subtraction occurs at precisely the bit positions in which its two incident faces agree. Hence

\[
\Pr(\text{full dimensional profile})\le2^{87}q^{-\mathcal C}.
\tag{7.1}
\]

No independence of classes or cuts is used. There are at most `(D+1)^55` dimensional profiles, from 33 pair dimensions and 22 common dimensions. Moreover `6mathcal C` and every gain are integers. Thus the total weighted contribution of all saving profiles `Delta>0` is at most

\[
2^{87}(D+1)^{55}q^{-1/6}.\tag{7.2}
\]

### 7.2 Strict span defect

By §5, a nonsaving singular profile has nonzero pair spaces `H_e` of dimension two on some nonempty subset of the 28 zero-excess pairs. Put `m=#such pairs`, `k=dim(sum_e H_e)`, and `k_i=dim(sum_{e incident i}H_e)`. Its total gain is `2m`.

For any ordering of the spaces, either endpoint's local dimension increment is at least the global dimension increment. Therefore `sum_i k_i>=2k`. If the family is not in direct sum, choose an inclusion-minimal nondirect subfamily and order it first. Its final space has a positive intersection, of dimension `t`, with the preceding global span. At least one endpoint of that final edge misses an earlier edge in the subfamily, since the graph is simple. The subfamily visible at that endpoint, including the final edge, is a proper subfamily and hence direct. Its local increment is the full dimension two, whereas the global increment is `2-t`. Later increments still satisfy the weak inequality. Thus

\[
\boxed{\sum_i k_i\ge2k+1\quad\text{for every nondirect family}.}\tag{7.3}
\]

This includes partial intersections, not just a fully redundant last space. The global span need not be isotropic. A nonisotropic local span has containment probability zero.

### 7.3 Direct families

For a globally direct family, order its edges and choose an ordered basis of each two-space. If the current edge has `a` previous neighboring edges, its first vector must be orthogonal to a `2a`-space, and its second must also be orthogonal to the first vector. Global directness makes these independent constraints, yielding at most `q^{4D-4a-1}` choices. For a fixed family every ordered basis choice preserves global directness, so division by the full number of bases is legitimate here. By (2.3), `|GL_2(q)|>=q^4/2`.

Write `d_i` for the selected support degrees. The sum of the previous-neighbor counts is `sum_i binom(d_i,2)`, and local containment costs at most
`product_i q^{-2Dd_i+binom(2d_i,2)}`. After division by bases and multiplication by the residual gain `q^{2m}`, the exponent is exactly

\[
4Dm-4\sum_i\binom{d_i}{2}-m-4m
-4Dm+\sum_i\binom{2d_i}{2}+2m=-m.
\]

Thus each support costs at most `2^m q^{-m}`. Summing all nonempty supports gives

\[
2^{56}q^{-1}.\tag{7.4}
\]

### 7.4 Nondirect families without per-pattern basis division

Fix a support and the actual global span dimension `2<=k<=2m-1<=55`. Count a prospective global `k`-space and then its `m` two-spaces, discarding exact-span and local-isotropy constraints only after bounding the weights. The count is at most

\[
{2D\brack k}_q{k\brack2}_q^m
\le2^{m+1}q^{k(2D-k)+2m(k-2)}.\tag{7.5}
\]

For every actual family (7.3) gives its endpoint-containment bound

\[
\prod_i\vartheta_D(k_i)
\le q^{-D(2k+1)+\sum_i\binom{k_i}{2}}
\le q^{-D(2k+1)+468},
\]

because `k_i<=2d_i` and (1.2) applies. Including `q^{2m}`, the exponent in (7.5) is at most

\[
-D-k^2+2mk-2m+468
\le-D+m^2-2m+468\le-D+1196.\tag{7.6}
\]

There are at most `2^28` supports, 55 span dimensions, and multiplier at most `2^29` per count. Their product is below `2^63`. Hence the total nondirect residual contribution is at most

\[
2^{63}q^{-D+1196}.\tag{7.7}
\]

In (7.5) a weight is first bounded on the actual families, then their number is enlarged. There is no division by bases on a type-refined subset and no unproved multiplicity claim.

Combining (7.2), (7.4), and (7.7), for every even `D>=7296`,

\[
\mathfrak T_D\le2^{87}(D+1)^{55}q^{-1/6}
+2^{56}q^{-1}+2^{63}q^{-D+1196}
\le2^{88}(D+1)^{55}q^{-1/6}.\tag{7.8}
\]

At `D=7296`, the last exponent is `-6100`. Using (6.14),

\[
|R_D-P|\le2^{170}Dq^{-1/2}
+2^{22D+1421}(D+1)^{165}q^{-1/6}
\le C_Dq^{-1/6},
\tag{7.9}
\]

where one valid uniform envelope is

\[
\boxed{C_D=2^{32D+2048}(D+1)^{256},\quad
 D\ge7296\text{ even},\quad q\ge16D.}\tag{7.10}
\]

For example, each summand's coefficient is at most `C_D/2`: their ratios are dominated by the spare factor `2^{10D+627}(D+1)^91` for the second summand and much more for the first. This is the effective rank-layer estimate needed below. It is uniform over **all** activity subsets and prescribed signs.

### 7.5 The refinement obstruction and why it is not used

The refinement's fixed-pattern argument applies a lower bound on each family's full ordered-basis multiplicity to the vector-list count of a single pattern. This inference need not hold: one family need not contribute all its bases to one pattern. A source-template example makes the issue concrete. In a symplectic basis, for even `D>=4` and odd prime `q>=13`, set

\[
\begin{split}
L_1&=\langle e_1,\ldots,e_D\rangle,\\
L_0&=\langle e_1,e_2,f_3,\ldots,f_D\rangle,\\
L_7&=\langle e_1,f_2,e_3,e_t+f_t:4\le t\le D\rangle.
\end{split}
\]

For the other ten points choose ten distinct `lambda` outside `{0,1}` and let
`L(lambda)=span(e_t+lambda f_t:1<=t<=D)`. Every displayed space is Lagrangian. The only positive intersections on point-graph pairs are

\[
H_{01}=\langle e_1,e_2\rangle,\qquad
H_{17}=\langle e_1,e_3\rangle.
\]

Their shared line also gives `L_0 intersect L_7=<e_1>`, but `{0,7}` is **not** a point-graph pair. All face common dimensions are zero and the excess is zero. This is an actual geometric residual profile with `k=3`, `sum k_i=7`.

Order `H_01` before `H_17`. Exactly the fraction `1/(q+1)` of the ordered bases of `H_17` have their first vector in the shared line. Thus a complete pattern selecting that event contains that fraction, not the family's full basis multiplicity. For two abstract two-spaces over `F_3`, the corresponding count is `48*12=576`, versus `48^2=2304` full bases; dividing the pattern by full multiplicity gives `1/4` for one family.

At `q=13`, the displayed source-template configuration is checked directly in symplectic dimension eight (`D=4`). A two-space has 26,208 ordered bases, of which 1,872 have their first vector in its specified line. The pattern therefore has `26,208*1,872=49,061,376` bases for the one family. This is even smaller than the refinement's proposed lower divisor `(3q^4/8)^2=7,341,576,489/64`, not just smaller than the exact full multiplicity `686,859,264`. Thus that uniform per-pattern multiplicity premise fails as stated. The checker verifies every pair intersection, common-zero face, and these basis counts exactly. The construction in the displayed formulas works for every even `D>=4` and prime `q>=13`; the small computation checks one instance, not the general argument.

The repair is to sum the weighted vector counts over **all complete basis patterns before division**:

\[
\sum_{\mathcal H}w(\mathcal H)=|GL_2(q)|^{-m}
\sum_{\text{all patterns}}\sum_{\text{basis lists in pattern}}w(\mathcal H).
\tag{7.11}
\]

This is an exact partition identity for basis-invariant weights. The present theorem avoids needing a sharpened `189` remainder at all: (7.5)–(7.7) provide an independently sufficient `1196` bound. This identifies an inference gap in that draft, not a counterexample to its numerical conclusion after suitable repair, and not a defect inferred merely from missing artifacts.

## 8. The exact source activation law and its negative identity coefficient

There are 66 independent matrix coordinates, one for each corner in `C`. For each type pair `(a,b)` in `I x J`, sample an activity subset `S subset C` and signs on it, then define the rectangular kernel by the expectation of

\[
\prod_{\kappa\in S}K_{\xi_\kappa}(x_\kappa-y_\kappa).
\tag{8.1}
\]

When multiplying kernel entries along the source graph, use an independent copy of the activity/sign sample for each source incidence, even when several incidences have the same type pair. This is the exact product-of-expectations identity for (8.1), not a shared random law across repeated type pairs. The matrix coordinates in both vertex spaces are independent uniform symmetric matrices, independent of their type draws. Every type-pair kernel has mean one. **Equal type values at different source vertices do not identify their matrix variables.** Conditional on any repeated type map those matrix samples remain independent, so (7.9) applies without an injectivity qualification.

Put `phi_alpha(S,xi)=1_{alpha subset S} product_{kappa in alpha}xi_kappa`, with `phi_empty=1`. For a corner `kappa=(v,j)`, let `e,f` be the two point pairs in face `j` incident with `v`; set

\[
M_\kappa=U_e\cup U_f,\qquad
\Gamma_\kappa=U_e\mathbin\triangle U_f.
\]

The literal graph gives `|M_kappa|=7`, `|Gamma_kappa|=6`, and `M_kappa\Gamma_kappa={kappa}`. Fix `theta=1/2`. Take `sigma_(0,0)=-1` and every other corner sign `sigma_kappa=+1`.

At an incident type pair `kappa`, use this base law:

* with probability `1/2`, use `S=M_kappa` and conditional sign probability
  `2^-7(1+sigma_kappa theta product_{Gamma_kappa}xi)`;
* with probability `1/2`, use `S=Gamma_kappa` and conditional sign probability
  `2^-6(1-sigma_kappa theta product_{Gamma_kappa}xi)`.

At a nonincident type pair use `S=empty`. All displayed probabilities are rational and strictly positive on their branch. Summing independent signs shows

\[
\mathbb E\phi_\alpha=0\quad(\alpha\ne\varnothing).\tag{8.2}
\]

Indeed, within each branch only the empty character and the `Gamma_kappa` character have nonzero Fourier coefficients, and the latter coefficients cancel between branches.

For `Q=alpha union beta`, `R=alpha symmetric-difference beta`, the exact overlap moment is

\[
\begin{split}
A_\kappa(\alpha,\beta)
={}&\tfrac12\mathbf1_{Q\subseteq M_\kappa}
      (\mathbf1_{R=\varnothing}+\sigma_\kappa\theta\mathbf1_{R=\Gamma_\kappa})\\
&+\tfrac12\mathbf1_{Q\subseteq\Gamma_\kappa}
      (\mathbf1_{R=\varnothing}-\sigma_\kappa\theta\mathbf1_{R=\Gamma_\kappa}).
\end{split}\tag{8.3}
\]

This follows from `phi_alpha phi_beta=1_{Q subset S} product_R xi`. The checker enumerates both finite branch distributions exactly, checks all 254 nonempty first moments for the two choices of sigma, and checks 4,374 compatible union/difference moment identities. In particular

\[
A_\kappa(U_e,U_f)=\sigma_\kappa/4.\tag{8.4}
\]

Now expand the product of the parity models (6.1) over all 66 coordinates. Label each point pair `e` by a coordinate subset `alpha_e subset C`. At a source corner the two adjacent labels contribute the overlap moment for its assigned type pair. By (8.2), a term with an empty label adjacent to a nonempty label vanishes. The connected graph of pair coordinates therefore forces every surviving term either to have all labels empty or to have all labels nonempty. The all-empty term is exactly one.

For a fixed part-preserving type map `f`, call the complete sum of all-nonempty terms `C(f)`. There are `(2^66-1)^33<2^2178` possible label tuples and each overlap moment is bounded in absolute value by one. Thus

\[
|C(f)|\le M_C:=2^{2178}.\tag{8.5}
\]

For the identity type map, (8.3) implies `alpha_e subset intersection_{kappa in U_e}M_kappa`. The literal supports satisfy

\[
\bigcap_{\kappa\in U_e}M_\kappa=U_e.\tag{8.6}
\]

Also `U_e intersect U_f={kappa}` at their shared corner. If the two nonempty labels there were disjoint, their overlap moment would be a zero first moment. They must therefore both contain `kappa`. Applying this at all four corners of `U_e` forces `alpha_e=U_e`. The identity all-nonempty labeling is unique. Equations (8.4) and the one negative sigma give the exact coefficient

\[
\boxed{C(\mathrm{id})=-4^{-66}=-2^{-132}.}\tag{8.7}
\]

The support intersections (8.6) and all 66 singleton overlaps are rebuilt in the finite certificate. Nothing is assumed about the signs of the other `C(f)`.

## 9. Source-realizable rational pinning, including every repeated type map

Color refinement starts with the two part colors. Let `h_t(v)` be the histogram of neighbors' colors before round `t`; the next color consists of the old color and this histogram. On the literal incidence graph, the within-part color-class counts after four rounds are

\[
(3,1),\quad(3,7),\quad(13,7),\quad(13,22).\tag{9.1}
\]

These are checked directly; in particular the final coloring is discrete within each part.

At round `t`, give each vertex type `a` score `-||h_t(a)||^2`, and **every** type pair `(a,b)`, including nonincidences, score

\[
2h_t(a)(\ell_{t-1}(b))+2h_t(b)(\ell_{t-1}(a)).\tag{9.2}
\]

For any part-preserving map `f`, repeated values permitted, its round score is the sum over the 35 source vertices and 66 source incidences. If it preserves the previous colors, exact completion of squares gives

\[
F_t(\mathrm{id})-F_t(f)
=\sum_{v\in V(H)}\|h_t(f(v))-h_t(v)\|^2.\tag{9.3}
\]

To see this, the directed-neighbor sum at a source vertex is the scalar product of its own histogram with the histogram of its image; previous-color preservation is the only property used. No graph-homomorphism or injectivity property of `f` is needed.

For all maps, a round score lies in `[-666,1188]`: the squared vertex loss is at most `13*6^2+22*3^2=666`, and the 66 pair contributions are individually at most `2*6+2*3=18`. Thus any round difference is at most 1854. Combine the four rounds with weights `1856^{4-t}`. At a nonidentity map's first failing round the loss is a positive integer, at least one; later gains cannot cancel it because

\[
1856^k-1854\sum_{j=0}^{k-1}1856^j\ge1.\tag{9.4}
\]

The final discrete colors ensure that such a first failing round exists. The identity is consequently the unique maximizer with integral score gap at least one, **over all `13^13 22^22` maps**.

Let the combined vertex and pair scores be `s_i,s_j,s_ij`. Shift them to nonnegative exponents

\[
a_i=s_i-\min_I s,\quad b_j=s_j-\min_J s,\quad
\ell_{ij}=\max_{I\times J}s_{ij}-s_{ij}.
\]

Choose the fixed integer score base `T=2^2459` and the rational common priors and pair thinnings

\[
Z_I=\sum_iT^{a_i},\quad Z_J=\sum_jT^{b_j},\qquad
\pi_i=T^{a_i}/Z_I,\quad\nu_j=T^{b_j}/Z_J,\quad
\lambda_{ij}=T^{-\ell_{ij}}.\tag{9.5}
\]

These scores are source-realizable: at a type pair keep the **whole** base activation law with probability `lambda_ij` and otherwise use the empty activity set. Consequently

\[
A^\lambda_{ij}(\alpha,\beta)
=\lambda_{ij}A_{ij}(\alpha,\beta)
+(1-\lambda_{ij})\mathbf1_{\alpha=\beta=\varnothing}.\tag{9.6}
\]

In an all-nonempty term this contributes exactly one `lambda` per source incidence. It is not an arbitrary assignment-dependent weight. All vertices in one part use the same prior, independently.

The type-map weight is precisely

\[
w_f=\frac{T^{E(f)}}{Z_I^{13}Z_J^{22}},\qquad
E(f)=\sum_{i\in I}a_{f(i)}+\sum_{j\in J}b_{f(j)}
                -\sum_{(i,j)\in C}\ell_{f(i),f(j)}.
\tag{9.7}
\]

The shifts change every map score by the same constant. Hence `w_f<=w_id/T` for every nonidentity map, including repetitions and maps taking incidences to nonincidences. Some such maps have zero coefficient; the bound does not need that fact.

The independently reconstructed exact score certificate gives

\[
\max a_i=127937502468,\qquad \max b_j=20679552,
\]
\[
E(\mathrm{id})=115295183886,
\qquad B_{\rm pin}=13\max a+22\max b-E(\mathrm{id})
=1548347298342.\tag{9.8}
\]

Since `13^13 22^22<2^147`, the competing coefficient sum has absolute value less than

\[
w_{\rm id}\,2^{147}2^{2178}/2^{2459}
=w_{\rm id}2^{-134}.
\]

With (8.7), the complete nonempty coefficient in the intended orientation satisfies

\[
t_0=\sum_f w_f C(f)\le-\tfrac34\,2^{-132}w_{\rm id}.
\tag{9.9}
\]

Also `Z_I<=13T^{max a}`, `Z_J<=22T^{max b}`, so

\[
w_{\rm id}>2^{-(147+2459B_{\rm pin})}.
\]

Define `Z=280+2459B_pin=3807386006623258`. Equations (9.9) and the last bound imply

\[
\boxed{t_0\le-m_0,\qquad m_0=2^{-Z}.}\tag{9.10}
\]

In the reversed orientation the corresponding coefficient `t_1` is an average, under the independently drawn common priors, of label sums whose terms are bounded by one. Thus

\[
|t_1|\le M_C=2^{2178}.\tag{9.11}
\]

All scores, priors, and activation laws in this section are rational and fixed **before** choosing `q` or taking any limit. The proof does not optimize priors separately for individual assignments.

## 10. Both orientations, inactive-type dilution, and the explicit field threshold

Add an inactive type `*` to the `I`-type side with probability `1-epsilon`, and multiply every old `I`-type probability by `epsilon`. Every pair involving `*` uses empty activity. Keep the `J` prior unchanged. Choose exactly

\[
\varepsilon=\frac{m_0}{8M_C}=2^{-(Z+2181)},
\qquad \alpha=m_0\varepsilon^{13}=2^{-A_0},
\quad A_0=14Z+28353.\tag{10.1}
\]

A nonempty-label term requires every source vertex on the diluted side to be active. There are 13 such vertices in the intended orientation and 22 in the reverse. The two integrated parity-model values are therefore exactly

\[
a_\infty=1+\varepsilon^{13}t_0,\qquad
b_\infty=1+\varepsilon^{22}t_1.\tag{10.2}
\]

They are nonnegative because they also are averages of the nonnegative coordinate parity products. By (9.10)–(9.11),

\[
0\le a_\infty\le1-\alpha,\qquad
0\le b_\infty\le1+\alpha/8,
\quad a_\infty b_\infty\le1-7\alpha/8.\tag{10.3}
\]

For the reverse upper bound, `epsilon^9 M_C<=epsilon M_C=m_0/8` because `0<epsilon<1`. This is why no sign claim about `t_1` is needed.

The matrix reversal is also legitimate. Negating a rank-`r` form multiplies its discriminant sign by `chi((-1)^r)`; here `r=3648` is even, so each signed layer is individually unchanged. More generally the four-corner parity product cancels the common sign multiplier. In the reverse orientation the point matrices and center matrices still have independent uniform laws conditional on their type maps. Repeated types cause no identification of samples.

For a rational bound on the finite-field error put

\[
\eta_q=C_D/\lfloor q^{1/6}\rfloor.
\]

By (7.9), each of the 66 coordinate moments differs from its parity model by at most `eta_q`. If `eta_q<=1`, both the moment and the model are at most `2^34`. Telescoping their product gives, uniformly before averaging any type or activation choices,

\[
|a_q-a_\infty|,\ |b_q-b_\infty|
\le H_c\eta_q,\qquad H_c=66(2^{34})^{65}=66\,2^{2210}.
\tag{10.4}
\]

Averaging this uniform error under arbitrary rational priors does not introduce a factor for the number of type maps. All source matrix coordinates are independent; all vertex matrix draws remain independent when type values repeat.

Now take

\[
J_q=64H_cC_D/\alpha
=66\,7297^{256}2^{53303404092991701},
\qquad Q_0=16D+J_q^6.
\tag{10.5}
\]

For every odd prime `q>Q_0`, `floor(q^{1/6})>=J_q`, hence `H_c eta_q<=alpha/64`. In particular `eta_q<=1`. Write `e=alpha/64`. Since `a_infty<=1`, `b_infty<=2`, the product perturbation is at most `3e+e^2<=4e`. From (10.3),

\[
\boxed{a_qb_q\le1-3\alpha/4\le1-\Gamma,
\qquad\Gamma=\alpha/2=2^{-\Lambda}.}\tag{10.6}
\]

This supplies a specified field threshold, not a choice described as merely sufficiently large.

## 11. A bounded rational kernel; no discretization error

Let `W` be the fixed finite rectangular kernel at the chosen prime, after both thinnings. Write its vertex spaces as `X` and `Y`, including types and their 66 independent matrix coordinates. On the finite product probability space `Omega=X x Y`, define

\[
V((x,y),(x',y'))=W(x,y')W(x',y).
\tag{11.1}
\]

It is symmetric and nonnegative. Its two factors have independent arguments under the product law, so `E V=1`. In its product over `H`, the factors using `(x_i)_{i in I},(y_j)_{j in J}` use variables disjoint from those using `(y_i)_{i in I},(x_j)_{j in J}`. Therefore, exactly,

\[
t(H,V)=a_qb_q\le1-\Gamma.\tag{11.2}
\]

Each signed rank-`r` layer is nonempty: take a diagonal rank-`r` form with the desired determinant character. Thus `p_xi>=q^{-b(D)}` and `K_xi<=q^{b(D)}`. Every activation term uses at most seven coordinates. Both thinnings are convex mixtures with the constant one kernel, so

\[
0\le W\le q^{7b(D)},\qquad0\le V\le q^{14b(D)}.
\]

Choose the specified bound, not an unevaluated maximum,

\[
L=q^{14b(D)},\qquad U=V/L.
\]

Then `0<=U<=1`, `mu=1/L`, and by homogeneity on the 66 edges,

\[
\mu^{66}-t(H,U)\ge\Gamma L^{-66}
=2^{-\Lambda}q^{-924b(D)}=\Delta_q.\tag{11.3}
\]

Here `b(D)=26619456`, `14b(D)=372672384`, and `924b(D)=24596377344`. This proves (K).

Every number in the construction is rational already. There are exactly `308q^{132b(D)}` possible atoms in `Omega` if the unused matrices of the inactive type are retained. A common denominator for their probabilities is the explicit integer

\[
\mathcal M=2^{Z+2181}Z_IZ_Jq^{132b(D)}.\tag{11.4}
\]

For a fixed matrix-tuple pair and old types `(i,j)`, its probability multiplied by `M` is `T^{a_i+b_j}`. For types `(*,j)` it is
`(2^{Z+2181}-1) Z_I T^{b_j}`. These are positive integers summing, over all atoms, to `M`. Replacing each atom by that many identical clones produces a uniform finite kernel **exactly**. All homomorphism densities and the mean are unchanged, including contributions of coincident original atoms. This is an exact pushforward of product measures, not a limiting discretization. Kernel values on original-atom and clone diagonals are retained in this step; the cloned object is still a kernel, not yet a loopless simple graph. Host-loop deletion is paid separately in §12.

The edge probabilities also have an explicit common denominator. Let `n_+` and `n_-` be the two positive integer signed rank-layer counts, and let `ell_max=max ell_ij`. One common denominator for all `W` entries is

\[
\mathcal D_W=512\,T^{\ell_{\max}}(n_+n_-)^7,
\]

because every branch probability has denominator dividing 512, every thinning denominator divides `T^{ell_max}`, and every term has at most seven signed-layer denominators. Hence a common denominator for `U` is

\[
\mathcal D=\mathcal D_W^2q^{14b(D)}.\tag{11.5}
\]

In particular `D U(z,z')` is an integer in `[0,D]`. If a source-specific deterministic generator is preferred, enumerate all `M^n D^{binom(n,2)}` choices of uniform clone labels and integer edge coins; for distinct host vertices put an edge when its coin is below `D U(z,z')`, and return the first graph passing the deficit test. The expectation argument in §12 proves this finite enumeration terminates. The smaller graph-space enumeration in (A) avoids enumerating redundant source outcomes.

The counts `n_+,n_-` are computable by a bounded loop through the `q^{b(D)}` symmetric matrices, testing rank and quotient discriminant by exact elimination modulo the explicitly chosen prime. Formula (2.6) is an alternative exact count. Thus neither normalizer nor an edge-coin denominator hides an existence-only choice. These loops were not executed at the enormous theorem parameters.

There is also a bound for this **source-specific** label-and-coin enumeration that eliminates the unevaluated normalizer counts. For the prime selected in §13, use `q<2^{F_q}` there, `n_+,n_-<=q^{b(D)}`, and the certified value `ell_max=25601296520`. Then

\[
\mathcal M<2^{L_{\rm atom}},\qquad
\mathcal D<2^{L_{\rm coin}},
\]
\[
L_{\rm atom}=Z+2181+9+2459(\max a+\max b)+132b(D)F_q
=1123774834967853447267918484,
\]
\[
L_{\rm coin}=18+4918\ell_{\max}+42b(D)F_q
=357564720215858629205464514.
\]

The factor `13*22<2^9` bounds the two prior normalizers. For `N` in (T), the source-specific generator therefore tests fewer than

\[
2^{N L_{\rm atom}+\binom N2 L_{\rm coin}}
\]

label-and-coin outcomes, after the bounded prime search and fewer than `2^{8513445719422207667361408}` symmetric matrices for the two signed normalizers. Each integer coin is interpreted exactly as in (11.5). This is a second explicitly terminating generator that follows the source sampling construction itself, distinct from the smaller exhaustive graph-space search. The exponent calculations are included in `certificate.json`. No outcome enumeration was performed.


## 12. Sampling, host diagonals, collisions, and deterministic generation

Let a symmetric finite probability kernel satisfy `0<=U<=1`, `mu=E U`, and `tau=t(H,U)<=mu^66-Delta_q`. Sample `n` labels independently. For each unordered pair of **distinct** host vertices sample one independent edge, conditional on labels, with probability `U` at those labels. Draw no loops. Equal labels on distinct host vertices are allowed; they use the kernel's actual diagonal entry and separate edge coins.

For the resulting simple graph,

\[
\mathbb E p(G)=(1-1/n)\mu.\tag{12.1}
\]

For any injective map of the 35 source vertices into the host, all 66 source edges map to distinct unordered host pairs; its probability of being a homomorphism is exactly `tau`. The proportion of all `n^35` maps identifying any two source vertices is at most `binom(35,2)/n=595/n`. Each such map has a homomorphism indicator in `[0,1]`. A collision on an edge gives zero; repeated image edges use their actual single Bernoulli trial. We never assign them independent trials. It follows that

\[
\mathbb E t(H,G)\le\tau+595/n.\tag{12.2}
\]

By convexity of `x^66` on the nonnegative reals and `(1-1/n)^66>=1-66/n`,

\[
\begin{split}
\mathbb E[p(G)^{66}-t(H,G)]
&\ge ((1-1/n)\mu)^{66}-\tau-595/n\\
&\ge\Delta_q-\frac{66\mu^{66}+595}{n}
\ge\Delta_q-661/n.
\end{split}\tag{12.3}
\]

Thus for `n>=1322/Delta_q` some simple graph has deficit at least `Delta_q/2`. This is a finite average over explicitly finite rational label and edge-coin spaces (§11), so the conclusion uses neither an asymptotic random-graph limit nor an assumed finite-host theorem. The graph must have an edge: an edgeless graph has both densities zero.

Here is the complete quantitative error ledger:

| Interface | Explicit bound or treatment |
|---|---|
| One coordinate's rank/parity error | `C_D q^(-1/6)`, §§2–7 |
| Its rational upper certificate | `eta_q=C_D/floor(q^(1/6))` |
| Product of 66 coordinates, each orientation | `H_c eta_q<=alpha/64` |
| Nonidentity type maps | `<2^-134 w_id`; all maps included |
| Reversed orientation before field error | positive loss at most `alpha/8` |
| Product of two orientation errors | at most `4(alpha/64)` |
| Surviving unscaled symmetric deficit | at least `Gamma=alpha/2` |
| Scaling | exact factor `q^(-924b(D))` in the deficit |
| Rational priors and finite vertex discretization | zero error, exact cloning (11.4) |
| Rational edge-probability discretization | zero error, exact integer coins (11.5) |
| Missing host loops in the edge-density moment | at most `66mu^66/n<=66/n` |
| Every noninjective source map, including repeated image edges | at most `595/n` |
| Total finite-host loss | at most `661/n` |

For a fixed simple host with neighborhoods `N_G(v)`, its all-map homomorphism count can be evaluated exactly as

\[
\boxed{\operatorname{hom}(H,G)=
\sum_{(z_i)\in V(G)^{13}}
\prod_{j\in J}\left|\bigcap_{i\in j}N_G(z_i)\right|.}\tag{12.4}
\]

To prove this, first choose the images of the 13 point vertices, with repetitions unrestricted. The image of each face vertex can be any common neighbor of its three point images. Those 22 choices are independent choices of vertices because `H` has no face-to-face edges; they too may repeat. Their product counts exactly the allowed face assignments. Repeated point images cause repeated identical neighborhood factors in the intersection, which is precisely the correct constraint, not a reason to discard that point assignment. Summing proves (12.4).

Consequently the graph enumerator in (A) uses at most `2^{binom(N,2)}` graph tests, at most `2^{binom(N,2)}N^13` point-label assignments, and at most `22*2^{binom(N,2)}N^13` common-neighborhood cardinalities. All remaining operations are total finite integer operations. Its mathematical implementation may use elementary binary-string counters and schoolbook arithmetic; no fast multiplication or exact-real RAM oracle is required. These are termination bounds, not practical resource estimates.

`generator.py` contains the exact all-map counter, integer acceptance predicate, and enumerator as a reference implementation. It defaults to printing symbolic parameters and has an explicit full-run guard. The mathematical specification is over arbitrary finite binary strings; a fixed real Python installation cannot allocate the full-size integers, let alone this host. Only the small sanity tests were run. This computational boundary does not replace or weaken the mathematical termination proof.

## 13. A bounded prime search and the completely fixed host order

A factorial-based prime choice would be effective but unnecessarily inflate the size bound. The following elementary binomial-coefficient argument gives the required bounded search, with no unquantified prime-distribution input.

**Large-input prime lemma.** For every integer `n>=2^16`, there is a prime strictly between `n` and `2n`.

**Proof.** Let `P(x)=product_{p prime,p<=x}p`. Strong induction proves `P(m)<=4^m` for integers `m`: for an even `m>=4`, `P(m)=P(m-1)`; for `m=2k+1`, every prime in `(k+1,2k+1]` divides `binom(2k+1,k)`, so

\[
P(2k+1)\le P(k+1)\binom{2k+1}{k}
\le4^{k+1}2^{2k}=4^{2k+1}.
\]

The small starting cases are immediate. The middle binomial bound follows because its two equal central terms are part of a sum `2^{2k+1}`. The bound extends to real `x` by taking the floor.

Suppose there were no prime in `(n,2n)`. In `binom(2n,n)`, each prime `p<=sqrt(2n)` contributes a prime power at most `2n`: its exponent is the sum of terms `floor(2n/p^a)-2floor(n/p^a)`, each zero or one. There are at most `sqrt(2n)` such primes. Above `sqrt(2n)` each prime exponent is at most one; primes in `(2n/3,n]` contribute zero, and by assumption none above `n` contribute. Therefore

\[
\frac{4^n}{2n+1}\le\binom{2n}{n}
\le(2n)^{\sqrt{2n}}4^{2n/3}.
\]

This would imply

\[
2n/3\le\log_2(2n+1)+\sqrt{2n}\log_2(2n).\tag{13.1}
\]

For `2^k<=n<2^{k+1}`, `k>=16`, elementary induction gives
`k+2<=2^{k/2-2}` and `k+3<=2^{k-3}`. Hence
`log_2(2n)<=sqrt(n)/4` and `log_2(2n+1)<=n/8`. Using `sqrt(2)<3/2`, the right side of (13.1) is at most `n/8+3n/8=n/2`, a contradiction. The endpoint `2n` is composite, so strict upper inequality holds. This proves the lemma.

Apply it to the explicit integer `Q_0`. Define `q` as the first prime in the ordered list `Q_0+1,...,2Q_0-1`, using trial division. It is an odd prime above the field threshold. The search tests fewer than `Q_0` candidates and at most `2Q_0^2` candidate divisors. This defines an exact deterministic prime, not an unspecified admissible one.

For the size estimate, use `66<2^7`, `7297<2^13`, and the exact constants (P). They imply

\[
J_q<2^{A_0+241071}=2^{53303404092995036},
\]
\[
Q_0<2J_q^6<2^{319820424557970217},
\qquad
\boxed{q<2^{F_q},\quad F_q=319820424557970218.}\tag{13.2}
\]

Let `S=24596377344` and

\[
B=11+\Lambda+SF_q=7866423844799423288734694969,
\qquad N=2^B.
\]

Then (11.3) and (13.2) give

\[
\Delta_q>2^{-\Lambda-SF_q}=2^{11-B}=2048/N.
\]

For the random simple host of order `N`, (12.3) consequently gives

\[
\mathbb E[p(G)^{66}-t(H,G)]> (2048-661)/N=1387/N.
\]

Some graph therefore has deficit greater than `1387/N`, in particular at least `1024/N`. This proves (T) and the termination of (A). Multiplying its density inequality by `N^132` gives exactly the integer acceptance test (A).

The size estimate is extremely large but literal: `log_2 N=B`, approximately `7.8664*10^27`. Even writing the integer `N` in binary would require `B+1` bits. No compact host or usable adjacency list has been constructed. The theorem gives a bounded deterministic generator and a compressed exact rational gap, not a practical graph search.

## 14. Approaches, revisions, and dependency ledger

Three distinct interfaces were addressed rather than assuming that a small residual lemma composed automatically.

First, the original coarse propagation route can establish large-dimension control, but makes the dimension choice unnecessarily large. The anchored 33-coordinate energy route instead produces an exact finite inverse certificate, bounds every nonsaving pair dimension by 608 independently of `D`, and the separate common-mode identity proves the all-integer residual classification at `D=7296`. The real-relaxation counterprofile in §5 demonstrates why the integer step is indispensable.

Second, the refinement's finer sequential-basis argument has the per-pattern multiplicity obstruction in §7.5. Summation before division is the valid repair. The theorem does not need to assume that repair closes every sharper remainder claim: the independently proved global-span count `q^{-D+1196}` is already more than adequate at the admitted dimension. Thus neither `189` nor an unaudited residual bound is a dependency.

Third, the source's qualitative pinning, field choice, and finite-host transfer are replaced by source-realizable integer scores, exact rational priors, a uniform finite-field remainder, exact rational cloning, a two-orientation budget, and a proved bounded prime search. The all-map host test (12.4) and the finite average in (12.3) complete the theorem. No giant field, factorial, or host was instantiated.

The dependency ledger is:

| Result | Depends on | Status |
|---|---|---|
| Original `H`, cuts, supports, color counts | Literal `[O:complex]` data and independent finite checks | Exact finite certificate |
| Elementary symmetric/symplectic counts | Basis counts, Schur complements, finite products | Proved in §2 |
| Individual ordered-orbit lower bound `2^{-D-15}q^{-C}` | Exact block splitting, residual form orbits, avoidance | Proved in §2.3 |
| Relaxed-domain planted bound `A_D q^g` | Orbit lower bound; exact quotient and correlated difference-form laws | Proved in §3 |
| Universal anchored energy | Exact source gain expansion and four-region inequalities | Proved in §4; identities checked |
| `M<=608` | Positive-definite energy and integer inverse certificate | Exact certificate (4.16)–(4.17) |
| Relaxed-domain residual classification at `D>=7296` | `M<=608`, integer equality cases, connectedness, excess anchor | Proved in §5; no retained gate |
| Transverse error `2^170 D q^-1/2` | Local projection count, restriction second moment, joint Fourier bound | Proved in §6 |
| Direct/nondirect residual constants | All-family basis count; strict global span defect | Proved in §7, independent of `189` |
| Rank-layer error `C_D q^-1/6` | All preceding geometric and energy components | Proved, uniformly in activity/signs |
| Identity coefficient `-2^-132` | Actual activation law, zero first moments, literal support forcing | Proved in §8; finite moment checks |
| All-map score gap and `t_0<=-2^-Z` | Four refinement rounds, integer dominance, actual whole-law thinning | Proved in §9; exact scores checked |
| Reverse orientation and explicit `q>Q_0` | Uniform rank error, nonnegative parity models, inactive-type dilution | Proved in §10 |
| Bounded rational kernel and gap `Delta_q` | Crossed product and specified scaling | Proved in §11 |
| Finite host and all-map count | Finite sampling average, Jensen, explicit collisions, (12.4) | Proved in §12 |
| Fixed `N=2^B` and deterministic termination | Elementary prime lemma and exact exponent arithmetic | Proved in §13 |

**Retained mathematical assumptions:** ordinary finite-dimensional linear algebra, elementary arithmetic and probability, and the definitions explicitly given above. The needed counting identities, Gaussian-sum bound, prime-search bound, and finite-host argument have been proved here. No separate unresolved research assumption is retained. The literal finite certificates must of course pass their documented arithmetic checks; they did in the included replay.

**Finite evidence:** the finite template/support/moment calculations, sparse-polynomial identities, matrix product and margins, score values, and parameter arithmetic. They are not substitutes for the universal domain arguments. The field and host were not sampled or exhaustively evaluated.

**Not established:** a smaller counterexample pattern; any claim for candidate 49243 or other speculative templates; an optimal dimension or field bound; a compact adjacency list; a practical generator; a Lean-checked version of this new quantitative theorem; an unconditional certification of every assertion in the refinement repository. The narrower statement (T) for the original pattern is the completed result.

## 15. Immutable sources, replay, and exact files missing from the upload

All original-paper paths below are under
`preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/`
at `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

| Source label | File | Git blob SHA-1 | Main use |
|---|---|---|---|
| `[O:complex]` | `complex.tex` | `178b0e9da21867a727ea847dae8e537b9d719a70` | Literal faces, bits, exposure orders |
| `[O:kernel]` | `kernel.tex` | `bbe11be8fffe968012060ec43e6aff597e922831` | Activation law, expansion, pinning, reversal, crossed product |
| `[O:transverse]` | `transverse.tex` | `d4991976e630f117c8d85a7e22deb60643a2450d` | Half-rank centers and joint signs |
| `[O:orbits]` | `orbits.tex` | `7da7ee247b4be60c3baf545a2e0f78309a667ee0` | Ordered orbit rather than profile mass |
| `[O:planted]` | `planted.tex` | `e1a4636e66361dae0f5918e1245950060535a83c` | Exact gains and correlated lift differences |
| `[O:tail]` | `tail.tex` | `dc11e07a592e70d3a13e3a005c72378c88edc351` | Global profile cost and residual organization |

Additional files at the same OpenAI pin are `lean/docs/161.md` (blob `b395e0eaa2462cf72aeea576d6c614cd544da2ec`), `lean/ComparatorChallenges/SidorenkoCounterexample.lean` (blob `3f4fa1074f812e2e823350ea50ff1a786e4a1927`), and its adjacent JSON (blob `3fdb7a849e7b1df1fc07013c901e1052b35170f8`). These identify statement fidelity and the distinct solution-module mapping; they do not supply an assumed proof.

The refinement file is `rohanarun/sidorenko-template-refinements@d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d/proof.tex`, blob `66fc5eb655e6471df0c266c986c0ab47d943fe0f`. The fixed-pattern step examined in §7.5 is in its residual-189 proof.

**All ten files just enumerated are absent from the uploaded archive.** Their relevant source text was recovered read-only at these pins; absence from the upload was not treated as a mathematical defect. The package includes source-pin metadata and the independently reconstructed literal certificate, not a claim that all fetched upstream file bytes were locally materialized. The optional source-comparison flags require local copies with the stated exact blob hashes. No such optional source-byte comparison is reported as having run.

Replay the finite certificate with Python's standard library:

```sh
python check_certificate.py
python generator.py --self-test
```

Optionally audit the original upload and independently supplied exact upstream source bytes:

```sh
python check_certificate.py --archive '/path/public-research-sources-20261011(3).zip'
python check_certificate.py --complex-source /path/complex.tex \
  --comparator-source /path/SidorenkoCounterexample.lean
```

`certificate.json` contains the full 33-by-33 integer matrix, all shifted scores and thinnings, and the exact parameter arithmetic. `replay.json` reports the checks actually run. `generator.py` defaults to symbolic output; it does not attempt to allocate `N`. Its small tests explicitly include collapsed homomorphisms. `source-pins.json`, `dependency-ledger.json`, and `SHA256SUMS` record provenance and package integrity. No installation, source-program execution, external write, or publication was performed.
