# Verification and review boundaries

## What is proved

The finite headline and expanded constant are the unchanged Lean theorems
`T7Weighted.source_weighted_negativity` and `T7Weighted.eta_source`.
Their 37-module core contains 312 authored theorems and 1,187 owned declarations.
It uses Lean 4.33.0 and Std only. The proof has no hypotheses and does not assume
negative coefficients, score bounds, a remainder estimate or a positive eta.

The delivery pins the exact source theorem, literal data and all copied proof
files. `REVIEWED-PROOF-PINS.json` was checked against both the original weighted
extension and the frozen author files submitted to Opus. Publication edits did
not change those proof files.

## Distinct evidence routes

| Route | What happened | What it does not establish |
|---|---|---|
| Original author build | Fresh `lean -t 0` build, all-declaration axiom/dependency audit, four mutation failures and archive replay | Independent mathematical review |
| Independent weighted audit | Separate fresh 37-module trust-zero build, declaration/statement/source checks and targeted controls; retained report and receipts | Its historical stalled beta reduction was not a semantic rejection |
| Opus 5.5 xhigh | Static inspection and mathematical reasoning over the frozen finite coefficient packet; no defect found in Contribution B | It executed no Lean/checker commands and did not review the newer RL/host work or these packaging changes |
| This publication replay | Rebuilds the unchanged core, checks the paired headline and margin, reruns author controls, and verifies four new beta-budget lemmas  | A second independent review of the new wrapper code, new mathematics downstream, or publication to an external venue |

The new beta controls prove exact arithmetic about a conservative bound. At
exponent 563, the crude `2^54*(2^450/β)` budget equals `2^-59`, which is strictly
larger than `2^-60`. No inference is made that the finite coefficient itself
would fail to be negative at that different beta.

## Trusted components and proof categories

- The pinned Lean kernel, release libraries and OS execution are trusted. All
  17,466 toolchain files are hash-checked. This pins an arm64 macOS build, not an
  interchangeable platform release.
- Ordinary proofs and `decide +kernel` computations produce kernel-checked proof
  terms. No `native_decide`, custom axiom, proof hole or unsafe declaration is
  accepted in the formal core.
- The transitive axiom allowlist is exactly `propext`, `Classical.choice` and
  `Quot.sound`. Audits include private/generated declarations and both types
  and proof bodies. New control declarations are audited separately by their
  owning module.
- Python provides hashes, build orchestration and evidence classification. A
  Python PASS is not a Lean theorem. Original source checkers remain historical
  evidence, not trusted proof oracles.
- Semantic source correspondence remains a review boundary. Byte equality and
  kernel checking do not automatically identify a formal definition with an
  informal claim; the independent audit and Opus review address that question
  for the finite expectation and constants.

## Offline and portable means

No network, service, install, agent call, push, PR, submission or scheduling
operation is part of replay. All executable commands use Python or the explicitly
supplied existing Lean binary. Relative paths locate proof/source inputs. Some
historical reports and receipts retain original local paths as provenance; replay
does not require those paths to exist.

`MANIFEST.json` labels immutable inputs separately from generated replay outputs.
By default replay verifies immutable entries, so rerunning after logs are
regenerated remains possible. Use `--verify-evidence` on a fresh extraction to
verify archived log hashes too. `SHA256SUMS` records every delivered file except
itself. Build outputs are intentionally excluded from the ZIP and rebuilt.

This is a local publication-ready verification supplement, not a publication
submission. Its scope stops at source §6's finite rational coefficient bound.
