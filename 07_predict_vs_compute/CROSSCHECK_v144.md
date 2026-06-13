# CROSSCHECK_v144 — SU(N) step 3: the production EoS route

**Claims.** (1) The first SU(N) EoS coefficients come from single-flavor g0 × the record: c1 = −β·N(N−1)·d²,
n1 = −(N−1)·d·d' (d, d' = per-flavor density and its μ-derivative of the free single-flavor 2-site system).
Both match the 2-site SU(N) ED to ~1e-7 for every N=2..6 — including N=6, with no N=6 diagonalization. (2) The
N=6 first-order EoS n(U) ≈ n₀+U·n1 tracks ED at small U (2.9e-3 at U=0.05) and departs at larger U. (3) So the
single-flavor g0 (once) × the combinatorial record gives the EoS at any flavor number — CoS at SU(2) cost.
Higher orders (full CDet + closed-loop record + τ-integrals, v132 fast minors) remain.

**Reproduce.** `cd 08_2d_interacting && python3 sun_lattice_production.py` (~45 s; N=6 ED is validation only).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
