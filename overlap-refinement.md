# Overlaps come only from defect vectors: residual constant 28

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

So vectors of type (1,1,1) and (0,0,0) create no overlap anywhere, and a
defect vector creates overlap only at later pairs through the point whose
span it raised. In the direct case the lemma gives pi = 0 for first vectors
and pi <= 1 for second vectors, recovering the exact exponent -m.

For the fixed pair order obtained from the point sequence
2,1,4,3,0,9,11,10,7,6,12,8,5 (each pair taken at the later of its points),
the remainder is bounded by a function of the per-point counts T_a of
earlier defect raises at points that still have unprocessed pairs, the
previous vector's g, and the defect so far; local dimensions are relaxed to
the number of earlier vectors at the point, and the global span before a
type (0,1,1) vector to its position minus ceil(d/2). At most five points are
open at any time, so an exact dynamic program maximizes the bound over all
type sequences. `audit_overlap.py` does this for every defect up to 38 in
about 45 seconds with at most 2.2 million states. The maxima are

    d:  1    2   3    4    5    6    7    8    9   10   11   12
    R: -11  38  54  101  116  163  177  222  235  280  292  335

and the ratio R/d peaks at **28** at d = 10, decreasing afterwards. For
d > 38 the averaging bound of the previous note, with the global span before
a type (0,1,1) vector at most 2m - n_1 - n_2, gives
R <= 178 + 23 n_1 / 2 + (67 - n_1 - n_2) n_2, whose ratio stays below 28.
An integer program keeping the exact local-dimension accounting returned the
same maxima for every defect tried up to 26.

Hence R <= 28 d for every nondirect stratum, this one residual contribution
is O_D(q^(-D+28)), and it vanishes for even D >= 30. The defect-one strata
alone contribute O_D(q^(-D-11)). The earlier residue and transverse
thresholds of the full construction remain required.

Reproduce with standard-library Python:

```sh
python3 -B audit_overlap.py --output build/overlap-audit.json
```

Create `build/` first if it does not exist. Saved expected results are in
`experiments/overlap-expected.json`. This finite check supplements the
proof and does not independently establish the upstream analytic theorem.
