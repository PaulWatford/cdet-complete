# CROSSCHECK_v116 — site-choice generalization: z(∞)=2 geometry-independent; sign is geometric

**Claims.** (1) The engine grid takes optional sites (args 11–13). (2) Over 5 geometries
(β=24/48/72), z = 2+ln(|A|/|c1|)/β rises monotonically toward 2 in every triple — z(∞)=2 is
geometry-independent (registered prediction confirmed). (3) The approach rate varies (|c1| ranges
16–807). (4) The sign of (A,c1) varies by geometry: opposite → physical leading root s*=−A/c1>0;
same → s*<0. (5) z(∞)=2 is doubly universal (probe- and site-independent); the sign structure is the
geometric degree of freedom.

**Reproduce.** `cd 08_2d_interacting && python3 site_generalization_test.py` (self-test PASS); grids
via `./cse grid 24 72 24 10 2048 31 0.002 0 2 <s0> <s1> <s2>` (e.g. `1 2 4`, `10 80 150`).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
