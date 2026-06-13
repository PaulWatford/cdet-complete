# CROSSCHECK_v115 — full dual consolidation at the frontier; the three-layer chain

**Claims.** (1) Surrogate brought current: `surr_l6_z_inf()` now returns 2.0 (was 1.8818), with
`surr_l6_z_finite(β)` the ln(β)/β law and `surr_l6_z_inf_legacy()`=1.8818 for the record. (2) Brute-
force C re-stamped v115, caveat points at the built `cdet_stable_engine.c`. (3) Rebuild test all
green (gate, stable C both builds, stable propagator, brute drivers, 4 analysis modules, frozen
194/194, constants). (4) Side-by-side: z(∞) surrogate 2.0 / stable-C 2.0 / brute-C too shallow;
benign agreement; deep β only stable-C correct; speed 7.4 / 14.2 / 17.4 ns. (5) The duality is a
chain — each layer covers a blind spot; the cross-validation caught every deep-β error.

**Reproduce.** `cd 08_2d_interacting && python3 csurrogate.py` (gate PASS); `gcc -O2 -Wall -Werror
-std=c11 -o cse cdet_stable_engine.c -lm && ./cse val < cdet_stable_engine_refs.txt` (PASS, both
`-DUSE_LD` and not); `./cdet_small ring 6 2.0 1.0 1.0 0.7 0.2` (brute benign).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
