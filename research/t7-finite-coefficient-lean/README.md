# T7 finite coefficient bound — Lean verification supplement

This packet formalizes **source §6, formula (5)**: strict negativity of the source's finite type-averaged, thinned, all-nonempty coefficient. It contains the same 37 proof modules reviewed by Opus 5.5 at xhigh effort, plus a separately identified correction to one arithmetic control and portable replay scripts.

The headline must be read together with its proved source constant:

```lean
T7Weighted.source_weighted_negativity :
  0 < T7Weighted.eta ∧
  T7Gap.averagedCoefficient < -T7Weighted.eta

T7Weighted.eta_source :
  T7Weighted.eta = (1/T7Gap.beta^8314) /
    (2^60 *
      (2/T7Gap.beta^333 + 2/T7Gap.beta^592 +
       2/T7Gap.beta^925 + 1/T7Gap.beta^1332)^7 *
      (8/T7Gap.beta^3 + 2/T7Gap.beta^5)^10)
```

Here `beta = 2^564`. The first theorem has no hypotheses. `averagedCoefficient` is the finite expectation defined by the source's normalized point/face priors and one Bernoulli thinning trial per source corner of the full all-nonempty labeling sum. It is **not claimed here to be a kernel-density coefficient**.

**Publication scope:** a Lean formalization and verification supplement for this finite bound. The mathematics is attributed to the pinned source theorem. No kernel-density deficit, non-Sidorenko graph, finite counterexample, minimality or priority claim is made. The later RL transfer and ongoing symmetric/host extension are excluded, including from the review attribution.

## Offline replay

Unzip anywhere writable. From this packet's root, run:

```sh
python3 replay.py --lean-bin /path/to/existing/lean-4.33.0/bin
```

Requirements are Python 3 and the existing pinned Lean 4.33.0 + Std toolchain. No mathlib, network access, package manager, installation or author workspace is used. This is **path portability**, with the exact audited arm64 macOS toolchain pinned by hash; cross-platform binary compatibility is not claimed. The script fails if the toolchain differs and never invokes elan to provision one.

Replay verifies the delivery manifest, all reviewed proof pins, all 105 source-packet files and all 17,466 toolchain files. It deletes only the packet's own build output, rebuilds every module with `lean -t 0`, audits all project-owned declarations, runs dependency checks and four original corruption controls, then verifies the paired publication claim and new beta-margin controls. Logs and machine-readable receipts are retained in `evidence/` and `formal/logs/`.

The reviewed core contains **312 authored theorems, 37 modules and 1,187 audited declarations**. The only permitted transitive axioms are `propext`, `Classical.choice`, `Quot.sound`. The four added beta-budget lemmas are separately compiled and audited; they are not represented as Opus-reviewed proof additions.

To test a delivered archive from a newly extracted directory:

```sh
python3 scripts/fresh_replay.py --archive ../t7-finite-coefficient-publication.zip --lean-bin /path/to/existing/lean-4.33.0/bin --receipt ../fresh-replay.json
```

## Review and control correction

Opus found no mathematical or formal defect in the finite headline. Its work was a **static source review**, not an executed Lean audit. The separate independent audit performed the fresh kernel build. Their roles and limitations are kept distinct in `review/`.

The independent audit's historical `InsufficientBeta` attempt did not reduce to true or false. This packet records it as **inconclusive**, not a successful rejection. `controls/BetaMargin.lean` now proves the exact budgets at exponents 564 and 563, and proves that the latter exceeds, and differs from, the required `2^-60` threshold. This establishes a limitation of that crude proof budget only; it does not disprove the coefficient theorem with a different beta.

See `CLAIM.md` for the complete publication claim, `REVIEW-RESPONSE.md` for each addressed item, `TRUST.md` for the evidence boundary, and `evidence/replay-receipt.json` for the new replay result. `MANIFEST.json` and `SHA256SUMS` bind the exact deliverable bytes.
