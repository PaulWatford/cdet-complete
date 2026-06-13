# 1d channeling (v62): CONFIRMED — collinearity carries ~2× at matched distance; the mechanism ledger

**The test.** Three families built from the *same axis-directed distances* — LINE (all on one axis
through the external), BENT (two on x, one on y), ZIG (one each on x, y, z) — so anisotropy is
controlled exactly by cubic symmetry. Pairs matched on MST to 0.01; **identical τ draws within each
pair** (the standing rule). Frozen predictions: distance law → all ratios ≈1; channeling → line >
bent > zig.

**Measured (L=6, β=4, μ=0.5, n=3):**

| pair | median paired ratio | IQR | n |
|---|---|---|---|
| line / bent | 1.82× (self-test seeds: 2.04×) | [1.25, 2.74] | 28 |
| line / zig | 1.93× (self-test: 2.43×) | [1.48, 2.24] | 12 |
| bent / zig | 1.33× | [0.82, 2.00] | 36 |

Monotone in collinearity and well separated from 1 for the line family: **channeling is real** —
coherent multi-bounce propagation along a shared direction enhances the connected weight at fixed
total distance. Consistent with v61 (twist-blind: channeling needs no winding closure).

## The mechanism ledger (v57–v62), honest accounting

| mechanism | status | size |
|---|---|---|
| distance decay (MST) | confirmed | τ-avg R²≈0.48, slope −0.69 |
| τ-interference | confirmed | 40% of var(ln\|C\|) |
| propagator anisotropy | confirmed, minor | ~35% slower per Euclid on diagonals |
| **1d channeling** | **confirmed (this version)** | ~1.8–2.4× at matched MST, graded |
| winding / ring closure | falsified (v61) | — |
| **residual** | **open** | composing distance × channeling ≈ 16× of the ~75× class gap → **~4× unaccounted** (candidates: mechanism interactions, MST-matching range, class tail composition) |

The universal weight concentration (v58) now has three confirmed components and one falsified
candidate, with the remaining ~4× stated rather than absorbed.

Reproduce: `python3 channeling.py` (gates: line/bent and line/zig medians >1.15; PASS, ~2 min).
Frozen engine untouched (194/194).
