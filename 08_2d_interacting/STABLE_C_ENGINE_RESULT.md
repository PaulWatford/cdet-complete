# The stable C deep-beta engine (v109): unbiased A(β) to β=64 — v107's asymptote was a low-biased underestimate; 15/8 falls

The v108 queue item: port the deep-β loop to a stable C engine so the 4-point grids become dense
grids and z(∞) tightens. Built `cdet_stable_engine.c` — the frozen connected determinant with the
log-domain propagator, reading the exact L=6 spectrum (`spectrum_l6.bin`) so it matches the Python
stable engine. **Validated** against `stable_cdet.StableFrozen.C_V` to machine precision (worst
significant rel dev 0.0 above the 1e-13 cancellation floor) and against a high-statistics Python
re-measurement: A(40) = 0.262(9) [C] vs 0.267(4) [Python] — 0.5σ.

## What the speed bought — and what it exposed

A 6-point grid to **β=64** (which Python could not reach) in **150 s** (Python: ~15–20 min and
heavy-tail-biased). The clean grid (fixed sites (1,2,4), cluster IS, median-of-means):

| β | A (e-9) | c1 (e-9) | z = 2+ln(A/\|c1\|)/β |
|---|---|---|---|
| 24 | 1.2033(149) | −236.3 | 1.7800 |
| 32 | 0.5552(117) | −204.7 | 1.8153 |
| 40 | 0.2518(64) | −185.0 | 1.8350 |
| 48 | 0.1580(45) | −177.2 | 1.8537 |
| 56 | 0.1017(31) | −168.8 | 1.8676 |
| 64 | 0.0677(27) | −161.8 | **1.8784** |

**The exposure: v107's A(β) was heavy-tail-biased LOW at high β.** The banked A(40)=0.119(28) is
2.3× below the true 0.267 (confirmed by independent high-statistics Python). So v107's rate ρ_A was
too large and its z(∞)=1.882(18) was an **underestimate**. The corrected A decays slower, the flow
runs higher.

## The decision, and the honest limit

- The clean leading-order flow **rises to z(64)=1.878 and is still climbing**, with no plateau.
- **15/8 = 1.875 is now disfavored** — the flow passes *through* it (at β≈62) rather than
  asymptoting to it. The asymptote is **≥1.88**, pointing to 17/9=1.889 or higher.
- **But the asymptote is not cleanly pinned.** A 1/β fit gives z(∞)=1.933, a 1/β² fit 1.961 — they
  disagree and both fit poorly (χ²=120/4, 20/3): the flow is still curving at β=64, so the simple
  extrapolation is unstable. The single-rational-asymptote model may itself be wrong (the flow is a
  multi-exponential object). The local high-β rate gives z(∞)≈1.95, but that is an upper-ish bound,
  not the converged value.
- **Internal consistency holds**: the leading-order flow sits below the robust pool by a *shrinking*
  cross-term lift (+0.013/+0.005/+0.003 at β=36/44/52) — exactly the v100 δ₁×f₂ correction,
  vanishing as β grows, confirming the C flow is the same object measured cleanly.

## Net

The C engine is the deliverable: validated, ~1000× the Python stable engine, and it **corrects a
hidden bias** in the v107 program (the high-β A values). The refined picture: the asymptote is
**higher than v107 thought**, 15/8 is out, 17/9 or above — but pinning it precisely needs either
β>64 (cheap now, in C) or a multi-exponential model of the curvature (the loop-format known-rate
tool, once A's emergent slow rate is channel-resolved — it is *not* a simple spectral gap). None of
it moves the wall.

Reproduce: `python3 cdet_stable_engine_dump.py` (regenerates spectrum + refs); `gcc -O2 -Wall
-Werror -std=c11 -o cse cdet_stable_engine.c -lm && ./cse val < cdet_stable_engine_refs.txt`
(validation PASS); `./cse grid 24 64 8 16 4096 2024 0.002 0` (the grid). Frozen engine untouched
(194/194).
