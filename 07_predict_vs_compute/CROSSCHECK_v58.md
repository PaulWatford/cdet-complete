# CROSSCHECK_v58 — weight universality robust and seed-stable; sign hierarchy downgraded

**Claim 1 (weight universality, robust).** Across order (n=2,3,4), temperature (β=2,4,8), filling
(μ=0, 0.5, 1.5) and the observable on the L=6 cube, the 1d-line/bulk per-configuration weight ratio
exceeds 10× in every cell: mean-based 10×–223×, median-based (heavy-tail robust) 11×–184×,
seed-stable (β=8: 66×/55×/61× at seeds 11/42/77). U is exactly universal by the banked theorem (C_V
contains no U).

**Claim 2 (sign hierarchy downgraded — the failed gate was the discovery).** The module's first
self-test FAILED because the same cell (L=6, β=8, seed 11) gives R(1d)=0.44 at 500 samples and 0.02
at 400: R over these heavy-tailed |C| distributions is estimator-fragile. Robust count-coherence
S=|2f₋−1| is near the binomial floor in most cells. The v54/v57 per-class sign statements are
downgraded to OPEN on the record (SLICE_SCALING_RESULT.md carries the amendment); v57's flagged L=8
bulk anomaly was this same instability.

**Reproduce.** `cd 08_2d_interacting && python3 slice_universality.py` → median-ratio universality
across the β flip (67×/82×), seed stability (54×/52×), with the non-robust R columns printed as the
fragility warning; "slice-universality self-test ... PASS" (~90 s). The full sweep table is in
SLICE_UNIVERSALITY_RESULT.md.

**Scope (honest).** One lattice size for the sweep (the L-dependence is v57's weight half, which
stands); 500–800 samples/class; the downgraded sign question needs weighted-bootstrap statistics
(v59 open item).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
