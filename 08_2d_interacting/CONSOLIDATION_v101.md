# Consolidation v101 — surrogate + brute-force C brought current, all mds self-contained

A sweep round (no new physics): bring the C layer and the documentation current with the v92–v100
findings, and verify nothing important is orphaned in the self-contained drop.

**The C surrogate (`csurrogate.*`).** The params header gained the full v96–v100 status block
(background alive; the v96 freeze "faithfulness" FALSIFIED at 3.4σ; the two-sector δ₁×f₂
cross-term picture; menu open among {13/7, 24/13}; the assembled root flow as the registered
closure) with new constants (`ATLAS_L6_ZPOL36`, `ATLAS_L6_A_IS36`, `ATLAS_L6_C1_FROZEN`,
`ATLAS_L6_F2STAR`, `ATLAS_L6_XSLOPE_B/D`). The surrogate now exposes the frontier as callable
values: `surr_l6_zpol36()` (one-sector frozen root 1.8249), `surr_l6_cross_slope(beta)` (the
β-growing cross-slope), `surr_l6_root_linear(beta)` (the cross-term-corrected root). Four new
gate cases pass; the surrogate still matches the Python reference to 1e-9 and builds -Wall -Werror.

**The brute-force C reference (`cdet2d.c`, `cdet_small.c`, `cdet_vs_naive.c`).** Stamped with a
v101 note: these are the exact-arithmetic, ED-validated ground truth the surrogate approximates,
intentionally unmodified; the deep-β frontier lives in the Python modules and is carried in C by
the surrogate. All three still compile against the frozen engine sources.

**Self-containment.** Audited every `.md` for references to missing modules. The only true orphan
— the engine's golden-regeneration tooling (`gen_golden.py`, `gen_golden2.py`, `cdet_reference/`),
referenced by both `START_HERE.md` and `engine*/README.md` but never bundled — was corrected in
place: `golden.json` ships (16 KB) and is authoritative (`make test` reads it, 194/194); the
regeneration path now points at the bundled Python reference (`cdet_port.py`, reproduces the
goldens to 1e-9). The README gained a live-record pointer (the ledger + the deep-β frontier +
the surrogate's role). `golden.json` confirmed present and the 194/194 check confirmed genuine.

**Audit.** Surrogate gate PASS (worst dev 3.6e-15); engine `make CC=gcc test` → 194/194; constants
bit-identical (−0.5082750022348369  0.44040518398732875); compileall clean; no remaining orphaned
module references.
