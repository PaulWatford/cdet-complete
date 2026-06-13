# The c1 sign in L: arithmetic jitter, not a Friedel period (v128)

v127 left a question: derive the period of the sign(c1) oscillation in L and connect it to the v119
density-matrix wavevector. The answer is that **there is no clean period** — and that absence, plus *why*,
is the result.

## Two hypotheses (frozen before measuring)

- **H1 period-16 Friedel wave** — sign(L) = sign(L+16).
- **H2 arithmetic jitter** — the sign is set by *which* cosine-sum multiplet is lowest-empty at each L.

## Measurement (sign(c1), sites 1,2,4, β=24, seed-stable)

| L | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 52 |
|---|---|---|---|---|---|---|---|---|
| sign c1 | − | + | + | + | − | − | + | − |

H1 predicts sign(L)=sign(L+16): 24/40 (−/−) ✓, 32/48 (+/+) ✓, but **28/44 (+/−) and 36/52 (+/−) mismatch**.
The period-breaking points L=28, 36, 44 are **seed-stable** (seeds 31/17), so the breakage is real. **H1
(period-16) is falsified; H2 (arithmetic jitter) holds.**

## Why — the probe momentum jumps number-theoretically

The lowest-empty eigenspace is whichever cosine-sum multiplet lands just above μ=1.0, and its dominant
|kx|/L jumps erratically with L — 0.29, 0.13, 0.05, 0.0, 0.07, 0.0, 0.0, 0.06 for L=24…52 — not smoothly.
So the Friedel phase cos(2π·kx·Δx/L) at the x-aligned vertices (0,1,2,4) jitters with no period.

## The connection to v119 — by contrast (the real insight)

- **A (background)** = (1/N) Σ over the *whole occupied Fermi sea* of cos(k·Δr): a smooth sum → a clean
  continuum Friedel wavevector (v119), so sign(A) **converges** as L→∞ (v127).
- **c1 (probe response)** = the derivative w.r.t. occupying the *single lowest-empty multiplet*: a
  discrete, arithmetically-sensitive selection → sign(c1) **jitters** with L, no period.

This is exactly why v127 saw sign(A) converging but sign(c1) oscillating: the background integrates the
sea (clean), the probe response picks one multiplet (jitter). The v116 selection rule lives in c1, so it
is arithmetic at finite L and marginal (|c1|→0) in the continuum. **There is no period to derive — the
background carries the clean continuum Friedel wavevector, the probe response carries only arithmetic
remnants of it.**

Reproduce: `./cpw grid 24 24 1 10 1536 31 0.002 2 2 1 2 4 1.0 -L <L> -fast` (signed c1 at col 4) for L in
{24,28,…,52}; `python3 probe_jitter_analysis.py`. Frozen engine untouched (194/194).
