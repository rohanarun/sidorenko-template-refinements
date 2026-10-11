# Progress on the residual-counting constant

The quantity tracked is the even dimension $D$ that suffices for the one
nondirect residual counting step in OpenAI's Sidorenko construction
(Lemma "Costs for the remaining profiles"). Lower is better. Only this
step is lowered; the other dimension thresholds in the proof are unchanged.

The table below is the current record. The existing `charts/progress.png` and
`charts/progress.svg` are historical PR #3 assets displaying the uncorrected
even-dimension claim 30, so they are not displayed as current evidence. See
[chart provenance](charts/README.md).

| Date | Source | Remainder | Even $D$ sufficient | Method |
|---|---|---:|---:|---|
| 2026-09-23 | OpenAI preprint, pinned commit `fd4aeeb` | 1641 | 1642 | all 33 pairs, free two-spaces in the global span |
| 2026-10-09 | this repository, initial draft | 1032 | 1034 | 28 allowed pairs, greedy/convex local caps |
| 2026-10-09 | this repository, PR #1 | 978 | 980 | active vertex supports |
| 2026-10-10 | this repository, PR #2 | 189 | 190 | sequential basis count with orthogonality |
| 2026-10-10 | corrected PR #3 proposal | 33 | 34 | full-support overlap DP through defect 26, support completion, and a separate averaging tail |

The old full-support DP still reports ratio 28 and defect-one maximum -11.
The support-uniform correction gives 33 and defect-one upper bound 17. These
are different scopes, not revised values in the same expected-output table.
External adversarial review of the correction remains pending.

Generate corrected `charts/support33-progress.png` and `.svg` with
`python3 charts/make_progress_chart.py` (requires matplotlib; not part of the
certificate runner). These corrected images were not generated for this
integration; matplotlib was unavailable. No installation was performed.

## Corrected draft for PR #3 (external review pending)

> The Sidorenko residual count now has a proposed support-uniform constant 33.
> The full 28-pair DP reports 28, but its `-2m` cost means that number does not
> automatically transfer to smaller active supports.
>
> Insert two nondefect vectors at each missing pair. Every old contribution
> stays the same or increases, and each inserted pair loses at most one after
> its pair cost. This gives R <= M_d + 28. A fresh, hash-pinned Python replay
> verifies the needed full-support maxima for defects 1 through 26; a separate
> averaging proof covers every larger defect. The resulting bound is R <= 33d,
> with defect-one bound 17.
>
> 1642 → 1034 → 980 → 190 → 34 (even D for this residual step only). The original
> cap-38 DP output and CI workflow are preserved, but were not freshly rerun
> for this correction. Other analytic thresholds remain required. This is an
> AI-generated correction with Codex, awaiting external adversarial review;
> it does not establish a smaller counterexample or claim optimality.
> github.com/rohanarun/sidorenko-template-refinements

## Tweet draft for PR #2 (explain-like-I'm-25)

> OpenAI's Sidorenko counterexample has one counting step that needed the
> ambient dimension D to be above 1641. We just cut that constant to 189.
>
> The trick: the paper counts each "pair space" as a free 2-dim subspace of
> the global span, then pays for containing it in a Lagrangian. But the
> paper's own direct-sum case already does something smarter: place basis
> vectors one at a time, and each new vector must be symplectically
> orthogonal to everything already at either endpoint. Run that same count
> for the non-direct case, track per vector whether it's new globally and
> new at each endpoint, and the containment cross terms cancel exactly.
> What's left is the overlap of two endpoint spans, which averages to
> Σ deg² − 3m + 11 = 189 on the 28-pair graph.
>
> 1642 → 1034 → 980 → 190 (even D for this one step). Exhaustive audit over
> 55,173 strata agrees; CI reruns it. Scope: one step of one proof, not a
> smaller counterexample. Chart + proof + code:
> github.com/rohanarun/sidorenko-template-refinements
