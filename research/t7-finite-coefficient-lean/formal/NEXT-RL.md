# Exact remaining RL-to-density obligation

The completed new theorem proves `0 < eta` and `averagedCoefficient < -eta` for the actual finite type expectation. It supplies source §6's negativity. It does **not** yet identify this coefficient with a limit of `constructedKernel.density`.

## Next finite connecting identity

Fix an actual type map `g=(a,b)`. At each of the thirty source corners c, independently draw o_c from `thinnedActivationLaw (a (corner c).1) (b (corner c).2)`. Its first Boolean is the entire-law thinning trial; its remaining data choose M/D and all thirty signs. Define

- A(c,gamma) to be that thinning Boolean AND target incidence AND membership of gamma in the chosen active M/D set;
- xi(c,gamma) to be the sign bit of o_c at gamma, interpreted as +1 or -1;
- U_e to be the unchanged literal four-corner support of source point edge e.

The finite expression to formalize and prove is

```math
P(g)=\mathbb E_{(o_c)_c}
 \prod_{\gamma\in\mathcal K}\prod_{e\in E(\Gamma)}
 \left(1+\prod_{c\in U_e}\mathbf1_{A(c,\gamma)}\xi(c,\gamma)\right)
 =1+\operatorname{thinnedCoefficient}(a,b).
```

This is a precise finite algebra/probability identity, not a density deficit assumption. It requires:

1. Expanding the two finite products into **all** assignments of coordinate masks to the fifteen point edges, including empty masks.
2. Reordering each expanded product by source corner, using the actual support-incidence identities; independence of the thirty activation draws then gives the product of `thinnedMoment` factors.
3. Proving zero first moments from the actual law and propagating the empty/nonempty status of labels across the literal face/edge incidence structure. A surviving labeling is either all empty, giving 1, or all nonempty, giving the existing `thinnedCoefficient`.
4. Averaging the identity over the unchanged point/face type laws. The result would be `E_g P(g)=1+averagedCoefficient`.

The current project has the moment formula, actual Bernoulli thinning, general non-incidence vanishing, finite independence/Fubini tools and full all-nonempty coefficient. It does **not** yet contain this all-mask expansion theorem. In particular `averagedCoefficient_negative` must not be relabeled as a density theorem.

## Precise analytic premise still to encode

For the source rank-layer instantiation, fix even D>=12 and let q tend through odd primes. Construct the uniform space S_D(q) of symmetric D-by-D matrices, quotient-form rank signs, the positive rational layer probabilities pi_xi(q), and the normalized kernels K_xi. Prove their nonnegativity, mean one and the required uniform-difference identities.

The explicitly unproved RL premise is exactly: for each activity mask A and sign assignment xi on the thirty source corners,

```math
\mathbb E_{X_i,Y_j\ {m independent\ uniform}}
 \prod_{c=(i,j)\in A}K_{\xi_c}(X_i-Y_j)
\longrightarrow
 \prod_{e:U_e\subseteq A}\left(1+\prod_{c\in U_e}\xi_c\right),
```

uniformly over the finite activity/sign choices, with the reverse-difference assertion as well. It is not replaced by the desired graph-density limit or a positive deficit hypothesis. No Lean constant currently states RL, and no custom axiom supplies it.

Given this precise premise, the remaining transfer proof must justify the finite row/column product-space reindexing for all thirty matrix coordinates and all seventeen source vertices; apply RL coordinate by coordinate under all independent activation/type draws; pass the finite sums/products through the limit; and use the finite identity above to conclude

```math
\operatorname{constructedKernel}(K_q).density\longrightarrow
1+\operatorname{averagedCoefficient}.
```

The reversed orientation and actual point-side dilution construction/estimates must then be connected to the existing symmetric-product density theorem to obtain a symmetric deficit at a sufficiently large odd prime. Exact prime choice/existence and the bounded rational scaling must be included. The source's unpublished generic proof of RL is a separate analytic project.

## Sampling stays open

Even after an actual symmetric bounded kernel deficit is established, the random simple host distribution still must be constructed from iid atom labels and independent unordered-edge trials. Its exact expected edge-density identity and 136/N collision estimate are unproved. The existing baseline `finite_host_conditional` is a reusable extraction result whose sampling and deficit premises have not been supplied by this extension.

## Tooling boundary

There is no missing prerequisite for the completed finite proof. Lean 4.33.0 and its pinned Std library suffice. A usable local mathlib checkout is absent; cached `.ltar` files do not constitute one. The copied provisioning request gives the exact bundle requirements and the locally evidenced, incompatible v4.21.0 alternative. The next finite expansion can be developed in the current tools; finite-field matrices and analytic limits would be more practical with a separately provisioned compatible mathlib bundle. These open proofs are mathematical development obligations, not failures solved merely by installing a package.
