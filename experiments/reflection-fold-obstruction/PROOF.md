# Exact score features and an obstruction for equatorial reflection doubles

This note concerns the literal seven/six-coordinate activation law in
`openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, `kernel.tex`.
It proves a finite, source-specific obstruction. It supplies no new graph
violating Sidorenko's inequality and proves no general rank-layer estimate.

Let Gamma be a finite simple simplicial triangulation of the sphere with
point set I, face set J, n>=5 points, f=2n-4 triangular faces, m=3n-6 point
edges and k=3f=2m corners. H is its point-face incidence graph. Write K for
the set of corners (i,j), i in j. For a point edge e={i,i'}, with its two
incident faces j,j', put

    U_e = {(i,j),(i',j),(i,j'),(i',j')}.

At a corner a, let e,e' be the two face edges through its point and set
M_a=U_e union U_e', D_a=U_e symmetric_difference U_e'. Then |M_a|=7,
|D_a|=6, and M_a minus D_a={a}. Choose exactly one negative target corner,
with sigma_a=-1 there and +1 elsewhere.

The source law chooses M_a or D_a with probability 1/2 each. Conditional
on that support its sign vector has law

    2^-7 (1 + (sigma_a/2) product_{gamma in D_a} xi_gamma), on M_a;
    2^-6 (1 - (sigma_a/2) product_{gamma in D_a} xi_gamma), on D_a.

A nonincident type pair has empty activation. This note chooses the specialization theta=1/2 of the source family,
which permits every 0<theta<1. This specialization is used throughout. For a label alpha subset K, let phi_alpha be its
signed activation indicator. If Q=alpha union beta and R=alpha
symmetric_difference beta, its exact two-label moment is

    A_a(alpha,beta)
      = (1/2) [Q subset M_a] ([R=empty] + (sigma_a/2)[R=D_a])
        + (1/2) [Q subset D_a] ([R=empty] - (sigma_a/2)[R=D_a]).       (1)

Every nonempty first moment is zero. For nonempty alpha,beta the only
nonzero cases are: alpha=beta subset D_a, value 1; alpha=beta containing a
and contained in M_a, value 1/2; or alpha intersection beta={a}, union M_a,
value sigma_a/4. In particular disjoint nonempty labels have zero moment.

## All maps and exactly realizable features

For every pair of maps h=(a:I->I,b:J->J), including maps with repetitions,
define the complete coefficient

    C(h) = sum_{alpha_e nonempty, e a point edge}
             product_{(i,j) in K} A_{a(i),b(j)}(alpha_e,alpha_e'),      (2)

where e,e' are the two edges of j through i. A map taking an incidence to
a nonincidence has coefficient zero. No injectivity assumption is imposed.

Use positive common independent point and face priors pi_s,nu_t, and
positive pair thinning probabilities lambda_st<=1. Thinning mixes the
whole law with empty activation. Every all-nonempty term therefore gets
one lambda factor per source incidence, including repeated target pairs.
It does not get one factor per distinct pair or per active coordinate.

For positive variables X_s,Y_t,Z_st, realize these probabilities by
pi_s=X_s/sum X, nu_t=Y_t/sum Y, lambda_st=Z_st/Zmax. The permitted feature
vector is Phi(h)=(u_s,v_t,w_st), where u counts point-type preimages, v
counts face-type preimages, and w counts source incidences mapped to each
target type pair. Thus

    P(X,Y,Z)=sum_h C(h) X^u(h) Y^v(h) Z^w(h),
    t0=P/[(sum X)^n (sum Y)^f Zmax^k].                              (3)

The normalization lambda_st=Z_st/Zmax has maximum thinning one. For any
admitted positive thinning probabilities, put Lmax=max lambda_st and
lambda_prime_st=lambda_st/Lmax. Every all-nonempty coefficient has degree k
in the thinning factors, so t0(lambda)=Lmax^k t0(lambda_prime), and the
right side of (6) scales by the same factor. The transpose has the same
homogeneity. Thus the normalized representation loses no admitted case.

These features are from common priors and pair thinning only. They supply
no source-vertex-specific bonus or correlated assignment prior. In
particular assignments in the same feature fiber cannot be separated.

## The only negative feature is the automorphism feature

Let G be the part-preserving incidence automorphism group, g=|G|, and
c=4^-k. Every negative nonzero summand in (2) belongs to an automorphism;
at each automorphism the unique summand is -c. Consequently the aggregated
coefficient at Phi(id) is -gc and all other aggregated coefficients are
nonnegative. Here is the proof, including the repeated-map case.

The local support identity is

    intersection_{a in U_e} M_a=U_e,
    U_e subset M_a iff a in U_e.                                  (4)

At a corner in face {i,u,v}, M contains that face's three corners and
the i,u endpoint corners across {i,u} and i,v endpoint corners across
{i,v}. A complete four-set U can fit only across one of these two edges.
This gives (4); the two other endpoint sets intersect only at i.

On a source face, the XOR of the three comparisons of its edge labels is
zero. The three distinct nonzero D-vectors of any target face have exactly
one nonempty F2 relation: their sum is zero. Thus off-diagonal comparisons
on a nonzero source face occur either zero times, twice at the same target
corner, or once at each of its three target corners. An odd total number
of negative factors forces at least one face of the third kind. There its
point map is bijective, and the intersection/union conditions in (1) force
the three labels to be exactly the corresponding U-edge sets. Coordinates
outside the face are forced into their respective single edge label by
the two union conditions and excluded from the other two.

If an edge has label U_e, (4) and (1) force the next edge at any adjacent
corner to have either that label or the other U-label through the target
corner. The medial graph of a triangulated sphere is connected, so every source edge gets a target
edge label. The resulting point/edge/face maps send each barycentric flag
triangle to a target flag triangle without collapsing its three kinds.

The mod-two sum of source flag triangles has zero boundary. Its image
therefore has zero boundary. On the strongly connected closed target flag pseudomanifold,
the coefficient of a mod-two 2-cycle is constant across all triangles.
At the distinguished target corner, a diagonal comparison contributes two
flags to the same target triangle; an off-diagonal comparison contributes
one to each. A negative term makes the common parity odd. Source and
target each have 6f flag triangles, so every target triangle has exactly
one preimage. Every target point and face occurs in a flag, making both
maps surjective. Their cardinalities agree, hence both maps are bijective
and preserve incidence: h is an automorphism.

At identity, (4) gives alpha_e subset U_e. Adjacent nonempty labels must
meet, and the two U-sets at each corner meet only at that corner. All four
corners of each U_e are thus forced into alpha_e. The unique labeling is
alpha_e=U_e and its product is -4^-k. Source reindexing gives the same
unique coefficient at every automorphism. This reindexes summation
variables, without assuming the target law preserves the negative corner.

The identity feature has all point and face multiplicities one. Its fiber
therefore consists of bijective maps; its pair-incidence counts force
incidence preservation, so the fiber is exactly G. Every other fiber
contains only nonnegative summands. This proves the asserted sign pattern.

## A precise leading-face criterion

Aggregate coefficients by Phi and remove only fibers with complete
coefficient zero. Let S+ be the positive-coefficient features and let
Q be the convex hull of S+ together with Phi(id). Let Fmin be the smallest
face of Q containing Phi(id), allowing Q itself. There exist integer
scores s with P(T^s)<0 for every sufficiently large T if and only if

    sum_{phi in Fmin intersect S+} d_phi < gc.                      (5)

Indeed the top supported score layer is an exposed face. Its coefficient
must be negative for eventual negativity. If its coefficient vanishes,
the sole negative feature has been canceled there and every lower layer
is nonnegative. Every negative face contains Phi(id), hence contains
Fmin; adding any other support contributes positively. Rational exposing
directions of this rational polytope can be cleared to integer scores.

The complete coefficients are computable in a finite rational search:
for edge e intersect the four M-sets at its mapped corners, then enumerate
its nonempty subsets and the full products (1). Each edge domain has at
most 127 labels. This is a termination statement, with no efficiency
claim. At the chosen specialization theta=1/2, 4^k C(h) is integral and |C(h)|<=127^m.
For an exposed negative face of sum -A, outside terms have an integer
score gap at least one. The choice T=2+ceil(2 n^n f^f 127^m/A) makes
their total absolute remainder less than A/2.

Criterion (5) concerns eventual negativity along a fixed score direction.
It does not decide negativity at an arbitrary moderate base: for example
2X^2-8X+7 has positive exposed-vertex coefficients and positive full-face
sum, but is negative at X=2. The exact finite-base question remains
whether P has a negative value on the positive orthant. The obstruction
below rules that out on its specified class.

## Equatorial doubles obstruct every positive score choice

Suppose Gamma is the union of two triangulated disks, intersecting exactly
in their common boundary cycle C. An involutory simplicial automorphism r
fixes C pointwise and interchanges the disks. These are the equatorial
reflection doubles considered here. The folds F+ and F- identify the two
disks onto the plus and minus disk respectively. They are noninjective
incidence endomorphisms and preserve stable refinement colors: each
vertex is mapped either to itself or to its r-partner.

For every positive choice of the common priors and thinning factors,

    t0 >= 63 sum_{(s,t) incident} pi_s^n nu_t^f lambda_st^k > 0.     (6)

The full transposed nonempty coefficient is also nonnegative.

First, condition on boundary point types and boundary nonempty edge
labels. Sum the plus half's internal point types, face types and edge
labels, including their priors and all local factors, to obtain F. Source
reindexing by r makes the minus half's sum the identical F. Common
independent priors give

    t0=sum_{boundary types} product pi
          sum_{boundary labels} F^2 >=0.                          (7)

Interchanging the two target type sets proves the transposed version.
The negative target corner stays fixed; no target-law reflection symmetry
is required. Correlated or source-dependent priors would not give (7).

For the stronger strict bound, put phi+=Phi(F+), phi-=Phi(F-),
phi*=Phi(id). Counting preimages gives phi++phi-=2phi*. Boundary point
types occur once in both folds; interior types, face types and incidence
types have complementary multiplicities two and zero. A canonical fold
labeling uses U of each folded edge. Every comparison is off-diagonal,
every target corner in the image half occurs twice, and its product is +c.

The stabilizer of each fold under source precomposition is exactly
{id,r}. If F+ composed with gamma equals F+, gamma fixes C pointwise and
sends each interior point p into {p,r(p)}. It sends a face to itself or
its reflected mate. Two adjacent faces in one disk cannot choose different
sides: their interior shared edge contains an interior point p, whose image
would then belong to both disks and hence C. That is impossible for either
p or r(p). The dual graph of a triangulated disk is connected, so one side
choice holds throughout the disk. For a face and its reflected mate, their
gamma-images lie in the same two-element fold fiber; injectivity on faces
forces the two images to be different. Thus the other disk makes the
complementary side choice. Vertices are determined by their incident faces
in a simplicial sphere, so the complete map is id or r. A disk has no
interior edge joining two boundary vertices: reflection would make that
edge belong to the intersection outside C. The excluded one-triangle
double is not a simple simplicial sphere.

Each fold source orbit therefore has g/2 distinct maps. Their features
are unchanged by source precomposition. Each fold fiber has coefficient
at least gc/2, since all its other terms are nonnegative. If M+,M-,M*
are the corresponding positive monomials, their midpoint relation gives
M+M-=M*^2. Consequently

    P >= (gc/2)(M++M--2M*)
      = (gc/2)(sqrt(M+)-sqrt(M-))^2 >=0.                           (8)

For every incident constant map to (s,t), assigning the same nonempty
subset of D_st to every edge gives 63 terms of value one. That map is
not an automorphism, so no negative terms occur. Its feature is distinct
from the three features in (8); in particular the fold has the boundary's
at least three point types. Retaining these constant monomials in (8)
and dividing by the common normalization (3) proves (6).

Thus neither a leading score layer nor any positive real
weights can make t0 negative on this class. Zero weights can give boundary
equalities; the strict claim uses positive weights.

## Relation to the analytic construction and exact examples

If the separately supplied rank-layer limit applies to Gamma at a fixed
even D and to both difference orientations, the source expansion has
oriented limits 1+t0 and 1+t1. Diluting the point side by any fixed
0<epsilon<=1 gives 1+epsilon^n t0 and 1+epsilon^f t1. By (6)--(7) their
product is strictly above one. The crossed-product kernel therefore has
the wrong limiting direction for this Sidorenko witness. Uniform errors
tending to zero preserve that strict direction for sufficiently large q.
This implication retains the rank-layer limit as an explicit premise.
It makes no assertion about all kernels on H or unrelated finite-q laws.

For ring size ell, use points 0,...,ell-1 and apices ell,ell+1, with faces
{apex,i,i+1} (indices modulo ell). Reflection exchanges the apices. Insert
the two apices into two distinct ring edges of a ring Hamiltonian cycle,
using all ell(ell-1) ordered choices with equal weight. Rim coverage is
(ell-2)/ell and spoke coverage 2/ell. Both are at least 1/3 for ell=3,4,5,6.
They are obstruction examples, with no favorable sphere search performed.

The supplied own replay checks only the newly uncovered ell=5,6 examples;
completed earlier small geometry checks were preserved. The ell=3,4 checks
are not supplied in this package. It verifies
20 and 24 automorphisms, fold orbit sizes 10 and 12, the complete feature
midpoint, every rational coverage and the signed canonical single terms.
It does not present a fold's one positive term as its full coefficient.

The incident constant coefficient has a second exact description. On
nonempty labels the local moment matrix has 63 singleton blocks of value
one and 32 blocks [[1/2,sigma/4],[sigma/4,1/2]]. The connected medial graph
is four-regular, so every spin cut has even size. Hence

    C(constant)=63+32*2^-k sum_{spin assignments on edges} 2^-cut.    (9)

The own Gray-code enumeration of all 32,768 and 262,144 spins gives
respectively 1108307726537083/17592186044416 and
1134907106239454873/18014398509481984. These finite checks support the
fixed examples. The universal arguments above establish the theorem;
neither a whole type polynomial nor a field, kernel or host was enumerated.

## Provenance and limits

The activation and its signed-rank construction belong to the pinned
OpenAI/math manuscript. The template and Hamiltonian-cut framework belong
to `rohanarun/sidorenko-template-refinements@d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d`.
Earlier Artus/ChatGPT Pro/Codex campaign work supplied the sign-rigidity,
orbit-transfer and reflection ideas. The publicly available orbit-transfer
lineage is credited in [Sidorenko PR6](https://github.com/rohanarun/sidorenko-template-refinements/pull/6);
that is source credit, without claiming its positive seven-point example
proves this reflection obstruction. This addendum gives their exact feature and strict
all-score formulation, with retained analytic scope. Source reindexing,
elementary convex-face separation, squares and AM/GM are credited as
methods rather than claimed as inventions. No worldwide priority claim is
made. Substantial OpenAI Codex and ChatGPT Pro assistance is disclosed.

No new Lean proof, practical large construction, complete sphere
classification, reduced pattern, or result for an altered prior interface
is claimed. Independent AI review is not independent human peer review.
