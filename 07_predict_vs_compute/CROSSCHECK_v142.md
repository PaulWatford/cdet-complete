# CROSSCHECK_v142 — SU(N) step 1: atom EoS + N-polynomial record

**Claims.** (1) The SU(N) atom linked-cluster ln Z has U-coefficients c_j = κ_j(Y)·(−β)^j/j! (Y=k(k−1)/2,
κ_j the cumulant under the U=0 binomial), and each c_j(N) is an exact degree-(j+1) polynomial in N: a fit on
N=2..7 predicts N=8,9,10 to 4.8e-9. (2) The exact-cumulant coefficients match an independent ED contour (N=3)
to 2.2e-11. (3) SU(6) atom per-flavor density at U=1 = 0.308978. This is the CoS N-independence (kernel
once, evaluate at any flavor number). Lattice connected-determinant record (reusing v132 fast minors) = step 2.

**Reproduce.** `cd 08_2d_interacting && python3 sun_atom_record.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
