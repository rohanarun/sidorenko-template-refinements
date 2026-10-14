# A seven-point orbit-pinnable template: a conditional transfer theorem

This note isolates the finite implication for one literal template. Its main theorem assumes the precise rank-layer limit **RL(T7,D)** below. A separate proposed corollary discharges that premise by retaining the complete proof in the **unpublished campaign manuscript L3**, with its hypotheses extracted before the coloring step. That corollary is source-dependent conventional mathematics, not a finite density computation, proof-assistant certificate, or independently accepted human theorem.

The activation construction originates in the [pinned OpenAI manuscript](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/kernel.tex). The orbit-transfer argument and T7 specialization below are attributed to campaign Task4 and Task11. Their complete texts, the complete L3 manuscript, finite checker and evidence accompany this note under [experiments/t7-orbit](experiments/t7-orbit/README.md). Exact pins, source line ranges, retained lemmas and acceptance boundaries are in [DEPENDENCIES.txt](experiments/t7-orbit/DEPENDENCIES.txt). No global novelty or minimum-order claim is made.

## 1. Exact graph and density conventions

Let $I=\{0,\ldots,6\}$ and $J=\{0,\ldots,9\}$ be disjoint vertex sets. In the listed order let

```math
(F_0,\ldots,F_9)=(012,013,023,124,134,235,245,346,356,456).
```

Here $012$ denotes $\{0,1,2\}$, and similarly for the other triples. Define the bipartite simple graph $H$ by
$E(H)=\mathcal K=\{(i,j)\in I\times J:i\in F_j\}$.
Thus $v(H)=17$ and $e(H)=30$.

For any finite probability space $(\Omega,\rho)$ and symmetric kernel $U:\Omega^2\to[0,1]$, put

```math
\mu=\mathbb E_{Z,Z'\sim\rho}U(Z,Z'),\qquad
t(H,U)=\mathbb E\prod_{\{u,v\}\in E(H)}U(Z_u,Z_v),
```

with all displayed draws independent. Source vertices may receive the same atom. A finite rational kernel means that every atom mass and every entry of $U$ is rational. For a finite simple graph $G$ on $N$ vertices, use ordinary, not injective, homomorphism density

```math
t(H,G)=\frac{\operatorname{hom}(H,G)}{N^{17}},\qquad
p(G)=\frac{2|E(G)|}{N^2}.
```

Let $\Gamma$ be the point graph whose edges are the pairs in the faces. Equivalently its fifteen edges are $\{i,h\}$ with $0<|i-h|\le3$. Each edge $e=\{i,h\}$ is in exactly two faces $F_j,F_l$; set
$U_e=\{(i,j),(h,j),(i,l),(h,l)\}\subset\mathcal K$.

## 2. The analytic premise and the two theorem statuses

Fix an even integer $D\ge12$, put $r=D/2$, and let $q$ tend through odd primes, with $D$ fixed. Let $\mathcal S_D$ be the uniform space of symmetric $D$ by $D$ matrices over $\mathbb F_q$. For a rank-$r$ matrix, its sign is the quadratic character of the determinant of the nondegenerate bilinear form on its quotient by the radical. Changing a quotient basis multiplies that determinant by a square.

For $\xi\in\{\pm1\}$ define the positive rational number
$\pi_\xi(q)=\Pr_{Z\in\mathcal S_D}(\operatorname{rank}Z=r,\operatorname{sign}Z=\xi)$ and

```math
K_\xi(Z)=\frac{\mathbf1_{\{\operatorname{rank}Z=r,\ \operatorname{sign}Z=\xi\}}}
{\pi_\xi(q)}.
```

Both signs occur, for example using a diagonal rank-$r$ form with a suitable last nonzero diagonal entry. In particular $K_\xi\ge0$ and $\mathbb EK_\xi=1$.

**Premise RL(T7,D).** For every $A\subseteq\mathcal K$ and every sign assignment $\xi\in\{\pm1\}^{A}$, independently uniform $X_i,Y_j\in\mathcal S_D$ satisfy

```math
\mathbb E\prod_{(i,j)\in A}K_{\xi_{ij}}(X_i-Y_j)
=
\prod_{e:\,U_e\subseteq A}
\left(1+\prod_{\kappa\in U_e}\xi_\kappa\right)+o(1).
\tag{RL}
```

The error tends to zero uniformly over these finitely many activity sets and sign assignments; the same assertion holds for $Y_j-X_i$. No quantitative rate is needed for the main implication. Reversal also follows from the forward assertion: $K_\xi(-Z)=K_{c_0\xi}(Z)$ where $c_0=\chi((-1)^r)$, and each parity factor uses four signs.

**Conditional theorem.** If RL(T7,D) holds for one fixed even $D\ge12$, there exist a finite rational probability space and a symmetric rational kernel $0\le U\le1$ with $\mu>0$ and $t(H,U)<\mu^{30}$. Consequently a finite simple graph $G$ with at least one edge satisfies $t(H,G)<p(G)^{30}$.

**Proposed source-dependent corollary.** Accepting the complete generic analytic argument in L3 §§2–8, as extracted in Task4 §2, discharges RL(T7,D) for every fixed even

```math
D\ge D_*:=103482288426242.
```

Thus that proof chain proposes that the above 17-vertex, 30-edge graph is non-Sidorenko without a remaining conjectural analytic hypothesis. “Unpublished” describes the source's status; it is not an extra mathematical assumption or a defect. The independent finite checks and the present specialization review do not by themselves prove the generic L3 analytic lemmas. This note keeps the conditional implication independently assessable.

## 3. Literal geometry and the analytic hypothesis extraction

The ten faces form a simple triangulated sphere: begin with the tetrahedral boundary on $0123$, insert $4$ in face $123$, then $5$ in face $234$, then $6$ in face $345$. Point degrees are $(3,4,5,6,5,4,3)$.

The following Hamiltonian cycles, each given weight $1/3$ and including its closing edge, cover every point edge with weight at least $1/3$:

| Cycle | Vertices in cyclic order | Face exposure on one side | Face exposure on the other side |
|---|---|---|---|
| $C_1$ | $0,1,2,4,5,6,3$ | $0,2,5,6,8$ | $1,4,3,7,9$ |
| $C_2$ | $0,1,3,4,6,5,2$ | $0,3,4,6,9$ | $1,2,5,8,7$ |
| $C_3$ | $0,1,4,6,5,3,2$ | $0,3,6,5,9$ | $1,2,4,7,8$ |

Each exposure starts with a triangle and each subsequent face adds one fresh point across an old edge. Each side uses all seven points and has boundary the stated cycle. The edge coverages are $a_{01}=a_{56}=1$, $a_{02}=a_{46}=2/3$, and $1/3$ on the other eleven edges. Thus $\sum_{e\ni i}a_e=2$, $\sum_e a_e=7$, $\sum_e(a_e-1/3)=2$, and the coverage denominator is $Q_{\rm cov}=3$. The face dual is connected with diameter $\ell=3$.

These are exactly the T7 geometric inputs to the retained L3 proof: sphere exposures, connected dual, maximum point degree at most six, coverage at least $1/3$, and total excess two. The local finite-field arguments use maximum degree six and $D\ge12$, with no minimum-degree-four assumption. Ordered-orbit counting, planted shared-form counting, the weighted cost, tail classification and final span estimates are retained analytic dependencies, not consequences of the finite template checker.

L3's combined theorem statement also assumes discrete color refinement. We do not invoke that combined theorem verbatim. The analytic conclusion is reached at L3 lines 834–842; the discrete-color hypothesis first enters its later pinning argument at lines 983–1006. Task4 §2 explicitly extracts the analytic argument before that step. For T7 its conservative constants are

```math
M_*=4104\cdot10(3+1)^2=656640,\quad
C_*=12M_*^2+2M_*=5174114388480,\quad
B_{\rm res}=15^2+20\cdot15=525.
```

The L3 condition is $D\ge12$ and $D>\max\{M_*+2fC_*,B_{\rm res}\}$, where $f=10$ and
$M_*+20C_*=103482288426240$. Hence $D_*$ above suffices, with L3 error $O_{T7,D,\lambda}(q^{-1/6})$. No improved 13-point residual constant or dimension is imported.

## 4. Stable maps, including repeated images

Start color refinement with the two part colors; each round retains the old color and the multiset of neighbor colors. The stable point cells are

```math
\{0,6\},\{1,5\},\{2,4\},\{3\},
```

and the stable face cells are

```math
\{F_0,F_9\},\{F_1,F_8\},\{F_2,F_7\},\{F_3,F_6\},\{F_4,F_5\}.
```

Point degrees distinguish the point cells. The face degree multisets are respectively $345,346,356,455,456$. Within each point cell, counts into these five face cells agree: they are respectively $(1,1,1,0,0)$, $(1,1,0,1,1)$, $(1,0,1,2,1)$, $(0,2,2,0,2)$. Thus the displayed partition is stable.

A stable-color-preserving incidence endomorphism may repeat images. Nevertheless it is either the identity or the reversal $r_I(i)=6-i$, $r_J(j)=9-j$. To prove this, the point $3$ is fixed. Compose with reversal if necessary to fix point $0$. The image of $F_0$ must then be $F_0$, since its cellmate $F_9$ does not contain $0$; its distinct degree slots force points $1,2$ to be fixed. Next $F_4=134$ must map to $F_4$ rather than $F_5$, since $1$ is fixed; this fixes $4$. Similarly $F_5=235$ fixes $5$, and $F_7=346$ fixes $6$. All points, and hence all faces, are fixed. This argument did not assume injectivity.

These two maps are automorphisms. Conversely every graph automorphism preserves these colors and cannot exchange the unequal parts of the connected bipartite graph. Hence
$\operatorname{End}_{\rm stable}(H)=\operatorname{Aut}(H)=\{1,r\}$.
The independent checker enumerates all $64$ stable point maps, including $56$ noninjective maps, and recovers exactly these two extensions.

## 5. An exact negative coefficient for the whole orbit

Use $\mathcal K$ also as the coordinate set. At a target corner $\kappa$, let $e,f$ be its two incident edges within its face, and define
$M_\kappa=U_e\cup U_f$, $D_\kappa=U_e\triangle U_f$.
The sets have sizes seven and six, with $U_e\cap U_f=\{\kappa\}$. Put $\theta=1/2$, set $\sigma_{(0,0)}=-1$, and set every other $\sigma_\kappa=1$.

At an incident target type pair $\kappa=(a,b)$, take $S=M_\kappa$ with probability $1/2$, assigning its signs conditional mass
$2^{-7}(1+\sigma_\kappa\theta\prod_{\gamma\in D_\kappa}\xi_\gamma)$.
With probability $1/2$ take $S=D_\kappa$, with sign mass
$2^{-6}(1-\sigma_\kappa\theta\prod_{\gamma\in D_\kappa}\xi_\gamma)$.
These are nonnegative normalized rational laws. At a nonincident type pair take $S=\varnothing$.

Write $\phi_\alpha=\mathbf1_{\{\alpha\subseteq S\}}\prod_{\gamma\in\alpha}\xi_\gamma$ and
$A_{ab}(\alpha,\beta)=\mathbb E(\phi_\alpha\phi_\beta)$.
Every nonempty first moment is zero, including the exceptional character $D_\kappa$, whose two branches cancel. If $Q=\alpha\cup\beta$ and $T=\alpha\triangle\beta$, the exact formula at a corner is

```math
A_\kappa(\alpha,\beta)=
\frac12\mathbf1_{Q\subseteq M_\kappa}
  (\mathbf1_{T=\varnothing}+\sigma_\kappa\theta\mathbf1_{T=D_\kappa})
+
\frac12\mathbf1_{Q\subseteq D_\kappa}
  (\mathbf1_{T=\varnothing}-\sigma_\kappa\theta\mathbf1_{T=D_\kappa}).
\tag{1}
```

In particular $|A|\le1$, disjoint labels with nonempty union have zero moment, and $A_\kappa(U_e,U_f)=\sigma_\kappa/4$.

For every pair of part maps $g=(a:I\to I,b:J\to J)$, allowing repetitions, define the full all-nonempty coefficient

```math
C(g)=\sum_{\alpha:E(\Gamma)\to\mathcal P(\mathcal K)\setminus\{\varnothing\}}
\prod_{\kappa=(i,j)\in\mathcal K}
 A_{a(i)b(j)}(\alpha_{e_\kappa},\alpha_{f_\kappa}).
\tag{2}
```

The support identity $\bigcap_{\kappa\in U_g}M_\kappa=U_g$ holds for every point edge $g$. Here is a structural proof. For a fixed coordinate $\gamma=(v,j)$, the corners $\kappa$ with $\gamma\in M_\kappa$ are all three corners of $F_j$, and the two endpoint corners in each of the opposite faces across the two edges of $F_j$ through $v$. The two opposite faces are distinct. If all four corners of some edge lie among these available corners, its two faces must be two of these three faces. The two opposite faces cannot supply both endpoints, since their available endpoint pairs meet only at $v$. If one face is $F_j$, the other forces precisely the corresponding edge through $v$. Thus that edge contains coordinate $\gamma$, proving the identity in both directions.

In a nonzero term of $C(1)$, this identity forces $\alpha_e\subseteq U_e$. At a corner the two nonempty labels must intersect, since otherwise their moment is zero; their supports intersect only in that corner. Applying this at every corner forces $\alpha_e=U_e$ for every edge. Consequently the entire sum, not just one selected term, is

```math
C(1)=\prod_{\kappa\in\mathcal K}\frac{\sigma_\kappa}{4}=-4^{-30}.
```

For any automorphism $h$, substitute $\beta_{h(e)}=\alpha_e$ in the full sum and reindex source corners by $h$. This gives $C(h)=C(1)$. It does not require the target law or its distinguished negative corner to be invariant under $h$. In particular $C(r)=-4^{-30}$. If $g$ is not an incidence endomorphism, one source corner gets an empty-law pair, so every term of (2) vanishes. There is no stabilizer division.

## 6. Common rational priors dominate all other type maps

Let $d_a$ be a target point's degree and $m_b$ the histogram of degrees in target face $b$, indexed by $3,4,5,6$. Define

```math
s_a=-37d_a^2,\quad s_b=-\|m_b\|^2,\quad
s_{ab}=74d_a+2m_b(d_a),\quad
Q(a,b)=\sum_i s_{a(i)}+\sum_j s_{b(j)}
       +\sum_{(i,j)\in\mathcal K}s_{a(i)b(j)}.
```

If $h_j$ is the degree histogram of the three image points of face $j$, counted with multiplicity, completing squares gives

```math
Q(a,b)=37\left(136-\sum_i(d_{a(i)}-d_i)^2\right)
+\sum_j(2\langle m_{b(j)},h_j\rangle-\|m_{b(j)}\|^2).
\tag{3}
```

Each last summand is at most seven. Indeed a face histogram has type $(1,1,1,0)$ or a permutation of $(2,1,0,0)$, so its largest pairing with a nonnegative histogram of total three is respectively three or six; subtract its squared norm, respectively three or five. If any point degree changes, $Q\le37\cdot135+70=5065$. If all are preserved, $h_j=m_j$ and

```math
Q=37\cdot136+34-\sum_j\|m_{b(j)}-m_j\|^2\le5066.
```

Equality holds exactly for stable-color-preserving part maps. Some such maps need not be endomorphisms, but their coefficient is zero by §5. The only nonzero maximum-score contributions are $1,r$.

Set

```math
\beta=2^{564},\quad
Z_I=2\beta^{-333}+2\beta^{-592}+2\beta^{-925}+\beta^{-1332},
\quad Z_J=8\beta^{-3}+2\beta^{-5},
```

and choose the common priors $\pi_a=\beta^{s_a}/Z_I$, $\nu_b=\beta^{s_b}/Z_J$ independently at every source vertex of the respective part. Since $\max s_{ab}=446$, let $\lambda_{ab}=\beta^{s_{ab}-446}\in(0,1]$. Thin the entire activation law: use it with probability $\lambda_{ab}$ and otherwise use the empty law. A nonempty coefficient gets one thinning factor per source incidence, not per activated coordinate.

The averaged coefficient is therefore

```math
t_0=Z_I^{-7}Z_J^{-10}\beta^{-13380}\sum_g C(g)\beta^{Q(g)}.
\tag{4}
```

There are $7^7\,10^{10}<2^{54}$ maps and at most
$\mathsf B=(2^{30}-1)^{15}<2^{450}$ labelings in (2); each summand has magnitude at most one. After division by $\beta^{5066}$ the two nonzero maximum-score terms sum to $-2\cdot4^{-30}=-2^{-59}$, and the absolute sum of all lower-score terms is less than $2^{54+450-564}=2^{-60}$. Thus

```math
t_0<-\eta,\qquad
\eta=\frac{\beta^{-8314}}{2^{60}Z_I^7Z_J^{10}}>0.
\tag{5}
```

No enumeration of the enormous sum in (2), and no evaluation of these large powers, is needed.

## 7. From RL to an oriented kernel deficit

On $X=I\times\mathcal S_D^{\mathcal K}$ and $Y=J\times\mathcal S_D^{\mathcal K}$, use the common type priors above and independent uniform matrix coordinates. Define

```math
W_q((a,x),(b,y))
=\mathbb E_{S,\xi\ {\rm from\ the\ thinned\ law\ at}\ (a,b)}
       \prod_{\gamma\in S}K_{\xi_\gamma}(x_\gamma-y_\gamma).
\tag{6}
```

It is nonnegative rational and has mean exactly one at each type pair. Each coordinate difference is uniform and different coordinates are independent. In a graph density all source-vertex matrix variables remain independent even when their types repeat. Likewise the activation draws at different source incidences are independent even when their type pairs repeat.

Apply RL separately to each of the thirty coordinates and expand its fifteen parity factors. A source point edge receives a subset $\alpha_e$ of coordinates. If one of the two labels at a corner is empty and the other nonempty, the corresponding first moment vanishes. Thus on each triangular face the three edge labels are all empty or all nonempty. The connected face dual propagates this choice throughout the sphere. The empty term is one; the full nonempty sum is (4). Hence

```math
t_{I,J}(W_q)=1+t_0+o(1).
```

Here $t_{I,J}$ uses independent draws from $X$ at $I$ and from $Y$ at $J$. For the transpose, draw from $Y$ at $I$ and $X$ at $J$, so the same argument uses reversed differences. Write its coefficient as $t_1$. Both $|t_0|$ and $|t_1|$ are at most $\mathsf B$; no sign is asserted for $t_1$.

Add an inactive point type $*$ of mass $1-\varepsilon$, give the old point types total mass $\varepsilon$ with conditional law $\pi$, keep $\nu$, and use the empty law on all pairs involving $*$. From this point onward, $X$ denotes the enlarged space $(\{*\}\cup I)\times\mathcal S_D^{\mathcal K}$ with this diluted type measure and independent uniform matrix coordinates. Fix the rational number

```math
\varepsilon=\frac1{2+\lceil4\mathsf B(1+\mathsf B)/\eta\rceil}.
\tag{7}
```

Every vertex has positive degree, so a full nonempty term requires all point-type draws to be active. There are seven such draws forward and ten backward:

```math
t_{I,J}(W_{q,\varepsilon})=1+\varepsilon^7t_0+o(1),\qquad
t_{I,J}(W_{q,\varepsilon}^{\mathsf T})=1+\varepsilon^{10}t_1+o(1).
```

The product's coefficient after subtracting one and dividing by $\varepsilon^7$ is
$t_0+\varepsilon^3t_1+\varepsilon^{10}t_0t_1
\le-\eta+\varepsilon^3\mathsf B(1+\mathsf B)<-3\eta/4$.
In particular its limiting product is at most $1-\eta\varepsilon^7/2$.

For explicit error bookkeeping, let $e_q$ be the maximum absolute error in RL, including reversal. Each parity model is in $[0,2^{15}]$. If $e_q\le1$, a telescoping product bound gives each full density error at most

```math
a_q=30(2^{15}+1)^{29}e_q.
```

Averaging over types, activations and signs introduces no additional factor. The limiting densities have magnitude at most $1+\mathsf B$; if $a_q\le1$ the product error is at most $(3+2\mathsf B)a_q$. RL permits an odd prime sufficiently large that these conditions hold and
$a_q<\eta\varepsilon^7/[4(3+2\mathsf B)]$. Fix one such prime. Then, writing $W=W_{q,\varepsilon}$,

```math
t_{I,J}(W)t_{I,J}(W^{\mathsf T})<1-\eta\varepsilon^7/4.
\tag{8}
```

The choices of $D$, coordinates, scores, priors, thinning and dilution were all fixed before $q$. The retained analytic prefactor is not evaluated here; this is a sufficient error condition, not a numerical prime threshold.

## 8. Symmetric rational kernel and ordinary simple host

On $\Omega=X\times Y$ with product probability, define

```math
V((x,y),(x',y'))=W(x,y')W(x',y).
```

This kernel is symmetric, nonnegative rational and has mean one. In its $H$ density, the forward factors use $(x_i)_{i\in I},(y_j)_{j\in J}$ and the backward factors use $(y_i)_{i\in I},(x_j)_{j\in J}$. These families are disjoint and independent. Therefore
$t(H,V)=t_{I,J}(W)t_{I,J}(W^{\mathsf T})$.

Put $b(D)=D(D+1)/2$. Every signed rank layer has at least one matrix, so $K_\xi\le q^{b(D)}$. Activation supports have size at most seven; hence $W\le q^{7b(D)}$ and $V\le L_q:=q^{14b(D)}$. The finite rational kernel $U=V/L_q$ satisfies

```math
0\le U\le1,\qquad \mu=1/L_q>0,\qquad
\Delta:=\mu^{30}-t(H,U)>\frac{\eta\varepsilon^7}{4L_q^{30}}>0.
\tag{9}
```

Atom duplication using a common denominator of their rational masses can make the finite probability space uniform, if desired.

To obtain a simple host, sample $N$ independent atom labels and then independent Bernoulli $U$ edges on unordered pairs of distinct host vertices; add no loops. For the resulting random graph $G_N$,

```math
\mathbb E p(G_N)=(1-1/N)\mu,\qquad
|\mathbb E t(H,G_N)-t(H,U)|\le\binom{17}{2}/N=136/N.
```

For injective source maps, distinct host vertices carry independent labels and distinct source edges use distinct edge trials. Noninjective maps occupy at most $136/N$ of all source maps and their actual indicators lie in $[0,1]$. This bound does not assign false independence to repeated host edges or colliding source vertices.

If $N>(136+30\mu^{30})/\Delta$, Bernoulli's inequality and Jensen's inequality give

```math
\mathbb E t(H,G_N)<((1-1/N)\mu)^{30}
=(\mathbb E p(G_N))^{30}\le\mathbb E[p(G_N)^{30}].
```

Some realization has $t(H,G_N)<p(G_N)^{30}$. It must have an edge, since an edgeless graph has both sides zero. By (9), the sufficient symbolic condition

```math
N>\frac{4(136L_q^{30}+30)}{\eta\varepsilon^7}
```

completes the conditional existence proof.

## 9. Evidence, scope and attribution

The separately authored standard-library checker verifies the literal sphere, cycle coverages, six exposures, stable partition, all 64 stable point maps, all fifteen support intersections, canonical orbit factors and the displayed small parameter arithmetic. It does not evaluate a rank-layer expectation, enumerate (2), prove generic L3 analytic lemmas, select a prime, tabulate a kernel or construct a host. The complete Task11 census is neither used nor certified here; its transferred archive was invalid as a ZIP. No minimality claim relies on it.

The finite transfer argument is a specialization of Task4 and the explicit T7 argument of Task11, with inherited construction credited to the pinned OpenAI manuscript. The analytic generalization is retained from the unpublished L3 manuscript and is supplied in full for review; it is not silently attributed to the public original. Earlier independent AI-agent static reviews and finite checks found no substantive gap in the scoped specialization. They are not evidence of formal verification or independent human referee acceptance.

Relative to the compared original 35-vertex, 66-edge discrete-refinement construction, the proposed contribution replaces discrete pinning by the exact stable endomorphism orbit and uses the literal 17-vertex, 30-edge template. Whether this is globally new is not established by this note. The conditional theorem and the source-dependent corollary should retain their separate labels in any submission.
