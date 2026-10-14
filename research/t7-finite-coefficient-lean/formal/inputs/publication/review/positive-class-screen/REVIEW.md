# T7 incidence graph: bounded Sidorenko-positive class screen

Date: 2026-10-11. Independent mathematical review of the literal graph specified in the delegation. No supplied program was executed or imported; no publication action occurred.

**Outcome: no positive-class contradiction found.** There are rigorous obstructions to the most immediate cube, cycle, tree-arrangement, and direct reflection explanations. This is a bounded screen, not a classification of all known positive closures. In particular, it neither establishes nor independently endorses the proposed non-Sidorenko conclusion.

The graph has point part P={0,...,6} and ten face vertices labeled by

    012 013 023 124 134 235 245 346 356 456.

A point is adjacent to a face precisely when it belongs to the triple. Thus v(H)=17, e(H)=30. Point degrees are (3,4,5,6,5,4,3), and all face degrees are 3. Pairs within either part have at most two common neighbors. All facts below concern this literal graph, not a graph with the historical faces retained.

## 1. The stellar construction does not supply cube bags

Start from tetrahedron faces 012,013,023,123. Subdivide face 123 with point 4, then face 234 with point 5, then face 345 with point 6. This gives exactly the ten listed faces.

In the incidence graph, a stellar step deletes the old face vertex and its three incident edges, then introduces a new point and three new face vertices. The replacement has seven vertices, including the three boundary points, and nine edges. It is Q3 with one vertex removed. A full cube would also contain the deleted face vertex and its three edges. Thus this operation is a replacement of a star, not graph-union gluing of intact cubes. Its net change is +3 vertices and +6 edges.

In fact H contains no cube subgraph. A cube in a connected bipartite incidence graph uses four points and four face vertices. Each of those faces has degree three already in H, so its three neighbors must be three of the four points. The four faces must be all four triples on those points. Any such tetrahedron involving 0 would require the missing face 123; one involving 6 would require the missing face 345. Among points {1,2,3,4,5}, the only available faces are 124,134,235,245, whose union has five points. No tetrahedron remains.

Conlon–Lee's N-decomposition theorem requires a tree decomposition into induced copies of a fixed weakly norming N, with an isomorphism between adjacent copies fixing their intersection. It therefore does not apply with N=Q3. [Finite reflection groups and graph norms, Section 5.3, Theorem 5.12](https://www.its.caltech.edu/~dconlon/norming.pdf).

Deleting the old stars after an application of a gluing theorem would need a separate preservation theorem. None was identified in this screen. Sidorenko positivity cannot simply be assumed to survive those deletions.

## 2. Neither side admits a tree arrangement

For the star-bag form of tree-arrangeability, a tree on one part must make every neighborhood from the other part a connected vertex set. This is the tree-arrangeable subclass described following Theorem 1.2 in [Some advances on Sidorenko's conjecture](https://arxiv.org/html/1510.06533v2).

Suppose first that the arrangement tree is on the seven points. Every face triple requires exactly two tree edges inside its neighborhood, so the ten faces require 20 incidences of a tree edge in a face neighborhood. Each pair of points belongs to at most two faces. A six-edge tree can therefore supply at most 12 such incidences, a contradiction.

Suppose instead that the tree is on the ten faces. Connectedness of the seven point neighborhoods requires sum_p(deg_H(p)-1)=30-7=23 incidences of a tree edge in a point neighborhood. Two distinct faces share at most two points. A nine-edge tree supplies at most 18 incidences, again a contradiction.

This excludes both full star-bag arrangements. It does **not** exclude arbitrary strong tree decompositions whose bags are more general trees.

## 3. H is not weakly norming or a reflection graph

A connected bipartite weakly norming graph must have constant degree on each part. H fails that necessary condition. See Theorem 4 in [Sidorenko, Weakly norming graphs are edge-transitive](https://arxiv.org/html/2003.13598v1). Reflection graphs are weakly norming by Conlon–Lee Theorem 1.2, so H itself is not a reflection graph either.

There is also a direct cut-involution obstruction. An automorphism preserves the two parts because their sizes differ. Degree classes force point 3 to be fixed and preserve the pairs {0,6}, {1,5}, {2,4}. If 0 is fixed, the union of its face neighborhoods distinguishes 1 from 5 and 2 from 4, so all points are fixed. The face vertices are then fixed because their triples are distinct. Reversal r(p)=6-p preserves the face set. Consequently Aut(H)={id,r}.

Reversal fixes point 3 and no face. H with point 3 removed remains connected: faces 012,124,245,456 connect all six remaining points, and every other face retains neighbors in that component. Hence the fixed set of the only nonidentity involution is not a vertex cut. There is no nontrivial cut involution of H in the sense of Conlon–Lee Section 3, so their direct cut-involution construction cannot start here.

These conclusions concern the entire graph. Irregular positive graphs can be obtained by decomposition, so this does not exclude all reflection-based gluing theorems.

## 4. Even-cycle bags do not rescue the elementary gluing argument

There are exactly fifteen C4s. Two distinct C4s intersect in at most one vertex or one edge. Indeed, two common vertices in the same part would determine their unique common-neighbor pair (codegree is at most two), hence the same C4. A three-vertex intersection is therefore impossible.

For any tree decomposition with b induced C4 bags, let I_e be the intersection across a tree edge. Running intersection gives the exact identities

    v(H) = 4b - sum_e |I_e|,
    e(H) = 4b - sum_e e(H[I_e]).

The preceding intersection bound implies 2|I_e|-e(H[I_e]) <= 3. Hence

    e(H)-2v(H) <= -4b + 3(b-1) = -b-3.

Here e(H)-2v(H)=-4, forcing b<=1, which cannot cover seventeen vertices. Thus H has no C4-bag tree decomposition, even before the extra intersection isomorphism condition is imposed.

For a fixed cycle length l>=6, the corresponding exclusion is simpler. Any induced subset I of C_l satisfies e(C_l[I]) >= 2|I|-l, so 2|I|-e(C_l[I])<=l. The same tree identities for b C_l bags imply

    e(H)-2v(H) <= -lb + l(b-1) = -l.

This contradicts -4 for every l>=6. Therefore no fixed even cycle can serve as N in an N-decomposition of H. This is an independent counting argument; it is not a claim that all graphs outside this construction fail Sidorenko's property.

## 5. Boundary for stronger decomposition results

The following theorems were inspected, but a qualifying decomposition of H was neither constructed nor comprehensively excluded:

* Strong tree decompositions: induced tree bags and compatible minimal connecting subtrees, beyond the full star-bag case. [Some advances, Theorem 1.2](https://arxiv.org/html/1510.06533v2).
* Higher strong decompositions: a recursive bag hierarchy, forest intersections, and isomorphisms fixing those intersections. [Sidorenko's conjecture for higher tree decompositions, recursive definition on pages 2–3 and Theorem 5](https://www.its.caltech.edu/~dconlon/HigherTree.pdf).
* Reflective decompositions: compatible labeled flag 2-cores and a domination hypothesis in the positive theorem. [Biregularity in Sidorenko's Conjecture, Definition 2.2 and Theorem 3.5](https://arxiv.org/html/2108.06599v2).
* N-decompositions with a weakly norming N other than cubes or cycles, or further entropy/reflection closures.

An ordinary tree decomposition of the stacked triangulation does not establish these additional hypotheses for its point-face incidence graph. Conversely, failure of the specific tests above does not rule out such a decomposition. The review makes no inference from planarity alone.

Some other immediate identities are unavailable: minimum degree three precludes a nontrivial edge-subdivision representation with degree-two subdivision vertices, and prime order seventeen precludes a nontrivial Cartesian product. Neither observation classifies arbitrary derived positive classes.

## 6. Relation to the proposed non-Sidorenko deduction

The local orbit-transfer integration and its adversarial/boundary reviews were read as context. They distinguish finite graph/orbit data from the L3 analytic signed-moment input and the subsequent existence deduction. This screen does not replay that analytic argument and provides no direct graphon or finite-host density test. No contradiction to it was found through the elementary positive classes examined here; its analytic obligations remain independent of this screen.

A proposed positive rebuttal needs an actual decomposition and all theorem hypotheses, or a separate valid closure theorem for the star-to-punctured-cube replacement. A proposed negative proof does not gain validity merely from these exclusions.

## 7. Reproducible finite checks and scope

`check_graph.py` is independently authored stdlib code, version t7-positive-class-structural-screen-v1. The recorded command is:

    python3 -B upstream/sidorenko/t7-publication/review/positive-class-screen/check_graph.py

Run from the workspace root `twelve-pro-verification-20261010`. It checks the literal graph, the three stellar steps, all 35 point quadruples for tetrahedron boundaries, all 5,040 point permutations for automorphisms, and all 105 pairs among the fifteen squares. It also checks the codegree and connectivity facts used in the written proofs. All assertions passed. The recorded execution took approximately 0.037 seconds; macOS peak resident size was 21,512,192 bytes.

`finite-receipt.json` is an independent standalone finite replay receipt, not an existing auditable-runner receipt. The mathematical tree counting arguments are written above; the checker does not search all decompositions or evaluate densities. All output/state is confined to this review directory. `source-pins.json` records the hashes of local context inputs and distinguishes remote bibliographic sources, whose bytes were viewed through the web tool but are not archived or byte-pinned here. `output-sha256.txt` pins the delivered files.
