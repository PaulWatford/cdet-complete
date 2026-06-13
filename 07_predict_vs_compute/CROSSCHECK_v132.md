# CROSSCHECK_v132 — integration #1: the connected determinant in O(2ⁿn²)

**Claims.** (1) Fast principal minors (one Schur-complement recursion, O(2ⁿn²)) give all 2ⁿ det(M[S,S]);
vs numpy det, worst 4e-14. (2) D_vac[mask]=(−1)^|S|det² reproduces the engine's D_vac for all masks (1e-17).
(3) Two PMDs (M and bordered M⁺) + the v131 subset-convolution reproduce the engine's C_V to 3e-15 (n=3..7),
at total cost O(2ⁿn²) vs O(2ⁿn³+3ⁿ). (4) Supplement only — engine untouched; wire-in is a separate
val-gated stage. (5) Prerequisite for #2 (SU(N)) and #3 (self-energy).

**Reproduce.** `cd 08_2d_interacting && gcc -O2 -I../engine -o cosh cos_harness.c ../engine/cdet_engine.c
-lm && python3 fast_minors.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
