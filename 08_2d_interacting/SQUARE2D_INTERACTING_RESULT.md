# 2D interacting Hubbard — first step, validated against exact diagonalization (v36)

This folder is where the toolkit becomes 2D *interacting*. The non-interacting 2D propagator already
existed (05_2d_lattice, square2d_init; re-validated here, free G0 vs numpy ED max|diff| 3.4e-9 on 4x4).
v36 feeds that propagator into the connected-determinant engine and validates the first interacting
orders against exact diagonalization of the 2D Hubbard model.

## What was built
- cdet2d.c / cdet_small.c: the order-(1,2) connected-determinant coefficient of the local Hubbard
  Green's function on a 1D ring (ring_init) or 2D square torus (square2d_init). This is driver.c's
  cdet_order with the lattice swapped and the external symmetry factor L -> N=Lx*Ly; the recursion C_V
  is geometry-blind, so nothing else changes. Deterministic nested Gauss-Legendre quadrature, n=1,2.
- hubbard_ed.py: exact diagonalization of the small-cluster Hubbard model (grand-canonical, finite-T),
  G_sigma(i,j;tau) via the Lehmann representation, in the engine's sign convention. Independent anchor.
- pin_convention.py / validate2d.py: pin the engine's order<->U convention against ED, then validate.

## The convention, pinned and verified (engine vs exact ED)
For the local Green's function G(0,0;tau;U), with a_n its U^n Taylor coefficient from ED:
    cdet_order(n)  =  N * a_n        (N = number of sites, sign +1)
This holds to ~1e-9 for BOTH orders n=1,2 and is IDENTICAL in 1D and 2D. The factor N is the
translation-symmetry external-site sum, confirmed N in {2,3,4,5} (rings) and the 2x2 square -- not a
coincidence of one size. That the same convention reproduces exact ED in both dimensions, at both
orders, is the validation: the 2D interacting engine is correct at orders 1 and 2.

  1D ring L=4   n=1: cdet=-0.4802981487  N*a_n=-0.4802981506  rel 3.8e-9
  1D ring L=4   n=2: cdet=-0.4948592231  N*a_n=-0.4948592239  rel 1.7e-9
  2D square 2x2 n=1: cdet=-0.5789477158  N*a_n=-0.5789477175  rel 2.8e-9
  2D square 2x2 n=2: cdet=-0.4662779161  N*a_n=-0.4662779165  rel 9.3e-10

## Capstone: the engine reconstructs the 2D interacting G(U)
Reconstructing G(U) = G0 + U*(cdet1/N) + U^2*(cdet2/N) from the ENGINE coefficients and comparing to
exact ED at finite U on the 2x2: the O(U^2) truncation error falls like U^3 (the first neglected order)
for small U -- |err| = 1.0e-3, 1.2e-2, 1.1e-1 at U = 0.25, 0.5, 1.0 -- confirming the engine's order-1,2
coefficients are the correct asymptotic series of the exact interacting 2D Green's function.

## Honest scope -- what this is and is NOT
IS: a validated first step. The connected-determinant engine works in 2D; its order-1,2 interacting
coefficients match exact 2D diagonalization to ~1e-9, with the convention cross-checked against 1D.
IS NOT: physics, or the frontier. The 2x2 cluster and the small rings are METHOD ANCHORS. At this size
there are no phases, no thermodynamic limit, and no finite-T transition (2D order needs large clusters
and low T). Only orders 1,2 are reached here, by deterministic quadrature; higher orders need a 2D
Monte-Carlo driver (the existing cdet_order_mc is 1D-hardwired) -- that is the next step (v37), and it is
there, at high order on larger clusters and low T, that the fermion SIGN PROBLEM -- the actual difficulty
of 2D Hubbard -- first appears. Stripes, d-wave pairing, and the cuprate question are far beyond this.
What v36 delivers is the validated foundation to build that on, not a claim about any of it.
