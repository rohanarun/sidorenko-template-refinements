# Quantitative transfer from identity pinning to automorphism-orbit pinning

## Result, attribution, and verification status

The proposed strengthening holds. The finite argument below exposes exactly the stable-color-preserving endomorphisms by integer vertex and pair scores. Under the stated endomorphism hypothesis these are precisely the part-preserving automorphisms. Their **entire** all-nonempty coefficients, not merely selected summands, are equal and negative. Explicit rational priors and thinning probabilities control every other type map and every nonempty coordinate labeling. Explicit rational dilution then controls the opposite orientation.

This note retains the analytic rank-layer theorem from §§3–8 of the recovered predecessor `template_transfer_proof.md` (L3), with its conservative dimension bound. Those sections prove the analytic limit without using color refinement. Color refinement first enters the finite pinning argument in §10.1. The recovered export is included as an attributed dependency, not presented as a new proof in this note. This is a conventional proof using that analytic result, not proof-assistant verification and not an independent re-audit of every analytic lemma in L3.

OpenAI's pinned manuscript supplies the rank layers, seven/six-coordinate activation law, support forcing, squared-histogram scores, thinning, dilution, crossed-product symmetrization, and host sampling. L3 supplies the parameterized analytic transfer. The problem statement attributes qualitative orbit pinning and coefficient reindexing to L4; these ingredients are rederived below, rather than assumed from an inaccessible manuscript. The quantitative integration and all-competitor bounds are the completed result here. No priority or novelty claim is made.

Both private conversation URLs returned login pages. A Library copy of `template_transfer_proof.md` was recovered and read in full. `orbit_pinning_certificates.zip` was not located. No fact about that archive or the predecessor's 28-vertex example is used.

## 1. The theorem

Let Γ be a finite simple simplicial triangulation of the sphere. Its point set is I and its triangular face set is J. Put

\[
 n=|I|\ge5,\quad f=|J|=2n-4,\quad m=|E(\Gamma)|=3n-6,
 \quad k=3f,\quad v=n+f.
\]

Let H be its point–face incidence graph, with corner set \(\mathcal K=E(H)\), of size k. Initialize color refinement with the two part colors, retaining the old color at each refinement step. Let \(\ell_R\) be a stable resulting coloring. Assume:

1. A rational probability distribution on Hamiltonian cycles of Γ has edge coverages \(a_e\ge1/3\) for every point edge e.
2. Every \(\ell_R\)-preserving endomorphism of H is an automorphism.

The second condition already implies part preservation because the stable coloring refines the part coloring. Write

\[
 G=\operatorname{Aut}_{I,J}(H),\qquad g=|G|.
\]

Since H is connected and n<f, every automorphism preserves its parts, so this is also the full automorphism group.

Let d be the diameter of the face dual graph, and define the analytic constants

\[
 M_{\rm an}=4104f(d+1)^2,\qquad
 C_{\rm an}=12M_{\rm an}^2+2M_{\rm an},\qquad
 B_{\rm an}=m^2+20m.
\]

**Theorem.** For every fixed even D satisfying

\[
 D\ge12,\qquad D>\max\{M_{\rm an}+2fC_{\rm an},\ B_{\rm an}\},       \tag{1}
\]

the retained L3 rank-layer limit, with the rational finite laws constructed below, yields a symmetric rational kernel U on a finite rational probability space such that

\[
 0\le U\le1,\qquad \mu=\mathbb EU>0,\qquad t(H,U)<\mu^k.           \tag{2}
\]

The score base and dilution are explicit in (17) and (22), and are fixed before q tends to infinity. The proof also supplies a finite simple host G_host with \(t(H,G_{\rm host})<p(G_{\rm host})^k\).

No algorithm for enumerating sphere templates, numerical prime, complete kernel table, or finite host adjacency matrix is part of this result.

## 2. Retained analytic input and its exact scope

The Hamiltonian-cycle assumption implies

\[
 \sum_{e\ni i}a_e=2,\qquad \deg_\Gamma(i)\le6,
 \qquad \sum_e(a_e-1/3)=2.                                  \tag{3}
\]

For a sphere triangulation, the degree of point i in H equals its degree in Γ, while every face vertex has degree three. Hence \(\Delta_H\le6\). H and the face dual are connected, and every vertex has positive degree.

Each Hamiltonian cycle cuts the sphere into two triangulated polygons, each admitting an exposure order with one fresh point per new triangle. This is the structural reduction in the pinned refinement, Lemma `hamilton-reduction`, and L3 §2.

Fix an odd prime q and write D=2r. On the uniform space \(\mathcal S_D\) of symmetric D-by-D matrices over \(\mathbb F_q\), set

\[
 K_\xi(Z)=\frac{1_{\{\operatorname{rank}Z=r,\ \operatorname{sign}Z=\xi\}}}
 {\Pr(\operatorname{rank}Z=r,\ \operatorname{sign}Z=\xi)},\qquad \xi\in\{\pm1\}.
\]

Both denominators are positive and rational, and \(K_\xi\ge0\), \(\mathbb EK_\xi=1\). For a point edge e={i,h} whose faces are j,l, define

\[
 U_e=\{(i,j),(h,j),(i,l),(h,l)\}\subseteq\mathcal K.
\]

L3 §§3–8, under (1), gives, uniformly in \(B\subseteq\mathcal K\) and incidence signs,

\[
 \mathbb E\prod_{(i,j)\in B}K_{\xi_{ij}}(X_i-Y_j)
 =\prod_{e:\,U_e\subseteq B}\left(1+\prod_{\kappa\in U_e}\xi_\kappa\right)
   +O_{\Gamma,D,\lambda}(q^{-1/(2Q_{\rm cov})}),                 \tag{4}
\]

where \(Q_{\rm cov}\) is a common denominator of the coverage numbers. All X_i,Y_j here are independent. The same statement holds for reversed differences. Indeed, with \(c_0=\chi((-1)^r)\), \(K_\xi(-Z)=K_{c_0\xi}(Z)\), and multiplication by c_0 at four corners leaves each parity product unchanged.

The exact dependency checks behind retaining (4) are as follows. Weighted polygon exposures give the profile cost

\[
 \mathcal C=\frac12\left[\sum_jC_j-\sum_e(1-a_e)b(h_e)\right],
 \qquad b(t)=t(t+1)/2.                                      \tag{5}
\]

L3 (6.3)–(6.5) obtains an exponent saving at least \(1/(2Q_{\rm cov})\) whenever the cost strictly exceeds the integral local gains. L3 (7.6)–(7.11) uses the total excess in (3) and the dual diameter to obtain M_an and C_an. The residual profiles have \(c_j=0\), \(h_e\in\{0,2\}\). The direct residual count saves at least one; the nondirect exponent is at most \(-D+B_{\rm an}\), by L3 (8.1) and the bound \(\sum_i\binom{d_i}{2}\le22|E'|\). The remaining transverse inputs use \(\Delta_\Gamma\le6\), D≥12, and local three-point geometry. None uses the coloring or endomorphism hypothesis.

The refinement's improved numerical remainder 189 is **not used**. It is a bound for one stratum of the original template, not a replacement for (1). Likewise, the source's conditional enumeration minimum under discrete refinement is not a premise here.

## 3. Integer scores expose exactly stable-color-preserving endomorphisms

The next lemma is valid for any finite bipartite graph F with vertex count v and maximum degree Δ. Choose R≥1 refinement rounds whose last partition is stable. R≤v suffices. For each t, let h_t(u) be the histogram of the round-(t−1) colors among neighbors of u. Define integer type scores

\[
 s^{(t)}_a=-\|h_t(a)\|_2^2,
\]

and, for **every** pair of opposite-part types, including nonedges,

\[
 p^{(t)}_{ab}=2h_t(a)(\ell_{t-1}(b))+2h_t(b)(\ell_{t-1}(a)).      \tag{6}
\]

Let F_t(z) be the resulting sum of vertex and source-edge scores for an arbitrary part-preserving map z. If z preserves round-(t−1) colors, regrouping the source-edge contributions by their source endpoints gives

\[
 F_t(z)=\sum_u\|h_t(u)\|_2^2-
         \sum_u\|h_t(z(u))-h_t(u)\|_2^2.                       \tag{7}
\]

This uses neither injectivity nor edge preservation. In particular, F_t(id)−F_t(z) is then a nonnegative integer, and is zero exactly when z also preserves the new colors.

For all part-preserving maps,

\[
 -v\Delta^2\le F_t(z)\le2v\Delta^2,\qquad
 0\le F_t(\mathrm{id})\le v\Delta^2.
\]

Thus \(M=2v\Delta^2\) bounds \(|F_t(z)-F_t(\mathrm{id})|\). Put L=M+2 and

\[
 Q_0(z)=\sum_{t=1}^R L^{R-t}F_t(z).
\]

If z first fails color preservation at round t, its loss in that round is at least \(L^{R-t}\), while its possible later gain is at most

\[
 M\sum_{j=0}^{R-t-1}L^j<L^{R-t}.
\]

Hence Q_0 has exactly the stable-color-preserving maps as its maximizers, with integer gap at least one to every other map.

Now let \(b_{\rm bad}(z)\) be the number of source edges whose image is a nonedge. Set

\[
 \mathcal Q(z)=Q_0(z)-b_{\rm bad}(z).                          \tag{8}
\]

Equivalently take

\[
 s_a=\sum_{t=1}^R L^{R-t}s^{(t)}_a,\qquad
 s_{ab}=\sum_{t=1}^R L^{R-t}p^{(t)}_{ab}-1_{\{ab\notin E(F)\}}.
                                                                    \tag{9}
\]

The penalty is always nonpositive and is zero at the identity. It cannot spoil the existing gap. Among the stable-color-preserving maps it is zero exactly at endomorphisms. Therefore

\[
 \operatorname*{argmax}_{z\text{ part-preserving}}\mathcal Q(z)
 =\operatorname{End}_{\ell_R}(F),\qquad
 \mathcal Q(\mathrm{id})-\mathcal Q(z)\ge1
 \quad\text{outside that set}.                              \tag{10}
\]

This proves the lemma with explicit integer scores and nonincidence penalties, over maps with arbitrary repetitions. For H under the theorem's hypothesis, the right side is G. Every part-preserving automorphism preserves every refinement round, so no automorphism has been omitted.

For reference, the score sizes also have the explicit bounds

\[
 -\Delta^2\sum_{t=1}^R L^{R-t}\le s_a\le0,
 \qquad -1\le s_{ab}\le4\Delta\sum_{t=1}^R L^{R-t}.
\]

## 4. The activation law and the whole orbit coefficient

Use the corner set \(\mathcal K\) as a coordinate set. At an incident type pair κ, let e,f be the two point edges of its face through its point, and set

\[
 M_\kappa=U_e\cup U_f,\qquad
 D_\kappa=U_e\mathbin\triangle U_f.
\]

Distinct triangular faces share at most one edge. Consequently

\[
 U_e\cap U_f=\{\kappa\},\quad |M_\kappa|=7,
 \quad D_\kappa=M_\kappa\setminus\{\kappa\},\quad |D_\kappa|=6.
\]

Choose exactly one negative sign σ_κ and all other signs positive. Fix θ=1/2. At type pair κ use the pinned source's law:

* With probability 1/2 take S=M_κ and give each sign vector probability \(2^{-7}(1+\sigma_\kappa\theta\prod_{\gamma\in D_\kappa}\xi_\gamma)\).
* With probability 1/2 take S=D_κ and give each sign vector probability \(2^{-6}(1-\sigma_\kappa\theta\prod_{\gamma\in D_\kappa}\xi_\gamma)\).

At a nonincident type pair use S=∅. These are rational probability laws with nonnegative masses. Put

\[
 \phi_\alpha=1_{\{\alpha\subseteq S\}}\prod_{\gamma\in\alpha}\xi_\gamma,
 \quad A_{ab}(\alpha,\beta)=\mathbb E_{ab}\phi_\alpha\phi_\beta.
\]

All nonempty first moments vanish: the only potentially nonzero one is indexed by D_κ and its two branch biases cancel. Hence

\[
 A_{ab}(\alpha,\beta)=0
 \quad\text{when }\alpha\cap\beta=\varnothing,\quad
                 \alpha\cup\beta\ne\varnothing.               \tag{11}
\]

For completeness, with Q=α∪β and T=α△β, the entire base moment is

\[
 A_\kappa(\alpha,\beta)
 =\tfrac12 1_{Q\subseteq M_\kappa}
       (1_{T=\varnothing}+\sigma_\kappa\theta1_{T=D_\kappa})
 +\tfrac12 1_{Q\subseteq D_\kappa}
       (1_{T=\varnothing}-\sigma_\kappa\theta1_{T=D_\kappa}).      \tag{12}
\]

In particular \(|A_{ab}|\le1\), and \(A_\kappa(U_e,U_f)=\sigma_\kappa/4\).

For every type map z=(a:I→I,b:J→J), define its **full** nonempty coefficient

\[
 C(z)=\sum_{\substack{\varnothing\ne\alpha_e\subseteq\mathcal K\\e\in E(\Gamma)}}
 \prod_{\kappa=(i,j)\in\mathcal K}
 A_{a(i)b(j)}(\alpha_{e(\kappa)},\alpha_{f(\kappa)}).             \tag{13}
\]

### Support forcing at the identity

The support identity is

\[
 \bigcap_{\kappa\in U_e}M_\kappa=U_e.                          \tag{14}
\]

To verify it, availability is symmetric: γ∈M_κ iff γ and κ lie in a common U_h. For γ=(i,j), write j={i,h,z}; let l,t be the opposite faces on {i,h} and {i,z}. Its available corners are all three corners of j, the two {i,h}-endpoint corners of l, and the two {i,z}-endpoint corners of t. For γ to be available at all four corners of an edge e, its two faces must be among j,l,t. The pairs j,l and j,t force the corresponding incident edge, so γ∈U_e. The pair l,t cannot work: both endpoints would have to lie in {i,h}∩{i,z}={i}. The reverse inclusion is immediate.

In a nonzero identity summand, (14) forces α_e⊆U_e. At a corner κ the two nonempty labels must intersect by (11), and their available U-sets meet only at κ. Each must therefore contain κ. Applying this at all four corners of every e forces α_e=U_e. This is the unique nonzero summand. Thus

\[
 C(\mathrm{id})=\prod_{\kappa\in\mathcal K}(\sigma_\kappa/4)
 =-4^{-k}=-c,\qquad c:=4^{-k}.                              \tag{15}
\]

This proves a statement about the full coefficient: no extra positive diagonal-label alternatives survive.

### Source reindexing, not invariance of the negative corner

Every h∈G induces permutations of the points, faces, point edges, and corners of Γ. For example, point edges are exactly pairs lying in some face, so the induced action follows from the incidence automorphism.

In (13) for z=h, replace the source corner κ by κ'=hκ and define β_{h(e)}=α_e. This is a bijection of all nonempty edge-label tuples. It gives exactly the identity-type sum, with the target coordinate subsets themselves **not relabeled**. Therefore

\[
 C(h)=C(\mathrm{id})=-c\quad(h\in G).                          \tag{16}
\]

Its unique surviving labeling is α_e=U_{h(e)}. Its local factors are σ_{hκ}/4, and κ↦hκ is a bijection, so the distinguished negative corner occurs exactly once. No invariance of σ under h is asserted or needed.

There are g distinct maximizing type assignments, one for every group element. Their leading coefficient is −gc. This is not a quotient by the stabilizer of the distinguished corner. Possible equalities among some resulting label tuples would not identify distinct type assignments in the density expansion.

We do not use the stronger L4 assertion that nonautomorphism assignments have no negative summands. Absolute bounds suffice below, independently of every such sign.

## 5. Explicit rational pinning and all competitors

There are

\[
 \mathsf N=n^n f^f
\]

part-preserving type maps. Each has

\[
 \mathsf B=(2^k-1)^m
\]

possible all-nonempty label tuples. Every summand in (13) has absolute value at most one, so \(|C(z)|\le\mathsf B\), for every map, including maps with repetitions and maps taking incidences to nonincidences.

Take the single explicit integer base

\[
 \boxed{T=1+2\mathsf N\mathsf B\,4^k.}                        \tag{17}
\]

Let s_a,s_b,s_ab be the scores in (9), let s_max=max s_ab, and set

\[
 Z_I=\sum_{a\in I}T^{s_a},\quad Z_J=\sum_{b\in J}T^{s_b},
 \quad \pi_a=T^{s_a}/Z_I,\quad\nu_b=T^{s_b}/Z_J,
 \quad\lambda_{ab}=T^{s_{ab}-s_{\max}}.                       \tag{18}
\]

Negative integer exponents cause no problem: all these numbers are rational. The π and ν are common per-part probability laws; they do not depend on the source vertex. Also 0<λ_ab≤1. Thin the entire base activation law by using it with probability λ_ab and using S=∅ otherwise. Then

\[
 A^\lambda_{ab}(\alpha,\beta)
 =\lambda_{ab}A_{ab}(\alpha,\beta)
 +(1-\lambda_{ab})1_{\{\alpha=\beta=\varnothing\}}.             \tag{19}
\]

Each full nonempty summand receives one thinning factor per source incidence, independent of the sizes of its labels. Let Q*=Q(id) and

\[
 w=\frac{T^{Q_*-ks_{\max}}}{Z_I^nZ_J^f}>0.
\]

The aggregate nonempty coefficient is exactly

\[
 t_0=w\left[-gc+\sum_{z\notin G}C(z)T^{\mathcal Q(z)-Q_*}\right]. \tag{20}
\]

Using the integer score gap,

\[
 \left|\sum_{z\notin G}C(z)T^{\mathcal Q(z)-Q_*}\right|
 \le\frac{(\mathsf N-g)\mathsf B}{T}<\frac c2.
\]

Thus \(t_0<-(g-1/2)cw\le-cw/2\). Define the explicit rational guaranteed deficit

\[
 \boxed{\eta=cw/2>0,\qquad t_0<-\eta.}                       \tag{21}
\]

The orbit multiplicity g is fully retained in (20); using the weaker bound η avoids having to enumerate G to choose the parameters.

## 6. Coordinate expansion and every independence condition

On \(\mathcal X=I\times\mathcal S_D^{\mathcal K}\) and \(\mathcal Y=J\times\mathcal S_D^{\mathcal K}\), use independent matrix coordinates and the type priors in (18). Define

\[
 W_q((a,x),(b,y))=\mathbb E_{S,\xi\mid a,b}
     \prod_{\gamma\in S}K_{\xi_\gamma}(x^\gamma-y^\gamma).
\]

For each fixed type pair its matrix mean is one, so \(\mathbb EW_q=1\) exactly.

In a density product, the activation draw is made independently at every **source incidence**. Repeated target types or repeated target type pairs do not identify source vertices, matrix draws, or activation draws. The type variables themselves are independent, with the same π for all source vertices on one part and the same ν on the other.

Applying (4) in each coordinate and expanding each edge parity factor selects α_e⊆K for every source point edge e. Averaging the two incident edge-label contributions at a source corner gives exactly its moment A^λ. A mixed empty/nonempty pair is zero by (11). Consequently a face containing one nonempty edge label has all three labels nonempty. Dual connectivity propagates this to all faces. The only surviving regimes are the all-empty labeling, contributing one, and (13). This proves

\[
 t_{I,J}(W_q)=1+t_0+o(1).
\]

The transpose uses independent type maps b:I→J and a:J→I and factors A^λ_{a(j)b(i)}. Call its aggregate nonempty coefficient t_1. Its sign is unrestricted. Since the type-map probabilities sum to one and the moments have absolute value at most one,

\[
 |t_0|\le\mathsf B,\qquad |t_1|\le\mathsf B.
\]

No reflection-positivity claim is used anywhere. In particular, neither correlated source assignments nor source-dependent priors have been substituted into an independence-based identity.

## 7. Explicit dilution and finite-prime passage

Choose, before q,

\[
 \boxed{\varepsilon=
 \frac1{\,2+\left\lceil4\mathsf B(1+\mathsf B)/\eta\right\rceil}.} \tag{22}
\]

Add one inactive point type *, with mass 1−ε, and give each old point type mass επ_a. Keep ν unchanged. Every type pair involving * uses S=∅.

Every vertex has positive degree. Therefore a full nonempty term cannot have any point-type draw equal to *. There are n such draws in the forward orientation and f in the transpose. Hence

\[
 t_{I,J}(W_{q,\varepsilon})=1+\varepsilon^n t_0+o(1),\qquad
 t_{I,J}(W_{q,\varepsilon}^{\mathsf T})=1+\varepsilon^f t_1+o(1). \tag{23}
\]

Because f−n=n−4≥1 and ε<1,

\[
 \begin{split}
 t_0+\varepsilon^{f-n}t_1+\varepsilon^f t_0t_1
 &\le-\eta+\varepsilon^{f-n}\mathsf B(1+\mathsf B)\\
 &<-3\eta/4.
 \end{split}
\]

The limiting product is therefore at most \(1-\eta\varepsilon^n/2\).

Here is also an explicit translation of the single-coordinate error into the full density error. Let e_q be the maximum absolute error in (4), including reversed differences. Its parity model lies in [0,2^m]. Once e_q≤1, a product of k coordinate expectations differs from its limiting product by at most

\[
 a_q=k(2^m+1)^{k-1}e_q.                                    \tag{24}
\]

This follows by telescoping; averaging over types, activations, and signs cannot increase a uniform bound. It holds for both orientations, without a factor for the number of configurations. Each limiting orientation density has absolute value at most 1+B. For a_q≤1 the product error is at most \((3+2\mathsf B)a_q\).

By (4), choose a sufficiently large odd prime q so that e_q≤1, a_q≤1, and

\[
 a_q<\frac{\eta\varepsilon^n}{4(3+2\mathsf B)}.
\]

Fix one such q. Then the resulting finite rational mean-one kernel W obeys

\[
 t_{I,J}(W)t_{I,J}(W^{\mathsf T})
 <1-\frac{\eta\varepsilon^n}{4}.                            \tag{25}
\]

The sequence of choices is Γ and its cycle distribution; D; the coordinates and θ; integer scores and T; π,ν,λ; ε; then q. No score or dilution parameter changes with q. The analytic error prefactor is not evaluated here, so (24) is a sufficient condition on q, not a reported numerical prime bound.

## 8. Rational symmetrization and finite hosts

On Ω=X×Y with product probability define

\[
 V((x,y),(x',y'))=W(x,y')W(x',y).
\]

This is symmetric, nonnegative, rational, and has mean one. In the H-density, the forward factors use \((x_i)_{i\in I},(y_j)_{j\in J}\), and the reverse factors use \((y_i)_{i\in I},(x_j)_{j\in J}\). These are disjoint families of independent variables. Thus

\[
 t(H,V)=t_{I,J}(W)t_{I,J}(W^{\mathsf T}).                     \tag{26}
\]

There is no need to compute the maximum entry of the full kernel. Put \(b(D)=D(D+1)/2\). Every signed rank layer contains at least one matrix, so its probability is at least \(q^{-b(D)}\) and \(K_\xi\le q^{b(D)}\). Every activation support has size at most seven. Therefore

\[
 W\le q^{7b(D)},\qquad V\le q^{14b(D)}.
\]

With \(L_q=q^{14b(D)}\), set U=V/L_q. All atom masses and entries are rational, and

\[
 0\le U\le1,\quad \mu=1/L_q,\quad
 \mu^k-t(H,U)>\frac{\eta\varepsilon^n}{4L_q^k}>0.             \tag{27}
\]

This proves the kernel assertion without a continuity-based rationalization step. A uniform finite probability space can also be obtained by duplicating atoms according to a common denominator of their masses.

For the finite-host assertion, let τ=t(H,U), Δ=μ^k−τ. Sample N host labels independently from Ω and, conditional on them, put independent Bernoulli U-edges on unordered pairs of distinct host vertices, with no loops. Then

\[
 \mathbb E p(G_N)=(1-1/N)\mu,
 \qquad |\mathbb E t(H,G_N)-\tau|\le\binom v2/N.              \tag{28}
\]

Indeed, each injective source map has independent labels and distinct host-edge trials, so its homomorphism probability is τ. The fraction of noninjective maps is at most binom(v,2)/N. Their actual indicators are in [0,1]; no unjustified independence is assigned to repeated host edges or colliding source vertices. The labels of different host vertices themselves may coincide, as required by kernel density sampling.

If \(N>[\binom v2+k\mu^k]/\Delta\), then Bernoulli's inequality and convexity give

\[
 \mathbb Et(H,G_N)<((1-1/N)\mu)^k
 =(\mathbb Ep(G_N))^k\le\mathbb E[p(G_N)^k].
\]

Some finite realization violates the Sidorenko inequality and has at least one edge. By (27), the entirely explicit sufficient symbolic choice is

\[
 N>\frac{4[\binom v2L_q^k+k]}{\eta\varepsilon^n}.             \tag{29}
\]

No finite host is instantiated in the computation.

## 9. Certificate format for the endomorphism hypothesis

A certificate includes the literal simple bipartite graph, its two part labels, the stable coloring, and a complete finite decision tree. A verifier recomputes refinement rather than trusting the supplied coloring.

At a split node, choose an unassigned source vertex u and supply **exactly one child for every target in its stable color class**. No injectivity restriction is imposed. A leaf either identifies a source edge whose already assigned image is a nonedge, or gives a complete map and proves it is bijective and edge-preserving. A valid noninjective terminal map is a counterexample, not a successful leaf.

The exhaustive children guarantee coverage of every stable-color-preserving map. A bijective endomorphism of a finite simple graph is an automorphism: the induced injection on edges has the same finite cardinality as the edge set, so its image is the entire edge set. Thus a verified tree proves exactly the required condition. Full valid leaves count the entire automorphism group. Duplicate full maps are rejected.

The included `stable-endo-tree-v1` format stores each split as `{"kind":"split","vertex":u,"children":[{"image":a,"tree":...},...]}`, conflict leaf as `{"kind":"nonedge","edge":[u,v]}`, and successful leaf as `{"kind":"automorphism","map":[...]}`. The verifier separately implements exhaustive domain checks and verifies all terminal maps. It does not assume that a repeated image can be pruned.

A shorter sufficient certificate is the following structural lemma.

**Lemma.** If F is connected and every vertex has at most one neighbor in each stable color class, every stable-color-preserving endomorphism is an automorphism.

**Proof.** Such an endomorphism is injective on each neighbor set because its members have different preserved colors. Stable-color preservation also preserves degree, so the induced map from N(u) into N(z(u)) is a bijection. The image of z is consequently closed under taking neighbors. A nonempty neighbor-closed subset of a connected graph is the entire vertex set. Thus z is surjective and hence bijective. It is an automorphism. ∎

The lemma and the decision-tree certificate are alternatives. The theorem does not require the stronger local-neighbor condition.

## 10. A strictness example, explicitly not a sphere template

Take the cycle on vertices 0,...,11 and add edges

\[
 (2,12),(4,13),(13,14),(8,15),(10,16),(16,17).
\]

Use the cycle's even/odd bipartition and the forced parts of the added paths. The part sizes are 8 and 10; there are 18 vertices and 18 edges. Refinement from these two part colors has successive cell counts

\[
 2,5,8,9,9.
\]

Its stable cells are

\[
 \{i,i+6\}\ (0\le i\le5),\qquad
 \{12,15\},\quad\{13,16\},\quad\{14,17\}.
\]

Every vertex has at most one neighbor in each stable cell. The lemma proves the endomorphism condition, while every cell has two vertices, so refinement is not discrete. The automorphisms are exactly identity and the half-turn swapping each displayed pair. A choice of the image of vertex 0 forces every other image by the unique neighbor of each stable color, so there are exactly two.

This graph has pendant paths and is **not** a triangular-sphere incidence graph. It establishes strictness of the finite pinning hypotheses, not a smaller Sidorenko counterexample. No sphere-template search is claimed.

## 11. Exact finite checks and limits

The independent standard-library checker performs the following completed finite checks:

* The 18-vertex example: a complete 71-node endomorphism decision tree is generated and checked. An independent brute-force pass through all \(2^{18}=262144\) stable-color-preserving maps finds exactly the same two endomorphisms, both automorphisms.
* Every part-preserving map for three small score test graphs is checked: 16 maps for P4, four for K1,2, and 729 for C6. The score maximizers equal the stable-color-preserving endomorphisms in each case. The failure controls retain noninjective maximizers rather than silently deleting them.
* The generic seven-coordinate activation law is checked by exact rational sign averaging for both bias signs: all 32768 ordered moment entries and 254 nonempty first moments agree with (12) and the zero-moment claim.
* Deleting a root branch of the endomorphism certificate is correctly rejected.

The limits were fixed at 35 vertices and 2^20 map/branch states per instance. They were not enlarged. No repository program, model program, field construction, prime search, kernel table, triangulation enumerator, package installer, or cloud service was run. The checker verifies these finite claims only; it does not verify the analytic theorem or substitute for the proof above.

Replay: `python check_orbit_transfer.py --out replay`.

Certificate-only verification: `python check_orbit_transfer.py --verify stable_endomorphism_certificate.json`.

## 12. Sources and dependency ledger

### Immutable public sources read

O is `openai/math` at commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, under `preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/`:

* `kernel.tex`: blob `bbe11be8fffe968012060ec43e6aff597e922831`. Exact dependencies: `eq:kernel-rank-definition`, `eq:rank-layer`, `eq:kernel-parity-model`, `eq:kernel-activation`, `eq:kernel-zero-moments`, `eq:kernel-coefficient`, `eq:kernel-base-moment`, `eq:kernel-support-intersection`, `eq:kernel-pinning-square`, `eq:kernel-thinning`, `eq:kernel-crossed-product`, and `lem:finite-host`. The original numerical k=66 is not silently retained in parameterized expressions.
* `tail.tex`: blob `dc11e07a592e70d3a13e3a005c72378c88edc351`. Exact dependencies and comparison points: `eq:global-cost`, `eq:tail-total-slack`, `eq:coercivity`, `eq:tail-leading-coefficient`, `eq:tail-integer-slack`, `lem:tail-span`, `lem:tail-residual-counts`, and `prop:singular-tail`. The tail uses exposure, local geometry, and dual connectivity, not discrete refinement.
* `complex.tex`: blob `178b0e9da21867a727ea847dae8e537b9d719a70`. The numerical certificate and `prop:complex` distinguish its exposure/coverage requirements from its separate discrete-refinement requirement. Its specific graph is not changed here.

R is `rohanarun/sidorenko-template-refinements` at commit `d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d`:

* `proof.tex`: blob `66fc5eb655e6471df0c266c986c0ab47d943fe0f`. `lem:hamilton-reduction` and the following coverage identities support the structural setup. The conditional minimum and `prop:residual-189` are inspected source claims, not premises of this integration theorem.

### Predecessor dependency

`dependencies/template_transfer_proof.md`, recovered Library version 1, SHA-256 `2d286841535e86965dd1af937a85c65ae11ed73281184636ccc5375b3526cba4`.

Its §1 (1.1), §§3–8, and especially (3.1), (6.3)–(6.5), (7.6)–(7.11), (8.1), establish the retained parameterized rank-layer theorem. Its §§9–11 supply the prior parameterized finite transfer and are superseded here only in the pinning and explicit domination step. The entire export is preserved with attribution, including its independent earlier claims; inclusion is not a new audit or endorsement of every computational statement elsewhere in that export.

The two private links specified in the task were attempted and returned login pages. The L4 archive was not located, so no inaccessible L4 proof is a dependency. Qualitative L4 ingredients named in the task were rederived in §§3–4.

### Logical ledger

| Obligation | Status and dependency |
|---|---|
| Sphere topology, rational cycle coverages, n≥5 | Retained theorem hypotheses; not inferred from the endomorphism condition. |
| Parameterized rank-layer limit at fixed D | Retained established L3 analytic result, §§3–8; dimension condition (1). |
| Exact global maximizing set over arbitrary type maps | Proved in (6)–(10), including nonincidences and repetitions. |
| Unique nonempty identity coefficient | Reproved from source activation support in (11)–(15). |
| Equal full coefficients on every automorphism | Proved by source reindexing in (16), without target-law invariance. |
| Complete orbit count in leading coefficient | Exactly −g c in (20); no corner-stabilizer quotient. |
| Every competitor and every nonempty labeling | Absolute bound B, map count N, score gap one, explicit T in (17)–(21). |
| Common independent per-part priors and source-incidence draws | Explicit construction in (18)–(19) and §6. |
| Opposite orientation and n<f dilution | Proved with unrestricted-sign t1 and explicit ε in (22)–(25). |
| Rationalization and symmetric [0,1] kernel | Rational from the outset; explicit scale in (26)–(27). |
| Ordinary finite-host homomorphisms, including collisions | Proved in (28)–(29). |
| Endomorphism-certificate soundness and strictness example | Proved in §§9–10; independent finite checks in §11. |
| New sphere with nondiscrete refinement satisfying all hypotheses | Not searched for or claimed. |
| Numerical q, full U, concrete host | Not instantiated; asymptotic prefactor not evaluated. |

**Strongest completed result:** the requested automorphism-orbit strengthening of the transfer theorem, with explicit finite pinning and dilution constants and a positive symbolic finite-kernel deficit. **Stopping boundary:** the analytic input is retained from the recovered L3 proof; no new sphere witness, evaluated prime threshold, full kernel, or host adjacency matrix is claimed.
