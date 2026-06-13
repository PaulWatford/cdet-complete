# CROSSCHECK_v127 — the v116 selection rule vs large L: a finite-gap Friedel phenomenon

**Claims.** (1) Prediction (rule persists uniformly) partially falsified. (2) sign(A) converges (stable −,
one flip at L=12; bulk background). (3) sign(c1) Friedel-oscillates with L (24:−, 32:+, 40:−, 48:+),
seed-stable (L=24 −/L=32 + across seeds 31/17/99; L=40 −/L=48 + across 31/17) — real Friedel, not noise.
(4) Outcome (physical iff opposite signs) alternates; |c1|→0 so the selection goes marginal in the
continuum. (5) The rule is a finite-gap Friedel phenomenon; only the background sign survives.

**Reproduce.** `cd 08_2d_interacting && gcc -O2 -Wall -Werror -std=c11 -pedantic -o cpw
cdet_planewave_engine.c -lm`; for L in 24,32,40,48: `./cpw grid 24 24 1 12 2048 31 0.002 2 2 1 2 4 1.0 -L
<L> -fast` (signed A col 2, c1 col 4); seed-check with seeds 17,99; `python3 selection_rule_continuum.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
