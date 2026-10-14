# Deterministic generator following the source kernel

This is a finite mathematical algorithm over arbitrary finite binary strings. Every loop bound and probability denominator is explicit. It is separate from the smaller graph-space enumeration implemented in `generator.py`. The full proof of termination is `PROOF.md`, §§2–13. No full-size run was performed.

## Parameters and conventions

Read the literal faces, shifted scores a_i,b_j and thinning exponents ell_ij from the independently checked certificate. Use the parameters P at the beginning of the proof: D=7296, r=3648, T=2^2459, Z=3807386006623258, epsilon=2^(-Z-2181), Q0, B and N=2^B. Every prior and thinning exponent is fixed before the prime search.

Order corners lexicographically by their point and face labels. Order symmetric D-by-D matrices by the base-q integer formed from their upper-triangle entries in row-major order. Fill the lower triangle by symmetry. All field arithmetic is exact modulo q. Atom and coin tuples are enumerated lexicographically with repetitions unrestricted.

## Algorithm

1. Construct the explicit integer Q0 in (10.5). Test the integers Q0+1,...,2Q0-1 by trial division and select the first prime q. The lemma in §13 proves this succeeds after fewer than Q0 candidates and at most 2Q0^2 divisor tests. No primality oracle is assumed.

2. Enumerate the q^b(D) symmetric matrices. Exact modular symmetric elimination gives the rank and the discriminant of the induced nondegenerate quotient. Count the rank-r matrices of signs +1 and -1, giving positive integers n_+ and n_-. A symmetric elimination may use nonzero-norm vectors to split a nondegenerate line; if all diagonal entries of a nonzero symmetric block vanish, a nonzero off-diagonal entry gives such a vector by adding its two basis vectors. Its eventual zero block is the radical. The product of the nonzero diagonal pivots determines the quotient discriminant. Quadratic character can be computed by modular exponentiation to (q-1)/2. This specifies a bounded elementary procedure and includes singular matrices.

3. Set Z_I=sum_i T^a_i and Z_J=sum_j T^b_j. Define the finite atom set

```
Omega = ({0,...,12,*} x S_D^66) x ({0,...,21} x S_D^66).
```

Use the common clone denominator

```
M = 2^(Z+2181) * Z_I * Z_J * q^(132*b(D)).
```

Each fixed matrix tuple with old types i,j has T^(a_i+b_j) clones; one with types *,j has `(2^(Z+2181)-1)*Z_I*T^b_j` clones. Enumerate atoms first, then their clones. These positive integer multiplicities sum exactly to M. All clone labels therefore have equal probability 1/M, and forgetting the clone index gives exactly the intended rational priors. Do not merge independent source draws merely because they receive equal types or labels.

4. Evaluate W at any pair as follows. At a star pair or nonincident type pair, W=1. At an incident pair kappa, let lambda=T^(-ell_kappa). Take `(1-lambda)+lambda*W_base`, where W_base is the sum over the two finite activation/sign branches in §8. The first branch has 128 sign vectors with unconditional probabilities `(2+sigma*chi_Gamma)/512`; the second has 64 sign vectors with unconditional probabilities `(2-sigma*chi_Gamma)/256`. Here `chi_Gamma` denotes the product of the selected coordinate signs over Gamma, not a new field evaluation. Each term is the product, over its activated coordinates, of

```
K_sign(A) = q^b(D)/n_sign  if rank(A)=r and discriminant_sign(A)=sign,
            0             otherwise.
```

Here A is the difference of the two corresponding coordinate matrices. The sign sigma is negative only at corner (0,0). All operations are exact rational operations on the finite integers already specified.

5. On two Omega atoms z=(x,y),z'=(x',y'), compute

```
U(z,z') = W(x,y')*W(x',y) / q^(14*b(D)).
```

Let ell_max=25601296520 and define

```
D_W   = 512*T^ell_max*(n_+*n_-)^7,
D_coin = D_W^2 * q^(14*b(D)).
```

The proof shows `D_coin*U(z,z')` is an integer between 0 and D_coin. No rounding, approximate integration, or approximate probability is used.

6. Enumerate every N-tuple of clone labels and every coin tuple indexed by the binom(N,2) unordered pairs of distinct host vertices, each coin in `{0,...,D_coin-1}`. For pair {u,v}, add its edge precisely when its coin is less than `D_coin*U(label_u,label_v)`. Add no loops. Coinciding labels at distinct host vertices retain the actual kernel diagonal value; they do not suppress their host edge.

7. Count all homomorphisms into that graph by formula (12.4), which sums over every N^13 point-image tuple and multiplies the 22 common-neighbor counts. Return the first graph passing

```
(2*edge_count)^66 - hom_count*N^97 >= 1024*N^131.
```

The test is an exact integer inequality.

## Explicit termination bounds

The source outcome search has exactly `M^N * D_coin^(binom(N,2))` possible candidates. A finite average over them has deficit greater than 1387/N by (12.3) and §13. At least one therefore passes step 7. This is the proof of termination, not a heuristic expectation about search behavior.

For bounds independent of the unevaluated signed-layer counts, the selected prime satisfies

```
q < 2^319820424557970218.
M < 2^1123774834967853447267918484.
D_coin < 2^357564720215858629205464514.
```

Thus the outcome search tests fewer than

```
2^(N*1123774834967853447267918484
   + binom(N,2)*357564720215858629205464514)
```

candidates. The normalizer pass visits fewer than `2^8513445719422207667361408` symmetric matrices. Each graph test has exactly N^13 point-label iterations, with 22 common-neighbor counts per iteration. All other operations are finite arithmetic and bounded loops. These are enumeration bounds, not unit-cost arithmetic or practical complexity claims.

The graph-space generator in `generator.py` eliminates duplicate source outcomes: it tests at most `2^binom(N,2)` labeled simple graphs and uses the same acceptance inequality. Both generators concern the original 35-vertex pattern and retain all noninjective homomorphisms.
