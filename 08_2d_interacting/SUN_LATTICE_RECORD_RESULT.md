# Queue #2 (SU(N)), step 2: the record survives hopping (v143)

Step 1 (v142) showed the SU(N) **atom** ln Z coefficients are exact degree-(j+1) polynomials in N. Step 2 asks
the question that matters for a real lattice EoS: does that N-polynomial record **survive hopping**, or is it an
atomic artifact?

## The test

A 2-site SU(N) Hubbard cluster by exact diagonalization (2N orbitals, 2^{2N} states):
H = −t Σ_a(c†_{1a}c_{0a}+h.c.) − μ Σ n + U Σ_site Σ_{a<b} n_a n_b.

## The finding (verified)

**The record survives hopping.** c_j(N) stays a degree-(j+1) polynomial in N:

| check | result |
|---|---|
| U=0 factorization ln Z(N) = N · single-flavor | 1.3e-14 (ED is correct) |
| c1(N) degree 2: fit N=2,3,4 → predict N=5,6 | 5e-5 (self-test: predict N=5 to 7e-6) |
| c1 3rd finite-difference over N | 3e-5 (≈0 ⇒ degree 2) |
| c2(N) degree 3: fit N=2..5 → predict N=6 | ~1e-3 (extraction-noise floor) |

So the CoS N-independence — compute the N-independent kernel once, evaluate the polynomial at any flavor number
— holds for the **lattice**, not just the atom. The EoS at N=6 (the ¹⁷³Yb flavor number) is reachable from the
kernel **without ever diagonalizing the N=6 system**.

## Scope

Verified: the 2-site lattice — c1 (degree 2) tightly, c2 (degree 3) at the finite-difference extraction-noise
floor; c3 (degree 4) is consistent but needs N>6 (dense ED OOMs at 2¹⁴). **Not yet built:** the production
lattice connected-determinant with the closed-loop record assembled from g0 minors — the v132 fast minors
compute the per-flavor minors and the N^{loops} record sits on top. That is the remaining engineering for the
full EoS.

Reproduce: `python3 sun_lattice_record.py`. ED is the anchor only; frozen engine untouched (194/194).
