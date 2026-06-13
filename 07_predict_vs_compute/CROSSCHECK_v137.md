# CROSSCHECK_v137 — exact 1PI coefficients + correction to v136

**Claims.** (1) Exact σ_n via the Dyson recursion σ_n = a_n/G₀² − (1/G₀)Σ_{m<n} σ_m a_{n−m} reproduce the ED
self-energy to 1.9e-9 at U=0.3, 6e-5 at U=0.5. (2) Coefficient decay gives R_G≈0.73 (|a_n|^{1/n}), R_Σ≈0.84
(|σ_n|^{1/n}) — essentially equal. (3) **Retraction:** v136's R_Σ≈1.76 / "2.2× larger" was a contour-proxy
artifact (the contour enclosed Σ's singularity near 0.8). The real Šimkovic–Kozik advantage is efficiency +
MC variance, not radius. (4) v133–135 unaffected.

**Reproduce.** `cd 08_2d_interacting && python3 self_energy_irreducible.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
