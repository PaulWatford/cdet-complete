# Integration #1 (the prefactor win): the connected determinant in O(2ⁿn²) (v132)

The first of the seven upgrades, built as a **supplement** — the frozen engine and all existing engines
are untouched. It removes both of the engine's removable costs without changing a single output.

## What the engine pays, and why it's removable

`C_V` costs O(2ⁿ·n³) + O(3ⁿ): it recomputes each of the 2ⁿ sub-determinants from scratch (an O(n³) LU
per mask) and then runs an O(3ⁿ) submask combine. Both are removable:

- **Fast principal minors.** Every D_vac[mask] = (−1)^|S|·det(M[S,S])² is a principal minor of the vertex
  matrix M; every D_corr[mask] adds the bordered minor det(M⁺[{0}∪S]). All 2ⁿ principal minors of a matrix
  come out of **one Schur-complement recursion in O(2ⁿn²)** — the fast-principal-minor algorithm that
  CoS / CDet-fast rely on (Kozik 2024 ref [45]). Two PMDs (on M and on the bordered M⁺) give every D_vac
  and D_corr.
- **Subset-convolution combine** (verified in v131): the O(3ⁿ) submask loop → O(2ⁿn²).

Chaining the two computes the entire connected determinant at **O(2ⁿn²)** instead of O(2ⁿn³ + 3ⁿ).

## Verified live against the engine

Via `cos_harness.c` (which dumps the engine's per-subset arrays and ground-truth C_V):

| quantity | check | worst dev (n=3…7) |
|---|---|---|
| fast principal minors | vs numpy det (128 minors) | 4e−14 |
| D_vac[mask] | vs engine, all masks | 1e−17 |
| **C_V** (fast-minors + subset-conv) | vs engine ground truth | **3e−15** |

So the O(2ⁿn²) path reproduces the engine exactly (to floating-point reassociation). The determinant
kernel alone is ~n/3× cheaper (e.g. ~4× at n=12), compounding with the combine win.

## Status and the supplement contract

This is a **standalone, verified computational path**, not a modification of the engine. Realizing the
speedup in production means wiring this path into the engine's hot loop in place of the per-mask LU + 3ⁿ
combine — a careful change gated by the engine's own `val`-mode validation, staged separately so the
194/194 frozen engine and the 0.00e+00 stable/plane-wave engines stay the baseline. The math is now
proven term-by-term against the real engine, which is the prerequisite for that wire-in.

It is also the prerequisite for integrations #2 (SU(N)) and #3 (self-energy): both reuse the fast-minor /
record-carrying machinery this establishes.

Reproduce: `gcc -O2 -I../engine -o cosh cos_harness.c ../engine/cdet_engine.c -lm`; `python3
fast_minors.py`. Frozen engine untouched (194/194).
