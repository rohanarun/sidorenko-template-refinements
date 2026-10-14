# A parameterized sphere-template transfer theorem

## Result and verification scope

The theorem below proves the proposed transfer, including the second certificate `candidate-13-49243.json`. It is a conventional mathematical proof, not a proof-assistant verification. Its finite-certificate calculations use independently written exact-arithmetic code. Neither repository's software was installed, imported, or executed. No repository changes or external submissions were made.

The analytic inputs used below are proved here, rather than assumed from the upstream rank-layer statement. The source draft supplied the construction and the local counting strategy; the weighted transfer, explicit dimension bookkeeping, use of total excess, relaxed finite gain maximization, and general pinning-to-host deductions are developed explicitly below. No optimality of the dimension bound is claimed. An individual prime, full kernel table, and finite host are not instantiated.

### Immutable sources inspected

**R:** `rohanarun/sidorenko-template-refinements` at commit `d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d`:

- `proof.tex`, including the sequential residual-count section;
- `experiments/order-13-classification-independent.json`;
- `experiments/order-13-cuts/candidate-13-49243.json`;
- `check_complex.py` (read, not executed).

**O:** `openai/math` at commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, under `preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/`:

- `complex.tex`;
- `kernel.tex`;
- `transverse.tex`;
- `orbits.tex`;
- `planted.tex`;
- `tail.tex`.

All required sources were available through the GitHub connector. No later revisions are used. The order-13 classification's enumeration completeness and its 47 obstruction certificates are not premises of the corollary and were not independently recomputed.

## 1. The theorem

Let Gamma be a simple sphere triangulation on a point set I of size n >= 5. Its face set is J. Write

\[
 f=|J|=2n-4,\qquad m=|E(\Gamma)|=3n-6,
 \qquad k=3f=6n-12,\qquad v=n+f=3n-4.
\]

Let H be its vertex-face incidence graph; let K be its set of k incidences, called corners. Suppose there is a probability distribution lambda on Hamiltonian cycles for which

\[
 a_e=\Pr(e\text{ is in the cycle})\ge 1/3\quad(e\in E(\Gamma)),
\]

and incidence color refinement, initialized with the two part colors, becomes discrete. Let ell be the diameter of the face dual graph. Define

\[
 M_*=4104f(\ell+1)^2,\qquad
 C_*=12M_*^2+2M_*,\qquad B=m^2+20m.
\]

**Theorem.** For every fixed even D with

\[
 D\ge12,\qquad D>\max\{M_*+2fC_*,B\},                 \tag{1.1}
\]

the rank-layer model defined below has the parameterized parity limit. If the coverage numbers have common denominator Q, its error is

\[
 O_{\Gamma,D,\lambda}(q^{-1/(2Q)})
\]

uniformly over all activity sets and incidence-sign choices, as q tends to infinity through odd primes. Consequently there is a symmetric rational-valued kernel U on a finite rational probability space, with 0 <= U <= 1 and positive mean mu, such that

\[
 t(H,U)<\mu^k.
\]

There is therefore a finite simple graph G with at least one edge and

\[
 t(H,G)<p(G)^k,
 \qquad p(G)=\frac{2|E(G)|}{|V(G)|^2}.
\]

The rationality of the cycle distribution is not needed for the qualitative conclusion. Because the finite cycle-coverage feasibility system has rational coefficients, any feasible real distribution can be replaced by a rational one. Rationality supplies the explicit exponent lattice.

Since ell+1 <= f, condition (1.1) admits a bound D = O(n^7). For example, with f=2n-4, the even integer

\[
 D=404227584f^7+16416f^4+4104f^3+2
\]

is sufficient. The sharper diameter-dependent expression (1.1) will usually be much smaller. These bounds are deliberately conservative and are not suggestions for feasible computation.

## 2. Combinatorial reductions

An admissible exposure class begins with a triangular face and repeatedly attaches a triangle along an existing edge, its third point being new. Suppose distinct triples form a complex in which every occurring point pair belongs to exactly two faces, and one cut partitions the faces into two such spanning classes.

At every attachment the shared edge is a boundary edge. An interior edge already has its two incident faces and cannot be used again. The fresh vertex belongs to no earlier triangle. Thus each class is a triangulated disk, obtained by replacing one boundary edge by two; its boundary remains a simple cycle containing every exposed point. A spanning class has n-2 triangles and boundary length n.

An edge is internal to a class exactly when both incident faces belong to that class. Hence the two classes have the same boundary edges and disjoint sets of interior edges. Gluing the disks along that common boundary produces a sphere. Distinct triples exclude repeated faces; the point graph is simple. Conversely a Hamiltonian cycle in a sphere triangulation separates it into two triangulated disks without interior vertices. Each is a triangulated polygon. Its weak dual is a tree, and removing ears, then reversing the order, gives an admissible exposure. The removed ear vertex is absent from the remaining polygon, so reversal really introduces a new point.

Thus admissible cuts and Hamiltonian cycles are the same objects for this purpose. In particular, no additional connectivity assumption is necessary. The dual of the resulting sphere triangulation is connected.

Euler's identity and double counting face-edge incidences give f=2n-4 and m=3n-6. Every Hamiltonian cycle has degree two at every point. Averaging gives

\[
 \sum_{e\ni i}a_e=2,\qquad \sum_e a_e=n.
\]

Therefore deg_Gamma(i) <= 6, and

\[
 \sigma:=\sum_e(a_e-1/3)=n-(3n-6)/3=2.              \tag{2.1}
\]

Strict excess is automatic. More importantly, its **total** is fixed: the propagation argument will use sigma=2, not the smallest positive a_e-1/3. Finally n<f is exactly n>4, which is the inequality needed by dilution.

This establishes and slightly sharpens the structural reduction in R, `proof.tex`, Lemma `hamilton-reduction`.

## 3. Elementary finite-field facts and the transverse model

Fix an odd prime q and an even D=2r. Let S_D be the uniform space of symmetric D by D matrices over F_q. The sign of a rank-r symmetric matrix is the quadratic character of the determinant of its nondegenerate quotient form. Put

\[
 K_\xi(Z)=\frac{1_{\{\operatorname{rank}Z=r,\,\operatorname{sign}Z=\xi\}}}
 {\Pr(\operatorname{rank}Z=r,\,\operatorname{sign}Z=\xi)},
 \qquad \xi\in\{+1,-1\},\qquad c_0=\chi((-1)^r).
\]

Each kernel is nonnegative and has mean one. For independent X_i,Y_j in S_D, the rank-layer conclusion is

\[
 \mathbb E\prod_{(i,j)\in A}K_{\xi_{ij}}(X_i-Y_j)
 =\mathbb E_\eta\prod_{j\in J}
   \prod_{\substack{\{i,h\}\subset j\\(i,j),(h,j)\in A}}
   (1+c_0\eta_{\{i,h\}}\xi_{ij}\xi_{hj})
   +O(q^{-1/(2Q)}),                                      \tag{3.1}
\]

where eta_e are independent uniform signs. A denotes an arbitrary activity set of corners.

### 3.1 Symmetric-matrix counts

Set b(t)=t(t+1)/2. Counting bases gives

\[
 {N\brack s}_q=q^{s(N-s)}(1+O_N(q^{-1})).
\]

A uniform symmetric matrix of positive size is nonsingular with probability 1-O(q^-1), and its two nonzero determinant characters have probability 1/2+O(q^-1). To prove both assertions, condition on a nonsingular leading principal minor C and use

\[
 \det\begin{pmatrix}C&z\\z^T&a\end{pmatrix}
 =\det(C)(a-z^TC^{-1}z).
\]

Given C,z, the final scalar is uniform. Induction bounds the exceptional minor.

A symmetric matrix with image a fixed s-space with basis-column matrix P is uniquely PRP^T with R a nonsingular symmetric s by s matrix. Its quotient-form sign is the sign of R. Choosing the image and R therefore gives

\[
 \Pr(\operatorname{rank}Z=s,\operatorname{sign}Z=\xi)
 =(1/2+O(q^{-1}))q^{-b(N-s)}.                         \tag{3.2}
\]

For a prospective radical u-space, vanishing of the corresponding rows and columns imposes Nu-binomial(u,2) independent linear conditions. Summing over such subspaces proves

\[
 \Pr(\operatorname{nullity}Z\ge u)=O(q^{-b(u)}).        \tag{3.3}
\]

In particular each signed rank-r normalization in S_D is

\[
 \pi_\xi=(1/2+O(q^{-1}))q^{-b(r)}.
\]

### 3.2 Restriction-sign balance without independence assumptions

For any family U of distinct r-subspaces of F_q^D and uniform symmetric form Q_0, let f_xi(Q_0) be the fraction on which its restriction is nonsingular of sign xi. Then

\[
 \mathbb E|f_\xi-1/2|
 =O(q^{-1/2}+|\mathcal U|^{-1/2}).                    \tag{3.4}
\]

Indeed, each restriction is uniform. For distinct subspaces U,V, their restricted forms overlap exactly in their common symmetric block on U intersect V. Conditional on that block, all other relevant coefficients are independent. Except with probability O(q^-1), the common block is nonsingular; when its size is zero this is automatic. Schur complements of positive size in U and V are then independent uniform symmetric forms. Their sign indicators have covariance O(q^-1). The variance of the average is consequently O(q^-1+1/|U|), giving (3.4) by Cauchy-Schwarz.

The same bound holds conditional on Q_0 being nonsingular, or on both Q_0 and Q_0-L being nonsingular for any fixed L. Those events have probability 1-O(q^-1), uniformly in L, and the expectation of the nonnegative error under conditioning is at most its unconditional expectation divided by that probability. No restriction-sign matching event is added to the conditioning.

### 3.3 Local transverse centers

A nondegenerate symmetric form on a 2r-space has an isotropic r-space precisely when its determinant character is c_0. Its number of maximal isotropic spaces, including both families, is

\[
 N_r=\prod_{a=0}^{r-1}(1+q^a)
 =2q^{r(r-1)/2}(1+O(q^{-1})).                         \tag{3.5}
\]

For completeness, diagonalization follows by splitting nonzero-norm lines. Every nondegenerate form of dimension at least three has a nonzero isotropic vector: two sets of the form {a x^2} and {t-b y^2}, each of size (q+1)/2, intersect. Splitting hyperbolic planes leaves an anisotropic part of dimension at most two, and the determinant character distinguishes the split case in even dimension. In split coordinates (x,y), isotropy is x^T y=0. Counting isotropic lines and reducing by one gives N_r=(1+q^(r-1))N_(r-1), with N_0=1. This proves (3.5).

For nonsingular B and symmetric rank-r A,

\[
 \operatorname{rank}(B-A)=r\quad\Longleftrightarrow\quad AB^{-1}A=A.
                                                               \tag{3.6}
\]

The forward direction follows because the rank-r images of A and B-A are complementary, and AB^-1 is their projection. Conversely the identity makes it an idempotent of rank r. If A and A-B have signs xi_1,xi_2, complementary image bases give

\[
 \chi(\det B)=c_0\xi_1\xi_2.                          \tag{3.7}
\]

For three pairwise transverse point matrices put B_0=X_1-X_2, B_1=X_1-X_3, Q_0=B_0^-1, and L=B_0^-1-B_1^-1. The symmetric matrix L is nonsingular. Centers meeting all three rank conditions are in bijection with maximal L-isotropic r-spaces U on which Q_0 is nonsingular: writing A=X_1-Y=PRP^T, equations (3.6) become

\[
 P^TLP=0,\qquad R=(P^TQ_0P)^{-1}.
\]

Off the three pair-sign matches in (3.7), the signed center count is zero. On the matches, L is split and only the sign of Q_0 restricted to U remains to be chosen. Its normalized center factor is exactly

\[
 \frac{q^{-b(D)}N_r}{\pi_{\xi_1}\pi_{\xi_2}\pi_{\xi_3}}
 f_{\xi_1}(Q_0;L)=(16+O(q^{-1}))f_{\xi_1}(Q_0;L).     \tag{3.8}
\]

The exponent cancels because r(r-1)/2-b(2r)+3b(r)=0. Conditional on fixed L and transversality, Q_0 is uniform subject to Q_0 and Q_0-L being nonsingular: inversion is a bijection on nonsingular symmetric matrices, and each Q_0 corresponds to exactly one inverse pair. Apply (3.4), retaining the matching indicator inside the error expectation. For r>1, N_r^-1/2=O(q^-1/2). The limiting factor is 8 on matches and 0 off them, with L1 error O(q^-1/2) and a uniform pointwise upper bound on the transverse locus.

For two active incidences the same calculation uses all r-subspaces, not the maximal isotropic family. Its factor is

\[
 \frac{q^{-b(D)}{2r\brack r}_q}{\pi_{\xi_1}\pi_{\xi_2}}f_{\xi_1}(Q_0)
 =(4+O(q^{-1}))f_{\xi_1}(Q_0),
\]

and thus tends in L1 to 2 on the pair match and 0 otherwise. With at most one active incidence the factor is exactly 1.

### 3.4 Joint determinant signs

Let eta_e^X=chi(det(X_i-X_h)). For every fixed graph of maximum degree at most six and every fixed even D>=12, these signs have asymptotically independent joint law, with error O(q^-1/2) in total variation after assigning any zeros the value +1.

To prove this, fix a nonempty subset of edges and choose a vertex i incident to s selected edges, 1<=s<=6. Write

\[
 X_v=\begin{pmatrix}a_v&z_v^T\\z_v&W_v\end{pmatrix},\qquad N=D-1.
\]

Given W_i, the selected differences M_l=W_i-W_(h_l) are independent uniform symmetric N-matrices. They are all nonsingular except with probability O(q^-1). Conditional on nonsingularity, their inverses have the independent uniform nonsingular symmetric law. For independent unrestricted symmetric Q_l, every nonzero linear combination is uniform. By (3.3), a union bound over nonzero t in F_q^s gives

\[
 \Pr\bigl(\exists t\ne0:\operatorname{rank}\textstyle\sum_l t_lQ_l\le s\bigr)
 =O(q^{s-b(N-s)}).
\]

This remains a valid upper bound up to a bounded factor under conditioning all Q_l nonsingular. Since N-s>=5 and b(N-s)>=15>s, with probability 1-O(q^-1) every nonzero combination of the M_l^-1 has rank at least s+1.

Now condition on all entries except z_i. The selected determinants equal det(M_l) times

\[
 h_l(z_i)=a_i-a_{h_l}-(z_i-z_{h_l})^TM_l^{-1}(z_i-z_{h_l}).
\]

Every nonzero additive Fourier frequency of the vector (h_1,...,h_s) is a quadratic Gauss sum whose quadratic part has rank >=s+1. The normalized magnitude is at most q^(-(s+1)/2). This bound follows directly by differencing: the squared Gauss-sum magnitude is bounded by the fraction of vectors in the kernel of the quadratic matrix. Parseval and Cauchy-Schwarz therefore put the distribution of (h_l) within (1/2)q^-1/2 in total variation of uniform F_q^s.

The product of its s quadratic characters has uniform expectation zero. All selected-edge factors not incident to i are fixed under the conditioning. Consequently every nonempty selected-edge sign moment is O(q^-1/2). The probability of any zero determinant is O(q^-1). Expansion in the characters of the finite sign cube gives the joint-law assertion.

This proof uses the degree bound, not the number thirteen. Constants can depend on the fixed graph, including its number of edges.

### 3.5 Assembly on the transverse locus

Let T be the event that all point-edge differences are nonsingular. Its complement has probability O(q^-1). Conditional on the points, centers are independent, so the density is a product of local center factors F_j. The corresponding sign models G_j and all F_j are bounded on T by a constant depending on D. Deterministic telescoping yields

\[
 \left|\prod_jF_j-\prod_jG_j\right|
 \le C_D^{f-1}\sum_j|F_j-G_j|\quad\text{on }T.
\]

Each local L1 error is O(q^-1/2), even when faces overlap. The bounded sign product permits removing 1_T at cost O(q^-1), and the joint-sign result then proves (3.1) on T with error O(q^-1/2). The singular contribution still needs the weighted estimate proved next. Small unweighted probability alone would not suffice.

These arguments audit and generalize O, `transverse.tex`, including its conditioning and joint-sign steps.

## 4. Ordered Lagrangian orbit costs

Use a nondegenerate symplectic space of dimension 2D. Write Lag for its uniform Lagrangians, and

\[
 L_N=\prod_{a=1}^N(q^a+1),\quad
 \vartheta_N(t)=L_{N-t}/L_N,\quad
 I_N(t)=\frac{L_N}{L_{N-t}}{N\brack t}_q.
\]

These count, respectively, all Lagrangians in a 2N-space, the probability of containing a fixed isotropic t-space, and the number of isotropic t-spaces. Reduction by an isotropic space is a bijection on containing Lagrangians. Counting incident lines gives the recurrence L_N=(q^N+1)L_(N-1); counting pairs of an isotropic subspace and a containing Lagrangian gives I_N(t). In particular,

\[
 \vartheta_N(t)\asymp_N q^{-Nt+\binom t2},\quad
 I_N(t)\asymp_N q^{2Nt-(3t^2-t)/2}.                   \tag{4.1}
\]

For fixed Lagrangian A, the number of B with intersection dimension h is

\[
 {N\brack h}_q q^{b(N-h)}.
\]

Choose A intersect B and reduce by it; the transverse Lagrangians in the quotient are graphs of symmetric forms. Thus the pair probability pi_(N,h) is asymptotic to q^-b(h). Every ordered pair of that dimension is in one symplectic orbit: choose a symplectic basis through the common space, then dual bases of the transverse quotient pair.

For an ordered triple put

\[
 c=\dim(L_1\cap L_2\cap L_3),\quad
 h_l=\dim(L_j\cap L_k),\quad s_l=h_l-c,\quad d=D-c,
 \qquad C=(D+1)c+\sum_l b(s_l).                      \tag{4.2}
\]

**Ordered-orbit lemma.** Every feasible dimensional profile has probability O_D(q^-C). Every individual occurring ordered symplectic orbit of that profile has probability bounded above and below by positive D-dependent constants times q^-C. Conditional on a fixed pair of intersection dimension h, completion of the specified profile costs O_D(q^-C+b(h)).

**Proof.** Choose the common isotropic c-space and impose its three containments. By (4.1), this has total exponent -(D+1)c. Reduce by it. The reduced triple has common intersection zero. Its three opposite pair spaces H_l, of dimensions s_l, are mutually orthogonal and in direct sum: a relation x_1+x_2+x_3=0 puts each x_l in all three Lagrangians. Their isotropic sum H_* has dimension a=sum s_l<=d. Put z=d-a.

Choose H_* and its ordered direct-sum decomposition into the H_l. There are

\[
 I_d(a)\frac{|GL_a|}{\prod_l|GL_{s_l}|}
\]

choices. The l-th Lagrangian must contain A_l=sum_(j!=l) H_j, of dimension a-s_l. Multiplying the three independent containment probabilities leaves exponent

\[
 2da-\frac{3a^2-a}{2}+a^2-\sum_l s_l^2
 +\sum_l\left[-d(a-s_l)+\binom{a-s_l}{2}\right]
 =-\sum_l b(s_l).                                   \tag{4.3}
\]

Dropping exactness proves the profile upper bound.

For the lower bound on an individual orbit, first classify the remaining extension data. Since H_l intersect L_l=0, the symplectic pairing of H_l with L_l has full rank s_l. Choose a dual s_l-space Q_l inside L_l. The block H_l+Q_l is symplectic; all three Lagrangians split over it, because each contains a Lagrangian of that block and its projection to the block must belong to that contained space. The other pair spaces remain in its orthogonal complement. Repeating leaves a pairwise transverse ordered triple in the symplectic 2z-space H_*^perp/H_*.

A transverse ordered pair can be made the coordinate pair, and the third Lagrangian is the graph of a nonsingular symmetric z-form. The pair stabilizer acts by congruence. Thus the dimensions and this residual form-congruence orbit determine the whole ordered triple orbit; there are no uncounted extension invariants.

Each occurring residual orbit has positive probability bounded below independently of q. Indeed its probability for three independent uniform residual Lagrangians is

\[
 q^{b(z)}|\mathcal O_{\rm form}|/L_z^2.
\]

Diagonalize a representative form. An isometry is determined by an orthogonal basis of prescribed nonzero norms. In a nondegenerate k-space, at most 2q^(k-1) vectors have a prescribed nonzero norm, by fixing k-1 diagonal coordinates and solving one quadratic equation. Hence

\[
 |\operatorname{Isom}(F)|\le2^zq^{z(z-1)/2},\qquad
 |\mathcal O_{\rm form}|\ge
 2^{-z}q^{b(z)}\prod_{a=1}^z(1-q^{-a}).
\]

The claimed residual probability has a positive z-dependent lower bound for all odd primes; for z=0 it equals one.

It remains to ensure exact intersections on lifting. Fix prospective H_l and sample L_l independently conditional only on A_l being contained in L_l. Impose separately the avoidance event L_l intersect H_*=A_l. In the containment quotient, failure means meeting a fixed isotropic s_l-space in a line. Its probability is at most

\[
 \frac{q^{s_l}-1}{q-1}\frac1{q^{z+s_l}+1}\le1/2,
\]

and is zero if s_l=0. These conditions preserve independence of the three samples. Their reductions to H_*^perp/H_* are independent and uniform: any quotient symplectic automorphism extends fixing H_* and a chosen dual, preserves the conditioning, and acts transitively on quotient Lagrangians.

Impose the desired residual transverse orbit, at uniformly positive probability. If x belongs to L_i intersect L_j, it is orthogonal to all H_l and its quotient image belongs to the zero intersection of the two residual Lagrangians. Thus x lies in H_*. Avoidance then forces x into A_i intersect A_j=H_k. The intersections are exactly the prescribed ones. The block decomposition places the triple in the desired orbit. Successful choices of the common and pair spaces are unique to the resulting triple, so this lower count has no multiplicity problem. Combining it with (4.3) proves the individual-orbit lower bound. Pair transitivity and division by pi_(D,h) give the conditional bound. QED.

### Matrix-chart comparison

The graphs Gamma_X={(x,Xx)} are precisely the Lagrangians transverse to one coordinate Lagrangian. Their fraction is

\[
 \beta_D=q^{b(D)}/L_D=\prod_{a=1}^D(1+q^{-a})^{-1},
 \qquad\dim(\Gamma_X\cap\Gamma_Y)=D-\operatorname{rank}(X-Y).
\]

Define the unsigned kernel

\[
 J_0(L,Y)=1_{\{\dim(L\cap Y)=r\}}/\pi_{D,r}.
\]

On the chart, K_xi(X-Y)<= (pi_(D,r)/pi_xi) J_0(Gamma_X,Gamma_Y). Conditioning all v=n+f independent Lagrangians to lie in the chart costs beta_D^-v. Dropping the chart indicator and signs bounds every nonnegative matrix expectation by the corresponding unsigned Lagrangian expectation times

\[
 \beta_D^{-v}\prod_{(i,j)\in A}\frac{\pi_{D,r}}{\pi_{\xi_{ij}}},
\]

which is bounded for fixed Gamma,D. This comparison includes singular-profile indicators and does not require bounded normalized kernels.

This proves the local ordered-orbit and chart assertions used from O, `orbits.tex`, in arbitrary template size.

## 5. Planted gain, including the shared-form constraint

For fixed point Lagrangians define a local unsigned center factor

\[
 F_j=\mathbb E_Y\prod_{i\in A_j}J_0(L_i,Y).
\]

With three active incidences, plant a uniform center Y and sample L_1,L_2,L_3 independently conditional on meeting it in dimension r. Relative to the independent point-triple law mu, this planted law nu has density F_j. The density is constant on each ordered orbit O and equals nu(O)/mu(O). The individual-orbit lower bound, not merely the profile probability, is consequently essential.

Use c,d,h_l,s_l from (4.2). For the unique actual common space C_0 define

\[
 u=\dim(C_0\cap Y),\quad r'=r-u,\quad\delta=2u-c=d-2r'.
\]

In the quotient by C_0 set Y'=((Y intersect C_0^perp)+C_0)/C_0. Because each L_i contains C_0,

\[
 (L_i/C_0)\cap Y'=((L_i\cap Y)+C_0)/C_0.
\]

Thus the quotient center-intersection dimension is exactly r'. For fixed C_0,Y, before imposing any mutual point profile, the three quotient Lagrangians are independent uniform. After their individual center conditions, the R_i=(L_i/C_0) intersect Y' are independent uniform r'-subspaces of the d-space Y'. Define

\[
 p_l=\dim(R_j\cap R_k),\quad t_l=s_l-p_l,\quad
 P=\sum_l p_l,\quad T=\sum_l t_l,
\]
\[
 v_0=d-\dim(R_1+R_2+R_3),\qquad
 w=3r'-d-P+v_0=\frac{d-3\delta}{2}-P+v_0.
\]

Here v_0 is a local dimension parameter, unrelated to the number v of incidence vertices. In the rest of the local calculations write it simply as v_0.

### 5.1 Four costs

The common-space count and its three containments have exponent -(D+1)c. Choosing a u-subspace in C_0 and imposing its containment in Y gives the center-intersection upper bound

\[
 O(q^{-u(D-c)-b(u)}).
\]

The quotient's three center conditions, with the planted normalization, give exponent

\[
 g_C=3[b(r)-b(r-u)]-u(D-c)-b(u)
 =(r+c+1)u-2u^2.                                    \tag{5.1}
\]

The R_i have common intersection zero in an actual quotient profile. Their pair spaces are in direct sum. To count their prescribed pair dimensions and span codimension v_0, first choose a prospective span of dimension d-v_0 and contain the three independent R_i in it. Then choose the three direct pair spaces and contain the appropriate two in each R_i. The resulting upper bound is

\[
 O(q^{-\delta P-\sum_l p_l^2-v_0w}).                  \tag{5.2}
\]

Explicitly, the span choice and containments give exponent (d-v_0)v_0-3r'v_0. The pair-space choice gives (d-v_0)P-sum p_l^2; the subsequent containments give -2(d-v_0-r')P. Their sum is the exponent in (5.2). Exact span and intersection conditions can be dropped for this upper bound. The inequality w>=0 follows because the three independent pair-relation spaces inject into the kernel of the summation map from the abstract direct sum R_1 direct-sum R_2 direct-sum R_3.

For the remaining lifts choose symplectic coordinates Y' plus (Y')*. For R_i fixed, put A_i=R_i^circ. Lagrangian lifts with intersection exactly R_i are parametrized bijectively by arbitrary symmetric forms F_i on A_i; the quotient lift sends alpha in A_i to a class in Y'/R_i represented by the functional beta -> F_i(alpha,beta). Hence the three lift forms are independent and uniform before imposing their mutual profile.

On Q_l=A_j intersect A_k, whose dimension is delta+p_l, define cyclic differences D_l=(F_j-F_k)|_(Q_l). There is an exact sequence

\[
 0\longrightarrow R_j\cap R_k\longrightarrow L'_j\cap L'_k
 \longrightarrow\operatorname{rad}D_l\longrightarrow0.
\]

A projected vector has simultaneous lifts precisely when their prescribed classes agree in Y'/(R_j+R_k), which is exactly the radical condition. Therefore the additional intersection dimension is nullity(D_l)=t_l.

The D_l are **not independent**. Put V_0=A_1 intersect A_2 intersect A_3, of dimension v_0. Their exact joint law is uniform on

\[
 \{(D_1,D_2,D_3):D_1|_{V_0}+D_2|_{V_0}+D_3|_{V_0}=0\}.       \tag{5.3}
\]

To prove sufficiency of this constraint, prescribe F_1|V_0=0, F_2|V_0=-D_3|V_0, F_3|V_0=D_2|V_0, extend one member of each required difference onto Q_l, and use the target difference to prescribe the other. Each F_i receives compatible prescriptions on two subspaces whose intersection is V_0. Two symmetric forms agreeing on an intersection extend simultaneously by choosing the remaining mixed block arbitrarily. This constructs all target triples in (5.3), regardless of other linear relations among the spaces. The constraint has codimension b(v_0), since the sum-of-restrictions map is onto the form space of V_0.

Using the independent target law and conditioning on (5.3) therefore gives

\[
 \Pr(\operatorname{nullity}D_l=t_l\text{ for all }l\mid R_1,R_2,R_3)
 =O(q^{-\sum_l b(t_l)+b(v_0)}).                       \tag{5.4}
\]

This is valid even if the upper bound exceeds one. Extra full-lift common-zero and orbit conditions only reduce the probability.

### 5.2 A finite, explicitly relaxed gain maximum

Divide the product of the four cost bounds by the individual ordered-orbit lower bound. A valid three-active gain is the maximum of

\[
 g_C+\sum_l b(s_l)-\delta P-\sum_l p_l^2-v_0w
                 -\sum_l b(t_l)+b(v_0)               \tag{5.5}
\]

over the following finite set of integer tuples:

\[
\begin{gathered}
 0\le u\le\min(c,r),\quad 0\le r'=r-u\le d,\quad\delta=2u-c,\\
 p_l,t_l\ge0,\quad p_l+t_l=s_l,\quad P+T\le d,\\
 0\le t_l\le p_l+\delta,\quad 0\le v_0\le p_l+\delta\quad(l=1,2,3),
 \quad w=3r'-d-P+v_0\ge0.
\end{gathered}                                                   \tag{5.6}
\]

Every actual quadruple satisfies these conditions. Empty feasible sets give zero local factors. Maximizing over all tuples satisfying (5.6), rather than a union of realizable tuples over prime fields, only weakens the valid upper bound. All subsequent inequalities use only (5.6). Thus neither a realizability oracle nor any assertion of sufficiency of these constraints is needed. The chosen maximum is an integer and is independent of q.

For two active incidences at pair dimension h, the analogous planted argument gives

\[
 g_2(h)=\max_{p+t=h,\,0\le t\le p\le r}
 \{b(h)-p^2-b(t)\}=b(\lfloor h/2\rfloor).             \tag{5.7}
\]

The two planted r-spaces have intersection p at cost O(q^-p^2), and their lift-form difference is a uniform symmetric p-form with nullity t at cost O(q^-b(t)). Pair-orbit division supplies b(h). The maximand decreases as p increases from ceil(h/2), because its successive difference is h-3p-1<0; evaluating the first value proves (5.7). With zero or one active incidence the gain is zero and the factor is exactly one.

This proves the pointwise local estimates from O, `planted.tex`, including the joint difference-form issue. They have no dependence on the size or shape of Gamma.

## 6. Weighted global profile cost

Let a point profile specify h_e=dim(L_i intersect L_h) for every edge and c_j=dim(intersection_(i in j) L_i) for every face. Define C_j by (4.2).

For each cut t and side s in {0,1}, let A_(t,s) be its side-profile event and c_(t,s) its exposure cost. Expose the root triangle, at cost C_j. At every later triangle the new point Lagrangian is still independent uniform conditional on **all** previously exposed points. The two old points form a specific ordered pair. Pair transitivity and the ordered-orbit lemma bound the conditional probability of completing the prescribed local profile by O_D(q^-C_j+b(h_e)). This remains true even though the old points have other constraints and relations. An incorrect pair dimension makes the conditional event impossible.

Iterated conditional expectation therefore gives

\[
 \Pr(A_{t,s})\le K_{t,s}\,q^{-c_{t,s}},\qquad
 c_{t,s}=\sum_{j\in J_{t,s}}C_j
          -\sum_{e\text{ internal to }J_{t,s}}b(h_e).            \tag{6.1}
\]

One may also subtract all internal edges from a spanning-tree exposure bound, which only weakens it; for a triangulated polygon the weak dual is already a tree.

Let A_full be the complete profile event. Since A_full is contained in every A_(t,s),

\[
 \Pr(A_{\rm full})
 \le\prod_t\prod_{s=0}^1\Pr(A_{t,s})^{\lambda_t/2}.            \tag{6.2}
\]

For positive probability this follows just by taking logarithms; at zero it is trivial. There is no independence assertion. Every face appears in exactly one side of each cut; an edge is internal to one side precisely when that cut does not cross it. Taking the weighted sum of (6.1) proves

\[
 \boxed{\displaystyle
 \mathcal C=\frac12\left[\sum_jC_j-\sum_e(1-a_e)b(h_e)\right],
 \qquad\Pr(A_{\rm full})=O_{D,\Gamma,\lambda}(q^{-\mathcal C}).}
                                                               \tag{6.3}
\]

The finitely many exposure constants stay bounded after the weighted product. The same argument works for arbitrary real nonnegative weights summing to one.

After integrating independent centers, all local factors are pointwise O(q^g_j), so this profile contributes

\[
 O(q^{\sum_jg_j-\mathcal C}).                         \tag{6.4}
\]

No new conditional independence is introduced by this center weighting.

### 6.1 Denominator bookkeeping

Let Q be the least common multiple of the reduced denominators of the **coverage numbers** a_e. Because each C_j and b(h_e) is an integer,

\[
 2Q\mathcal C\in\mathbb Z.
\]

Each selected gain is also integral. Thus

\[
 \mathcal C>\sum_jg_j\quad\Longrightarrow\quad
 \mathcal C-\sum_jg_j\ge\frac1{2Q}.                  \tag{6.5}
\]

If the raw cut weights have common denominator Q_w, then Q divides Q_w, so 1/(2Q_w) is always a valid, possibly weaker, guarantee. The exact exposure inequality has no separate loss from the number of cuts or overlap of classes. For the second certificate Q_w=11544 but Q=3, so (6.5) gives 1/6, not merely 1/23088.

## 7. Uniform residual classification and dimension bound

Set

\[
 \beta_j=C_j/2-\frac16\sum_{e\subset j}b(h_e),\quad
 S_j=\beta_j-g_j,\quad
 \mathcal E=\frac12\sum_e(a_e-1/3)b(h_e).
\]

Each edge occurs twice, so exactly

\[
 \mathcal C-\sum_jg_j=\sum_jS_j+\mathcal E.           \tag{7.1}
\]

Individual S_j can be negative. The following argument controls their total.

### 7.1 Local slack inequalities

On a face with at most two active incidences, let h=max_(e subset j) h_e. Then

\[
 S_j\ge0,\qquad S_j\ge h^2/24-h/12.                 \tag{7.2}
\]

To prove this, write h=c+max s_l and choose l_0 maximizing s_l. Expanding, using sum s_l<=D-c, gives

\[
 \beta_j\ge b(h)/3+b(c)/6+\frac13\sum_{l\ne l_0}b(s_l).
\]

For every integer h>=0,

\[
 b(\lfloor h/2\rfloor)\le b(h)/3,\qquad
 b(\lfloor h/2\rfloor)\le h(h+2)/8.
\]

The first equality occurs only at h=0,2. Combining with (5.7) proves (7.2). Zero slack requires c=0 and either all h_e=0, or exactly one h_e=2; the latter requires the two active endpoints of that pair.

For a three-active face, a maximizing tuple in (5.6) gives the exact identity

\[
\begin{split}
 S={}&\frac{c(d+\delta-1)-\delta(d+2)+2\delta^2}{4}\\
 &+\sum_{l=1}^3\left[
 \frac{(2p_l-t_l)(2p_l-t_l-1)}6
 +\delta p_l-\frac c6(p_l+t_l)\right]+v_0w-b(v_0).
\end{split}                                                     \tag{7.3}
\]

This follows by substituting (5.5) into beta-g; the two identities needed are

\[
 p^2+b(t)-\tfrac23b(p+t)=\frac{(2p-t)(2p-t-1)}6
\]

and the common-space expansion using D=d+c and u=(c+delta)/2. Let Q_0 be the homogeneous quadratic part of (7.3):

\[
\begin{split}
 Q_0={}&\frac{c(d+\delta)-\delta d+2\delta^2}{4}\\
 &+\sum_l\left[\frac{(2p_l-t_l)^2}{6}
 +\delta p_l-\frac c6(p_l+t_l)\right]
 +v_0\left(\frac{d-3\delta}{2}-P\right)+\frac{v_0^2}{2}.
\end{split}
\]

Then

\[
 Q_0\ge\frac{P^2+T^2+\delta^2}{342},\qquad
 S=Q_0-c/4-\delta/2-(2P-T)/6-v_0/2.                  \tag{7.4}
\]

Here is a proof of the coercivity constant. Set

\[
 a=\left(P-\frac{d-3\delta}{2}\right)_+,\quad
 z=\min\left(P/3+\delta,(P-T+3\delta)/2\right).
\]

The constraints imply 0<=a<=z; completing the square bounds the v_0 part below by -a^2/2>=-z^2/2. Cauchy-Schwarz bounds sum(2p_l-t_l)^2 below by (2P-T)^2/3. Thus

\[
 Q_0\ge\frac{c(d+\delta)-\delta d+2\delta^2}{4}
       +\frac{(2P-T)^2}{18}+\delta P-\frac{c(P+T)}6-\frac{z^2}{2}.
                                                               \tag{7.5}
\]

Its c coefficient is at least (d+3delta)/12>=0, since d>=P+T and T<=P+3delta. Replace c by |delta|.

If delta>=0, the remaining function of T on [0,P+3delta] is

\[
 F(T)=\frac{3\delta^2}{4}+\frac{(2P-T)^2}{18}
       +\frac{(5P-T)\delta}{6}
       -\frac12\min(P/3+\delta,(P-T+3\delta)/2)^2.
\]

It is decreasing up to T=P/3+delta and concave after that. Its minimum is at the breakpoint or the last endpoint. Those values are respectively

\[
 \frac{32P^2+84P\delta+45\delta^2}{324},\qquad
 \frac{2P^2+12P\delta+27\delta^2}{36},
\]

each at least (P^2+delta^2)/18. Also P^2+T^2+delta^2<=19(P^2+delta^2).

If delta=-y<0, put x=P-3y>=0. The remaining d coefficient is y/2, so replacing d by P+T is a lower bound. For 0<=T<=x the result is

\[
 G(T)=y^2/4+(2x-T)y/3+(2x-T)^2/18
       -\tfrac12\min(x/3,(x-T)/2)^2.
\]

It is decreasing up to x/3 and concave afterward. Its breakpoint and endpoint values are

\[
 \frac{32x^2+180xy+81y^2}{324},\qquad
 \frac{2x^2+12xy+9y^2}{36},
\]

each at least (x^2+y^2)/18. Finally P^2+T^2+y^2<=19(x^2+y^2). This proves the first inequality in (7.4) in both cases. The second follows by separating the linear terms of (7.3).

### 7.2 Propagation using total excess

Suppose the first cost fails to save, namely sum S_j+E<=0. Put M=max_e h_e. On a three-active face, c<=M, P<=3(M-c), delta<=c, and v_0<=M. Equation (7.4) gives S>=Q_0-3M/2. On a lower-activity face use (7.2). Summing yields

\[
 \sum_{j\text{ three-active}}\frac{P_j^2+T_j^2+\delta_j^2}{342}
 +\sum_{j\text{ lower-active}}\frac{h_j^2}{24}+\mathcal E
 \le\frac32fM.                                      \tag{7.6}
\]

In particular, with K^2=1026f,

\[
 P_j+T_j\le K\sqrt M\text{ on three-active faces},\quad
 h_j\le K\sqrt M\text{ on other faces},\quad
 \mathcal E\le\frac32fM.                             \tag{7.7}
\]

If M>M_*=4(ell+1)^2K^2, choose a face containing a pair of dimension M. It cannot have lower activity. On a three-active face each reduced pair dimension s_l<=P+T<=K sqrt(M), so a pair of dimension h forces the common dimension, and every pair on that face, to be at least h-K sqrt(M).

Induct along a shortest path in the connected dual. Every face at distance t is three-active and each of its pair dimensions is at least M-(t+1)K sqrt(M). Indeed every shared pair passed along the path remains larger than K sqrt(M), which excludes lower activity at the next face. By distance ell, all edges therefore have h_e>=M/2.

Use the **sum** of excess coverages, sigma=2:

\[
 \mathcal E\ge\frac12\sum_e(a_e-1/3)\frac{h_e^2}{2}
 \ge\frac{\sigma M^2}{16}=\frac{M^2}{8}.             \tag{7.8}
\]

Combined with (7.7), this forces M<=12f, contradicting M>M_* (which is much larger than 12f). Hence every non-saving profile satisfies M<=M_*, uniformly in D, activity, and local maximizing tuples.

For a more general setup with total excess sigma>0, the same argument works with

\[
 M_*=\left\lceil\max\{4104f(\ell+1)^2,24f/\sigma\}\right\rceil.
\]

For sphere templates sigma=2, so the displayed bound in the theorem has no dependence on a small individual excess or on a cut denominator.

### 7.3 Removing all positive common modes

Writing n_l=2p_l-t_l and substituting w into (7.3) gives

\[
 S=Ad+R,\qquad A=(c-\delta+2v_0)/4=(c-u+v_0)/2\ge0,
\]

where

\[
\begin{split}
 R={}&[c(\delta-1)-2\delta+2\delta^2]/4\\
 &+\frac16\sum_l[n_l(n_l-1)+6\delta p_l-c(p_l+t_l)]
 -(3\delta/2+P)v_0+v_0(v_0-1)/2.
\end{split}                                                     \tag{7.9}
\]

All c,p_l,t_l,v_0 lie in [0,M_*] and |delta|<=M_*. Bounding the four groups of terms in (7.9) gives

\[
 |R|\le\tfrac34(M_*^2+M_*)+(6M_*^2+M_*)
                  +\tfrac92M_*^2+\tfrac12M_*^2
 \le C_*=12M_*^2+2M_*.
\]

Since c,u,v_0 are integers, a positive A is at least 1/2. If any face had A>0, its slack would be at least (D-M_*)/2-C_*. Every other three-active face has slack at least -C_*; lower-activity slacks and E are nonnegative. Thus the total would be at least

\[
 (D-M_*)/2-fC_*>0
\]

under (1.1), a contradiction. All three-active faces must have u=c, delta=c, and v_0=0.

For those parameters,

\[
 S=\frac{3c(c-1)}4+\frac16\sum_l[n_l^2+(c-1)n_l+3cp_l].       \tag{7.10}
\]

For c>=2, completing squares gives S>=(c-1)(5c+1)/8>0. For c=1, S=sum(n_l^2+3p_l)/6>=0, with equality only when all p_l=t_l=0; then all pair dimensions are one. For c=0, t_l<=p_l implies the nonnegative integer n_l>=p_l. Equality requires (p_l,t_l)=(0,0) or (1,1), independently for each l.

All slacks are now nonnegative. The assumed non-saving inequality forces every S_j=0 and E=0. A c=1 equality face passes a pair of dimension one to every neighbor. It can only border another c=1 equality face, since the other equality cases have pair dimensions zero or two. Connectivity would make every pair dimension one. But then E=sigma/2=1, impossible.

We have proved that all remaining profiles satisfy

\[
 c_j=0,\qquad h_e\in\{0,2\},\qquad
 h_e=0\text{ whenever }a_e>1/3,\qquad
 \sum_jg_j=\frac23\sum_e b(h_e).                     \tag{7.11}
\]

No simultaneous realizability of the local maximizing tuples was used.

## 8. Final span counts

Let E'={e:h_e=2} and s=|E'|. Put H_e=L_i intersect L_h for active pairs and

\[
 d_0=\dim\sum_eH_e,\quad d_i=\dim\sum_{e\ni i}H_e,
 \quad\delta_0=\sum_i d_i-2d_0.
\]

Always delta_0>=0, and a nondirect family has delta_0>=1. For the first assertion, adding an edge space increases each endpoint's local span by at least its increase in the earlier global span; sum increments. For strictness, start with an inclusion-minimal nondirect subfamily and let e be its last member. Some endpoint of e is absent from some other member of that subfamily, since edges are distinct unordered pairs. The spaces seen at this endpoint form a proper, therefore direct, subfamily. At this endpoint the increment of H_e is its full dimension, strictly larger than its global increment. This proves delta_0>=1, also for partial dependencies.

For a nondirect family, choose its arbitrary global d_0-space and s two-spaces inside it. The number is

\[
 O_D(q^{d_0(2D-d_0)+2s(d_0-2)}).
\]

A nonisotropic local span is impossible in a Lagrangian. For isotropic local spans, independence of the point Lagrangians supplies the containment factor

\[
 O_D(q^{-D\sum_i d_i+\sum_i\binom{d_i}{2}}).
\]

The gain in (7.11) is 2s. Thus the contribution exponent is

\[
 -D\delta_0-d_0^2+2sd_0-2s+\sum_i\binom{d_i}{2}.     \tag{8.1}
\]

If the active point degrees are a_i<=6, then d_i<=2a_i and

\[
 \sum_i\binom{d_i}{2}\le\sum_i(2a_i^2-a_i)
 \le11\sum_i a_i=22s.
\]

Completing the square in d_0 bounds the remainder in (8.1) by s^2+20s<=m^2+20m=B. Nondirect profiles therefore contribute O_D(q^-D+B). The global span need not be isotropic; only the local spans are required to be so.

For a direct family with arbitrary prescribed dimensions h_e, order its spaces and choose ordered bases. Every new vector must be orthogonal to previous vectors of its own space and of spaces sharing an endpoint. These vectors are globally independent, so nondegeneracy makes their orthogonality equations independent, whether or not their span is isotropic. Dividing the vector count by the number of bases gives at most

\[
 O_D\left(q^{2D\sum_eh_e-\sum_eh_e^2-\sum_e\binom{h_e}{2}
                         -\sum_{e\sim h}h_eh_h}\right)
\]

families. Here each unordered pair of distinct edges sharing an endpoint is counted once. Directness gives local dimensions d_i=sum_(e incident i) h_e, and hence

\[
 \sum_i d_i=2\sum_eh_e,\qquad
 \sum_i\binom{d_i}{2}=2\sum_e\binom{h_e}{2}+\sum_{e\sim h}h_eh_h.
\]

The containment factors cancel the D and cross terms, leaving probability O_D(q^-sum b(h_e)). With (7.11), its contribution is O_D(q^(-sum b(h_e)/3))=O_D(q^-s). Every singular direct residual profile has s>=1.

For fixed D there are finitely many profiles, activity sets, and relaxed local tuple choices. Equations (6.5), (7.11), and (8.1), with D>B, therefore bound the entire unsigned singular contribution by

\[
 O_{\Gamma,D,\lambda}(q^{-1/(2Q)}).
\]

The chart comparison transfers this to the signed matrix singular contribution. Adding the transverse contribution proves (3.1). Negating matrix differences merely changes every incidence sign by c_0; all pair sign-products are unchanged. Thus (3.1) also holds with Y_j-X_i.

This is a complete rank-layer transfer. In particular, it does not rely on the original numerical residual constant 1641 or the refinement's newer residual constant 189. All dimension requirements used here are included in (1.1).

## 9. From the rank-layer limit to a negative coefficient

This section generalizes the finite construction in O, `kernel.tex`, without retaining its numerical sizes.

### 9.1 Coordinate expansion, including repeated types

For each point edge e={i,h}, let j,l be its two incident faces, and put

\[
 U_e=\{(i,j),(h,j),(i,l),(h,l)\}\subseteq\mathcal K.
\]

At a single matrix coordinate, averaging the rank-layer parity model over eta_e gives a factor one if only one face uses the pair, and gives

\[
 1+\prod_{\kappa\in U_e}\xi_\kappa
\]

if all four corners are active. The c_0 factors cancel because c_0^2=1. Independent eta_e therefore give the exact integrated model

\[
 \prod_{e:\,U_e\subseteq A}\left(1+\prod_{\kappa\in U_e}\xi_\kappa\right). \tag{9.1}
\]

Let the point and face type sets initially be I and J. Give them priors pi and nu. At each type pair (a,b), specify a probability law for a subset S of the coordinate set K and signs xi on S. Define

\[
 W_q((a,x),(b,y))=\mathbb E_{S,\xi\mid a,b}
                   \prod_{\gamma\in S}K_{\xi_\gamma}(x^\gamma-y^\gamma),
 \qquad x,y\in\mathcal S_D^{\mathcal K}.              \tag{9.2}
\]

All matrix coordinates are independently uniform. For every fixed type pair the matrix average is one, so E W_q=1 exactly.

Put

\[
 \phi_\alpha(S,\xi)=1_{\{\alpha\subseteq S\}}\prod_{\gamma\in\alpha}\xi_\gamma,
 \qquad A_{ab}(\alpha,\beta)=\mathbb E_{S,\xi\mid a,b}\phi_\alpha\phi_\beta.
\]

Here phi_empty=1. We will arrange E phi_alpha=0 for every nonempty alpha and every type pair. Consequently

\[
 A_{ab}(\alpha,\beta)=0
 \quad\text{if }\alpha\cap\beta=\varnothing,\quad
                   \alpha\cup\beta\ne\varnothing.                 \tag{9.3}
\]

For type maps a:I->I and b:J->J, independently sample the law at each **source incidence** when expanding the product of W_q. Then factor the matrix integral across coordinates, apply (3.1), and expand (9.1). Choosing the nonconstant term for edge e at selected coordinates produces a label alpha_e subset K. At a source corner (i,j), the two face edges e,f through i contribute precisely

\[
 A_{a(i)b(j)}(\alpha_e,\alpha_f).
\]

There are finitely many activation and sign configurations, independently of q. Products and averages of their rank-layer limits are therefore valid, with the same positive error exponent at fixed parameters.

The all-empty labeling contributes one. A face with both an empty and a nonempty edge label has a zero corner factor by (9.3). Thus in a nonzero labeling any face with a nonempty edge has all three edge labels nonempty. Shared edge labels and dual connectivity propagate this to every face. It follows that

\[
 t_{I,J}(W_q)=1+
 \sum_{a:I\to I,\,b:J\to J}
 \left(\prod_i\pi_{a(i)}\right)\left(\prod_j\nu_{b(j)}\right)C_A(a,b)+o(1), \tag{9.4}
\]

where

\[
 C_A(a,b)=\sum_{\substack{\alpha_e\subseteq\mathcal K\ (e\in E)\\
                               \alpha_e\ne\varnothing\ (e\in E)}}
 \prod_{(i,j)\in\mathcal K}A_{a(i)b(j)}(\alpha_{e(i,j)},\alpha_{f(i,j)}). \tag{9.5}
\]

All maps are included. A repeated type does not identify source vertices, their matrix variables, or their activation samples. Those remain independently drawn. A repeated type pair means only that independent samples at the different source incidences have the same law. Formula (9.4) therefore includes noninjective type maps, maps taking edges to nonincident type pairs, and every other part-preserving map. The transpose formula uses maps b:I->J, a:J->I and factors A_{a(j)b(i)}; reversed differences are covered by (3.1).

### 9.2 The universal support identity

For a corner kappa=(i,j), let e,f be the two edges of j through i. Define

\[
 M_\kappa=U_e\cup U_f,
 \qquad \Delta_\kappa=U_e\mathbin\triangle U_f.
\]

The other faces on e and f are distinct: otherwise two distinct triangular faces would share two edges and hence be the same triple. It follows that

\[
 U_e\cap U_f=\{\kappa\},\qquad |M_\kappa|=7,
 \qquad\Delta_\kappa=M_\kappa\setminus\{\kappa\},\quad |\Delta_\kappa|=6. \tag{9.6}
\]

Moreover, for every point edge g,

\[
 \boxed{\quad\bigcap_{\kappa\in U_g}M_\kappa=U_g.\quad}           \tag{9.7}
\]

Here is a proof using only distinct triangular faces and two occurrences of every edge. Availability is symmetric: gamma belongs to M_kappa exactly when gamma and kappa lie in a common U_e, which is also exactly when kappa belongs to M_gamma. Fix gamma=(i,j), write j={i,h,z}, and let the opposite faces on e={i,h} and f={i,z} be l and t. Gamma is available at the three corners of j, the two e-endpoint corners of l, and the two f-endpoint corners of t, and nowhere else. For gamma to be available at all four corners of U_g, the two faces on g must be among j,l,t. Using j,l forces g=e; using j,t forces g=f. Using l,t is impossible, because both endpoints of g would have to lie in {i,h} intersect {i,z}={i}. Thus availability at all four corners is equivalent to gamma belonging to U_g. This proves (9.7).

### 9.3 An admissible law with exactly one negative identity term

Fix a rational theta with 0<theta<1, for example theta=1/2. Choose signs sigma_kappa, one negative and all others positive. At the incident type pair kappa, use the following law:

With probability 1/2 take S=M_kappa, with conditional sign-vector probability

\[
 2^{-7}\left(1+\sigma_\kappa\theta
                  \prod_{\gamma\in\Delta_\kappa}\xi_\gamma\right).
\]

With probability 1/2 take S=Delta_kappa, with conditional sign-vector probability

\[
 2^{-6}\left(1-\sigma_\kappa\theta
                  \prod_{\gamma\in\Delta_\kappa}\xi_\gamma\right).
\]

These are positive rational probabilities summing to one. For a nonincident type pair take S empty. Denote their moments by A^base.

The only possibly nonzero nonempty sign monomial under either conditional law has index Delta_kappa. Its biases cancel when averaging the two branches. Thus all nonempty first moments vanish. But only the first branch contains U_e union U_f, and hence

\[
 A^{\rm base}_\kappa(U_e,U_f)=\sigma_\kappa\theta/2.              \tag{9.8}
\]

At identity types, a nonzero term of (9.5) must have alpha_g contained in every maximal activation support at its four corners. Equation (9.7) gives alpha_g subset U_g. At a corner kappa, the two nonempty labels must intersect by (9.3). Their available four-sets intersect only at kappa by (9.6), so both labels contain kappa. Applying this to all four corners of each g forces alpha_g=U_g.

There is therefore exactly one nonzero identity term, and

\[
 C_{A^{\rm base}}(\mathrm{id},\mathrm{id})
 =\prod_{\kappa\in\mathcal K}(\sigma_\kappa\theta/2)
 =-(\theta/2)^k.                                                \tag{9.9}
\]

This proves the support and sign construction on **k=3f coordinates**, without a special use of 66. No other global nonempty label term at the identity survives, including possible local diagonal moment alternatives.

## 10. Pinning all type maps and controlling the opposite orientation

### 10.1 Integer scores from discrete color refinement

The following argument applies to any bipartite graph whose two part colors refine to singleton classes. Let l_t(u) be its round-t color and h_t(u) the histogram of round-(t-1) colors among its neighbors. At round t assign vertex score -||h_t(a)||^2 to type a, and pair score

\[
 2h_t(a)(l_{t-1}(b))+2h_t(b)(l_{t-1}(a))                         \tag{10.1}
\]

to every type pair (a,b), including nonedges. Let F_t(g) be the sum of vertex and source-edge scores for a part-preserving map g. If g preserves all round-(t-1) colors, then

\[
 F_t(g)=\sum_u\|h_t(u)\|^2
             -\sum_u\|h_t(g(u))-h_t(u)\|^2.                   \tag{10.2}
\]

Indeed the edge sum, regrouped by its source endpoints, is twice the sum of inner products of h_t(g(u)) with the histogram of the previous colors of g(v), for source neighbors v of u. Preservation of the previous colors identifies that latter histogram with h_t(u). Expanding squared distances gives (10.2). This uses neither injectivity nor adjacency preservation.

Suppose R rounds are discrete. If the incidence graph has maximum degree Delta_H, then -v Delta_H^2 <= F_t(g) <= 2v Delta_H^2 and 0 <= F_t(id) <= v Delta_H^2. Thus M=2v Delta_H^2 is an explicit integer bound for |F_t(g)-F_t(id)| for every g,t; here Delta_H<=6. Put L=M+2. Set

\[
 \mathcal Q(g)=\sum_{t=1}^R L^{R-t}F_t(g).
\]

For a nonidentity map, take its first violated refinement round t. Earlier scores tie the identity. Equation (10.2) gives an integer loss at least one at t. The total possible later advantage is at most M sum_(j=0)^(R-t-1) L^j < L^(R-t), so the first loss wins. Thus identity uniquely maximizes Q, with integer gap at least one. The combined vertex scores s_a,s_b and pair scores s_ab are all integers. This covers all n^n f^f part-preserving maps, including all repeated-type maps.

### 10.2 Rational priors and thinning

An integer parameter T>1 makes the construction rational; real exponential priors are unnecessary. Set

\[
 \pi_a=T^{s_a}/Z_I,\quad \nu_b=T^{s_b}/Z_J,
 \quad\lambda_{ab}=T^{s_{ab}-s_{\max}},\quad
 s_{\max}=\max_{a,b}s_{ab},
\]

where Z_I=sum_a T^{s_a}, Z_J=sum_b T^{s_b}. Use the base activation law with probability lambda_ab and the empty law otherwise. These are rational probabilities and 0<lambda_ab<=1. The new moments satisfy

\[
 A^\lambda_{ab}(\alpha,\beta)
 =\lambda_{ab}A^{\rm base}_{ab}(\alpha,\beta)
 +(1-\lambda_{ab})1_{\{\alpha=\beta=\varnothing\}}.               \tag{10.3}
\]

Every all-nonempty term gets one thinning factor per source incidence. Therefore its aggregate coefficient in (9.4) is

\[
 t_0(T)=Z_I^{-n}Z_J^{-f}T^{-ks_{\max}}
        \sum_{a:I\to I,\,b:J\to J} C(a,b)T^{\mathcal Q(a,b)},    \tag{10.4}
\]

where C uses the base laws. The factors outside the sum are positive and common to all maps. By (9.9) and the strict integer score gap, the leading term as T grows is negative. A sufficiently large integer T therefore makes t_0<0.

This is also an effective finite choice without enumerating all maps. Each local moment has absolute value at most one, and (9.5) has at most (2^k-1)^m terms. Hence |C(a,b)|<=(2^k-1)^m. Writing c=(theta/2)^k and N_maps=n^n f^f, any integer

\[
 T>2(N_{\rm maps}-1)(2^k-1)^m/c
\]

makes the competitor sum, after dividing by T^{Q(id)}, smaller than c/2. Thus no unresolved sign condition on the competing type maps is hidden in the choice of priors.

### 10.3 Dilution

Let t_1 be the finite opposite-orientation coefficient in (9.4), using all maps b:I->J and a:J->I and the moments A^lambda_{a(j)b(i)}. No assumption is made about its sign.

Add an inactive type * to the point type set, with probability 1-epsilon, and multiply each old point-type probability by epsilon, leaving the face prior unchanged. Type pairs involving * use empty activation. Take epsilon rational and 0<epsilon<1.

Every vertex has positive degree. In a nonempty-label term, a source vertex drawing * makes an incident corner factor zero. Therefore all source vertices drawing point types must remain active. There are n such vertices in the forward orientation and f in the opposite orientation. Consequently

\[
 \begin{split}
 t_{I,J}(W_{q,\epsilon})&=1+\epsilon^n t_0+o(1),\\
 t_{I,J}(W_{q,\epsilon}^{\mathsf T})&=1+\epsilon^f t_1+o(1).
 \end{split}                                                     \tag{10.5}
\]

The limiting product equals

\[
 1+\epsilon^n\bigl[t_0+\epsilon^{f-n}t_1+
                         \epsilon^f t_0t_1\bigr].              \tag{10.6}
\]

Because f-n=n-4>0 and t_0<0, this is less than one for every sufficiently small positive epsilon. A rational such epsilon exists. More explicitly, for 0<epsilon<=1 the bracket is at most

\[
 t_0+\epsilon^{f-n}|t_1|(1+|t_0|),
\]

so it suffices that epsilon^(f-n)|t_1|(1+|t_0|)<|t_0|/2 (with no restriction of this kind when t_1=0). Fix epsilon first, then take a sufficiently large odd prime q. Equations (10.5)-(10.6) give a fixed finite nonnegative mean-one kernel W with

\[
 t_{I,J}(W)t_{I,J}(W^{\mathsf T})<1.                            \tag{10.7}
\]

The limiting coefficients do not depend on the prime's congruence class because c_0 already canceled in (9.1). The order of choices is D, theta, integer scores and T, epsilon, and finally q. No simultaneous D,q limit or unbounded number of coordinates is used.

All atom probabilities and kernel entries are rational: the priors, thinning, activation laws, and epsilon were rational; matrix variables are uniform on finite sets; the signed rank-layer probabilities are ratios of finite integers.

## 11. Symmetrization and ordinary finite simple hosts

Let the two finite probability spaces of W be X and Y. On Omega=X times Y with product probability, define

\[
 V((x,y),(x',y'))=W(x,y')W(x',y).
\]

V is nonnegative and symmetric, and E V=(E W)^2=1. In its H-homomorphism product, factors using x_i for points and y_j for faces involve variables disjoint from the factors using y_i for points and x_j for faces. Therefore

\[
 t(H,V)=t_{I,J}(W)t_{I,J}(W^{\mathsf T})<1.
\]

Let L=max V, so 1<=L<infinity. Set U=V/L and mu=E U=1/L>0. Homogeneity gives

\[
 0\le U\le1,\qquad t(H,U)<\mu^k.                              \tag{11.1}
\]

The finite probability space and U remain rational. This proves the finite-kernel assertion of the theorem.

For completeness, the passage to ordinary finite simple graphs counts **all** source maps, not just embeddings. Put tau=t(H,U), Delta=mu^k-tau>0, and choose an integer N with

\[
 N>\frac{\binom v2+k\mu^k}{\Delta}.                            \tag{11.2}
\]

Sample N labels independently from Omega. Given the labels, independently put an edge on each unordered pair of distinct host vertices with its U-probability; put no loops. For the resulting random simple graph G_N,

\[
 \mathbb E p(G_N)=(1-1/N)\mu.
\]

Each injective map from V(H) to these N host vertices has homomorphism probability tau, since its source edges correspond to distinct host pairs. The labels themselves need not be distinct; independent labels are exactly what tau averages. Among all N^v source maps, the fraction identifying any two source vertices is at most binom(v,2)/N. Each of their true homomorphism indicators lies in [0,1], even if host edges repeat, and an identified source edge simply makes it zero. Hence

\[
 |\mathbb E t(H,G_N)-\tau|\le\binom v2/N.                       \tag{11.3}
\]

Using (11.2), the inequality (1-1/N)^k>=1-k/N, and convexity gives

\[
 \begin{split}
 \mathbb E t(H,G_N)
 &\le\mu^k-\Delta+\binom v2/N\\
 &<\mu^k-k\mu^k/N\\
 &\le((1-1/N)\mu)^k
   =(\mathbb E p(G_N))^k
   \le\mathbb E[p(G_N)^k].
 \end{split}
\]

Some realization therefore has t(H,G)<p(G)^k. Such a graph cannot be edgeless. This proves the theorem with the ordinary homomorphism-density convention requested in the question.

## 12. Application to candidate-13-49243

### 12.1 Data and independent checks

The candidate at R has the following faces, in the certificate's order:

```
012, 015, 023, 034, 045,
128, 156, 167, 178, (2,3,10),
289, (2,9,10), (3,4,12), (3,10,11), (3,11,12),
456, 467, (4,7,12), (7,8,12), (8,9,12),
(9,10,11), (9,11,12).
```

Three-digit strings here denote triples of single-digit point labels. The source JSON was read from its pinned commit. The companion script `independent_audit.py` contains a separate literal transcription of all faces, cycles, exposure orders, and rational weights; it does not import or execute repository code. Its checks use exact integers, fractions, finite sets, partition splitting, and breadth-first search.

All 22 triples are distinct, use exactly the points 0,...,12, and produce 33 edges each occurring twice. Every vertex link is a simple cycle. The point degrees are

\[
 (5,6,6,6,6,4,4,5,5,5,4,4,6).
\]

All 20 supplied cyclic orders are Hamiltonian cycles of this point graph. Each of the 40 supplied side orders has 11 distinct faces and covers all 13 points. At each of the 400 noninitial steps, exactly one point is new and the shared pair is a current boundary edge. The code verifies that the boundary stays a simple cycle after every attachment, that each pair of sides partitions all faces, and that both final boundaries agree with the supplied Hamiltonian cycle. Thus the sphere and exposure properties are independently checked, rather than inferred from a stored PASS string.

The cut weights have least common denominator 11544. In certificate order their numerators are

\[
\begin{split}
 &(257,264,148,1274,805,440,660,604,196,834,\\
 &\hspace{12mm}542,687,416,421,956,714,232,910,363,821).
\end{split}
\]

Every numerator is positive and their sum is 11544. Computing coverages both from the literal cycles and from the face-side separation gives exactly

\[
\begin{array}{c|c}
 e&a_e\\\hline
 \{0,5\},\{5,6\},\{6,7\},\{8,9\}&2/3\\
 \{10,11\}&1\\
 \text{all other 28 edges}&1/3.
\end{array}
\]

Thus the reduced coverage denominator is Q=3, total excess is 2, and strict first-cost savings are at least 1/6. The opaque stored `mask` values are not used by this audit; the explicit cycles, exposure orders, and reconstructed boundaries contain all required combinatorial information.

For every one of the 33 point edges, the audit verifies (9.7) directly. At every one of the 66 corners it also checks the two incident U-sets have intersection exactly that corner and that M has seven elements. The general proof above explains why these checks necessarily pass for this template, but the literal-data checks were done as well.

Starting with the two part colors, the numbers of point and face cells after each refinement round are

\[
 (1,1),\ (3,1),\ (3,7),\ (11,7),\ (11,22),\ (13,22).
\]

In round three, the only nonsingleton point cells are {5,6} and {10,11}. All faces are distinguished in round four, and both remaining point pairs split in round five. Thus refinement is discrete. The all-pairs dual distances give diameter ell=6.

These are exact finite computations, not floating-point evidence. The audit report retains the full partitions, all edge coverages, and every side's new-vertex sequence.

### 12.2 Quantitative corollary

For this graph, n=13, f=22, m=33, k=66, v=35, ell=6. The theorem's conservative parameters are

\[
 M_*=4{,}424{,}112,\qquad
 C_*=234{,}873{,}212{,}710{,}752,\qquad B=1749.
\]

For example, the even dimension

\[
 D=10{,}334{,}421{,}363{,}697{,}202
\]

satisfies every dimension condition in this proof. This is an existence bound, not a useful computational choice or a claimed minimum. With D fixed at this or any larger admissible even value, the rank-layer error is O_D(q^-1/6). The construction above consequently gives a finite rational kernel and a finite simple graph G with at least one edge for which

\[
 \boxed{\ t(H_{49243},G)<p(G)^{66}.\ }
\]

No classification/minimality premise is required for this corollary. The original graph in O has incidence-graph degree multiset 3^22 4^3 5^6 6^4; the new one has 3^22 4^4 5^4 6^5. These distinct degree multisets independently establish nonisomorphism, without relying on the classification JSON's isomorphism flag.

### 12.3 Verification status and remaining nonclaims

The proof is a complete conventional transfer argument from the stated combinatorial hypotheses. Every local analytic lemma used in it is proved above, including the individual-orbit lower bound, the cyclic lift-form image, restriction-sign concentration, and joint determinant-sign control. The tail argument uses only explicitly stated necessary integer constraints and includes a sufficient dimension choice. Thus this note does not make its conclusion conditional on the upstream rank-layer lemma or on an unproved realizability assertion.

The certificate was checked using the companion independent exact-arithmetic program. A separate, newly written symbolic script checks ten displayed polynomial identities used in the analytic bookkeeping; those identities support the transcription but do not substitute for the inequalities and counting proofs.

This is **not** proof-assistant verification. The source manuscripts and this proof remain subject to ordinary mathematical scrutiny. No particular prime q, complete finite kernel table, numerical final density gap, or concrete host adjacency matrix was computed. Their existence is proved, but the enormous dimension bound and unspecified asymptotic prefactors are not a practical witness algorithm as implemented here. No optimal dimension, new minimality theorem, or independent verification of plantri enumeration completeness is claimed. Only the two immutable commits listed at the start are used; no later changes are imported.

The pinned refinement explicitly stopped at a finite certificate for this alternative graph. The conclusion here rests on the transfer proof in this note and the new finite audit, not on reinterpreting that repository disclaimer as an analytic claim.
