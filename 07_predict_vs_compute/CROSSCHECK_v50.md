# CROSSCHECK_v50 — exact symmetry reduction of the site sum (involution search outcome)

**Claim 1 (involution search).** No sign-cancelling involution (ratio C_V(σx)/C_V(x) = −1) exists
among the natural lattice symmetries of the 2×2 (time reversal, sublattice translate, diagonal
reflection, products). An exact symmetry (ratio +1) does: the stabilizer of the external site,
|G_0| = 2 (diagonal swap of the B-sublattice sites). Reproduce by extending the symmetry scan in
`symmetry_reduction.py` — the engine ratio returns +1, never −1.

**Claim 2 (exact reduction).** `cd 08_2d_interacting && python3 symmetry_reduction.py` →
symmetry group |G|=8, stabilizer |G_0|=2; folded site sum matches brute force to 6.6e-17 (n=2),
1.2e-16 (n=3), 8.5e-17 (n=4), with 1.60×/1.78×/1.88× fewer C_V evaluations (→ |G_0|=2× as n grows).
Self-test prints PASS.

**Claim 3 (symbolic proof).** `python3 symmetry_audit_sympy.py` → the stabilizer permutations satisfy
P^T·H(t)·P − H(t) = 0 and [P,H(t)] = 0 as polynomial identities in the hopping t (sympy simplifies
both to the zero matrix). Returns PASS. This proves the fold is exact for every t, μ, β — not a
numerical coincidence at t=1. (sympy is an audit-time dependency only; the runtime module needs only
numpy.)

**Scope (honest).** The fold removes redundancy on the discrete site-configuration space (L^n), a
constant |G_0|× saving that grows with lattice symmetry. It does NOT fold the Rossi per-evaluation 2ⁿ
recursion, and it does NOT touch the physical sign — orbit members share the same value and sign, so
nothing cancels.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; `cdet_order` constants
bit-identical (−0.5082750022348369  0.44040518398732875). `symmetry_reduction.py` wraps the engine
(via the validated `cdet_port.py`, itself bit-identical to the frozen ring port at 0.00e+00).
