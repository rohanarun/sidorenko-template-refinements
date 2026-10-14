# Exact proof coverage and assumptions

## Completed connecting theorem

```lean
T7Weighted.source_weighted_negativity :
  0 < T7Weighted.eta ∧ T7Gap.averagedCoefficient < -T7Weighted.eta
```

This theorem has **no hypotheses**. Its probability spaces, activation laws, priors, thinning probabilities, scores and finite sums are instantiated by the source data. In particular neither coefficient negativity, a positive deficit, nor a finite remainder bound is assumed.

`averagedCoefficient` is the unchanged actual finite expectation from the completed gap-repair. It samples seven point types and ten face types independently from `pointPrior` and `facePrior`, and averages `thinnedCoefficient`; the latter uses actual thinned activation-law moment expectations. The complete dependency audit checks the path from the new theorem through that definition and the activation moment/formula bridge.

`eta_source` establishes exactly

```math
\eta=\frac{\beta^{-8314}}
{2^{60}(2\beta^{-333}+2\beta^{-592}+2\beta^{-925}+\beta^{-1332})^7
(8\beta^{-3}+2\beta^{-5})^{10}}>0,
\qquad\beta=2^{564}.
```

## Proven components

| Component | Proof and connection |
|---|---|
| Literal score | `sourceScore` is the sum of all actual point and face prior exponents plus thirty pair scores. `sourceScore_eq_score` proves the completed-square representation for every point/face map, including repeated images. |
| Score bound and exact maximizers | Each changed point degree costs at least 37; every face contribution is at most 7. When point degrees agree, the exact histogram defect is nonnegative and vanishes precisely for the literal face colour. `score_le_max` and `score_max_iff` prove the maximum is 5066 and characterize it by `StablePoints ∧ StableFaces`. |
| Non-vacuity | `score_identity` and `score_reversal` explicitly attain the maximum. The unchanged source activation laws are normalized; both prior normalizers and `averagedScale` are proved strictly positive. No maximum or weight family is an uninstantiated theorem parameter. |
| Actual coefficient bound | `pairFeature_values` puts each feature in {-1,0,1}. Positivity/normalization of the actual law bounds each moment in [-1,1]. Product and sum bounds then prove `-2^450 ≤ generalCoefficient a b ≤ 2^450`. |
| Exhaustive finite map count | `allTypeMaps` lists all pairs of functions, without injectivity restrictions. Completeness, no duplicates and exact length `7^7*10^10` are proved. Its rational count is strictly below `2^54`. The nonempty label count is bounded by `2^450`, symbolically. |
| Only two nonzero maximal terms | The existing stable-incidence classification gives identity or reversal. Every other stable map is a non-incidence map and its full coefficient vanishes. The existing actual orbit coefficient is -2^-59. |
| Finite remainder | `finiteRemainder` is the concrete full finite sum with only the identity/reversal terms removed. Lower-score terms have a relative weight at most `1/beta`. `finiteRemainder_two_sided` proves `-2^-60 < finiteRemainder < 2^-60`; there is no remainder hypothesis. |
| Normalized negativity | `normalizedWeightedSum_split` separates the two orbit terms from that exact remainder. `normalizedWeightedSum_negative` proves the full relative-score-weighted sum is below -2^-60. |
| Actual weights | `exponentCost` sums the nonnegative natural exponents in the real prior and thinning weights. `exponentCost_sourceScore` proves `cost+Q=13380`; `exponentCost_gap` gives `cost=8314+(5066-Q)`. Thus `actual_weight_relative` proves every original weight equals `averagedScale * relativeWeight`. |
| Actual expectation | `averagedCoefficient_raw_sum` flattens the original independent type expectation. `averagedCoefficient_normalized` proves its exact equality with the positive scale times the normalized weighted sum. This is the semantic connection that rules out an unrelated negative scalar surrogate. |
| Source constants | `pointNormalizer_source`, `faceNormalizer_source`, and `eta_source` prove the displayed source normalizers and margin. They are no longer only prose correspondence claims. |

## Assumptions, trust, and what is not proved

The eight new proof modules introduce no custom axioms. Intermediate generic sum/product lemmas have ordinary explicit finiteness, positivity or inequality premises, all discharged in the final closed theorem. Decidable equality of complete type maps uses the standard classical equality instance; it contributes only allowed standard logical axioms, not a computational oracle.

All authored theorem axiom closures and all project declarations are checked against exactly `propext`, `Classical.choice`, `Quot.sound`. The declaration audit selects by module ownership, including private generated declarations, and records type and proof-body dependencies separately. Numerical finite tables use `decide +kernel`. Large type and label sums are handled symbolically, not enumerated by Python or native compilation. The reference build uses `lean -t 0` for every imported/local module.

Python handles hashes, compiler orchestration, manifests and dependency checks. It is not mathematical proof evidence by itself. Statement/data correspondence is reviewed against pinned `inputs/publication/theorem.md`, specifically §§5–6, and now includes the proved score and normalization identities above.

The following remain **open**:

- the full-mask parity expansion and empty/nonempty propagation identity `P(g)=1+thinnedCoefficient(g)`;
- finite-field rank-layer instantiation and a precise formal RL premise;
- the conditional passage from that premise to the actual oriented kernel-density limits;
- actual dilution and sufficiently large odd-prime selection giving a symmetric kernel deficit;
- the random finite-host distribution and its mean/collision estimates.

The exact next identity, RL quantifiers, and dependency boundary are specified in [NEXT-RL.md](NEXT-RL.md). The existing generic `SignedBase` assumptions express only nonnegativity and mean one. They do not supply RL. The baseline host theorem still has unsupplied positive-deficit and sampling hypotheses. **No theorem here proves a kernel-density deficit or the full conditional RL-to-host/non-Sidorenko result.**

## Preservation and provenance

`PARENT.json` pins the completed gap-repair archive and all 26 copied proof modules. `BASELINE.json` separately pins the original baseline proofs. Both predecessor projects and archives remain unchanged, and all 105 publication-packet files retain their hashes. The reference build and fresh-directory replay use only the copies inside this isolated extension and the pinned installed Lean toolchain.

No missing build prerequisite, network call, download, installation, external agent/service contact, publication or scheduling operation is involved. Future analytic dependencies are separately documented in the copied provisioning request; unresolved proof obligations are not hidden behind a dependency request.
