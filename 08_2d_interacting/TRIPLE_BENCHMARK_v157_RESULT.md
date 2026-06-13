# Triple-run benchmark + hybrid auto-fast improvement (v157)

The consolidation rule now runs all **three** models head-to-head and applies improvements to the evolving two.
The brute-force frozen reference is the anchor; its source is never edited (only its `make fast`/`make omp`
builds), because editing it would destroy every "validates == reference" claim.

## The three models, compared (gcc -O2, this environment)

| model | time | correctness vs anchor | strength | weakness |
|---|---|---|---|---|
| surrogate (csurrogate.c) | ~1.5 ms | dev 3.55e-15 | instant; pure arithmetic, no CDet sum | coverage-limited |
| hybrid (cdet_planewave_engine.c) | ~4 ms (val) | 0.00e+00 vs reference | exact + scalable + auto-fast | needs L=6 spectrum file |
| brute force (engine/) | ~2.5 s | 194/194 (the anchor) | exact + general (canonical) | slow; L-limited |

The chain is consistent: the surrogate carriers feed the hybrid, the hybrid validates == the frozen reference at
0.00e+00, the frozen reference is 194/194.

## Improvement found and applied — hybrid projector fast path

The triple run surfaced the hybrid's biggest lever: the `-fast` projector path collapses the modes by their
distinct eigenvalues (216 → 13, ~17×) for crystallographic L. Verified **bit-identical** to the default:
`val` stays 0.00e+00 and the grid output is unchanged.

**Applied:** auto-enable it for crystallographic L (default-on; `-nofast` escape hatch). **Retested gain:**

    grid NT=1500, L=6:   auto-fast (new default) 0.34 s   vs   -nofast (old path) 8.83 s   = ~26×

with bit-identical numbers and `val` still 0.00e+00. The **frozen reference engine/ (194/194) is untouched** — only
the hybrid (an evolving model) changed, and only its default speed, never its numbers.

## Other levers benchmarked (recorded, not adopted)

- Brute force `make fast` (-O3 -march=native) vs default: ~2% on this workload (no source edit either way).
- Hybrid -O3-native vs -O2: ~2% (the 26× win is algorithmic — the projector collapse — not the compiler).

Reproduce: `python3 triple_benchmark.py` (~6s).
