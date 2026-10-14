Independent adversarial review of the recovered Sidorenko certificate
2026-10-12; AI reviewer: Codex. Adapted for portable publication; no human or formal acceptance is claimed.

Verdict: ACCEPT Theorem (T) and the parameterized kernel/host statements as
conventional mathematical results for the literal original 35-vertex,
66-edge incidence graph. I found no additional research hypothesis or
missing implication in the reviewed dependency chain. This is a fresh
mathematical review, supported by independently written exact checkers;
it is not a proof-assistant certification or an execution of the theorem's
huge construction. No numerical correction to the main theorem is required.

The accepted fixed statement is: put
  B = 7866423844799423288734694969, N = 2^B.
There exists a nonempty simple graph G with exactly N vertices satisfying
  (2|E(G)|/N^2)^66 - hom(H,G)/N^35 >= 1024/N > 0,
where hom counts EVERY edge-preserving map, including repetitions.
The graph-space search with integer acceptance predicate
  (2|E(G)|)^66 - hom(H,G) N^97 >= 1024 N^131
terminates within 2^binom(N,2) graph tests in the mathematical model of
arbitrary finite binary strings and exact integer arithmetic. This says
nothing about a feasible run on the supplied Python runtime.

The accepted parameterized statement uses exactly PROOF.md (P), D=7296,
r=3648, Q_0=116736+J_q^6. For EVERY odd prime q>Q_0 the specified finite
rational kernel U is symmetric, 0<=U<=1, has mean q^-372672384, and satisfies
  (E U)^66 - t(H,U) >= 2^-53303404092753966 q^-24596377344.
For every integer n>=1322/Delta_q a nonempty simple host of order n has
deficit at least Delta_q/2. The bounded prime search and the fixed N then
give the displayed literal theorem. The prior review's conditional transfer
conclusion is strengthened here by reviewing its previously unaudited
universal premises, rather than assuming them from its finite checks.

Frozen evidence:
  Input: the recovered user-directed research artifact packet, frozen by the hashes below.
  ZIP SHA256:
    b9ef98c4e1d89a3531f075fe307eea2932c9673a92123135242e05d2f9e884e3
  PROOF.md SHA256 (1573 lines):
    20c917f8fbab9cc51a92d0a4c853ca2080541a9a15c116bd3343150993aaf031
  certificate.json SHA256:
    c69f0ce403e229ea81d72f1b6e3aab085b35cbe9ae7ca19941dba3895abb1302
The fresh ZIP extraction has 13 members; all 12 internal SHA256SUMS entries
pass. All 13 original input files still matched my snapshots at completion
of the checks. I read the prior task-3 review and the supplied programs as
evidence, and executed only my three new standard-library checkers.

Source fidelity is independently checked beyond the packet metadata.
I recovered all ten declared source files through read-only GitHub file
reads at the two immutable commits, saved copies in my own upstream/
directory, and recomputed all ten Git blob SHA-1 values from the complete
bytes. The authentication ledger records length, SHA256, blob SHA-1, commit
and path for each file. The graph's 22 faces, bits and six exposure orders
were parsed from the pinned complex.tex; its graph also matches the pinned
Lean comparator literally. The comparator's main is a sorry stub; its
adjacent JSON maps a separate solution module. Neither provides a premise
for accepting this new quantitative proof.

Pins:
  openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb
  rohanarun/sidorenko-template-refinements@
    d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d
Key blobs:
  complex.tex 178b0e9da21867a727ea847dae8e537b9d719a70
  kernel.tex bbe11be8fffe968012060ec43e6aff597e922831
  transverse.tex d4991976e630f117c8d85a7e22deb60643a2450d
  orbits.tex 7da7ee247b4be60c3baf545a2e0f78309a667ee0
  planted.tex e1a4636e66361dae0f5918e1245950060535a83c
  tail.tex dc11e07a592e70d3a13e3a005c72378c88edc351
  comparator 3f4fa1074f812e2e823350ea50ff1a786e4a1927
  refinement proof.tex 66fc5eb655e6471df0c266c986c0ab47d943fe0f

Complete dependency ledger (line references are to the frozen PROOF.md):

1. ACCEPT literal graph and exposure classes: lines 78-133, 1045-1107,
   1111-1117. All 33 pairs occur twice; the face and pair-coordinate graphs
   are connected; the six classes have their actual ten shared pairs as
   exposure-tree edges. The finite inverse and score data are rebuilt from
   those source literals, not from an assumed predecessor matrix.

2. ACCEPT elementary counts and chart comparison: lines 135-243.
   Quotienting by an isotropic subspace gives the containment formula;
   incidence counting gives L_n and the isotropic-subspace count. Symmetric
   rank layers are counted by image subspace and its nonsingular form.
   Schur complements give sign balance; the union over prospective radicals
   gives the nullity bound. With q>=16D, beta_D>=1/2 and pi/p_xi<=16 give
   2^299 for the 35 charts and 66 incidences. Nonnegativity permits this
   comparison even for an unbounded singular-tail integrand.

3. ACCEPT EVERY occurring individual ordered orbit: lines 245-295.
   Removing the common space leaves direct, mutually orthogonal pair spaces.
   A dual chosen inside the opposite Lagrangian forces an actual symplectic
   block splitting; it does not merely match dimensions. Repeating reduces
   the remaining invariant to a nonsingular symmetric-form congruence orbit.
   Orbit-stabilizer bounds that residual orbit below by 2^(-z-3).
   The three avoidance events are imposed separately, so conditional samples
   remain independent, with uniform reductions under quotient automorphisms.
   A transverse residual orbit forces exact pair intersections. The common
   and pair spaces are then unique, avoiding a multiplicity loss. The paid
   factors give 2^(-D-15) q^-C uniformly, including z=0 and zero pair spaces.

4. ACCEPT planted-center bound on the ENLARGED INTEGER domain: lines 297-432.
   The ratio is planted orbit mass divided by individual orbit mass, not a
   profile average. The quotient identity (3.4) fixes r'=r-u exactly.
   Common-zero reduced center subspaces imply the pair relation-space bound
   w>=0. The pair lift exact sequence gives t_i=nullity D_i. The cyclic
   difference image has precisely the single restriction relation on V;
   extensions of two forms agreeing on their intersection give sufficiency.
   Conditioning independent targets on that image costs q^b(v), explicitly
   included in (3.9). Thus no false independence of the three differences is
   used. Actual tuples satisfy every constraint in (3.1); discarded further
   realizability constraints only enlarge the maximum. Empty domains have
   zero planted contribution. Zero-, one- and two-active faces are included.
   Constants 2^32, the orbit denominator and (D+1)^5 choices give A_D exactly.

5. ACCEPT universal energy and all lower-activity faces: lines 434-593.
   I checked the source-gain/slack algebra and all four regional identities
   independently over rational unisolvent sets. The inequality signs also
   follow on the actual stated real domain: |delta|<=c, d>=P+T,
   T<=P+3delta, and w>=0 justify the replacements and the two bounds on a_*.
   For negative delta the d coefficient is nonnegative; for either sign the
   regional endpoints/chord terms are nonnegative. Lower-activity faces use
   the exact beta decomposition and the integer floor(h/2) formula.
   This review of the domain argument supplies the universal step; the small
   dimension sweep alone would not prove it.

6. ACCEPT anchored inverse/ellipsoid bound: lines 594-652.
   Connectedness plus positive excess anchors makes K positive definite.
   Completion of the square bounds each coordinate even when different
   coordinate extrema cannot be attained simultaneously. My exact inverse
   gives AN=tau I in all 1089 entries, tau=821810346672, and independently
   recovers both strict margins:
     327514878189744;
     419595924675382839454010976.
   Each upper bound is strictly below 609, hence integer M<=608. Altering one
   inverse entry violates five entries of AN and is detected by my check.

7. ACCEPT integer residual classification: lines 654-705.
   The common-mode identity and its two bracket lower bounds apply to the
   same enlarged domain used in the planted estimate. At D>=12M they give
   nonnegative slack. The c>=2 completed square is strictly positive; c=1
   equality forces all three pair dimensions one. Connected face adjacency
   would propagate this everywhere, where excess energy is 1, a contradiction.
   At c=0 integer n_i>=p_i>=0 gives only (p_i,t_i)=(0,0) or (1,1) as equality.
   Therefore every nonsaving integer profile has c=0, h in {0,2}, zero excess,
   zero slack and gain 2m. The fractional profile with p_i=t_i=1/2 has Delta
   =-7/4; it disproves a continuous replacement of this integer step, as the
   manuscript itself correctly states. It is not geometric dimension data.

8. ACCEPT transverse center counts: lines 707-822.
   Complementary half-rank images give the projection identity and the sign
   matching condition. The isotropic count includes both families. Given L,
   Q is conditioned exactly on Q and Q-L nonsingular; there is no additional
   conditional sign-independence assertion. For two distinct restrictions,
   conditional Schur complements are independent after the common block is
   fixed nonsingular. The singular-block probability is paid in the second
   moment. The matching indicator stays inside the error expectation. This
   yields the normalized factors 16*f and 4*f, and models 8 and 2 on matches.

9. ACCEPT JOINT determinant-sign estimate: lines 823-866.
   Condition first on the central lower-right minor; the neighbor difference
   minors are independent uniform. A union bound controls every nonzero
   linear combination of their inverses. Freeze the other variables only
   after establishing this good event: the central off-diagonal vector stays
   uniform. All nonzero joint frequencies have rank at least s+1, so the
   supplied differencing/Parseval argument gives the stated total variation.
   Every other selected edge-sign factor is fixed and bounded. Walsh inversion
   after paying for determinant zeros controls the entire 33-sign law.
   Marginal sign balance alone would have been insufficient; it is not used
   as a substitute here.

10. ACCEPT assembly and saving-profile tail: lines 868-909, 972-996.
    Telescoping uses the bounded transverse factors and expectation errors;
    the singular part uses the nonnegative chart comparison and the planted
    envelope. Six conditional exposure bounds can be geometrically averaged
    without independence between classes. Their shared-pair subtractions give
    exactly mathcal C. Since 6*Delta is integral, every positive saving is
    at least 1/6. The (D+1)^55 profile count and stated constant are valid.

11. ACCEPT direct/nondirect residual tail: lines 910-970.
    A minimal dependent family contains an endpoint missing an earlier edge;
    its local increment is full while the global one loses positive dimension.
    Thus sum k_i>=2k+1, including partial intersections. For direct families,
    neighbor orthogonality constraints are independent and ALL basis choices
    are counted before division. For nondirect families the proof instead
    counts actual spans and bounds actual-family weights before enlarging the
    count. No pattern-specific basis divisor is used. The caps m<=28, k<=55
    and sum binom(k_i,2)<=468 give -D+1196 with multiplier <2^63.
    Together these prove the uniform C_D q^-1/6 rank-layer estimate for every
    activity/sign pattern, at every even D>=7296 and q>=16D.

12. ACCEPT actual activation and identity negativity: lines 1034-1107.
    Both seven-/six-coordinate branch probabilities are strictly positive,
    normalized rational laws. My direct sign enumeration verifies every 254
    nonempty first moment and 4374 compatible union/difference moments for
    both sigma choices. Zero first moments and pair-coordinate connectedness
    exclude mixed empty/nonempty labels. Literal support intersections force
    alpha_e=U_e uniquely at identity; each corner contributes sigma/4 and the
    single negative corner gives -2^-132. This is an actual probability law,
    not an unsupported assigned moment table.

13. ACCEPT ALL type maps and source-realizable pinning: lines 1109-1221.
    Repeated types retain independent matrix draws, and repeated type pairs
    retain separate activation draws via product of expectations. At a first
    failed refinement round, the square identity uses only prior-color
    preservation; neither injectivity nor incidence preservation is assumed.
    The scores include all 286 type pairs, including nonincidences. Four-round
    discreteness and weights 1856^(4-t) give the integral all-map score gap.
    Whole-law thinning gives exactly ONE lambda per incidence in a nonempty
    term, hence the claimed T^E(f) weight from common independent priors.
    The bounds on all 13^13*22^22 maps and all label sums, with T=2^2459,
    give t_0<=-2^-Z. My reconstructed score arrays agree entry for entry.

14. ACCEPT reverse orientation and field threshold: lines 1223-1284.
    The diluted side has 13 vertices in the intended orientation and 22 in
    reverse. A nonempty term requires each to have an active old type; thus
    the exact powers are epsilon^13 and epsilon^22. The reverse coefficient
    needs only the absolute bound 2^2178. At the chosen even r, each signed
    layer is unchanged under negation. Matrix draws stay independent under
    every repeated type map in either direction. The per-coordinate estimate
    is uniform before averaging, so no type-map count multiplies field error.
    q>Q_0 gives floor(q^(1/6))>=J_q and orientation error <=alpha/64.
    The nonnegative limiting factors and the product error give (10.6).

15. ACCEPT symmetric kernel, scaling and exact rationalization: lines 1286-1368.
    The crossed-product factors use disjoint source variable families, so the
    mean is exactly 1 and t(H,V)=a_q b_q. Signed layer counts are positive;
    W uses at most seven coordinates, giving the stated q^14b(D) bound for V.
    Scaling on all 66 incidences gives exponent 924b(D), not an auxiliary-pair
    exponent. Cloning is an exact pushforward of product probability measures.
    Original-atom/clone diagonals are retained. The displayed atom and coin
    denominators are integers clearing every branch, prior, thinning and
    signed-layer denominator. My exponent arithmetic matches all size bounds.

16. ACCEPT finite simple-host transfer and all-map counter: lines 1371-1430.
    Distinct host vertices with equal labels use the kernel's actual diagonal
    and separate edge coins. An injective source map uses 66 distinct coins;
    noninjective source maps, including repeated image edges, are bounded by
    1 rather than falsely assigned independent trials. Their total proportion
    is at most 595/n. Jensen and deleted host loops cost at most 66/n, yielding
    Delta_q-661/n. Eliminating face assignments as common-neighbor counts is
    exact even when point or face images repeat. I checked tiny hosts by two
    distinct enumerations and recovered exactly two H->K2 homomorphisms.

17. ACCEPT bounded prime search and literal order: lines 1432-1498.
    The product-of-primes induction and central-binomial argument prove the
    stated large-input Bertrand interval. Q_0 already exceeds 2^16. Trial
    division therefore finds the first prime in its bounded candidate list.
    The exponent bounds on J_q, Q_0 and q are strict in the needed directions.
    Delta_q>2048/N leaves expected deficit >1387/N after the 661/N loss,
    exceeding 1024/N. Multiplying by N^132 gives precisely predicate (A).

18. ACCEPT scope and termination boundary: lines 1500-1573 and README.
    No proof depends on a passed predecessor program, the comparator stub,
    a Lean axiom allowlist, a retained residual-classification gate, or the
    refinement's sharper 189 remainder. Every new universal interface has a
    mathematical argument above. These checks establish no smaller pattern,
    compact host, practical generator, Lean proof, or unrelated complexity
    result. The supplied finite replay expects Python >=3.10, as README says.

REJECT the unused refinement's per-pattern basis-division inference as
written (upstream/proof-refinement.tex:298-309). This is already acknowledged
and bypassed in recovered PROOF.md:998-1032. My q=13,D=4 reconstruction gives
actual Lagrangians with source-pair intersections H_01=<e1,e2> and
H_17=<e1,e3>, every source-face common intersection zero, and the extra
shared line only on the nonedge {0,7}. It has k=3 and sum k_i=7. Each
two-space has 26208 bases, while only 1872 bases of the second have their
first vector on the shared line. That pattern contributes 49061376 bases
for ONE family, below both the full 686859264 bases and the claimed lower
divisor 7341576489/64. The displayed configuration extends to every even
D>=4 by the same coordinate formulas, so the inference obstruction also
applies at the refinement's stated even D>=190. The repair is to sum over
all complete basis patterns before dividing by full basis multiplicity.
I do not certify every part of the sharper numerical 189 claim. The accepted
main proof uses its separate valid 1196 estimate and does not need it.

Reproducible independent evidence (scripts in independent/; fixed expected outputs in evidence/):
  python3 independent/own_geometry_audit.py
    F_3: 40 Lagrangians, all 64000 ordered triples, 20 transvection-orbit
    components across 15 profiles; all 1728 planted triples; 2184 common-zero
    center-subspace triples checking the cyclic image rank; 6552 pair lift
    exact sequences; 210 translated transverse triples and 1680 signed
    center counts. Both residual form classes and repeated/equal spaces occur.
  python3 independent/own_data_audit.py
    Ten pinned full-file hashes; literal graph and six exposure trees;
    freshly reconstructed inverse, all margins, mutation detection;
    4374 overlap/254 first moments and all 66 signed corner moments;
    all score entries, 4000 square identities with repetitions, 5904
    adversarial constant/collision/random type maps, and exponent arithmetic;
    eight tiny hosts, original H->K2, and the geometric refinement obstruction.
  python3 independent/own_algebra_audit.py
    780 unisolvent evaluations covering ten quadratic polynomial identities;
    303 evaluations covering regional/chord and other identities;
    all 10032 enlarged integer tuples at even D=2,4,6,8,10 check the quadratic
    and local loss inequalities. Small-D negative local slack is permitted;
    the universal residual theorem separately uses D>=12M and integrality.

The evidence/expected-*-results.json and evidence/audited-*-run.log files record
these successful audit runs. verification/audit-input-authentication.json and
upstream-authentication.json bind the source bytes. verification/PACKAGE-SHA256SUMS
binds this portable publication package. verify_package.py repeats the small
checks and compares exact outputs in an isolated temporary copy.
The finite tests are targeted adversarial checks and exact data/algebra
certificates. None is represented as proving all-dimensional geometry or
enumerating all type maps by itself; the universal arguments in items 2-17
are the reason for mathematical acceptance.

Remaining boundary: no mathematical blocker to this precise theorem was
identified. The huge prime, field, complete kernel, host, and exhaustive
generator were NEVER instantiated or executed. The full Lean solution closure
was neither compiled nor audited. No supplied/archive/repository program was
executed. No author file, source mirror, pin, or PR branch was modified. Only own audit files were written during that review; source reads were read-only.
No installation, upload, publication, person-directed communication or spending
occurred during the original audit. Subsequent publication packaging is separately
authorized and does not change that audit execution boundary.
