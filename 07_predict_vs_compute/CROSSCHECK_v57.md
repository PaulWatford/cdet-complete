# CROSSCHECK_v57 — the slice hierarchy survives scale (weight strengthens; sign persists, narrows)

**Claims.** (1) FastCDet (vectorized eigenmode loop) is value-identical to the frozen-port-validated
CDet: max diff 4.2e-17 over random configs n=1..3 on the 4×4×4 (self-test gate 1e-12). (2) With
targeted 1d-line sampling vs matched bulk samples (900 each; ratio noise floor 0.027), the 1d/bulk
per-configuration weight ratio GROWS with size — 32× (L=4) → 74× (L=6) → 165× (L=8) — and R(1d) beats
the bulk at every size (0.652/0.366/0.244 vs 0.062/0.064/0.157). Uniform-sample d=2 concentration
grows 2.06× → 3.35× → 4.34×. (3) v54's d=1 R=0.224 is refined on the record (12-config noise; the
targeted value at L=4 is 0.652). Flagged unresolved: the L=8 bulk R=0.157 sits above the floor —
possible heavy-tail inflation of the ratio estimator.

**Reproduce.** `cd 08_2d_interacting && python3 slice_scaling.py` → validation gate, then L=4 and L=6
class stats with gates (density ratio grows with L; R(1d) > R(bulk)+floor at both); prints
"slice-scaling self-test ... PASS" (~60 s). The L=8 row reproduces via `line_class_stats(FastCDet(
cube_hopping(8),...), 8)`.

**Scope (honest).** Cubic lattices, n=3, one μ, one β; ratio R for near-zero means is noisy — floors
quoted; the conceptual statement is a measured geometric structure, not yet a derived theory.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
