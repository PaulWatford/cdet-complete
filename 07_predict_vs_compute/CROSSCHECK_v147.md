# CROSSCHECK_v147 — full consolidation, three models at highest capability

**Claims.** (1) Three-model architecture: frozen reference `engine/` (194/194, never altered, fast/omp targets);
production hybrid `cdet_planewave_engine.c` (validates == reference 0.00e+00, all caps: any-L, -fast, -DUSE_LD,
mode-2 freeze, 3 guards); surrogate `csurrogate.c` (carriers + new SU(N) EoS coeffs sun_c1, sun_n1). (2) The
surrogate SU(N) carriers match the python production route at N=6; surrogate addition pole == python (L=12);
fast minors live. (3) Analysis supplements kept as separate CLI modules (design directive). (4) The frozen
engine's validated numerics were not altered (trust anchor).

**Reproduce.** `cd 08_2d_interacting && python3 consolidation_v147.py`; surrogate gate `gcc … csurrogate_test.c
csurrogate.c -lm && ./a.out`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
