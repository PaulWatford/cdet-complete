# cdet control-variate (hexring) — self-contained

Variance reduction for the connected-determinant integrand using a TCI
surrogate as a control variate. Self-contained: the oracle and the minimal
engine it needs are bundled here, nothing is read from /tmp.

## Build
    make                # or: make CC=gcc
Produces ./oracle_hex from oracle_hex.c + cdet_engine.c + lattices.c.

## Run
    pip install teneva numpy
    python3 cv.py       # n=4 fixed
    python3 cv6.py 5    # n given on the command line

## Oracle protocol and convention (this was the undocumented part)
oracle_hex reads n imaginary-time values per line on stdin and prints C_V
(connected determinant) per line. Fixed parameters, set in oracle_hex.c:
  - 6-site hexagonal ring, vertex i -> site (i mod 6)   [V[i].site = i%6]
  - beta = 5.0, mu = 0.3, t = 1.0
  - external times: tau_outer = 0.4*beta, tau_inner = 0.6*beta
  - Green function: lattice_G0 (hexring_init)

## Reproducibility
  - TARGET (exact grid mean), deterministic by brute force:
        exact grid mean = -3.385301e-05
  - The TCI surrogate is stochastic in general, so cv.py/cv6.py now seed the
    cross initial tensor: teneva.rand(..., seed=0). With that, a run is fully
    reproducible. At seed 0, n=4: surrogate accuracy 11.7% (pointwise),
    corr(f,g)=0.99293, control-variate speedup ~71x.
  - A control variate only needs to be CORRELATED with f, not accurate, and a
    wrong surrogate cannot bias the mean. The ~11-24% surrogate accuracy and the
    77x/93x figures in CONTROL_VARIATE_RESULT.md were from earlier UNSEEDED runs
    within that same stochastic spread; the seeded ~71x above is the one that
    now reproduces exactly. The target mean is the stable, checkable number.
