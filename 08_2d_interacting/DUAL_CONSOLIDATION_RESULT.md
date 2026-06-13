# Consolidation + side-by-side of both C layers (v108): dual insights — one root cause, one cure

Both C layers — the **surrogate** (`csurrogate.*`) and the **brute-force** drivers
(`cdet2d.c`, `cdet_small.c`, `cdet_vs_naive.c`) — brought current with v104–v107, then compared
across three axes. The comparison surfaced that **both carried the same latent flaw inherited from
the naive engine, and both take the same cure.**

## What was stale, now current

- **Surrogate**: its menu carriers still said "open {13/7, 24/13}, PENDING RE-FIT". v104–v107
  resolved that: the pool survives robustly and *rises*, no menu line fits, and the assembled flow
  gives **z(∞)=1.8818(184)** — the lower menu falls, 15/8 returns. Added the live carriers
  `surr_l6_z_inf()` (1.8818) and `surr_l6_pool(β)` (the robust pool 36/44/52); the old menu lines
  are now labelled superseded history.
- **Brute C**: re-stamped v108 with the precision caveat. Its propagator is the frozen engine's
  naive `G0_atom`, correct and ED-validated at benign β but carrying the v103 deep-β bug latent.

## The three-axis side-by-side

**Value** (surrogate carriers vs the stable-engine ground truth):

| quantity | surrogate | stable truth | verdict |
|---|---|---|---|
| z(∞) assembled | 1.8818 | 1.8818 | agree (carries v107) |
| pool z(36), z(52) | 1.8428, 1.8642 | 1.8428, 1.8642 | agree (carries v105) |
| superseded 13/7 line @β=52 | 1.8483 | 1.8818 | **disagrees 1.8σ** → retired |
| superseded 11/6 line @β=52 | 1.8419 | 1.8818 | **disagrees 2.2σ** → retired |

**Precision** (the brute-force C propagator at a deep-β far level, β=36, ξ=−3, τ=35):

| | value | |
|---|---|---|
| naive C `G0_atom` (brute drivers) | −0.000000 | the v103 bug, latent in C |
| stable C `G0_atom_stable` | −0.049787 | = analytic; certified fix |

**Speed** (C, per call):

| engine | ns/call | deep-β correct? |
|---|---|---|
| surrogate carrier (lookup) | 4.4 | — (approximate) |
| naive `G0_atom` (brute) | 17.3 | **no** (benign only) |
| stable `G0_atom_stable` (new) | 22.4 | **yes** |
| Python stable g0 (216-level) | 21,375 | yes (the slow workhorse) |

## Dual insights — where each can be improved

**The surrogate.** (1) Its superseded menu carriers diverge 1.8–2.2σ from the resolved asymptote —
they now *mislead* if called at high β, and should be guarded, not just commented. (2) It has **no
deep-β engine**, only fitted lookups; linking `cdet_stable` would let it *compute* deep-β values
(correctly) instead of interpolating. (3) The ln-magnitude deep-bulk tail (the 64× over-prediction
from v102) is still uncaptured — a regime-conditional model (point estimate on the coherent sector,
a calibrated *bound* on the deep bulk) is the honest fix.

**The brute force.** The naive `G0_atom` is the deep-β bug. The fix — the log-domain
`G0_atom_stable` (built and certified here against the Python stable / mpmath) — costs only **1.29×**
the naive call while being deep-β-correct, and a stable **C** engine would be **~1000× faster** than
the Python stable engine that the v104–v107 program leaned on. That speed is the real prize:
v107's z(∞)=1.88(2) carries 10–40% rate errors from only 4 β-points per series; a stable C engine
makes a 20-point grid cheap, which is exactly what tightens the asymptote.

**The combination (one root cause, one cure).** The four engines fill a 2×2 of
(fast/slow)×(deep-correct/deep-wrong): surrogate = fast/approximate, naive-C = fast/deep-wrong,
stable-Python = slow/deep-correct, and **stable-C = fast/deep-correct — the missing quadrant, now
filled.** Consolidating the two layers together revealed they share *one* flaw: both inherit the
naive propagator (the surrogate indirectly, via carriers fit to naive-corrupted pool data; the
brute directly). And both take *one* cure: the log-domain propagator — re-grounding the surrogate
on the certified z(∞) (done) and porting `G0_atom_stable` into C (done). The ideal stack is now
visible: **surrogate for triage → stable-C for deep-β production → mpmath for spot certification.**

Reproduce: `python3 csurrogate.py` (surrogate gate, PASS); `gcc -O2 -Wall -Werror -I. -I../engine
cdet_stable_test.c cdet_stable.c ../engine/cdet_engine.c -lm && ./a.out` (benign match + deep-β
stable-correct, PASS). Frozen engine untouched (194/194).
