# T7 actual weighted coefficient negativity

This isolated extension proves the next missing connection from the completed gap-repair: **the actual type-averaged stochastic coefficient is strictly negative**, with the explicit positive source margin. Neither negativity nor a remainder estimate is assumed.

The headline theorem is:

```lean
T7Weighted.source_weighted_negativity :
  0 < T7Weighted.eta ∧ T7Gap.averagedCoefficient < -T7Weighted.eta
```

Here `T7Gap.averagedCoefficient` is the unchanged prior project's actual expectation over independent point and face type draws, whose local moments come from the actual normalized activation and thinning laws. `eta_source` proves the margin equals the source's printed rational expression, including its exact prior normalizers.

**RL-to-density transfer and finite-host sampling remain unproved.** This package does not prove an actual kernel-density deficit or the full non-Sidorenko theorem. See [NEXT-RL.md](NEXT-RL.md) for the exact remaining finite identity and analytic obligations.

## Reproduce offline

```sh
cd /Users/artus/LocalData/Codex-LYTiQ/2026-10-11/task-5/t7-weighted-extension
export T7_LEAN_BIN=/Users/artus/.elan/toolchains/leanprover--lean4---v4.33.0/bin
python3 scripts/verify_manifest.py --include-evidence
python3 scripts/build_offline.py
python3 scripts/review_dependencies.py
python3 scripts/negative_controls.py
```

The full build verifies the pinned toolchain, packet inputs, original baseline proof files and all copied gap-repair proof files. It rebuilds everything into a fresh local directory with `lean -t 0` and `LEAN_PATH` restricted to that directory. No predecessor compiled files are used by the reference build. Every authored theorem's statement and axioms are printed; every declaration owned by any project module, including generated/private declarations, receives an axiom and type/proof-body dependency audit.

The verified build contains **312 authored theorems (85 new) in 37 modules**, and audits **1187 declarations**.

The only allowed axioms are `propext`, `Classical.choice`, `Quot.sound`. Proof source holes, custom axioms, unsafe declarations and `native_decide` are rejected. Python orchestrates compilation and evidence checks; it is not the proof engine.

## New proof chain

1. `sourceScore_eq_score` identifies the score with exactly the source prior and pair exponents. `score_max_iff` proves the maximum 5066 is attained precisely by stable-colour maps. Identity and reversal attain it.
2. `generalCoefficient_bounds` derives a uniform bound of `2^450` from actual feature values, normalized expectations, finite products and the number of labels.
3. The complete type-map enumeration is proved exhaustive, duplicate-free and of size `7^7*10^10 < 2^54`. Non-orbit maximum-score terms vanish by the previously proved stable-map classification and non-incidence vanishing. Every lower-score weight is at most `1/beta`.
4. `finiteRemainder_two_sided` proves the concrete remainder lies strictly between `-2^-60` and `2^-60`. `normalizedWeightedSum_negative` combines this with the proved orbit coefficient `-2^-59`.
5. `exponentCost_gap` and `actual_weight_relative` identify every actual prior/thinning weight with the score-normalized weight times one common positive factor. `averagedCoefficient_normalized` proves the actual expectation is exactly that factor times the normalized sum.
6. `averagedCoefficient_negative` and `source_weighted_negativity` establish the actual negative average and positive explicit margin. `pointNormalizer_source`, `faceNormalizer_source` and `eta_source` prove the source's displayed constants, rather than leaving their correspondence to inspection.

The original `t7-gap-repair` project and archive are preserved for independent audit. `PARENT.json` pins that archive and all 26 copied proof modules. The publication packet and original `t7-formal` baseline are also unchanged.

Evidence: [coverage ledger](COVERAGE.md), [build receipt](logs/rebuild/build-receipt.json), [theorem statements](logs/rebuild/theorem-statements.log), [axiom audit](logs/rebuild/axioms.json), [all declarations](logs/rebuild/declaration-audit.json), and [proof dependency checks](logs/correspondence-review.json).

No external interactions or installations occurred. There are no missing prerequisites for this Std-only build. The copied [mathlib provisioning request](provisioning/request.json) remains a possible aid to the future matrix/limit development; installing it would not by itself prove the open mathematical obligations.
