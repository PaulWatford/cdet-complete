# Consolidation v161 — the v157–160 arc, with the frozen baseline retained for parity

A periodic health gate (the consolidation rule, with the v157 triple-run + improvement-cycle extension). Nothing new
is asserted; the whole current state is re-proven to cohere, all three models are run, and the **frozen reference
engine/ (194/194) is retained as the parity baseline** every benchmark is measured against.

## 1. Health gate — `consolidation_v161.py` (~4 s, PASS)

- **[v147] cross-model invariants:** surrogate == production (SU(N) c1, n1), addition pole == python, fast-minors
  connected determinant == numpy det.
- **[parity] frozen baseline:** the hybrid validates **0.00e+00** against the frozen reference (the retained anchor).
- **[v157] auto-fast:** the projector fast path is **bit-identical** to `-nofast` and default-on (crystallographic L).
- **[v158] chained continuation:** the hybrid exposes its terminal sampler state → ~√2 gain, no cycle.
- **[v159] two-particle:** the chained walk sweeps 10/10 pair-configs with exclusion (Pauli) held.
- **[v160] conformal-Borel:** beats plain Padé in the crossover (the order-axis tool), keyed to |t_c|≈1.05.

## 2. Triple-run benchmark (parity vs the frozen baseline + timing)

| model | time | correctness (vs frozen baseline) | strength | weakness |
|---|---|---|---|---|
| surrogate | ~2.9 ms | dev 3.55e-15 | instant; exact on coverage | coverage-limited |
| hybrid | ~5.6 ms | **0.00e+00 vs reference** | exact + scalable + auto-fast | needs L=6 spectrum |
| brute force (frozen) | ~2.5 s | **194/194 anchor** | exact + general (canonical) | slow; L-limited |

All three remain consistent against the frozen anchor. The hybrid's auto-fast grid speedup re-measures **~28×**
(auto 0.13 s vs −nofast 3.56 s), still bit-identical.

## 3. Improvement cycle (this consolidation)

The big lever — the bit-identical projector fast path (~26–28×) — was found and applied in v157. This cycle profiled
the remaining per-sample cost and looked for a parity-preserving win:

- **Identified:** the inner loop recomputes `set_freeze_d()` (the s=0 and s=δ occupation arrays) on every one of the
  millions of inner samples, although those arrays depend only on the fixed eigenvalues/probe — not on the τ sample.
- **Applied (in a copy) + verified:** precomputing the two freeze states once and swapping pointers is **bit-identical**
  (val 0.00e+00; grid output identical to the baseline) — parity preserved.
- **Measured:** the gain is **negligible — 0.621 s → 0.617 s (~0.6 %, within noise)**. C_V (the connected determinant)
  dominates; the freeze recompute is a tiny fraction. So this micro-opt is **not** added to the source — it adds
  complexity for no real benefit. Honest outcome: not every cycle yields a new safe lever.
- **Deferred (the genuine next lever):** a **low-rank determinant update** for the freeze-0 → freeze-δ change. The
  freeze only flips the probe-level occupation, which enters g0 linearly, so the second C_V differs from the first by
  a low-rank update — replacing a full re-evaluation could ~halve the per-sample cost. But it is a deep change to the
  connected-determinant evaluation and is **parity-risky**; it is deferred until it can be validated bit-identical
  against the frozen baseline. The order-axis resummation (v160 conformal-Borel) remains the higher-value lever.

## Bottom line

The v157–160 arc is internally coherent; all three models agree; the frozen reference (194/194) is untouched and
retained as the parity baseline for every benchmark. The improvement search this cycle confirmed the major speed lever
is already applied and the remaining safe micro-opt is negligible, with the real next lever (low-rank freeze update)
identified and deferred as parity-risky.

Reproduce: `python3 consolidation_v161.py` (~4 s) and `python3 triple_benchmark.py` (~6 s).
