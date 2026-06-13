# Wiring the shift into the engine: counterterm = d/dmu (v46)

v45 proved the shifted-reference scheme exactly but only at the ED coefficient level; the one-body counterterm
-alpha*N was not in the C connected-determinant. v46 closes that loop -- WITHOUT re-architecting the frozen
engine -- by using the fact that -alpha*N is the generator of chemical-potential shifts: counterterm
insertions resum exactly into mu-derivatives of the bare coefficients.

## The exact resummation
Writing the shifted scheme H(xi;alpha)=[H0(mu)+alpha N]+xi(U Hint-alpha N) as a 2D Taylor expansion about
(mu_ref=mu-alpha, U=0) gives a finite closed form for every shifted coefficient:

    b_n(alpha) = sum_{j=0}^{n} (alpha^j / j!) * U^(n-j) * a_{n-j}^{(j)}(mu - alpha),

where a_m^{(j)} = d^j/dmu^j of the BARE CDet coefficient a_m. The spin structure is automatically correct:
d/dmu of G inserts -N = -(n_up+n_dn), exactly the counterterm. So the engine, unchanged, computes bare
coefficients at a few nearby mu; a thin resummation produces the shifted coefficients.

## Verified two ways (2-site ring, mu=1.1, beta=4, U=4, alpha=1.5)
(i) FORMULA vs ED shifted coeffs -- machine precision:
    n :   0     1     2     3     4     5     6
  |diff|: 0  1e-16 5e-16 6e-15 6e-14 4e-13 2e-12
(ii) REAL C ENGINE (cdet_small; cdet_n = N*a_local) bare coeffs fed through the resummation:
    b1: engine 0.03418925 vs ED 0.03418324  (|diff| 6.0e-06)
    b2: engine 0.04078553 vs ED 0.04074089  (|diff| 4.5e-05)
  residual = engine np=64 quadrature + finite-diff on engine outputs; the formula itself is exact (see (i)).
  (Convention pinned: engine cdet_n(m) is the EXTENSIVE N*a_m^local; a0=G0 is already local. Divide by N.)

## Why this is the right "2^n reduction"
The bare coefficients a_m exist and are finite even when the bare SERIES diverges; only LOW orders are needed
(up to the shifted convergence order). At this (mu,U) the bare series diverges (v45), yet the resummed shifted
sum from a few engine coeffs converges: K=2 err 1.3e-2 -> K=5 err 6.3e-4. So the engine computes a handful of
low-order bare coefficients and the resummation delivers the convergent answer -- the order saving is the
exponential (2^Delta K) cost cut, realised through the real engine.

## Honest scope
- EXACT: the counterterm=d/dmu identity (machine precision, orders 0-6).
- REAL ENGINE: cdet_small bare coeffs -> shifted coeffs to engine precision (limited by quadrature + the
  finite-diff mu-derivative, not the identity). For production one would sample d/dmu directly (density
  insertions) rather than finite-difference; that is an efficiency refinement, not a correctness gap.
- The frozen reference engine is UNTOUCHED (still 194/194; cdet_order constants bit-identical). The shift is
  realised as a resummation layer over bare engine output -- which is the honest meaning of "wired in"
  without modifying the validated core. Reproduce: make counterterm.
