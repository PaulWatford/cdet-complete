# Cross-check (v32) — the two-version / control-variate idea: where it wins and where it stalls

User's idea: keep a cheap "generated" version and an exact "calculated" version, and use the exact one
to error-correct the cheap one each step -- "like another control variate." This is exactly the
control variate, it is already in the codebase, and it works -- with one decisive condition.
Reproduce: 02_control_variate/cv.py ; engine_exp/cv_highorder.c.

## It is already here, and it works (low order)
02_control_variate/cv.py: f = exact target, g = a TCI surrogate that is only 11.7% accurate.
- correlation rho(f,g) = 0.993
- control variate  f - beta*(g - E[g]),  beta = cov(f,g)/var(g)
- plain MC var 3.39e-8 -> CV var 4.77e-10 = 71x fewer samples, matching theory 1/(1-rho^2)=71x.
The decisive insight (and why the user's instinct is right): it is the CORRELATION that buys the win,
NOT the surrogate's accuracy. An 11.7%-accurate surrogate still gives 71x because rho=0.993. The
mechanism is COMBINE, not flip/alternate: at each step use both, corrected = E[g]_exact + mean(f -
beta*g). The reduction is 1/(1-rho^2).

## Does it extend to the HIGH-ORDER C_V? Measured: not with a simple surrogate
engine_exp/cv_highorder.c samples vertex configs at order n and measures the correlation between the
full lattice C_V (exact "calculated") and cheap references (the "generated"): decoupled atoms,
shifted-mu lattice, weak-hopping lattice.
| n | rho(decoupled) | rho(shifted-mu) | rho(weak-hop) | best CV reduction |
|---|----------------|------------------|----------------|-------------------|
| 4 | ~0.0 / -0.6*   | ~0.5-0.6         | ~0.5           | ~1.4-1.6x         |
| 6 | ~0.0           | ~-0.1            | ~-0.05         | ~1.0x             |
| 8 | ~0.0           | ~-0.72           | ~-0.64         | ~2.1x             |
(*rho is noisy at high order -- C_V is a sign-oscillating residual, so estimates wander with sample
count and seed; the ROBUST conclusion is |rho| <= ~0.7 and erratic.) None of the simple parametric
references stays well-correlated: the best variance reduction is ~1-2x, nowhere near the low-order
71x. The fully-decoupled atom is worst (rho -> 0 by n=6) -- it discards exactly the inter-site
structure that dominates high-order connected diagrams.

## Why, and what it implies (honest)
At high order the connected value is a sign-oscillating residual of huge cancelling terms (#31); a
simple fixed parametric surrogate cannot track it, so the correlation -- and thus the CV payoff --
collapses. Getting high correlation there is essentially as hard as the sign problem itself. So:
- The control-variate idea is SOUND and PROVEN at low order (71x); the user's framing is correct.
- It is NOT free at high order: the surrogate must be ADAPTIVE/LEARNED (the TCI surrogate that gave
  rho=0.993 at low order is data-driven, not a fixed reference) -- a fixed shifted/decoupled reference
  is not enough. The promising path is a learned surrogate (TCI-like) fitted to the actual high-order
  integrand, accepting that high correlation is the open challenge.
- Two clarifications on the literal proposal: (i) it is COMBINE, not flip/alternate -- alternating
  per n leaves the cheap orders uncorrected; the win is the correlation-weighted correction at the
  same n; (ii) the butterfly is NOT a useful CV partner -- a control variate needs a CHEAPER
  CORRELATED observable with a KNOWN mean, whereas the butterfly computes the SAME quantity less
  accurately (no known-mean, no cheaper-different-observable).

## Status
VALIDATED (v32): the control-variate idea is already realized (02_control_variate, 71x at n=4,
rho=0.993) -- correlation, not accuracy, drives it. Tested at high order (engine_exp/cv_highorder.c):
simple parametric references (decoupled / shifted-mu / weak-hop) DE-CORRELATE (|rho|<=~0.7, ~1-2x),
because the high-order connected value is a sign-oscillating residual. CONCLUSION: keep the CV idea,
but the high-order surrogate must be adaptive/learned (TCI-like), not a fixed reference; high
correlation at high order is the open problem (the sign problem in disguise).
