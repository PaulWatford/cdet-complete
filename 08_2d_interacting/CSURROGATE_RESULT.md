# The core C surrogate (v86): every banked advance, frozen into C beside the engine

**What it is.** `csurrogate.c/h` — a dependency-free core C module carrying the program's banked
advances, composing with (and never touching) the frozen engine:

| API | Carries | Provenance | Scope (banked) |
|---|---|---|---|
| `surr_features` | the 10 geometric features | v74 | exact port (MST-with-origin, integer rank, canonical-direction collinear groups) |
| `surr_ln_magnitude` | transferable magnitude model, frozen weights + L-intercepts | v74/v79 | median transfer error 2.3× pooled over four draws, per-draw 1.7–2.7× (v87 revision); ceiling 0.95 |
| `surr_sector` | wrap-safe coherent-sector test (cyclic line through 0) | v75 | exact, group-invariant |
| `surr_thermal_period` | π/β period law | v77/v78 | β 4–8; offsets geometry-dependent there |
| `surr_regime` | thermal/crossover/resonance | v80 | empirical βΔε ≈ 8–12 |
| `surr_class1_flips` | μ\* = ε + logit(root)/β from frozen residue-polynomial roots | v81/v83 | L=6 level 1, three geometries; β-transfer max 0.022 |
| `surr_class2_static` | μ\* = mid + K/2β, K = −0.355 | v82/v84 | the (0.828, 2.828) crossing, flow-confirmed |
| `surr_orientation` | parity stepping from one anchor + a flip set | v77/v85 | the calibrated channel protocol |

The standing wall is restated in the header: none of this moves the exponential sign problem.

**Validation, engine-style.** `csurrogate_test.c` compares every output against Python-generated
reference vectors; the gate `csurrogate.py` regenerates the references **live with a fresh seed
every run** (features via `feats2`, sector via `classify_true_rank1`, magnitude via the frozen
linear model parsed back out of the header, atlas numbers live from `residue_ratio` and
`selection_rule`), rebuilds with `-Wall -Werror`, and demands the line
"ALL CASES MATCH THE PYTHON REFERENCE TO 1e-09" — observed worst deviation **3.6e-15** across 28
configs (features ×10, ln-magnitude, sector), 15 class-1 references, 4 statics, plus regime /
period / orientation API checks.

**Generated files.** `csurrogate_params.h` (the frozen trained weights, seeds 130/131 — retraining
is the documented regeneration path) and `csurrogate_refs.h` (rewritten fresh by every gate run).

Reproduce: `python3 csurrogate.py` (~20 s). Frozen engine untouched (194/194).

**v101 consolidation.** The surrogate now carries the coefficient-program frontier as callable
values, not only comments: `surr_l6_zpol36()` (the v99 one-sector frozen-polynomial root,
1.8249), `surr_l6_cross_slope(beta)` (the v100 delta1xf2 cross-slope d1, the two measured
matched-s points interpolated; grows with beta), and `surr_l6_root_linear(beta)` (the
cross-term-corrected linear root, sitting above the one-sector value toward the physical f2*).
The params header gained the full v96-v100 status block (background alive; faithfulness FALSIFIED
at 3.4 sigma; the two-sector cross-term picture; menu open among {13/7, 24/13}; the assembled
root flow as the registered closure). Four new gate cases (ZPOL/XSLOPE/XGROW/XROOT) pass; the
surrogate still reproduces the Python reference to 1e-9 and builds -Wall -Werror.
