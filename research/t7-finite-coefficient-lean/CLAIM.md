# Publication claim and source correspondence

In Lean 4.33.0, using core and Std, we prove without hypotheses that the source's finite expectation t₀ satisfies

```
t₀ < -η < 0,
β = 2^564,
Z_I = 2/β^333 + 2/β^592 + 2/β^925 + 1/β^1332,
Z_J = 8/β^3 + 2/β^5,
η = (1/β^8314)/(2^60 Z_I^7 Z_J^10).
```

The Lean statements are `T7Weighted.source_weighted_negativity` **together with** `T7Weighted.eta_source`. Their complete source is `formal/T7Weighted/SourceConstants.lean`; the publication replay prints both statements and both axiom reports. The underlying `beta` definition is in `T7Gap.Priors`.

Here t₀ is exactly `T7Gap.averagedCoefficient`: the expectation over seven independent normalized point-type draws and ten independent normalized face-type draws of `thinnedCoefficient`. That coefficient sums over every assignment of a nonempty subset of the thirty corners to each of the fifteen point edges. Its local moments are derived from actual normalized activation laws. Thinning is one Bernoulli trial for the whole source corner, not separate trials for its coordinates. Repeated target types do not merge source draws, and noninjective maps are included.

This is a formalization of the finite bound in `formal/inputs/theorem.md`, §6, formula (5), whose SHA-256 is `a4996ac29fdc54e31f7ebb25bffe233fe4f4caa164d557ad9e7dd7fbd89fb960`. The mathematical construction and argument belong to that source. The added formal contribution connects its actual prior/thinning expectation to the score-weighted finite sum, proves the score classification and tail bound, and closes the strict negative margin.

The literal incidence graph has seven point vertices and ten face vertices with thirty incidence edges. The formal development also checks the stable-map classification and signed orbit coefficient on which the weighted bound depends. Those facts do not by themselves certify this graph as a non-Sidorenko counterexample.

## Proof route

1. The actual source score is at most 5066 for every point/face map, including repeated images. Equality is classified by the stable cells.
2. Non-incidence terms among the maximum-score maps vanish. The remaining identity and reversal terms sum to `-2^-59`.
3. The complete coefficient is bounded in magnitude by `2^450`; the number of type maps is `7^7*10^10 < 2^54`; lower-score relative weights are at most `1/β`.
4. The concrete remainder lies strictly between `-2^-60` and `2^-60` at `β=2^564`.
5. Every actual prior/thinning weight is proved equal to its score-relative weight times the common positive scale. The actual expectation is therefore below `-η`, and `eta_source` identifies the displayed source constant.

No negative coefficient, remainder bound, score classification or positive margin is assumed in the headline.

## Claims outside this packet

This packet does not establish the all-mask parity-to-density identity, the finite-field rank-layer model, analytic RL, a kernel-density deficit, symmetric dilution/reversal, prime choice or a sampled finite host. Some later work addresses parts of that route; none is included here or attributed to this Opus review.

No claim of first proof, smallest counterexample, priority, or completed 35/66-to-17/30 reduction is made. A bounded comparison statement is possible only against the frozen comparison files: the review found no Lean formalization of this finite bound there. It is not a search of the current literature or public record.
