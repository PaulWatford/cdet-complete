# CROSSCHECK_v136 — integration #3 step 3: the 1PI series has a larger radius

**Claims.** (1) Atom radii: R_G=|iω₀+μ|≈0.80 (G-pole), R_Σ=|U_Z|≈1.76 (partition-function zero) — 2.2×
larger, because the G-pole is a regular point of Σ. (2) vs exact ED Σ (order 14): past R_G the bare-G+Dyson
series diverges (U=0.9→2.5, 1.1→13.5, 1.3→10) while the direct 1PI series stays converged (~0.1). (3) This is
why Šimkovic–Kozik compute Σ directly; the exact σ_n come from the 1PI determinant recursion (reusing v132
fast minors), the σ_n here being a contour proxy (~1e-1 floor). ED is the anchor only.

**Reproduce.** `cd 08_2d_interacting && python3 self_energy_irreducible.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
