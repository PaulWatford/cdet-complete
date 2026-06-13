# CROSSCHECK_v109 — the stable C deep-β engine; v107's A was biased low; 15/8 falls; asymptote unpinned

**Claims.** (1) `cdet_stable_engine.c` (frozen connected determinant + log-domain propagator,
reading `spectrum_l6.bin`) matches the Python stable engine's C_V to machine precision (worst
significant rel dev 0.0 above the 1e-13 floor) and high-statistics Python A(40)=0.262(9) vs
0.267(4). (2) Speed: a 6-point grid to β=64 in 150 s. (3) v107's A(40)=0.119(28) was heavy-tail-
biased low (true 0.267), so z(∞)=1.882 was an underestimate. (4) The corrected leading-order flow
z=2+ln(A/|c1|)/β rises 1.780→1.878 over β=24→64, still climbing; 15/8=1.875 is disfavored (the
flow passes through it); asymptote ≥1.88 (17/9 or higher). (5) Honest limit: the asymptote is not
pinned — 1/β fit 1.933, 1/β² fit 1.961, both poor χ² (the flow still curves at β=64). (6) Internal
consistency: the leading flow sits below the robust pool by a shrinking cross-term lift
(+0.013/+0.005/+0.003 at β=36/44/52).

**Reproduce.** `cd 08_2d_interacting && python3 cdet_stable_engine_dump.py` (regenerate spectrum +
refs); `gcc -O2 -Wall -Werror -std=c11 -o cse cdet_stable_engine.c -lm && ./cse val <
cdet_stable_engine_refs.txt` (validation PASS); `./cse grid 24 64 8 16 4096 2024 0.002 0`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
