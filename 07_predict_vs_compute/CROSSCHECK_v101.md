# CROSSCHECK_v101 — consolidation: surrogate + brute-force C current, archive self-contained

**Claims.** (1) The C surrogate carries the v96–v100 coefficient-program frontier as callable
values: `surr_l6_zpol36()` = 1.8249 (one-sector frozen root), `surr_l6_cross_slope(28/36)` =
41.8/88.8 e-9 (β-growing δ₁×f₂ cross-slope), `surr_l6_root_linear(36)` above the one-sector
root toward the physical f₂\*; four new gate cases (ZPOL/XSLOPE/XGROW/XROOT) pass and the
surrogate still matches the Python reference to 1e-9 under -Wall -Werror. (2) The params header
gained the full v96–v100 status block (faithfulness falsified at 3.4σ; two-sector cross-term;
menu open {13/7, 24/13}; assembled root flow as closure). (3) The brute-force C drivers are
stamped v101, unmodified, and compile against the frozen engine. (4) The archive is
self-contained: the only true orphan (engine golden-regeneration tooling) was corrected in
place — `golden.json` ships (16 KB) and `make test` reads it for a genuine 194/194; regeneration
now points at the bundled `cdet_port.py`. The README gained a live-record pointer to
`real_patterns_v101.md` and the deep-β frontier.

**Reproduce.** `cd 08_2d_interacting && gcc -O2 -Wall -Werror -std=c11 -pedantic -o ./cst_check
csurrogate_test.c csurrogate.c -lm && ./cst_check` (ALL CASES MATCH … 1e-9); `python3 csurrogate.py`
(gate PASS); the three brute drivers compile against `engine/` sources.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
