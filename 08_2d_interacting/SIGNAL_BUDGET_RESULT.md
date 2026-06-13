# The signal budget: what it costs to resolve z(∞) at large L (v126)

z(∞) is read from z = probe_val + ln(|A|/|c1|)/β. As L grows the gap g = lowest_empty(L) − μ closes
(~L⁻³·³, v125) and the determinant signal weakens. This sizes the cost of pushing to large L.

## Which signal binds (fast path, fixed stats K12 NT2048, β=24, μ=1.0)

| L | gap | \|A\| | relErr(A) | \|c1\| | relErr(c1) |
|---|---|---|---|---|---|
| 8 | 0.414 | 9.5e−2 | 6.9% | 5.76 | 15.5% |
| 12 | 0.268 | 1.1e−1 | 6.9% | 0.235 | 3.0% |
| 16 | 0.082 | 1.0e−1 | 8.3% | 0.558 | 7.4% |
| 20 | 0.061 | 2.2e−1 | 3.5% | 6.1e−2 | 16.4% |
| 24 | 0.035 | 1.4e−1 | 6.5% | 3.1e−2 | 19.5% |

**relErr(A) ~ gap⁰·⁰⁶ (flat)** — A stays O(0.1) with ~5–8% error at any L. **relErr(c1) ~ gap⁻⁰·⁴⁷
(grows)** — c1, the probe-channel response, is the **binding signal**: it shrinks toward the Fermi sea as
the probe level merges in.

## The budget law

MC error ~ 1/√samples, so the budget to hold a target z-precision ~ relErr² ~ gap⁻⁰·⁹. With gap ~ L⁻³·³:

> **budget(samples) ~ L³ ~ N — polynomial, not exponential.**

This is the headline sizing result: resolving z(∞) costs only ~linearly in the number of sites. **There
is no exponential sign-problem wall in this observable** — doubling the linear size needs ~8× the
statistics, no more.

## A million-site check

At L=100, K5 NT384 (1920 samples), c1 = 5.5e−4 ± 3.9e−4 (~70% error, barely resolved), 117 s/point —
consistent with the law. Reaching ~5% on c1 needs ~170× more samples (~3.3e5/point, ~5.5 h/point at the
fast-path rate), so a **day-long unattended run resolves a coarse z-flow (a handful of β points) at a
million sites**.

## Launch recipe (day-long, crash-safe)

```
python3 run_to_log.py /path/L100.log -- \
   ./cpw grid 24 144 24 24 8192 31 0.002 2 2 1 2 4 1.0 -L 100 -fast
```

K24 NT8192 ≈ 2e5 samples/point × 6 β points. Streams every line, fsync-logs (survives a hard crash),
records last_good_beta; watch live with `tail -f`. Reproduce the budget scan: `python3
signal_budget_study.py`. Frozen engine untouched (194/194).
