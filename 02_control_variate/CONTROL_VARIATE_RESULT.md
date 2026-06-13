# Control-variate hybrid: exact engine + TCI surrogate + Monte Carlo

Paul's idea: Monte Carlo reaches high order but only with an error bar; the exact
engine is accurate but can't run as far. Combine them so the exact data pulls the
MC error bar down.

This is the standard variance-reduction technique called CONTROL VARIATES, and it
works. Measured below.

## The method

To estimate the integral of the expensive integrand f (one C_V time-integral),
build a cheap surrogate g whose exact integral is KNOWN, then estimate:

    integral(f) = integral(g)        [known exactly]
                + MC[ f - beta*g ]   [Monte Carlo of the residual]

Two facts make this powerful:
- UNBIASED regardless of how bad g is. g only changes the variance, never the
  mean. A wrong surrogate cannot bias the answer.
- Variance drops by 1/(1 - rho^2), where rho = correlation(f, g). The surrogate
  does not need to be ACCURATE, only CORRELATED.

The control g here is the tensor-train (TCI) surrogate of the integrand, and its
exact integral is teneva.sum(g) on the grid. The surrogate is built by the exact
engine (the oracle), so "the exact accurate data" is what supplies both the
control and its known integral.

## The twist

The hexring TCI surrogate FAILED as an integrator this session (plateaued at
~11-24% accuracy because of cross-site coincidence cusps). As a control variate
that does not matter: it is 11-15% inaccurate yet 99% correlated with f. The
thing that flopped as an answer is an excellent accelerator.

## Measured (hexring, real target lattice, beta=5 mu=0.3 t=1)

| order n | surrogate accuracy | correlation rho | variance reduction | source              |
|---------|--------------------|-----------------|--------------------|---------------------|
| 4       | 11.2%              | 0.9935          | 77x (theory 77.6x) | brute-force exact   |
| 4       | 15.2%              | 0.9884          | 43x                | 60k-sample estimate |
| 6       | 15.9%              | 0.9875          | 40x                | 60k-sample estimate |
| 8       | (under-built)      | 0.52            | 1.4x               | INCONCLUSIVE *      |

Live sampling demo at n=4 (RMS error of the integral over 200 runs), confirming
the speedup is real and the estimator unbiased:

| MC samples | plain MC error | control-variate error | speedup |
|------------|----------------|-----------------------|---------|
| 200        | 1.26e-5        | 1.30e-6               | 93x     |
| 2,000      | 4.46e-6        | 4.82e-7               | 86x     |
| 20,000     | 1.42e-6        | 1.40e-7               | 103x    |

Both estimators land on the exact value -3.385e-05; the control variate just has
a ~10x tighter error bar (= ~100x fewer samples for equal accuracy).

The reduction factor is TUNABLE: a richer surrogate raises rho toward 0.999 and
the reduction toward the hundreds; a leaner surrogate lowers it. The 43x vs 77x
at n=4 is purely the surrogate budget.

## Honest boundaries

* The n=8 row is INCONCLUSIVE, not a failure. Every surrogate budget rich enough
  to correlate exceeded this container's RAM and was killed; the only build that
  fit was too starved (corr 0.52). So at n=8 the open question is whether a
  correlated-enough control can be BUILT at the orders where the wall bites. On a
  machine with more memory it is buildable and untested here. Do not assume the
  ~40x holds at high n until the control's correlation is measured there.

* This reduces the NUMBER of expensive evaluations MC needs (MC error ~ sigma /
  sqrt(N); cutting sigma by the control cuts the N needed by 1/(1-rho^2)). It does
  NOT reduce the per-evaluation 2^n subset sum, which is combinatorial and
  measured-irreducible. The control g is cheap (a tensor-train contraction, no
  2^n), so fewer expensive f-calls is a real wall-clock speedup, same boundary as
  the TCI integrator: act on the count of integrand calls, not on the per-call
  cost.

* Demonstrated on the time-integral at fixed order and fixed site pattern. The
  control-variate identity applies to any MC estimator with a known-mean
  correlated control (including full diagrammatic MC over orders and sites), but
  only the time-integral slice is measured here.

## Why this is the session's synthesis

- exact engine -> builds the control surrogate and its EXACT known integral
- TCI         -> the control surrogate itself (even the one that "failed")
- Monte Carlo -> the long-reach approximator whose error bar the control shrinks

That is exactly "combine the two so the accurate data pulls the MC error down,"
and it is the one combine-them idea this session that measured a large, real,
unbiased win.

## Files
- cv.py   : n=4 control-variate test, brute-force validated + sampling demo
- cv6.py  : correlation / variance-reduction estimate at given order (large sample)
