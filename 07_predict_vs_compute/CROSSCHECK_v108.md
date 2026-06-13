# CROSSCHECK_v108 — consolidate + side-by-side both C layers; dual insights

**Claims.** (1) Surrogate brought current with v104–v107: new carriers `surr_l6_z_inf()`=1.8818
and `surr_l6_pool(β)` agree with the stable ground truth; the superseded menu lines (13/7, 11/6)
diverge from the resolved asymptote at 1.8 / 2.2σ and are retired. (2) Brute C re-stamped v108
with the precision caveat: its naive `G0_atom` is benign-correct (ED-validated) but deep-β-wrong
(naive −0.000000 vs analytic −0.049787 at β=36, ξ=−3, τ=35). (3) The log-domain `G0_atom_stable`
(`cdet_stable.c`) matches the frozen propagator at benign β (1e-12) and is deep-β-correct,
certified vs the Python stable / mpmath path. (4) Speed: stable C is 1.29× the naive call (22.4 vs
17.3 ns) and ~1000× the Python stable g0 (21375 ns) — a stable C engine is the enabler for the
denser grids v107's z(∞)=1.88(2) needs. (5) Dual insight: both layers inherit one flaw (the naive
propagator) and take one cure (the log-domain form).

**Reproduce.** `cd 08_2d_interacting && python3 csurrogate.py` (surrogate gate PASS); and
`gcc -O2 -Wall -Werror -std=c11 -I. -I../engine cdet_stable_test.c cdet_stable.c
../engine/cdet_engine.c -lm -o ./cst_stable && ./cst_stable` (benign match + deep-β stable-correct;
PASS).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
