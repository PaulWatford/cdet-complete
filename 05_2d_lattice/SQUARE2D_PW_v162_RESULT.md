# Large-L plane-wave propagator — reaching 100×100 and confirming the thermodynamic limit

The 2D engine already showed thermodynamic-limit convergence up to 16×16 (SQUARE2D_RESULT.md), capped there because the
numerical path stores the eigenvectors (O(LMAX²); LMAX=256 = 16×16). The documented route past that cap is the
**closed-form / plane-wave propagator** — and that is what this adds.

## What was added

`square2d_pw_init` / `square2d_G0_pw` (in lattices.c/.h): the free propagator evaluated straight from the analytic
dispersion,

  G0(i,j;τ) = (1/N) Σ_{kx,ky} cos(k·(r_i−r_j)) · g_band(ε_k;τ),   ε(kx,ky) = −2t(cos kx + cos ky),

with **no eigenvector storage** — only a 1D cosine table, so memory is **O(L)** instead of O(L⁴). The cosine table
doubles as the phase table. This reaches lattices far beyond the numerical cap (here 100×100 = 10⁴ sites; the path
supports up to 2048×2048).

Note: the numerical LMAX cap is *bypassed*, not raised — raising LMAX would only extend the numerical path modestly
(its struct is O(LMAX²)); the plane-wave path is the right tool for large L, exactly as the original notes recommended.

## Result 1 — the closed-form path is exact

Against the numerical square2d path where both apply (L=6, L=12): worst |G0_numerical − G0_planewave| over probe
points = **1.25e-16** (machine round-off). The two paths are the same propagator.

## Result 2 — thermodynamic-limit convergence, now out to 100×100

Equal-time nearest-neighbour propagator G0(r=(1,0),τ=0), β=5, μ=0, t=1:

| lattice | sites | G0_NN | Δ vs previous L |
|---|---|---|---|
| 4×4 | 16 | 0.18748865 | — |
| 8×8 | 64 | 0.19675657 | 9.3e-3 |
| 12×12 | 144 | 0.19881946 | 2.1e-3 |
| 16×16 | 256 | 0.19929464 | 4.8e-4 |
| 24×24 | 576 | 0.19942816 | 1.3e-4 |
| 32×32 | 1024 | 0.19943727 | 9.1e-6 |
| 64×64 | 4096 | 0.19943796 | 7.0e-7 |
| **100×100** | **10000** | **0.19943796** | **2.2e-11** |

Past ~12–16 sites the value is already within ~5e-4 of the infinite-system result, and by 32×32 within ~1e-5. The
100×100 point (Δ=2.2e-11 from 64×64) confirms the thermodynamic limit — and confirms the method's central strength:
**you don't need huge finite lattices.** Once past the correlation length (~12–16 sites here), the finite-lattice
result is already representative of the infinite system. The plane-wave path makes that check cheap and removes the
size cap when one wants it.

This G0 is the drop-in free propagator for CDet at large L; the O(L²)-per-entry plane-wave sum can be upgraded to the
circulant FFT (O(N log N) for all separations at once) if a full large-L interacting grid is ever wanted — though, per
the convergence above, it isn't needed for thermodynamic-limit physics.

Reproduce: `make square2d_pw_demo && ./square2d_pw_demo`. The frozen reference engine/ (194/194) is used read-only and
untouched.
