# Shifted-reference CDet: pole-moving + the closed-shell operating point (v45)

Combining the literature map (v44) into a concrete upgrade. Two literature-grounded levers, both controlled
by the SAME knob -- the Fermi level's position relative to the single-particle shells (the v41/v44 detuning):

  (1) WHERE to compute (operating point): the average sign / per-order R is maximal (least cancellation) AT a
      closed shell, and collapses through zero at the detuning delta* just above it. Compute at closed shells;
      avoid delta*. [the v41/v44 finding = the documented closed-shell "magic-density" sign effect.]
  (2) HOW to expand (reference): shift the reference by a Hartree-scale alpha to MOVE the convergence-limiting
      pole out of the unit disk, so the series converges in a few orders (Wu-Ferrero-Georges-Kozik pole-moving,
      PRB 96 041105). [NEW here, exactly verified.]

## The shifted-reference scheme (exact, ED-verified)
Physical H is recovered at xi=1 for ANY shift alpha:
    H(xi; alpha) = [H0(mu) + alpha*N] + xi*(U*Hint - alpha*N),   H(1;alpha) = H0(mu) + U*Hint.
The reference sits at mu_ref = mu - alpha (alpha re-centres the reference's Fermi level). Tuning alpha moves
the pole; alpha=0 is the bare series. All results below are EXACT (exact diagonalisation), independent of the
Monte-Carlo layer. Module: shifted_expansion.py (make shift).

### Hubbard atom (mu=1.3, beta=4, U=3.5, <n>=1.00): bare is marginal, shift converges
  alpha* = +1.50 (Hartree scale U<n>/2 = +1.75); bare radius ~1.00 -> shifted radius ~1.81
  K :    bare |S_K-exact|   shifted |S_K-exact|
  2 :         3.4e-02            4.8e-02
  4 :         4.6e-01            2.8e-02
  6 :         1.6e-01            1.8e-02
  8 :         4.1e-01            2.0e-03
 12 :         2.7e+00            2.8e-03
The bare series is erratic (radius ~ 1, sitting on its disk); the shift gives clean monotone convergence.
  (High-order coeffs have a Cauchy-extraction FP floor ~1e-6..1e-5; table entries below ~1e-5 are floor-limited.)

### 2-site ring (mu=1.1, beta=4, U=4.0, <n>=1.00): bare DIVERGES, shift converges
  alpha* = +1.50 (Hartree scale U<n>/2 = +2.00); bare radius ~1.00 -> shifted radius ~2.64
  K :    bare |S_K-exact|   shifted |S_K-exact|
  2 :         2.1e-01            1.3e-02
  4 :         9.4e-02            1.4e-03
  6 :         5.8e-03            2.0e-04
  8 :         7.4e-01            9.7e-05
 12 :         1.8e+00            2.4e-05
Bare never reaches 1e-3 within 14 orders (it diverges past order 6); shifted reaches 1e-3 at ORDER 5.

## The "2^n reduction": fewer orders, exponentially less work
CDet's per-order cost is ~2^n (the connected-determinant subset sum). Reaching a target accuracy at order
K_shift instead of K_bare is therefore a ~2^(K_bare - K_shift) reduction in determinant evaluations. When the
bare series sits outside its disk (radius < 1) it never converges at any order, so the shift is not a mere
speed-up -- it makes the calculation possible at all (2-site case: divergent -> converged-at-order-5).

## The unification (and why alpha* ~ Hartree scale)
The optimal shift came out at the Hartree scale U<n>/2 in both cases -- i.e. expanding around the mean-field
(Hartree) reference, which absorbs the leading self-energy and moves the pole. That is the SAME Fermi-level
re-centring that defines the detuning delta: the operating point sets delta=0 (closed shell, best sign), and
the shift sets the reference's Fermi level to the Hartree-corrected position. One physical knob, two gains.

## Honest scope (what is and is not done)
- EXACTLY VERIFIED (ED): the shifted-reference scheme, its convergence-radius extension, the order-to-accuracy
  gain, and alpha* ~ Hartree scale. Shipped as a usable module + optimal-alpha selector (best_shift).
- LIVE ENGINE: the operating-point half -- R maximal at the closed shell -- is the measured mc2d behaviour
  (v41-v44).
- NOT DONE (scoped v46): wiring the one-body counterterm (-alpha*N) into the C connected-determinant MC so the
  SHIFTED coefficients are computed stochastically by the engine. Here the shift is proven at the exact
  coefficient level and provided as a resummation/reference-selection tool; the in-recursion counterterm is
  the next step. No claim that the C engine computes shifted CDet end-to-end.
