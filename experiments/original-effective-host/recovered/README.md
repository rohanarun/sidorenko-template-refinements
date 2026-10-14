# Effective original-pattern Sidorenko certificate

## Completed theorem

Let H be the exact 35-vertex, 66-edge incidence graph of the 22 faces in `template.json`. All homomorphisms, including noninjective maps, are counted. Set

```
B = 7866423844799423288734694969
N = 2^B
```

The conventional proof in `PROOF.md` establishes a finite nonempty simple graph G on exactly N vertices with

```
p(G)^66 - hom(H,G)/N^35 >= 1024/N > 0,
p(G) = 2*edge_count(G)/N^2.
```

The deterministic graph-space generator returns the first graph satisfying

```
(2*edge_count)^66 - hom(H,G)*N^97 >= 1024*N^131.
```

It requires at most `2^(N*(N-1)/2)` graph tests. The proof also gives a deterministic source-kernel label-and-coin generator, described in `SOURCE_GENERATOR.md`, with a fully numerical termination bound. The existence/termination conclusion is derived from explicit finite-field estimates, rational pinning, both orientations, scaling and finite sampling; it is not an assumed finite-host theorem.

These orders are mathematical bounds, not practical resource estimates. No full-size prime, field, kernel or host was constructed. Even N's binary representation would need B+1 bits. The Python reference implementation defaults to symbolic output. Do not attempt the guarded full-size run on a real machine.

## Replay

Python 3.10 or newer and its standard library are sufficient. No installation, network access, or execution of upstream repository programs is needed.

```sh
python3 check_certificate.py
python3 generator.py --self-test
python3 generator.py
```

The first command independently reconstructs the finite template, exact inverse, rational margins, activation moments, color scores and constants, then compares them with `certificate.json`. Its universal domain assertions remain mathematical proofs in `PROOF.md`; a passed finite check is not represented as a proof-assistant certificate. The inverse mutation test checks rejection of a corrupted entry.

The supplied replay records 389 upload-manifest checks, six exposure orders, 1,089 inverse entries, 33 coordinate margins, 4,628 finite activation identities and 16 rational polynomial identities. A separate small geometric check over F_13 validates the refinement multiplicity obstruction. Generator tests compare all maps on eight small hosts and verify that the original H has exactly two homomorphisms into K2, both necessarily noninjective.

Optional input checks, not prerequisites for the mathematical result:

```sh
python3 check_certificate.py --archive '/path/public-research-sources-20261011(3).zip'
python3 check_certificate.py --complex-source /path/complex.tex \
    --comparator-source /path/SidorenkoCounterexample.lean
```

The upload check was run. The optional upstream source-byte comparisons were not run; those flags require independently supplied full files matching the pinned Git blobs. The default package has the reconstructed literal certificate and source metadata, not materialized copies of all upstream source bytes.

## File guide

`PROOF.md` contains the full proof, parameterized kernel theorem, fixed-order host theorem, all-domain energy argument, both orientation errors, rational cloning, collision and diagonal bounds, proof of the bounded prime search, source attribution and acceptance boundary.

`certificate.json` contains the complete 33-by-33 integer inverse certificate, all vertex and pair scores, all thinning exponents, and exact parameter arithmetic. `template.json` contains the original faces, bits, auxiliary pairs, incidences and six exposure orders.

`check_certificate.py` is the newly written exact arithmetic checker. `generator.py` contains the all-map homomorphism counter, acceptance predicate, small tests and guarded exhaustive reference generator. `SOURCE_GENERATOR.md` specifies the alternate deterministic generator following the finite source-kernel sampling construction itself.

`replay.json`, `generator-tests.json` and `generator-spec.json` record the actual small checks and symbolic output. `source-pins.json` and `dependency-ledger.json` distinguish source data, proved components, finite checks and nondependencies. `SHA256SUMS` checks the package bytes, not the truth of mathematical claims.

## Attribution and precise boundary

The graph, activation construction and source proof architecture are from `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, Family 161. The inspected refinement draft is `rohanarun/sidorenko-template-refinements@d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d`. Two recovered predecessor documents proposed the quantitative composition and energy route; they were treated as untrusted evidence and their programs were not executed. No novelty or priority claim is made.

The uploaded archive contained no Sidorenko files; the ten required public source files were recovered read-only at the immutable pins. All are named in `source-pins.json`. The comparator is a challenge stub with `sorry`; its adjacent JSON maps the real solution module. Neither that stub nor an axiom allowlist is a proof input. The full Lean solution closure was not audited or compiled.

The former residual-classification condition is discharged by the all-integer argument at D=7296. No separate research hypothesis about rank layers, pinning negativity, moment identities or finite-host existence is retained in the completed conventional proof. This is not a Lean-checked theorem. The result makes no claim for smaller templates, candidate 49243, optimal parameters, a compact host or a practical search. It makes no Family 109 multitape bit-complexity or Family 130 exact-arithmetic RAM claim.
