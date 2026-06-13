# Queue #2 (SU(N)), step 3: the production EoS route (v144)

Steps 1–2 established that the SU(N) linked-cluster coefficients are degree-(j+1) polynomials in N (the
combinatorial record) on the atom and the lattice. Step 3 builds the **production route** the record enables:
compute the SU(N) equation of state from the N-independent single-flavor propagator g0 **times the record**,
without ever diagonalizing the N-flavor system — the CoS value proposition (cost independent of N).

## The first coefficient (built and verified)

For the 2-site lattice, with d the per-flavor density and d' = d(d)/dμ of the **free single-flavor** system (the
N-independent g0 amplitudes, here d=0.741007, d'=0.267663):

| quantity | production formula (g0 × record) | vs ED, N=2..6 |
|---|---|---|
| c1 (dlnZ/dU at U=0) | −β·N(N−1)·d² | 5e-7 |
| n1 (d(density)/dU at U=0) | −(N−1)·d·d' | 2e-7 |

Both reproduce the SU(N) ED for **every N=2..6**, and the N=6 (¹⁷³Yb) value comes purely from the single-flavor
g0 and the record — **no N=6 diagonalization**. The first-order EoS n(U) ≈ n₀ + U·n1 at N=6 tracks the ED curve
at small U (dev 2.9e-3 at U=0.05) and departs at larger U (≈0.1 at U=0.3), where higher orders enter.

## Why this is the production route

The single-flavor g0 is computed once; the record N(N−1), (N−1), … is pure combinatorics; the EoS at any flavor
number is their product. This is exactly how CoS reaches N=6 at SU(2) cost.

## Scope

Built and verified: the first-order (Hartree) EoS coefficient via g0 × record, at all N including N=6, with no
N-flavor ED. **Not yet built:** the higher orders — the full connected-determinant sum with the closed-loop
record and the imaginary-time integrals (the v132 fast minors supply the per-flavor minors). That is the
remaining engineering toward the strong-coupling EoS curve.

Reproduce: `python3 sun_lattice_production.py` (~45 s; the N=6 ED is for validation only). ED is the anchor only;
frozen engine untouched (194/194).
