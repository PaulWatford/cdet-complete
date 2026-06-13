# The value channel's −1 (dressed) and the slice hierarchy of the cube (v54)

Two computed results. Reproduce both: `python3 value_channel_slices.py` (PASS).

## 1. The −1 we hunted lives in the value channel — but it is dressed by a counterterm

Every geometric operation (v50–v52) could only fold (+1), because a site permutation commuting with H
fixes the propagator on all indices. The one channel that could carry a −1 is **particle-hole**, which
acts on the propagator's *values*. Measured on the engine propagator (bipartite, sublattice signs ε):

| piece | identity | max err |
|---|---|---|
| off-diagonal, any τ | G(−μ)(i,j,τ) = −ε_i ε_j G(μ)(j,i,−τ) | 2.5e-11 (square), 1.8e-08 (cube) |
| off-diagonal, τ=0 | same | 2.5e-16 / 4.7e-16 |
| **diagonal, τ=0 (0⁻)** | **G(−μ)(i,i,0) + G(μ)(i,i,0) = 1** | 1.1e-15 / 8.9e-16 |

So exactly: **G(−μ) = −D_ε G(μ)ᵀ D_ε + I|_equal-time**. The transpose carries the −1; but PH maps the
0⁻ equal-time convention to 0⁺, and the difference is the identity on the equal-time diagonal — a
contact/**density counterterm**, precisely the v46 d/dμ object.

**Consequence (measured, the honest part).** The naive predictions fail by computation:
C_V(V′;−μ)/C_V(V;μ) is wildly non-constant (std up to 5e3), and the algebraically derived bare −1
(externals swapped, same times) also fails (off by up to 1.5e3) — because every determinant's
equal-time diagonal picks up the +1. The truth is an **operator identity between observables**:
C_V at −μ equals −(C_V with externals swapped) at +μ **plus a computable counterterm tower** from
the equal-time diagonal — not a per-configuration cancellation at fixed μ. The sign wall is untouched;
what the value channel actually provides is the doping reflection μ ↔ −μ with exact, computable
corrections (composable with the v45–v47 shift/contour machinery).

**The elimination is now complete and mechanistic:** label channels fold (+1, proven); the value
channel carries the −1 but dressed into an inter-observable identity. There is no per-config −1 at
fixed μ in either channel — measured, with the exact mechanism (the equal-time sum rule) identified.

## 2. The cube's weight and sign concentrate on low-dimensional slices

A cube admits 0d/1d/2d/3d slices through the external site. Classifying sampled n=3 configs by the
dimension of the affine span of (external + vertices) (minimal-image torus displacements), 4×4×4,
μ=0.5, 4000 configs:

| span dim | share of configs | share of \|weight\| | concentration | per-class R |
|---|---|---|---|---|
| 1 (line) | 0.3% | 5.6% | **×18.5** | 0.224 |
| 2 (plane) | 20.5% | 43.0% | ×2.09 | 0.089 |
| 3 (bulk) | 79.2% | 51.5% | ×0.65 | 0.004 |

**Pattern:** weight density falls ~an order of magnitude per added dimension (mean |C|: 3.2e-06 →
3.6e-07 → 1.1e-07), and the per-class sign quality collapses with dimension. Locality appears as a
slice hierarchy: configurations confined to lines/planes through the external dominate per config and
carry the best sign; the bulk is numerous, individually tiny, and nearly sign-dead.

**The hint this gives for what to do next:** slice-stratified evaluation — compute the low-dimensional
slice classes exactly/cheaply (they are few: a cube has 3 axis lines + 6 diagonal lines and 3+6 planes
through a point, each a lower-dimensional sub-lattice, and they carry outsized weight at the best
sign), and spend sampling only on the 3d remainder (numerous, tiny, worst sign — i.e. variance lives
there). Stratification by an exactly-known label never biases; the candidate gain is concentrating
exact work where weight concentrates. This is the v55 candidate, to be tested before claimed.

Honest scope: the slice numbers are one lattice (4×4×4), one order (n=3), one μ — a measured pattern
and a hypothesis generator, not yet a law. Frozen engine untouched (194/194).
