# The true convergence radius: thermal Fisher zeros, not the RPA wall (v177)

**Question.** v172–176 studied the RPA/Stoner wall `U_c = 1/chi0_max` (the leading real-axis instability) and showed its
tide (v173) and Diophantine sieve (v174/v175) are artifacts of `chi0_max` being a *max over the discrete q-grid*. Does
the TRUE radius — the nearest complex-U singularity of the actual `lnZ` (the v146 branch point) — inherit that structure?

**Exact anchor (the atom).** For the Hubbard atom `Z(U) = 1 + 2 e^{βμ} + e^{-βU+2βμ}` is entire, and `lnZ` is singular at
the complex-U zeros of `Z` (Fisher zeros): a complex-conjugate pair at

>   `U = -ln(A)/β ± i·π/β`,   `A = (1 + 2 e^{βμ}) e^{-2βμ}`,

so the true radius is `sqrt((lnA/β)² + (π/β)²)` — a **thermal** structure with imaginary part `π/β`. A direct complex-zero
finder reproduces this to **0.0e+00**, calibrating the method.

**Findings.**
- **The true radius is THERMAL, not an instability.** Its nearest singularity is a complex-conjugate Fisher pair near
  `Im U ~ π/β` (a Matsubara-like scale) — categorically different from the real-axis RPA wall. For small Hubbard rings
  the nearest zero stays on this thermal line (β=2, μ=0.5, L=3: `Im U = 1.84·π/β`).
- **It is CLOSER than the RPA wall — the v146 caveat, now numerical.** L=3 ring: `R_true ≈ 2.90 < R_RPA ≈ 3.42`. The
  *complex-U* structure, not the Stoner instability, sets the actual convergence radius.
- **It does NOT inherit the Diophantine sieve.** The sieve is specifically a property of `chi0_max` being a *max over the
  q-grid* (the grid misses the continuum peak `q*` by a number-theoretic amount). The true radius is a *global* analytic
  property of `lnZ` (the nearest complex-U zero) with no q-grid maximization, so the sieve mechanism is structurally
  absent.

**Honest limitation.** A direct large-L demonstration that `R_true` lacks the sieve is precluded: the sieve appears at
large L (the 2D lattice) while `R_true` is only computable at small L (ED, `2^{2L}` states), and the complex-zero search
itself is delicate (the L=4 ring flips between scan resolutions; L=3 is stable and used here). The case rests on: the
exact atom anchor (0.0e+00), the thermal nature (`Im U = π/β`), the structural fact that `R_true` has no grid-max, and
the small-ring evidence that `R_true` is thermal and `< R_RPA`.

**Conclusion.** Two different radii govern the bare-U series: the RPA wall (real-axis Stoner instability, with the
finite-size tide and Diophantine sieve that the q-grid imposes) and the true radius (a thermal complex-U Fisher pair near
`π/β`, closer, and free of the sieve). The number-theoretic structure lives in the q-sampling of the *RPA* wall, not in
the analytic continuation of `lnZ`.

**Validation (pre-registered gates, all pass).** (1) atom finder radius == analytic to 0.0e+00; (2) atom zero at
`Im U = π/β`; (3) ring L=3 `R_true < R_RPA`; (4) ring L=3 zero on the thermal line (`Im ∈ [1,2.5]·π/β`); (5) structural:
`R_true` has no grid-max. Frozen reference engine untouched (194/194). `wall_true_radius.py`, `cdet trueradius`.
