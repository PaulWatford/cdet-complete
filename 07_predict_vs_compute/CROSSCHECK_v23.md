# Cross-check proof data (v23) — the two-engine methodology, and the first order-reduction experiment

The reverse direction (v22) needs the same discipline that drove the simulation arc: an exact
anchor for every claim. For the engine, the anchor is a FROZEN baseline engine. v23 sets that up
and runs the first acceleration experiment against it.

## Two engines (the methodology)
- `engine/` -> FROZEN BASELINE ORACLE (stamped BASELINE_FROZEN.txt); never edited.
- `engine_exp/` -> sandbox (stamped EXPERIMENTAL.txt); every change validated against the baseline.
Clean-fork check (must pass before any experiment): both build, both 194/194, and a reference order
computation is BIT-IDENTICAL:
  cdet_order(1) = -0.5082750022348369, cdet_order(2) = 0.44040518398732875  (engine == engine_exp).
So the baseline is a faithful oracle and the sandbox starts identical to it.

## Experiment 1 — does the expansion scheme set the order needed? (atom; anchor = G_exact_atom)
The engine's cost is ~3^n per order, so the wall is the ORDER n needed. On the atom the engine's
CDet series is the bare U-expansion of G. At beta=4, mu=0.7, tau=0.123:
- bare-series convergence radius R = 0.942 (nearest complex U where Z(U)=0), so U=2 is BEYOND it.

| U | exact G_atom | bare N=2 | bare N=6 | bare N=12 | Pade[6/6] (same coeffs) |
|---|--------------|----------|----------|-----------|-------------------------|
| 0.5 | -0.25457152 | -0.2499 | -0.2520 | -0.2545 (err 2.9e-5) | -0.25457152 (err 1.2e-10) |
| 2.0 | -0.44451192 | -1.7719 | +29.50 | +2798.6 (err 2.8e3) | -0.44431 (err 2.0e-4) |

At strong coupling (U=2) the bare engine expansion DIVERGES (no order converges); a resummation of
the SAME coefficients, informed by the analytic pole structure, converges. At U=0.5 the resummation
reaches 1.2e-10 where the bare order-12 sum is only at 2.9e-5 -- same orders, far more accuracy.

## Reading
The engine's cost wall is the order needed, and the order needed is set by the EXPANSION SCHEME,
not just the physics: the bare (U=0) expansion is useless at the strong coupling we operate in,
while a resummation/shift rescues it at a few orders. This is the order-reduction lever (v22) made
concrete and validated against the baseline's exact anchor. (Requires mpmath for the high-precision
Taylor/Pade; the rest of the package needs only numpy/scipy.)

## Status
ESTABLISHED (v23): the two-engine methodology (frozen baseline oracle + validated sandbox), proven
clean (bit-identical fork). FIRST RESULT: the bare engine expansion diverges at strong coupling and
a scheme change (resummation now; shifted-action / atomic-reference expansion next) recovers the
answer at far fewer orders -- validated against G_exact_atom. NEXT (v24): implement the shifted
reference in engine_exp's C (the engine already ships G_exact_atom) and validate the resummed
observable against the baseline at strong coupling.
