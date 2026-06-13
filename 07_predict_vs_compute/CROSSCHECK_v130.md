# CROSSCHECK_v130 — consolidation: surrogate, brute, merged hybrid

**Claims.** (1) Surrogate gained surr_lowest_empty(L,mu) and surr_friedel_edge(L,mu) (no eig); strict gate
clean, 28/28 match. (2) Brute (cdet_vs_naive/cdet_small/cdet2d) re-stamped v130, still ED-validated small-β
anchor (builds -I../engine). (3) Hybrid header merged (fast path + continuous freeze + NaN guard), validates
== stable at L=6 (0.00e+00). (4) Three-way z(∞)=lowest-empty: surrogate-C == hybrid-C == python (L=6→2.0,
8→1.41421, 12→1.26795, 48→1.00092). (5) Friedel edge surrogate-C == python. (6) Only build-hygiene drift
fixed, no numerical drift.

**Reproduce.** `cd 08_2d_interacting && gcc -O2 -Wall -Werror -std=c11 -pedantic csurrogate_test.c
csurrogate.c -lm && ./a.out`; `gcc -O2 -Wall -I../engine -o cvn cdet_vs_naive.c ../engine/lattices.c
../engine/quad.c ../engine/cdet_engine.c -lm`; `python3 dual_consolidation_v130.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
