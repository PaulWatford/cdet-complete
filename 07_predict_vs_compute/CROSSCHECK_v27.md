# Cross-check proof data (v27) — the high-order time-integration driver (the v26 gate), built + validated

The asks: build the high-order time-integration driver named as the gate in v26, and raise the stress
harness RAM guard to 90% of available. Both done. Reproduce against engine_exp/ (diagmc.c +
diagmc_validate.c).

## What was missing, and what was built
engine/driver.c cdet_order integrates the vertex times only for n=1,2 (NAN beyond), by nested
deterministic quadrature. That was the gate blocking ANY high-order physical series in C (bare or
atomic). engine_exp/diagmc.c now integrates the SAME integrand for ARBITRARY order by Monte Carlo
over the vertex times and sites:
    cdet_order(n) = L * (1/n!) * SUM_{s_1..s_n} INT dtau_1..dtau_n  C_V({(s_i,tau_i)}, ...)
    estimator:  cdet_order_mc(n) = L * (1/n!) * (L*beta)^n * < C_V >_{uniform (s_i,tau_i)}
with a 1-sigma standard error from a Welford running variance. Propagator and external convention are
exactly those of cdet_order (hexring_init + lattice_G0, external site 0, the L* translational
prefactor), so n=1,2 is a direct check against the frozen baseline.

## Validation against the FROZEN baseline (L=6, beta=4, mu=0.7, t=1, tau_out=0.123, tau_in=0.877)
Baseline (nested quadrature, exact): n=1 = -0.5082750022348369 ; n=2 = 0.4404051839873288.
| order | nmc      | MC estimate          | deviation |
|-------|----------|----------------------|-----------|
| n=1   | 1e5      | -0.502337 +/- 0.0071 | +0.84 s   |
| n=1   | 1e6      | -0.5077135 +/- 0.0022| +0.25 s   |
| n=2   | 1e5      | 0.452839 +/- 0.011   | +1.15 s   |
| n=2   | 1e6      | 0.4409232 +/- 0.0035 | +0.15 s   |
The MC estimate sits sub-sigma on the exact value at 1e6 samples for BOTH orders, and the error bar
shrinks ~1/sqrt(nmc) (n=1: 0.0071 -> 0.0022; n=2: 0.011 -> 0.0035). Converging to the right value
(not many-sigma off) confirms the estimator's measure/prefactor is correct -- a wrong factor would
converge to a wrong number with a tight bar.

## First high-order terms (baseline returns NaN)
| order | nmc    | MC estimate          |
|-------|--------|----------------------|
| n=3   | 5e5    | 0.008085 +/- 0.006   |
| n=4   | 5e5    | -0.340664 +/- 0.0081 |
These are the first orders the engine could never reach before. n=3 is consistent with ~0 within its
bar; n=4 is clearly nonzero.

## Honest scope and the known wall
This is a Monte-Carlo integrator: results carry a statistical error, not bit-exactness; it is
validated against the exact baseline exactly where the baseline exists (n=1,2). The integrand C_V is
sign-oscillating, so the MC variance per sample GROWS with order (the diagrammatic sign problem) --
this is the real high-order wall now, not RAM or a code buffer. That is precisely where a better
reference helps: the atomic/strong-coupling reference (v23 atom, v24 dimer) shrinks the integrand's
oscillation at strong coupling, so the same nmc reaches higher order. With the high-order path now
existing and validated, that atomic-reference swap (feed G_exact_atom / shifted-mu as g0 into
cdet_order_mc, add the counterterm) is UNBLOCKED and is the next step (v28), to be validated against
this baseline and re-raced through the v26 crash-safe stress harness.

## RAM guard
engine_exp/stress_cv.c: the graceful-stop threshold was raised from 85% to 90% of available RAM
(on the 4 GB box this moves the guard's trip point but the time wall still hits first, ~n=20-24).

## Status
DELIVERED + VALIDATED (v27): the high-order time-integration driver (cdet_order_mc) reproduces the
frozen baseline at n=1,2 within MC error (sub-sigma at 1e6, error ~1/sqrt(nmc)) and returns the first
n>=3 terms. Two-engine gates intact (new files only; cdet_order(1,2) and C_V n=16 still bit-identical
to baseline, 194/194). RAM guard at 90%. KNOWN WALL: MC sign-variance grows with order -> the atomic
reference (next, v28) is the lever, now unblocked.
