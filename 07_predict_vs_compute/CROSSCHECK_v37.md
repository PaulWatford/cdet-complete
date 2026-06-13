# Cross-check (v37) — 2D high-order Monte Carlo: validated vs exact ED, sign-problem wall measured

Reproduce: 08_2d_interacting/ (make mc-validate, then make sign). Builds on v36 (orders 1,2 deterministic).

## What was checked
- A 2D high-order MC driver (mc2d.c, generalizing the 1D-hardwired diagmc.c to any lattice via a
  prebuilt LatticeCtx + site count N) reproduces the EXACT 2x2 Hubbard Green's-function coefficients
  cdet_order(n) = N*a_n at orders n=1..6, every order within <2 sigma. a_n exact from diagonalization
  via the Cauchy contour integral (r-independent to 1e-13). Orders 5,6 are beyond deterministic
  quadrature's practical reach (np^n = 1e9..7e10) -- the MC reaches them and lands on the exact value.
- Sign-problem characterization via R = mean(C_V)/mean(|C_V|) and the cost Nsamp->1% for 1% rel.err.

## Numbers (2x2, beta=4, mu=0.5, tau=0.5; gate run, ~70 s)
  n: MC          stderr     exact N*a_n   sigma
  1  -0.5796135  0.000923   -0.5789477    0.72
  2  -0.4669807  0.001258   -0.4662779    0.56
  3   0.1383506  0.001165    0.1366135    1.49
  4   0.4713411  0.002769    0.4669114    1.60
  5   0.2214447  0.003824    0.2144823    1.82
  6  -0.2463949  0.007863   -0.2466214    0.03

## The wall (order 3)
  cluster size (beta=4): 2x2 |R|=0.342 (Nsamp->1% 7e5) -> 4x4 |R|=0.047 (1.8e8), ~260x costlier.
  temperature (3x3):     beta=2 |R|=0.085 (2.5e7) -> beta=8 |R|=0.025 (1.4e10), ~570x costlier.
  |R| collapses and cost explodes ~geometrically in system size and inverse temperature = sign problem.

## Status (honest)
DONE: 2D MC driver validated vs exact ED at orders 1-6; sign-problem wall mapped vs size and T.
NOT done / NOT claimed: beating the sign problem (2x2 has none; reaching order 6 there is correctness,
not a large/cold-system result); a CDet-vs-naive-expansion variance comparison (no naive baseline built,
so no "higher order than a conventional expansion" claim). Overcoming the 1/R^2 wall -- a real analytic-
mean reference for CVAR, importance sampling, or a better estimator -- is the open frontier (v38+).
