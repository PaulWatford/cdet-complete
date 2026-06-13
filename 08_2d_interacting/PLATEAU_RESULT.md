# The plateau run (v110): there is no plateau — the flow crosses every menu rational and keeps rising; the menu identification falls

The v109 queue item: push the C grid to β=80–120 for the plateau, to decide 17/9 vs higher. Done —
and the answer overturns the framing.

## Two precision walls, and why the freeze lets us reach the plateau

Pushing deep first hit a wall: the float64 stable engine degrades on extreme-corner configs. But
the wall is on the **physical** engine (StableCDet vs mpmath: 2.6% error already at β=56, rising to
15% at β=80) — a **determinant-level** cancellation beneath the v103 propagator-level one. The
**frozen** engine (which measures A) is different: freezing the deep occupied levels removes the
ill-conditioned occupied-far physical amplitudes, so the frozen determinant is well-conditioned.
float64-vs-long-double agree to ~1e-6 at β=64 and ~1e-4 at β=80 — **the v109 grid is clean, no
retraction**. float64 only fails (NaN) at β≥96; **long double (x87 80-bit, +3.3 digits) reaches
β=120**, validated (matches Python at β=36, matches float64 to β=80). The freeze is also a numerical
regulator — that is what makes the plateau reachable at all.

## The full flow — monotonic rise, no plateau

| β | 24 | 32 | 40 | 48 | 56 | 64 | 80 | 100 | 120 |
|---|---|---|---|---|---|---|---|---|---|
| z=2+ln(A/\|c1\|)/β | 1.780 | 1.815 | 1.835 | 1.854 | 1.868 | 1.878 | 1.895 | 1.909 | **1.920** |

The flow **rises monotonically and is still climbing at β=120** (+0.011 from β=100). It does not
asymptote to any menu rational — it **crosses** them:

- **15/8 = 1.875** crossed at β≈61
- **17/9 = 1.889** crossed at β≈74
- **19/10 = 1.900** crossed at β≈87

And the A-decay rate ρ_A is **still decreasing** at β=120 (0.097→0.058→0.051→0.044→0.035→0.027) —
the slowest spectral channel has not yet dominated, so the asymptote lives at β≫120. The rate
difference (2−z)·β = ln(\|c1\|/A) has slope ρ_A−ρ_c1 ≈ 0.045 and *shrinking*, giving z(∞)∈[1.95, 2.0]
— **plausibly the trivial value z=2** (the zero sitting at the probe level 2) with slow 1/β
corrections, though the data does not prove a specific limit.

## What this retracts

The menu-rational identification program (v93–v107: 11/6, 13/7, 24/13, 15/8, 17/9 …) read
**finite-β values as the asymptote**. The clean deep flow shows there is **no low-q rational
asymptote in [1.83, 1.90]** — those were all finite-β crossings of a monotone rise toward a high
value (≥1.92, likely →2). The question "which menu rational is z(∞)?" is **not supported by the
data**; it was the wrong question. z(∞) is high and slow-converging, and pinning it precisely is not
possible by brute β-extension (the multi-exponential convergence is too slow even at β=120) — it
needs the known-rate resummation with A's channels resolved (the standing queue item), or it is
simply 2.

None of this moves the wall (R and 2^n are unchanged); it relocates *where the sign structure
sits* — at the probe level in the deep-β limit, not at an exotic rational.

Reproduce: `gcc -O2 -Wall -Werror -std=c11 -DUSE_LD -o cse_ld cdet_stable_engine.c -lm && ./cse_ld
grid 80 120 20 10 2048 7777 0.002 0`. Frozen engine untouched (194/194).
