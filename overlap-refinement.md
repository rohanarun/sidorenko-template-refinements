# Defect overlaps and the support-uniform residual constant 33

October 10, 2026. This additional research draft sharpens the sequential
basis count of `sequential-refinement.md`, retaining its upstream
dependencies.

That count writes the nondirect remainder as

    R = -2m + sum over non-defect vectors of pi(x) + defect terms,

where pi(x) = dim(V'_i cap V'_j) is the overlap of the two endpoint spans
when the basis vector x of the pair {i,j} is placed, and it bounded pi by the
smaller endpoint span. The overlap is in fact controlled by the defect
alone. Write tau_a(y) = l_a(y) - g(y) for a vector y at a pair through the
point a; tau_a(y) = 1 exactly when y lies in the earlier global span but
not in the earlier span at a, and the defect is d = sum of all tau.

**Lemma.** For a basis vector x of the pair {i,j}, let F be the earlier
pairs sharing a point with {i,j}. Then

    pi(x) <= sum over vectors y of pairs in F of tau_{a(y)}(y)
             + [x is the second vector] (eps(u) + g(u)),

where a(y) is the shared point and u is the first vector of the pair.

*Proof.* No earlier pair contains both i and j, so F = F_i + F_j and
dim V'_i = sum over F_i of l_i(y). The globally new vectors (g = 1) are
linearly independent, and those of pairs in F lie in V'_i + V'_j, so
dim(V'_i + V'_j) >= #{y in F : g(y) = 1}. Subtracting gives the bound for
the first vector; the second vector adds u to both spans, which raises the
two dimensions by l_i(u) + l_j(u) and the sum by at least g(u).

So vectors of type (1,1,1) and (0,0,0) create no overlap at later pairs, and a
defect vector creates overlap only at later pairs through the point whose
span it raised. In the direct case the lemma gives pi = 0 for first vectors
and pi <= 1 for second vectors, recovering the exact exponent -m.

## What the original DP computes

The fixed order of the full allowed graph comes from the point sequence
2,1,4,3,0,9,11,10,7,6,12,8,5, taking each pair at its later endpoint.
The remainder is relaxed using the per-point counts T_a of earlier defect
raises, the previous vector's g, and the accumulated defect. Local dimensions
are bounded by the number of earlier vectors at each point, and the global
span before a type (0,1,1) vector by its position minus ceil(d/2).
The implementation can retain **six** live coordinates, including after some
forgetting steps; the original claim of at most five was incorrect.

`audit_overlap.py` and `experiments/overlap-expected.json` are preserved
byte-for-byte. Their original cap-38 output is a full-support computation,
with `refined_constant: "28"` and defect-one maximum -11. Those fields do not
assert a maximum over all active pair subsets. A fresh bounded replay for
this correction covers only defects 1 through 26, obtaining

    d:  1    2   3    4    5    6    7    8    9   10   11   12   13
   M_d:-11  38  54  101  116  163  177  222  235  280  292  335  346
    d: 14   15   16   17   18   19   20   21   22   23   24   25   26
   M_d:389  399  441  450  491  499  538  545  583  589  626  631  668

Every value matches the saved prefix. The cap-26 run took 10.5822 worker
seconds and peaked at 732,233,728 bytes RSS and 913,968 retained states in
this local run. These are measurements, not performance guarantees. The
original cap-38 result and the full repository workflow were not freshly
replayed for this correction.

## The missing support comparison

Write B_E for the relaxed objective on an active set E of m pairs, including
its cost -2m. Order E by restriction of the full order. Insert two consecutive
nondefect type-(1,1,1) vectors at every missing pair. This completes a relaxed
type sequence; no geometric realization of the added vectors is asserted.

The inserted vectors do not change d or any old T_a. At every old vector the
endpoint counts and position only increase, while its earlier defect and the
first vector's g within its own pair stay fixed. Every old contribution
therefore stays the same or increases. For an inserted pair the first term
is nonnegative and the second is at least one; after the pair cost -2 the
pair loses at most one. Thus

    R <= B_E <= M_d + (28-m) <= M_d + 28.

The relaxed full-support DP drops realizability constraints, so it includes
the completed type sequences. Defect never decreases, so truncating at 26
loses no path ending with defect at most 26. The first five maxima plus 28
are 17,66,82,129,144, all at most 33d. For 6 <= d <= 26 the replay gives
M_d <= 28d, hence M_d + 28 <= 33d. In particular this argument gives
**defect-one bound 17**, not the original full-support value -11.

## A separate support-uniform tail

For d >= 27 use the averaging bound from `sequential-refinement.md`, with
n_1 one-defect vectors and n_2 two-defect vectors. On every active support,
the connected full graph bounds sum(deg_i^2)-3m by 178; missing edges may
first be added along paths from an existing edge, so their increments
2a+2b-1 are positive. Endpoint degrees are at most six, and
k <= 2m-n_1-n_2 <= 56-n_1-n_2. Thus

    R <= 178 + 23 n_1/2 + (67-n_1-n_2)n_2.

With t=n_2 and d=n_1+2n_2 this is
178 + 23d/2 + (44-d)t + t^2. Its maximum on 0 <= t <= floor(d/2)
is at an endpoint. At t=0 it is at most 33d for d >= 9. At the other
endpoint, for even d=2t >= 28 the required inequality is
t^2-t-178 >= 0, true for t >= 14; for odd d=2t+1 >= 27 it is
t^2 >= 313/2, true for t >= 13. Hence **R <= 33d** for every active
support and every d >= 1. This tail does not rely on the saved cap-38 run.

For the counting passage, sum the bounds on ordered vector lists over all
complete type patterns before dividing by the common lower bound on the
number of ordered bases of each pair-space family. The finite number of
patterns is absorbed into the fixed-D constant. With the retained source
gain and containment estimates this gives O_D(q^(-D+33)) for fixed even
D >= 34, with defect-one contribution O_D(q^(-D+17)). This is for the
residual step only; all other analytic thresholds remain required.

See Proposition `prop:residual-33` in [proof.tex](proof.tex). External
adversarial review remains pending. No optimality of 33, falsity of a
support-uniform 28, new counterexample, or mathematical priority is claimed.
The original draft and upstream authorship are preserved; the completion
correction and this integration are explicitly AI-generated with Codex.

## Evidence and optional reproduction

The [optional standard-library experiment](experiments/support33/README.md)
contains the unchanged, hash-pinned bounded driver, exact source/data copies,
and the cap-5 and cap-26 receipts and outputs. The finite replay alone does
not prove the support-uniform theorem: the completion, tail, and retained
analytic arguments are separate obligations.

The original `run_checks.py` still runs the unchanged cap-38 audit and
compares its original expected output. Its full-support semantics are
preserved; that workflow is not the fresh bounded evidence for this
correction. No whole-repository or CI execution was performed for this
integration.
