# CROSSCHECK_v135 — integration #3 step 2: the diagrammatic self-energy converges to exact Σ

**Claims.** (1) Pipeline: a_n(iω) (connected-determinant order series) → G_diag=Σ a_n Uⁿ → Σ_diag=G₀⁻¹−G_diag⁻¹.
(2) Atom, vs closed-form/ED Σ: geometric convergence inside the bare-series radius ~π/β — U=0.3 order8→7e-6,
U=0.5 order8→6.6e-4, U=0.8 (near radius) order8→4.9e-2. (3) The radius limit motivates the direct irreducible
(1PI) series (step 3, the Šimkovic–Kozik algorithm). ED is the anchor only.

**Reproduce.** `cd 08_2d_interacting && python3 self_energy_diagrammatic.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
