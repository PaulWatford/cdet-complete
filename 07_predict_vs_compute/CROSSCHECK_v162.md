# CROSSCHECK_v162 — large-L plane-wave propagator (100×100, thermodynamic limit)

**Claims.** (1) `square2d_G0_pw` computes the free 2D propagator from the analytic dispersion ε=−2t(cos kx+cos ky)
with O(L) memory (no eigenvectors), reaching 100×100 — far past the 16×16 numerical LMAX cap. (2) Exact vs the
numerical square2d path where both apply: worst |diff| = 1.25e-16 at L=6 and L=12. (3) Thermodynamic-limit convergence
of the NN propagator: within ~5e-4 by 16×16, ~1e-5 by 32×32, Δ=2.2e-11 at 100×100 vs 64×64 — confirming big lattices
are unnecessary past the correlation length. (4) Existing numerical val2d unchanged (3.39e-09, no regression); frozen
engine read-only.

**Reproduce.** `cd 05_2d_lattice && make square2d_pw_demo && ./square2d_pw_demo` (gate: exits non-zero if parity ≥1e-12).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
