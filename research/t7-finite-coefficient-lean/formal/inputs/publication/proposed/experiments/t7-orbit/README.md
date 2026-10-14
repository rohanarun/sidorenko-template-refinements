# Seven-point orbit-pinning witness and review evidence

The [theorem](../../t7-orbit-theorem.md) states an exact rank-layer-conditional implication for one 17-vertex, 30-edge bipartite graph. It separately states the proposed unconditional corollary obtained by accepting the complete supplied L3 analytic proof. This package makes that proof dependency available for review; it does not present an independently instantiated finite counterexample.

The graph is the point–face incidence graph of the sphere with faces `012,013,023,124,134,235,245,346,356,456`. Its stable refinement is not discrete. The relevant new condition is that every stable-color-preserving endomorphism is an automorphism; the only two are identity and reversal. The full orbit-pinning argument is in [Task 4](dependencies/task04-orbit-transfer-theorem.md), and the seven-point specialization is in [Task 11](dependencies/task11-response.md).

Read [DEPENDENCIES.txt](DEPENDENCIES.txt) and [the acceptance boundary](reviews/acceptance-boundary.txt) before interpreting a `PASS`. All reviews here are separate AI-agent reviews, not independent human acceptance or proof-assistant verification. The fresh T7 challenge checked the specialization and interfaces; the generic finite-field lemmas remain the complete L3 source and its earlier analytic reviews.

The [exact draft review](reviews/exact-draft-review.txt) is additive to the historical acceptance-boundary report. The [positive-class screen](reviews/positive-class-screen/REVIEW.md) examines several immediate positive graph classes without finding a contradiction; it does not classify all positive closures or validate the negative analytic argument. Its structural checker and receipt are historical standalone evidence; copy them to a scratch directory before replaying because that checker writes its receipt next to its source.

## Exact finite check

From the repository root, with Python 3 and no third-party dependencies:

```sh
python3 -I -B experiments/t7-orbit/checks/check_t7.py
```

The independently authored checker reads only the included JSON literals, whose SHA256 is embedded in its source. It checks stellar construction, six exposure orders, rational coverage, all 64 stable point maps (including 56 noninjective maps), support intersections, two canonical negative products, and finite score/dimension arithmetic. It also checks the supplied small-case fold witnesses. The full-sum uniqueness argument and the classification of all smaller sphere types are conventional proofs, not exhaustive computations performed by this script.

The original check took 0.0331 seconds and about 21.2 MB peak RSS on Tintagel. Its unchanged [result](evidence/original-result.json) and [receipt](evidence/original-execution-receipt.json) are included. A packaging replay is separately recorded. This workload needs no cloud resources. The checker does not prove the analytic rank-layer limit, evaluate its hidden error constant, choose a numerical prime, build a kernel table, or produce a host adjacency list.

## Sources and attribution

- OpenAI's [original construction](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026) supplies the original graph construction and analytic/kernel method.
- The [refinement repository at the compared commit](https://github.com/rohanarun/sidorenko-template-refinements/tree/d1df2a5cc0cb0c9003466b1c7f8ecb77a8e72a7d) supplies the sphere/cut reduction and the stated discrete-template classification/refinements.
- The campaign's GPT-6 Pro outputs supply the recovered [L3 proof](dependencies/l3-template-transfer-proof.md), [Task 4 orbit transfer](dependencies/task04-orbit-transfer-theorem.md), and [Task 11 seven-point proof](dependencies/task11-response.md). Their exact original bytes and attributions are preserved.
- Codex supplies the source comparison, separate proof reviews, independent finite checker, parameter audit, and publication synthesis. These are not a claim of mathematical priority.

[SOURCE-MANIFEST.json](SOURCE-MANIFEST.json) maps included portable files to original workspace-relative custody paths and pins exact hashes. Some historical reports retain those original path names; they are provenance references, not additional executable dependencies.

The complete Task 11 response is retained as source evidence, including its distinct classification claims. The supplied classification ZIP was invalid/truncated and is excluded. Its claimed 9,149-class census through twelve points is unverified and is not a premise of the theorem here. No global minimum order is claimed.

The unchanged source response retains historical ChatGPT conversation and sandbox attachment links. These are original provenance references, not working public attachments or additional verified evidence. Use the portable dependency files and pinned finite data supplied in this package.

## Source comparison and publication scope

The [bounded comparison](reviews/source-comparison.txt) distinguishes the original 35-vertex/66-edge discrete construction from this proposed 17-vertex/30-edge orbit-pinning construction. The earlier 13-point minimum concerns the stronger discrete-refinement template. It remains consistent with this example.

The current source comparison covers exact main commits and all five refinement PR bodies at the saved read. The [public search boundary](reviews/public-novelty-boundary.txt) explains why a wider priority claim is unestablished. Neither the Task 9 dimensions nor the support-33 correction is used here. The displayed sufficient dimension `103482288426242` comes from the conservative, support-uniform L3 argument and is not optimized.

This focused package changes neither the earlier classification nor its verification programs. It adds the exact theorem/dependencies, literal witness, independent small checker and explicit review boundaries. External mathematical review remains pending.
