Source: https://chatgpt.com/c/6aca7925-1238-83ec-accb-04bd9d93b1d0

# The smallest order is seven

**There is a simple triangulated sphere on seven vertices satisfying both A and B. No sphere on five or six vertices satisfies B.** Its vertex–face incidence graph has **17 vertices and 30 edges**, and its complete stable-color-preserving endomorphism set consists of exactly two automorphisms.

I also completed the classification of the entire prescribed universe:

\[
\boxed{
9{,}149\text{ sphere triangulations},\qquad
44\text{ satisfying A},\qquad
8{,}119\text{ satisfying B},\qquad
15\text{ satisfying both}.
}
\]

For the seven-vertex sphere, the original activation/support law and explicit rational, common per-part priors give a **strictly negative finite coefficient**. The analytic rank-layer limit for this changed template remains a named hypothesis, \(RL(T_7)\). **A Sidorenko counterexample for its incidence graph is not proved here.**

## Deliverables

- orbit_pinnable_templates_report.pdf[orbit_pinnable_templates_report.pdf](sandbox:/workspace/scratch/ef4fe9cd0244/orbit_pinnable_templates_report.pdf) — 13 pages containing the construction, proofs, complete census, reflection argument, and dependency ledger.
- orbit_pinnable_classification.zip[orbit_pinnable_classification.zip](sandbox:/workspace/scratch/ef4fe9cd0244/orbit_pinnable_classification.zip) — all 9,149 canonical face complexes; an exact A certificate and B certificate for every class; coverage evidence; independently written verifiers; original checker sources; source and byte manifests.
- smallest_template_certificate.json[smallest_template_certificate.json](sandbox:/workspace/scratch/ef4fe9cd0244/smallest_template_certificate.json) — the standalone seven-vertex artifact, including literal incidence data, all stable map branches, cycles, exposure orders, supports, scores, and symbolic rational priors.

The following separates hand proofs, exact finite certification, source claims, and the retained analytic hypothesis.

---

## 1. What the existing enumeration actually covers

Reading the pinned generator as literal source establishes that it invokes `plantri`, filters out graphs of maximum degree greater than six, and then retains **only graphs whose stabilized incidence refinement is discrete**. That last condition is stronger than B. I did not execute this downloaded generator. See the pinned [enumeration source](https://github.com/rohanarun/sidorenko-template-refinements/blob/d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d/enumerate_triangulations.py) and [refinements proof](https://github.com/rohanarun/sidorenko-template-refinements/blob/d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d/proof.tex).

The source’s order-13 chain is therefore:

\[
49{,}566\text{ total spheres}
\longrightarrow
115\text{ of maximum degree }\le6
\longrightarrow
49\text{ with discrete refinement}
\longrightarrow
47\text{ obstructed}+2\text{ feasible}.
\]

These are **source-reported counts**. In particular, the [order-13 receipt](https://github.com/rohanarun/sidorenko-template-refinements/blob/d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d/experiments/order-13-classification-independent.json) concerns those 49 discrete candidates; its filename does not establish classification under B. I did not generate or search order 13.

Through order 12, the degree-eligible universe has 184 graphs. Only 40 have discrete incidence refinement, leaving **144 nondiscrete cases** relevant to the weaker criterion. The new computation classifies those cases and also records B for every higher-degree graph.

This is a distinction between mathematical targets, not a defect in the source. The refinements source describes itself as an independent AI-generated research draft; I preserve that attribution and make no formal-verification or historical-novelty claim.

Both linked private ChatGPT answers were inaccessible to the reader, which returned `DisabledError`. Neither optional named export was supplied as an accessible attachment. I used the user-provided predecessor statement only for scope; the public source-defined target was sufficient.

---

## 2. The literal smallest template

Let \(I=\{0,1,\ldots,6\}\), and number the ten faces as follows.

| Face | Vertices | Face | Vertices |
|---|---|---|---|
| \(F_0\) | \(012\) | \(F_5\) | \(235\) |
| \(F_1\) | \(013\) | \(F_6\) | \(245\) |
| \(F_2\) | \(023\) | \(F_7\) | \(346\) |
| \(F_3\) | \(124\) | \(F_8\) | \(356\) |
| \(F_4\) | \(134\) | \(F_9\) | \(456\) |

Here \(012\) denotes \(\{0,1,2\}\).

This is a sphere by an explicit construction: start with the boundary of the tetrahedron \(0123\), insert vertex \(4\) into face \(123\), then \(5\) into face \(234\), then \(6\) into face \(345\).

Its point graph is the third power of the path \(0,1,\ldots,6\):

\[
uv\in E \iff 0<|u-v|\le3.
\]

It has 15 point edges and degree vector

\[
d=(3,4,5,6,5,4,3).
\]

The incidence graph is specified literally by

\[
V(H)=I\sqcup\{F_0,\ldots,F_9\},
\qquad
E(H)=\{\,iF_j:i\in F_j\,\}.
\]

Thus \(|V(H)|=17\) and \(|E(H)|=30\).

### Property A: three cycles suffice

Give each of these Hamiltonian cycles probability \(1/3\), including its closing edge:

\[
\begin{aligned}
C_1&=(0,1,2,4,5,6,3),\\
C_2&=(0,1,3,4,6,5,2),\\
C_3&=(0,1,4,6,5,3,2).
\end{aligned}
\]

The exact edge marginals are

\[
a_{01}=a_{56}=1,\qquad
a_{02}=a_{46}=\frac23,
\qquad
a_e=\frac13\quad\text{on the other eleven edges}.
\]

Consequently,

\[
\sum_{e\ni v}a_e=2,\qquad
\sum_e a_e=7,\qquad
\sum_e\left(a_e-\frac13\right)=2.
\]

This is an explicit rational certificate for A.

For the source’s admissible-cut interpretation, the two sides of each cycle have the following face exposure orders. After the first face, each listed face shares an already exposed edge and introduces exactly one new vertex.

| Cycle | First side: face indices | Second side: face indices |
|---|---|---|
| \(C_1\) | \(0,2,5,6,8\) | \(1,4,3,7,9\) |
| \(C_2\) | \(0,3,4,6,9\) | \(1,2,5,8,7\) |
| \(C_3\) | \(0,3,6,5,9\) | \(1,2,4,7,8\) |

These orders are checked directly in the positive artifact. The Hamiltonian-cut reduction is attributed to the pinned [refinements proof](https://github.com/rohanarun/sidorenko-template-refinements/blob/d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d/proof.tex).

### Stable refinement

Start color refinement with the point and face parts distinguished, and continue until the partition stops changing.

The stable point cells are

\[
P_3=\{0,6\},\quad
P_4=\{1,5\},\quad
P_5=\{2,4\},\quad
P_6=\{3\}.
\]

The stable face cells are

\[
\begin{aligned}
A&=\{F_0,F_9\},&
B&=\{F_1,F_8\},&
C&=\{F_2,F_7\},\\
D&=\{F_3,F_6\},&
E&=\{F_4,F_5\}.
\end{aligned}
\]

Their point-degree multisets are, respectively,

\[
345,\quad346,\quad356,\quad455,\quad456.
\]

The point-to-face neighbor counts are:

| Point cell | \(A\) | \(B\) | \(C\) | \(D\) | \(E\) |
|---|---:|---:|---:|---:|---:|
| \(P_3\) | 1 | 1 | 1 | 0 | 0 |
| \(P_4\) | 1 | 1 | 0 | 1 | 1 |
| \(P_5\) | 1 | 0 | 1 | 2 | 1 |
| \(P_6\) | 0 | 2 | 2 | 0 | 2 |

The face degree multisets give the reverse neighbor counts. Hence this partition is equitable. Degree refinement and the next face refinement produce it, and the subsequent stability check makes no further split.

### Theorem 1 — Complete endomorphism set

Every stable-color-preserving, part-preserving endomorphism of \(H\) is either the identity or

\[
r_I(i)=6-i,\qquad r_J(F_j)=F_{9-j}.
\]

In particular, **B holds although the stable partition is not discrete**.

**Proof, without assuming injectivity.** Let \(f\) be the point map of an allowed endomorphism. The singleton cell forces \(f(3)=3\). Compose with reversal if necessary, so \(f(0)=0\).

The image of \(F_0\) must lie in \(\{F_0,F_9\}\). Since it must contain \(f(0)=0\), it is \(F_0\). Stable point colors then force \(f(1)=1\) and \(f(2)=2\).

The image of \(F_4=134\) lies in \(\{F_4,F_5\}\). It contains the already fixed point \(1\), so it is \(F_4\), forcing \(f(4)=4\). Similarly, the image of \(F_5=235\) contains the fixed point \(2\), so it is \(F_5\), forcing \(f(5)=5\).

Finally, the image of \(F_7=346\) lies in \(\{F_2,F_7\}\). It contains the fixed point \(4\), so it is \(F_7\), forcing \(f(6)=6\).

Thus the point map is the identity. Each source face now has three distinct fixed image points, so its image face is uniquely itself. Undoing the possible reversal gives exactly the two maps stated. ∎

The standalone checker additionally examines **all 64 stable point maps**, including **56 noninjective maps**. Exactly two admit face-map extensions. This is supporting finite verification; the hand proof already establishes completeness.

---

## 3. Why seven is minimal

The lower bound does not depend on the large census.

A simple sphere triangulation has minimum degree three and \(3n-6\) edges.

At \(n=5\), a degree-three vertex exists. Deleting it and capping the resulting triangular hole gives the tetrahedron. All tetrahedral faces are equivalent, so there is one five-vertex sphere.

At \(n=6\), if there is no degree-five vertex, every degree is four, giving the octahedral graph. Otherwise a degree-five vertex is universal. Its link is a pentagon, and its complementary disk is a triangulated pentagon. The two diagonals must share an endpoint; all such pentagon fans are equivalent. Thus there are exactly two six-vertex spheres.

Representatives are:

\[
\begin{aligned}
T_5:\;&012,013,023,124,134,234,\\
T_6^{\mathrm{st}}:\;&012,013,023,124,134,235,245,345,\\
T_6^{\mathrm{oct}}:\;&012,013,025,035,124,134,245,345.
\end{aligned}
\]

In each row, number faces from zero in the displayed order. The following are noninjective incidence endomorphisms:

| Sphere | Point images, in order | Face images, in order |
|---|---|---|
| \(T_5\) | \((0,1,2,2,4)\) | \((0,0,2,3,3,5)\) |
| \(T_6^{\mathrm{st}}\) | \((0,1,2,2,4,5)\) | \((0,0,2,3,3,5,6,6)\) |
| \(T_6^{\mathrm{oct}}\) | \((0,1,2,2,4,5)\) | \((0,0,2,2,4,4,6,6)\) |

Literal containment verifies every incidence. Moreover, \((2\ 3)\) is a simplicial automorphism in each row, and every displayed vertex or face image is either itself or its image under this automorphism. Automorphisms preserve every refinement round, so these maps preserve the stable colors.

All three maps identify points \(2\) and \(3\). Therefore B fails at both smaller orders, proving

\[
\boxed{n_{\min}=7.}
\]

---

## 4. Original support law and an exact negative orbit coefficient

The activation law, four-corner supports, and refinement-score approach below are inherited from the pinned OpenAI manuscript, particularly [kernel.tex](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/kernel.tex). The following establishes their finite specialization to \(T_7\).

Let

\[
\mathcal C=\{(i,j):i\in F_j\},\qquad |\mathcal C|=30.
\]

For a point edge \(e=\{v,w\}\), whose two incident faces are \(F_j,F_l\), retain

\[
U_e=\{(v,j),(w,j),(v,l),(w,l)\}.
\]

At a corner \(\kappa\), let \(e,f\) be its two incident point edges and set

\[
M_\kappa=U_e\cup U_f,\qquad
\Gamma_\kappa=U_e\triangle U_f.
\]

Then

\[
U_e\cap U_f=\{\kappa\},\qquad |M_\kappa|=7,\qquad|\Gamma_\kappa|=6.
\]

Choose \(\sigma_{(0,0)}=-1\) and all other \(\sigma_\kappa=1\). For \(0<\theta<1\), use exactly the original two-branch law:

- With probability \(1/2\), take \(S=M_\kappa\), with conditional sign mass
  \[
  2^{-7}\left(1+\sigma_\kappa\theta
  \prod_{\gamma\in\Gamma_\kappa}\xi_\gamma\right).
  \]
- With probability \(1/2\), take \(S=\Gamma_\kappa\), with conditional sign mass
  \[
  2^{-6}\left(1-\sigma_\kappa\theta
  \prod_{\gamma\in\Gamma_\kappa}\xi_\gamma\right).
  \]

Nonincident type pairs receive the empty law.

Define

\[
\phi_\alpha(S,\xi)
=\mathbf1_{\{\alpha\subseteq S\}}\prod_{\gamma\in\alpha}\xi_\gamma,
\qquad
\mathsf A_{ab}(\alpha,\beta)
=\mathbb E[\phi_\alpha\phi_\beta].
\]

Each \(\mathsf A_{ab}\) is positive semidefinite, and every nonempty first moment vanishes.

For arbitrary part maps \(a:I\to I\), \(b:J\to J\), let

\[
C(a,b)=
\sum_{\alpha:E\to\mathcal P(\mathcal C)\setminus\{\varnothing\}}
\prod_{\kappa=(i,j)\in\mathcal C}
\mathsf A_{a(i)b(j)}
\bigl(\alpha_{e_\kappa},\alpha_{f_\kappa}\bigr).
\]

### Support lemma

For every point edge \(g\),

\[
\boxed{\quad
\bigcap_{\kappa\in U_g}M_\kappa=U_g.
\quad}
\]

A structural proof is available, so this does not rest only on a checked table. A coordinate \((v,j)\) belongs to exactly two four-corner sets: those of the two edges of \(F_j\) through \(v\). Its available corners are the three corners of \(F_j\), together with two corners in each of those edges’ opposite faces. These available corners can contain all four corners of another edge only when that edge itself contains the coordinate.

In a nonzero identity term, this intersection identity forces \(\alpha_g\subseteq U_g\). At a corner \(\kappa\), the two labels cannot be disjoint: otherwise their moment is a nonempty first moment and vanishes. Their maximal supports meet only at \(\kappa\), so both labels contain \(\kappa\). Applying this at all four corners forces

\[
\alpha_g=U_g\quad\text{for every }g.
\]

Thus there is exactly one nonzero identity labeling. Its local factor at \(\kappa\) is \(\sigma_\kappa\theta/2\), giving

\[
C(\mathrm{id})=-\left(\frac{\theta}{2}\right)^{30}.
\]

Transporting coordinates by reversal gives its unique nonzero labeling and the same sign:

\[
C(r)=-\left(\frac{\theta}{2}\right)^{30}.
\]

A map that is not an incidence endomorphism has coefficient zero, because some source corner receives an empty-law type pair. Therefore the complete allowed orbit contributes exactly

\[
\boxed{-2\left(\frac{\theta}{2}\right)^{30}.}
\]

---

## 5. Explicit rational common priors pin that orbit

This step includes maps with repeated images and establishes an actual finite negative coefficient.

For a target point \(a\), let \(d_a\) be its degree. For a target face \(b\), let \(m_b(d)\) count its points of degree \(d\in\{3,4,5,6\}\).

Use integer scores

\[
s_a=-37d_a^2,\qquad
s_b=-\|m_b\|^2,\qquad
s_{ab}=74d_a+2m_b(d_a).
\]

For a part map \(g=(a,b)\), put

\[
Q(g)=\sum_i s_{a(i)}
+\sum_j s_{b(j)}
+\sum_{(i,j)\in\mathcal C}s_{a(i)b(j)}.
\]

Let \(h_j\) be the degree histogram of the three image points of \(F_j\), **with multiplicity**. Direct expansion yields

\[
Q(g)=
37\left(
136-\sum_i(d_{a(i)}-d_i)^2
\right)
+
\sum_j\left(
2\langle m_{b(j)},h_j\rangle-\|m_{b(j)}\|^2
\right).
\]

The final sum is at most 70 for every map. If any point degree is not preserved, therefore,

\[
Q(g)\le37\cdot135+70=5065.
\]

If point degrees are preserved, \(h_j=m_j\), and the final sum becomes

\[
34-\sum_j\|m_{b(j)}-m_j\|^2.
\]

Consequently,

\[
\boxed{
Q_{\max}=5066,
}
\]

with equality exactly for stable-color-preserving part maps. Every other map has an integer score gap of at least one.

Now set, symbolically,

\[
\theta=\frac12,\qquad \beta=2^{564},
\]

and define

\[
\pi_a=\frac{\beta^{s_a}}{Z_I},
\qquad
\nu_b=\frac{\beta^{s_b}}{Z_J},
\qquad
\lambda_{ab}=\beta^{s_{ab}-446}.
\]

Here

\[
\begin{aligned}
Z_I&=2\beta^{-333}+2\beta^{-592}
       +2\beta^{-925}+\beta^{-1332},\\
Z_J&=8\beta^{-3}+2\beta^{-5}.
\end{aligned}
\]

The maximum pair score is 446, so \(0<\lambda_{ab}\le1\). Use the original law with probability \(\lambda_{ab}\), and the empty law otherwise.

**Every source point independently uses the same prior \(\pi\). Every source face independently uses the same prior \(\nu\).** There are no source-dependent priors or correlated type assignments.

The resulting all-nonempty coefficient is

\[
t_0=
Z_I^{-7}Z_J^{-10}\beta^{-13380}
\sum_g C(g)\beta^{Q(g)}.
\]

Normalize the sum by \(\beta^{5066}\), writing it as \(T\). The two nonzero maximum-score terms contribute

\[
-2\cdot4^{-30}=-2^{-59}.
\]

There are fewer than \(2^{54}\) part maps. Each \(C(g)\) has fewer than

\[
(2^{30}-1)^{15}<2^{450}
\]

terms, each of absolute value at most one. The absolute contribution from all lower-score maps is thus less than

\[
\frac{2^{54+450}}{2^{564}}=2^{-60}.
\]

Hence

\[
\boxed{
T<-2^{-60},
\qquad
t_0
<
-\frac{\beta^{-8314}}{2^{60}Z_I^7Z_J^{10}}
<0.
}
\]

This is a proved finite rational sign statement. No large powers, finite fields, or full kernels were instantiated.

---

## 6. Complete classification through order twelve

The exact results are:

| \(n\) | All spheres | \(\Delta\le6\) | Discrete among \(\Delta\le6\) | A | B | A and B |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 1 | 1 | 0 | 1 | 0 | 0 |
| 6 | 2 | 2 | 0 | 2 | 0 | 0 |
| 7 | 5 | 5 | 0 | 3 | 1 | 1 |
| 8 | 14 | 10 | 0 | 4 | 3 | 1 |
| 9 | 50 | 15 | 1 | 5 | 23 | 1 |
| 10 | 233 | 30 | 4 | 8 | 156 | 3 |
| 11 | 1,249 | 44 | 12 | 8 | 1,025 | 4 |
| 12 | 7,595 | 77 | 23 | 13 | 6,911 | 5 |
| **Total** | **9,149** | **184** | **40** | **44** | **8,119** | **15** |

The four joint classes have sizes

\[
15\text{ both},\quad
29\text{ A only},\quad
8104\text{ B only},\quad
1001\text{ neither}.
\]

All fifteen joint-positive classes are identified in the supplied canonical catalogs:

```text
7-0, 8-0, 9-0,
10-0, 10-225, 10-229,
11-0, 11-1228, 11-1239, 11-1247,
12-0, 12-7519, 12-7559, 12-7566, 12-7583
```

These are indices in this investigation’s sorted canonical catalogs, not source `plantri` indices.

### Why the enumeration is complete

The coverage proof uses the following reduction.

**Lemma.** Every simple triangulated sphere with more than four vertices has an edge whose contraction produces another simple triangulated sphere.

**Proof.** If there is no separating three-cycle, every edge has exactly its two facial opposite vertices as common neighbors.

Otherwise choose a separating triangle and a side disk \(D\) with the smallest positive number of interior vertices. Choose an interior vertex \(v\) and an incident edge \(vu\). Any triangle containing this edge lies in \(D\). If such a triangle separated the sphere, its side away from the exterior of \(D\) would contain a nonempty, strictly smaller set of interior vertices, contradicting minimality. Thus \(vu\) belongs to no separating triangle and has exactly the two facial opposite common neighbors.

The only further link obstruction would create all four faces of a closed tetrahedral component, forcing the entire connected sphere to be the tetrahedron, which was excluded. Contracting \(vu\) therefore replaces a disk by a disk and gives a smaller simple sphere. ∎

The inverse operation splits a vertex’s cyclic link at any two distinct link vertices, **including adjacent choices**. Every such split is generated.

Canonicalization uses all ordered root faces. For each, label its vertices \(0,1,2\), deterministically traverse adjacent oriented faces, label new vertices on discovery, sort the relabeled triples, and minimize the resulting code. Isomorphic face complexes have corresponding traversals; equal codes explicitly exhibit an isomorphism.

Starting from the tetrahedron, the independent checker:

1. performs every legal split;
2. verifies that each result occurs in the next catalog;
3. verifies that every catalog child is reached;
4. verifies distinctness of canonical classes.

The numbers of checked splits into orders \(5,\ldots,12\) are

\[
12,\ 24,\ 74,\ 262,\ 956,\ 4259,\ 23857,\ 150139,
\]

totalling **179,583**. The contraction lemma and checked closure prove coverage by induction. Membership is also established inductively by the disk-replacement construction.

### Exact A certificates

A positive certificate lists Hamiltonian cycles with rational probabilities.

A negative certificate supplies rational weights

\[
y_e\ge0,\qquad \sum_e y_e=1,
\qquad
\max_{C\text{ Hamiltonian}}\sum_{e\in C}y_e<\frac13.
\]

Any proposed distribution satisfying A would have expected \(y\)-weight at least \(1/3\), contradicting this bound.

For a vertex of degree \(d>6\), take \(y_e=1/d\) on its incident edges and zero elsewhere. Every Hamiltonian cycle then has weight \(2/d<1/3\). This supplies 8,965 immediate exact obstructions.

For the remaining 184 graphs, the package contains 44 rational primal certificates and 140 rational separating certificates. An independent integer Held–Karp dynamic program verifies the dual maxima after clearing denominators. A separate counting recurrence counts **63,399 Hamiltonian cycles** across this eligible class. Floating-point optimization was used only to propose some certificates; all acceptance was exact.

### Exact B certificates

Let \(c_I,c_J\) be the fully stabilized colors. For a stable-color-preserving point map \(f\), define

\[
D_j(f)=
\left\{
k:
c_J(F_k)=c_J(F_j),\
\{f(v):v\in F_j\}\subseteq F_k
\right\}.
\]

The braces denote a set: repeated images are explicitly permitted.

Such a point map extends to an incidence endomorphism **if and only if every \(D_j(f)\) is nonempty**. Face images can then be chosen independently from these domains. If \(f\) is injective, each domain has exactly one element and the resulting map is an automorphism.

Thus B reduces to the exact statement that every feasible stable point map is injective. B-false records contain a literal countermap. B-true records contain complete branching certificates, independently checked to include every allowed next image and to justify every pruned branch. The maximum search-tree size encountered was 49 nodes.

---

## 7. Reflection obstruction: a certified scope

A barycentric half/half/boundary certificate consists of a nonidentity involutive simplicial automorphism \(\tau\) and a partition

\[
V(\operatorname{sd}T)=H_+\sqcup B_\partial\sqcup H_-
\]

such that

\[
\tau(H_+)=H_-,
\qquad
\tau|_{B_\partial}=\mathrm{id},
\]

there is no barycentric edge between \(H_+\) and \(H_-\), and each half contains an original point.

Folding \(H_-\) onto \(H_+\) gives a noninjective, stable-color-preserving incidence endomorphism. This structurally excludes B for every sphere admitting this certificate.

For \(T_5\) above, take \(\tau=(2\ 3)\). Write \(v_i\) for original vertices and \(e_{ij}\) for edge barycenters. An explicit certificate is

\[
\begin{aligned}
H_+&=\{v_2,e_{02},e_{12},e_{24},F_0,F_3\},\\
H_-&=\{v_3,e_{03},e_{13},e_{34},F_1,F_4\},\\
B_\partial&=\{v_0,v_1,v_4,e_{01},e_{14},e_{23},F_2,F_5\}.
\end{aligned}
\]

Its boundary cycle is

\[
v_0,e_{01},v_1,e_{14},v_4,F_5,e_{23},F_2,v_0.
\]

### Reflection positivity with the required priors

For arbitrary common independent point and face priors \(\pi,\nu\), consider

\[
S=\sum_{a,b}
\left(\prod_i\pi_{a(i)}\right)
\left(\prod_j\nu_{b(j)}\right)C(a,b).
\]

Condition on boundary types and fixed-edge labels. At each fixed corner, factor the positive-semidefinite local matrix as a Gram matrix,

\[
\mathsf A_{ab}(\alpha,\beta)
=\sum_z L_{ab}(\alpha,z)L_{ab}(\beta,z).
\]

Reflection identifies the two half-partition functions. With a separate Gram index for each fixed corner, this gives

\[
S=
\sum_{\text{boundary data}}
(\text{nonnegative boundary prior weight})
\sum_{\mathbf z}
Z(\text{boundary data},\mathbf z)^2
\ge0.
\]

The common per-part priors and independence are essential to that equality.

For \(T_7\), Theorem 1 gives the entire automorphism group. Its only nonidentity involution is reversal. Its barycentric fixed set is exactly

\[
\{v_3,e_{24}\}.
\]

The artifact supplies a 29-edge spanning tree of the remaining 30 barycentric vertices. Their connectedness rules out a half/half partition with no cross-edge. Thus **the specified simplicial barycentric reflection obstruction is absent for \(T_7\)**.

This is not a converse characterization of all folds or all positivity obstructions. Indeed, the A-feasible catalog sphere `12-7564` has no reflection found by this complete simplicial-involution detector but has a certified noninjective stable endomorphism. Its failure of B is certified by that literal map, not inferred from a reflection test.

---

## 8. Exact analytic stopping boundary

The finite sign theorem above does not require a rank-layer asymptotic.

For a Sidorenko transfer, the remaining hypothesis is the following specialization of the source’s rank-layer statement. The source definitions are in [kernel.tex, `eq:kernel-rank-definition`, `eq:rank-layer`, and `eq:kernel-parity-model`](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/kernel.tex).

For fixed even \(D=2r\), let \(\mathcal S_D\) be the uniformly distributed symmetric \(D\times D\) matrices over \(\mathbb F_q\), and define

\[
K_\xi(Z)=
\frac{
\mathbf1_{\{\operatorname{rank}Z=r,\ \operatorname{sign}(Z)=\xi\}}
}{
\Pr_{Z'\in\mathcal S_D}
(\operatorname{rank}Z'=r,\ \operatorname{sign}(Z')=\xi)
}.
\]

Here the sign is the quadratic character of the determinant of the induced nondegenerate form on the quotient by the radical.

**Retained hypothesis \(RL(T_7)\).** There is \(D_0\) such that, for every fixed even \(D\ge D_0\), as \(q\to\infty\) through odd primes,

\[
\mathbb E
\prod_{(i,j)\in B}K_{\xi_{ij}}(X_i-Y_j)
=
\prod_{\substack{e\in E(T_7)\\U_e\subseteq B}}
\left(1+\prod_{\kappa\in U_e}\xi_\kappa\right)
+o(1),
\]

uniformly over all \(B\subseteq\mathcal C\) and sign choices, with all \(X_i,Y_j\) independent and uniform. The corresponding reversed-difference assertion is also required.

The dimension is fixed **before** the prime tends to infinity.

Conditional on \(RL(T_7)\), the source’s coordinate expansion and dilution give

\[
t_{I,J}(W_{q,\varepsilon})
=1+\varepsilon^7t_0+o(1),
\qquad
t_{I,J}(W_{q,\varepsilon}^{\top})
=1+\varepsilon^{10}t_1+o(1).
\]

Since \(t_0<0\), their limiting product is below one for sufficiently small fixed \(\varepsilon>0\), followed by sufficiently large \(q\). The source’s crossed-product symmetrization would then apply.

I inspected the additional pinned transverse, orbit, planted, and tail arguments as literal sources. The degree-three vertices of \(T_7\) do not invalidate any finite support, sign, or pinning proof above. But I did **not** complete a transfer of every analytic lemma to this new sphere. Accordingly, \(RL(T_7)\) is retained explicitly; no numerical dimension, prime, kernel, or finite Sidorenko host is certified.

---

## 9. Replay, resources, sources, and dependency ledger

After extracting the archive, run:

```bash
python3 verify_all.py
```

The default replay checks recursive coverage, every rational A certificate, every B certificate, the standalone positive artifact, reflection certificates, exact binding to the canonical catalog, and eight deliberately corrupted certificates that must be rejected.

The completed replay reported:

```text
coverage_replayed = true
all = 9149
A_true = 44
B_true = 8119
A_and_B = 15
minimal_order = 7
```

It completed in approximately 91 seconds in this environment. The coverage stage has an explicit 60-second cap per closure and a 250,000-expansion cap. The search was checkpointed through orders eight, ten, eleven, and twelve. Declared production limits included 1 GiB memory, a \(10^7\)-node B-search cap per graph, and a 120-second cap per order. No cases remain unresolved.

A smaller standalone replay is:

```bash
python3 verify_t7.py smallest_template_certificate.json --negative-controls
```

The standalone artifact’s SHA-256 is:

```text
8599d47e7168e03ca7d86fa5c2e046175503c041b9fd81eb7aaf55041431e330
```

The archive contains an additional byte manifest for its proof inputs. Verification requires only Python’s standard library. No downloaded repository program was executed, no software was installed, and no source repository was modified.

### Source attribution

The source manifest records exact immutable paths and observed integrity hashes for:

- The refinements [proof](https://github.com/rohanarun/sidorenko-template-refinements/blob/d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d/proof.tex), enumeration source, and receipts at commit `d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d`.
- The OpenAI manuscript’s [complex section](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/complex.tex), [kernel section](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/kernel.tex), and the further analytic sections inspected at commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

The activation/support law and score-pinning approach retain the OpenAI manuscript’s attribution. The admissible-cut reduction and earlier discrete census retain the refinements draft’s attribution. No historical novelty claim is made.

### Dependency ledger

| Conclusion | Dependencies | Status |
|---|---|---|
| \(T_7\) is a simple sphere | Literal tetrahedral face insertions | **Proved here** |
| A for \(T_7\) | Three literal cycles, weights \(1/3\) | **Exact rational certificate** |
| Stable cells and full B for \(T_7\) | Equitable partition and forcing proof allowing repeated images | **Proved here; independently replayed** |
| No smaller order in the universe | Elementary classification at orders five and six; literal noninjective maps | **Proved here** |
| Unique support term for each allowed automorphism | Original activation law and four-corner intersection identity | **Proved here** |
| Strictly negative finite \(t_0\) | Explicit score gap, common independent priors, symbolic remainder bound | **Proved here** |
| All 9,149 classes covered | Contractible-edge lemma, complete split closure, canonicalization | **Proof plus exact coverage certificate** |
| Full A/B census | Rational primal/dual certificates and complete endomorphism certificates | **Independently replayed finite result** |
| Specified reflection obstruction | Literal barycentric certificates and Gram-factor square argument | **Proved with common independent priors** |
| Rank-layer limit for \(T_7\) | Transfer of the source’s analytic arguments | **Retained hypothesis \(RL(T_7)\)** |
| Sidorenko violation for the 17-vertex incidence graph | \(RL(T_7)\) plus the proved finite sign and source transfer construction | **Conditional; not claimed proved** |

**The strongest completed result is the exact minimum \(n_{\min}=7\), a strictly negative finite orbit-pinned coefficient for that template, and a complete certified A/B classification through \(n=12\). The stopping boundary is the unproved analytic transfer \(RL(T_7)\).**