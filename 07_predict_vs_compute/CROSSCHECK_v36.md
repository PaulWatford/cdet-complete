# Cross-check (v36) — begin 2D: interacting engine validated against exact 2D diagonalization

v36 turns the toolkit from a validated 1D engine into a validated 2D *interacting* one, at the first
orders. Reproduce: 08_2d_interacting/ (make validate).

## What was checked
- Free 2D propagator (square2d_init): re-validated vs independent numpy ED, max|diff| 3.4e-9 (4x4).
- Interacting orders 1,2 (connected determinant) vs EXACT diagonalization of the 2D Hubbard model:
  cdet_order(n) = N * a_n, where a_n is the U^n Taylor coefficient of the exactly-diagonalized local
  Green's function. Verified to ~1e-9 at n=1,2 for the 2x2 square AND the 1D ring L=4 -- SAME convention
  in both dimensions. The prefactor N (translation symmetry) confirmed across rings N=2,3,4,5.
- Capstone: G(U) reconstructed from engine coefficients (G0 + U*cdet1/N + U^2*cdet2/N) vs exact ED at
  finite U on the 2x2; O(U^2) truncation error scales like U^3 (the first neglected order).

## Numbers (engine vs exact ED)
  1D ring L=4   n=1: -0.4802981487 vs -0.4802981506 (rel 3.8e-9)
  1D ring L=4   n=2: -0.4948592231 vs -0.4948592239 (rel 1.7e-9)
  2D square 2x2 n=1: -0.5789477158 vs -0.5789477175 (rel 2.8e-9)
  2D square 2x2 n=2: -0.4662779161 vs -0.4662779165 (rel 9.3e-10)

## Status (honest)
DONE: the connected-determinant engine is validated in 2D at orders 1,2 against exact diagonalization,
with the order<->U convention cross-checked against 1D. This is the validated foundation, NOT physics:
2x2 / small rings are method anchors (no phases, no thermodynamic limit, no finite-T transition at this
size); only orders 1,2 (deterministic quadrature) are reached. Higher orders need a 2D Monte-Carlo
driver (cdet_order_mc is 1D-hardwired) -- the next step, and where the fermion SIGN PROBLEM (the real
2D difficulty) first appears. Stripes, pairing, the cuprate question remain far beyond this.
Open (v37): a 2D high-order MC driver (square2d + cdet_order_mc_cfg), then confront the sign problem.
