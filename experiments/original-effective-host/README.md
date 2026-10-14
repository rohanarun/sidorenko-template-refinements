# An effective finite host for the original Sidorenko pattern

For the exact original incidence graph $H$ with 13 points, 22 faces and 66 incidences, set

```text
B = 7866423844799423288734694969
N = 2^B
```

The [full conventional proof](recovered/PROOF.md) gives a nonempty simple graph $G$ on exactly $N$ vertices with

$$
\left(\frac{2|E(G)|}{N^2}\right)^{66}
-\frac{\operatorname{hom}(H,G)}{N^{35}}\ge\frac{1024}{N}>0.
$$

Every edge-preserving map is counted, including all repetitions. The deterministic graph-space search tests at most `2^(N*(N-1)/2)` labeled graphs and accepts the first satisfying

```text
(2*edge_count)^66 - hom(H,G)*N^97 >= 1024*N^131.
```

The proof also gives the actual rational kernel, a bounded prime search and an exact label-and-coin generator. At `D=7296`, for every odd prime above the literal threshold `Q_0` in the proof, the kernel has mean `q^-372672384` and deficit at least `2^-53303404092753966 * q^-24596377344`. Its atom/coin denominators, both orientations, collision loss and fixed-order arithmetic are explicit.

This quantifies the original pattern's existing counterexample construction. It reuses the global energy route credited to GPT-6 Pro in [PR4](https://github.com/rohanarun/sidorenko-template-refinements/pull/4), and supplies the complete geometric, transverse, pinning and finite-host chain. The [current repository comparison](review/novelty-and-campaign.md) explains the difference from PR4's retained-input dimension theorem, PR5's overlap correction and PR6's separate 17-vertex pattern. Global novelty, priority and optimal parameters are unestablished.

## Proof, evidence and the unused refinement

The frozen [recovered manuscript](recovered/PROOF.md) is 1,573 lines, SHA256 `20c917f8fbab9cc51a92d0a4c853ca2080541a9a15c116bd3343150993aaf031`. All 13 recovered files are retained byte-for-byte, including their internal manifest. Execution statements in those files describe the original research run; this portable replay and draft publication are recorded separately. The [18-component independent dependency review](review/dependency-review.md) and [machine-readable ledger](review/dependency-ledger-18.json) review every universal interface, including individual ordered orbits, correlated planted lifts, every repeated type map, source-realizable whole-law thinning, both orientations and all-map finite sampling.

The conventional proof uses the separate all-family nondirect bound `2^63 * q^(-D+1196)`. It does **not** use the merged proof's pattern-specific division by full basis multiplicity, or require the sharper `189`, `28` or `33` bounds. [Proof §7.5](recovered/PROOF.md#75-the-refinement-obstruction-and-why-it-is-not-used) isolates that inference obstruction and states summation before division as its repair. The independent checker reproduces an actual source-template family over `F_13`; this is an inference counterexample, not a refutation of every suitably repaired sharper bound. Acceptance of this effectiveness theorem does not certify those separate refinements.

Finite replay is distinct from the mathematical proof: small-field cases and exact data/identities support the conventional arguments. They do not establish all-dimensional lemmas or exhaust every type map by finite sampling.

## Reproduce the independent small checks

Python 3.9 or newer and its standard library suffice for this independent replay. From the repository root:

```sh
python3 -I -B experiments/original-effective-host/verify_package.py
```

The command verifies package hashes, the 12 internal recovered-manifest entries, all ten complete pinned source blobs, and the 18-component ledger. It runs only the three independently written small checkers in an isolated temporary copy and compares every resulting JSON value with the [fixed expectations](evidence/). Keep assertions enabled; optimized Python is rejected. No network or installation is needed.

The independent cases include all 64,000 ordered Lagrangian triples in a small symplectic space, 1,728 actual planted triples, 2,184 correlated subspace triples, 6,552 pair lift exact sequences, 1,680 signed center counts, all activation moments, the reconstructed rational inverse and mutation control, score checks with repetitions, symbolic parameter arithmetic and all-map tiny-host checks. The 10,032 small integer-domain cases are stress checks; the universal inequality signs are justified by the written domain proof.

The recovered `check_certificate.py` and `generator.py` are retained as inspectable reference artifacts and their historical replay records are preserved. This independent publication replay does not invoke them. Their optional small replay requires Python 3.10 or newer, as [their README](recovered/README.md) states. Never invoke the reference generator's full-run option on an actual runtime. Mathematical termination uses arbitrary finite binary strings; no present hardware feasibility is asserted.

## Attribution and limits

The fixed graph, activation kernels and analytic architecture belong to the original OpenAI manuscript at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. The refinement authors retain credit for the finite-template and residual work at `d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d`. GPT-6 Pro receives the earlier global-energy credit recorded in PR4. The recovered manuscript and its original small programs came from user-directed AI research. Codex independently reviewed the conventional dependencies, wrote the three additional exact checkers, and prepared this portable contribution. This is **AI-generated and AI-reviewed research**; independent human acceptance is not claimed.

The [source pins](recovered/source-pins.json), [complete source authentication](upstream-authentication.json), [publication provenance](verification/publication-provenance.json) and [source notice](upstream/NOTICE.md) record attribution and byte identity. The unchanged OpenAI snapshots retain their [Apache 2.0 license](upstream/OpenAI-LICENSE.txt). Checker changes for publication are only package-relative input/output paths and are recorded by both source and publication hashes.

The enormous prime, theorem-sized field, complete kernel, host and exhaustive generator were never materialized or executed. Small fields `F_3` and `F_13` were instantiated only for the stated checks. The new quantitative result has no Lean certification; neither the comparator's `sorry` stub nor an axiom allowlist supplies its proof. No claim is made for a smaller pattern, candidate 49243, a compact host, a practical search, mathematical priority or unrelated arithmetic complexity.
