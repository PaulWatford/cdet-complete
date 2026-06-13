# Consolidation pass: surrogate, brute force, and merged hybrid brought current (v130)

A consolidation sweep bringing all three engines current to the v124-v129 program and cross-validating
them side by side.

## What was updated

**Surrogate** (`csurrogate.c/.h`, `csurrogate_params.h`). Added two L-generalized carriers, both pure
cosine arithmetic with **no eigendecomposition**:
- `surr_lowest_empty(L, mu)` — the scale law z(∞) for any L (= the lowest-empty eigenvalue; marches to μ
  as L→∞, gap ~ L⁻³·³).
- `surr_friedel_edge(L, mu)` — the v129 density-matrix Friedel edge (half-max of W(kx)) → ~0.347 (120°).

Banner updated with the v124-v129 program. Strict gate (`-Wall -Werror -pedantic`) clean; 28/28 reference
cases match (worst dev 3.55e-15).

**Brute force** (`cdet_vs_naive.c`, `cdet_small.c`, `cdet2d.c`). Re-stamped v130 — still the ED-validated
naive-but-benign small-β anchor; the deep-β / large-L frontier now lives in the hybrid. Builds from the
frozen engine sources (`-I../engine`).

**Merged hybrid** (`cdet_planewave_engine.c`). Header consolidated — one engine carries phase-1 laws +
phase-2 connected determinant + projector fast path (`-fast`) + continuous freeze (mode 2) + NaN guard;
validates == stable engine at L=6 (0.00e+00).

## Three-way cross-check of z(∞)=lowest-empty(L,μ)

| L | μ | surrogate(C) | hybrid(C eng) | python | agree |
|---|---|---|---|---|---|
| 6 | 1.845 | 2.00000 | 2.00000 | 2.00000 | ✓ |
| 8 | 1.0 | 1.41421 | 1.41421 | 1.41421 | ✓ |
| 12 | 1.0 | 1.26795 | 1.26795 | 1.26795 | ✓ |
| 48 | 1.0 | 1.00092 | 1.00092 | 1.00092 | ✓ |

Friedel edge (v129): surrogate-C 0.4250 / 0.3604 / 0.3483 / 0.3472 == python (L=6/24/96/384).

## Lesson (recurring)

The dual is a **chain**: the surrogate *carries* the laws (C, no eig), the hybrid *derives* them
(plane-wave determinant), python *references* them, the brute *anchors* at small β. Cross-validation keeps
all four mutually consistent. This pass found and fixed only build-hygiene drift (a missing `stdlib`
include, `calloc` initialization for the strict gate, the brute include path) — **no numerical drift**:
the v124-v129 physics is carried identically across all three engines.

Reproduce: `gcc -O2 -Wall -Werror -std=c11 -pedantic csurrogate_test.c csurrogate.c -lm && ./a.out`
(gate); `python3 dual_consolidation_v130.py`. Frozen engine untouched (194/194).
