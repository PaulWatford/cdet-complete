# Cross-check (v46) — wiring the shift into the engine: counterterm = d/dmu

Reproduce: 08_2d_interacting (make counterterm). Realises the v45 shifted-reference scheme through the REAL
CDet engine without modifying the frozen core, via the exact identity that a one-body counterterm is a
chemical-potential derivative.

## Identity
b_n(alpha) = sum_{j=0}^{n} (alpha^j/j!) U^(n-j) a_{n-j}^{(j)}(mu-alpha), a_m^{(j)} = d^j a_m/dmu^j of the BARE
CDet coefficient. (d/dmu inserts -N = -(n_up+n_dn) = the counterterm; spin-correct automatically.)

## Verified (2-site ring, mu=1.1, beta=4, U=4, alpha=1.5)
- FORMULA vs ED shifted coeffs: machine precision -- |diff| = 0, 1e-16, 5e-16, 6e-15, 6e-14, 4e-13, 2e-12 for
  n=0..6 (via Cauchy-in-mu derivatives).
- REAL ENGINE (cdet_small, cdet_n=N*a_local): b1 engine 0.03418925 vs ED 0.03418324 (6e-6); b2 engine
  0.04078553 vs ED 0.04074089 (4.5e-5). Residual = engine np=64 quadrature + finite-diff mu-derivative, not
  the identity. Convention pinned: cdet_n(m) is extensive N*a_m^local; a0=G0 is local; divide by N.
- Payoff: bare series DIVERGES at this (mu,U) (v45), yet the resummed shifted sum from a few low-order engine
  coeffs converges (K=2: 1.3e-2 -> K=5: 6.3e-4). Order saving = exponential (2^Delta K) cost cut, realised
  through the real engine.

## Honesty
EXACT: counterterm=d/dmu identity (machine precision). REAL ENGINE: bare->shifted to engine precision
(quadrature + FD limited; production would sample d/dmu directly via density insertions -- efficiency, not
correctness). Frozen engine UNTOUCHED: 194/194, cdet_order constants bit-identical. The shift is a
resummation layer over bare engine output -- the honest meaning of "wired in" without altering the validated
core; an in-recursion one-body vertex remains an optional future optimisation, not needed for correctness.
