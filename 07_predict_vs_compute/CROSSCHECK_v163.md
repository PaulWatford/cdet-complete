# CROSSCHECK_v163 — unified `cdet` CLI

**Claims.** (1) A single top-level `cdet` command wraps the suite: validate, converge, resum, eos, run, sweep, lab,
shell, info — each with `--help`. (2) Output is rich-optional: pretty tables/panels if `rich` is installed, clean ASCII
otherwise, so the package needs no external dependency. (3) `cdet validate` runs all gates green in one table (frozen
194/194, surrogate, hybrid 0.00e+00, 2D plane-wave, consolidation). (4) Snappy defaults (resum/eos N=4, ED-validated);
N≥6 guarded by a status note + disk cache. (5) Frozen engine used read-only.

**Reproduce.**
```
python3 cdet.py --selftest      # gate
python3 cdet.py validate        # all gates green
python3 cdet.py converge        # 4x4 -> 100x100 TD table
python3 cdet.py resum           # conformal-Borel vs Pade
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
