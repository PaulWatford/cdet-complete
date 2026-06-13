# CROSSCHECK_v151 — sweep / stress harness (cdet_study.py)

**Claims.** (1) `cdet_study.py` scans a parameter (U/N/L/beta/mu/n) for any (target, method), collecting
x, y, error, step-time, elapsed. (2) Convergence is flagged when |Δy| < tol for k consecutive steps. (3) Cutoffs
fire: `--accuracy-cutoff` stops when error vs the reference exceeds the bound (diagrammatic Σ vs ED breaks at the
series radius ~π/β); `--max-time` stops within a wall-clock budget. (4) Outputs per run: data.csv, summary.json,
plot.png (matplotlib, graceful fallback), run.log, and a headless ASCII plot, with convergence/breakdown/cutoff/
extrema marked. (5) Plain-language sweeps work in `cdet_shell` (interpret → confirm → run → saveable).

**Reproduce.** `cd 08_2d_interacting && python3 cdet_study.py --selftest`; a real run:
`python3 cdet_study.py --target self-energy --method diagrammatic --sweep U --range 0.2:1.6:0.1 --beta 5 --mu 1 --accuracy-cutoff 1e-3`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
