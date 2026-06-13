# CROSSCHECK_v121 — the elementary Friedel object ρ(0,r) ported to C

**Claims.** (1) `cfriedel.c` computes ρ(0,r) = (1/N)Σ_{ε(k)≤1} cos(k·r) from the plane-wave structure —
no eigenvectors, no spectrum file, no eigendecomposition. (2) `cfriedel test` passes (9 embedded refs,
worst 4.8e-11). (3) Full 216-point cross-check vs the Python eigh density matrix: worst dev 4.81e-11.
(4) The C map (`cfriedel map 0`) is identical to the v119 Python map; occupied=156; integer-spectrum
μ-rigid. (5) Closes the v120 open fix — the sign side now has full three-layer C coverage.

**Reproduce.** `cd 08_2d_interacting && gcc -O2 -Wall -Werror -std=c11 -pedantic -o cfriedel cfriedel.c
-lm && ./cfriedel test`; cross-check vs `frozen_friedel_map.py` (numpy eigh of cube_hopping(6)).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
