# Optional bounded replay for the support-uniform 33 correction

This experiment supplements Proposition `prop:residual-33` in
[proof.tex](../../proof.tex) and the [overlap report](../../overlap-refinement.md).
It is not part of `run_checks.py` and does not change the original full-support
DP, expected output, or CI workflow.

The proof uses three separate ingredients: completion of missing pairs gives
`R <= M_d + 28`; exact full-support DP maxima through defect 26 give
`M_d + 28 <= 33d`; a conventional support-uniform averaging proof covers every
`d >= 27`. This yields the proposed support-uniform bound 33 and defect-one
upper bound 17, hence even dimension 34 for this residual step only. The
retained analytic hypotheses and other dimension thresholds remain required.
External adversarial review is pending; no novelty, optimality, or formal
verification is claimed.

## Source and authorship

All original files are pinned to PR #3 head
`9aecdfbd987ecda60b7c5e0b382849d67c6bbc2f` of
`rohanarun/sidorenko-template-refinements`. The original draft, its model-derived
DP, and upstream construction retain their existing attribution. The support
completion correction, bounded driver, and integration are explicitly
AI-generated with Codex, not an official OpenAI publication.

The four files beside this README are unchanged copies of the reviewed driver,
original DP, original finite baseline, and original expected output. Deliberate
duplication makes the historical driver's relative paths portable without
changing a single reviewed byte. The driver checks source/data hashes before
and after execution, admits only cap 5 or 26, and emits one JSON result. Its
historical docstring says review was pending when authored; both source and
driver were reviewed and explicitly approved before the recorded runs, as the
review records explain. No new DP execution occurred during this integration.

`overlap-expected.json` is the original full-support cap-38 table. Its
`refined_constant: "28"` and defect-one maximum -11 are not support-uniform
claims. Only the prefix through 26 was freshly replayed for this correction.
The driver explicitly returns `support_uniform_claim_verified_by_this_run:
false`, because completion, tail, and analytic counting are separate proofs.

## Optional fresh reproduction

Read the source and verify the accompanying SHA256SUMS first. From this
experiment directory, `shasum -a 256 -c SHA256SUMS` checks the pinned bytes.
Then, from the repository root, with standard-library Python and assertions
active:

```sh
python3 -B experiments/support33/overlap-cap-driver.py 5
python3 -B experiments/support33/overlap-cap-driver.py 26
```

These commands emit their results on stdout and do not resume an interrupted
invocation. In the original durable campaign each cap was one completed unit;
interrupted units restarted, while completed units were reused by immutable
input/source pins. The exact campaign manifests, inputs, outputs, checkpoints,
and runtime sources are retained below as historical evidence. Their original
workspace paths are not portable runner configuration; the direct commands
above are the portable entry points.

The measured cap-5 run took 0.0294 worker seconds and 24,870,912 bytes peak RSS.
The cap-26 run took 10.5822 worker seconds and 732,233,728 bytes peak RSS, with
913,968 retained states. The original cap-26 budget was 120 CPU seconds,
180 wall seconds, and a 2 GiB memory estimate (not an enforced memory sandbox).
Actual resource use may differ on another host. Neither the full cap-38 audit
nor the whole repository workflow was freshly run for this correction.

## Exact evidence

- [Cap-5 result](evidence/cap5-result.json), [receipt](evidence/cap5-receipt.json),
  and [job manifest](evidence/cap5/manifest.json).
- [Cap-26 result](evidence/cap26-result.json), [receipt](evidence/cap26-receipt.json),
  and [job manifest](evidence/cap26/manifest.json).
- [Runner audit](evidence/runner-audit.json),
  [parallel static review](evidence/parallel-static-review.txt), and
  [root static review](evidence/root-static-review.txt).
- [Live-coordinate clarification](evidence/live-coordinate-clarification.txt):
  six coordinates can persist after a first-vector forgetting step. This
  supersedes the historical reviews' suggestion that only a transient opening
  qualification was needed; the frozen reviews remain unchanged.
- [Evidence index](evidence-index.json) lists exact hashes and canonical receipt
  identifiers. `evidence/cap5/` and `evidence/cap26/` retain the exact historical
  specs, input payloads (including embedded source bytes), stdout, empty stderr,
  registration, checkpoint, result, and receipt. `evidence/runtime/` contains
  the exact runner, worker, and adapter sources referenced by those manifests.

The mathematical claim follows conditionally from the reviewed conventional
arguments plus finite arithmetic; the receipts themselves certify only their
stated bounded computations. These copies are evidence records, not new runs.
