# Exact certificates for the global residual energy theorem

The [theorem note](../../global-residual-dimension.md) proves the new energy and mode-removal implications relative to its explicitly retained geometric and transverse inputs. These finite certificates give the arithmetic bounds used in that proof:

| Template | Strict coordinate bound B | Integer M bound | Sufficient even D | Nondirect residual constant |
|---|---:|---:|---:|---:|
| Original | 609 | 608 | 7296 | 189 |
| Candidate 49243 | 638 | 637 | 7644 | 197 |

GPT-6 Pro supplied the discovery, proof, checker and certificates in research Task 9. Codex independently reviewed the conventional proof and the complete checker, then independently executed the unchanged supplied checker. This is independent replay of that checker, not a second implementation or proof-assistant verification. The original source authors retain credit for the construction and retained lemmas. No optimality or mathematical-priority claim is made.

## Run

From the repository root, using Python 3 with assertions enabled:

```sh
python3 -I -B experiments/global-residual-energy/check_global_residual.py
```

The program reads the two JSON files beside itself, uses only the standard library, prints deterministic text plus JSON, and writes no files. It refuses `-O` and `-OO`. It makes no network requests and executes no repository modules. The existing full enumeration runner is unchanged; this is a separate, small check.

For source-literal comparison as well, supply the existing candidate and a local copy of the exact OpenAI source pinned in [source-pins.json](source-pins.json):

```sh
python3 -I -B experiments/global-residual-energy/check_global_residual.py \
  --candidate-source experiments/order-13-cuts/candidate-13-49243.json \
  --complex-source /path/to/pinned/complex.tex
```

The optional files are parsed as data. They are not imported or executed.

## Evidence

- [template_data.json](template_data.json): literal faces, original bit cuts, and candidate cycles/weights. The canonical replay compared these with both pinned repository sources.
- [certificates.json](certificates.json): two 33-by-33 integer inverse certificates and strict coordinate bounds. The checker reconstructs the matrix from the faces and coverages before testing it.
- [check_global_residual.py](check_global_residual.py): unchanged reviewed GPT-6 Pro checker; SHA256 `89d506983eaf7ad0d81fcf92d7c00df3a49b408e72545dd976a1d406de57ec31`.
- [expected-output.txt](expected-output.txt): all 1,164 bytes matched the canonical replay.
- [verification.json](verification.json): measured resources, exact mutation definitions, source comparisons and resume evidence.
- [Finite receipt](verification/R2-T09-global-residual-v1.receipt.json), [inverse-entry mutation receipt](verification/CTRL-R2-T09-adjugate-v1.receipt.json), and [strict-bound mutation receipt](verification/CTRL-R2-T09-bound-v1.receipt.json): exact content-addressed canonical records.

The legitimate job passed in 0.114 seconds orchestration wall time, with 27,082,752 bytes peak RSS. Adding one to an original-template diagonal inverse-certificate entry failed the inverse identity. Replacing the original bound B=609 with B=1 failed the strict coordinate test before the M/D metadata checks. Both controls changed only the stated semantic field. Resume reused all three durable receipts without a second execution attempt.

The checker verifies finite combinatorics, exact polynomial identities, matrix multiplication and integer inequalities. It does not prove inequality-domain arguments, common-mode equality classification, retained geometric lemmas, or the transverse theorem. Its printed phrase “all-D proof certificates” refers to finite symbolic identities supporting the separate conventional proof. The artifact supplies no complete effective negative witness, numerical transverse prefactor, particular prime, kernel table, host, new minimum theorem, or global novelty determination.
