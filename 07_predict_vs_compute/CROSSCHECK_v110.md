# CROSSCHECK_v110 — the plateau run: no plateau, the menu identification falls

**Claims.** (1) Two distinct precision walls: the *physical* engine degrades at the determinant
level from β≈56 (2.6%→15% at β=80, vs mpmath); the *frozen* engine (which measures A) is
well-conditioned because the freeze removes the ill-conditioned occupied-far physical amplitudes —
float64-vs-long-double agree to ~1e-6 at β=64, ~1e-4 at β=80, so the v109 grid is clean. (2) float64
NaNs at β≥96; long double (`-DUSE_LD`) reaches β=120, validated (matches Python at β=36, matches
float64 to β=80). (3) The full flow z=2+ln(A/|c1|)/β rises monotonically to z(120)=1.920, still
climbing; it crosses 15/8 (β≈61), 17/9 (β≈74), 19/10 (β≈87) rather than asymptoting. (4) ρ_A still
decreasing at β=120 (not converged); z(∞)∈[1.95, 2.0], plausibly z=2. (5) Retraction: the menu-
rational identification (v93–v107) read finite-β crossings as the asymptote.

**Reproduce.** `cd 08_2d_interacting && gcc -O2 -Wall -Werror -std=c11 -DUSE_LD -o cse_ld
cdet_stable_engine.c -lm && ./cse_ld grid 80 120 20 10 2048 7777 0.002 0`; float64 grid via the
non-`USE_LD` build (`./cse grid 24 64 8 16 4096 2024 0.002 0`). Validation: `./cse val <
cdet_stable_engine_refs.txt` (PASS, both builds).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
