# CROSSCHECK_v80 — the resonance regime: the KT-review round

**Claims.** (1) Phase-0 reversal: fine-grid (0.025) β=4 median flip spacing 0.625 (q≈1.26) — the
banked 0.70 was grid-inflated; two spacing populations already at β=4. (2) The two-regime law:
flips attract to single-particle levels with growing β (mean-distance ratio vs frozen uniform null
0.87/0.86/0.71–0.84/0.79 at β=4/8/12/16; p=0.025 at β=12 and β=16 in independent runs) and become
geometry-independent (cross-geometry median nearest-flip distance 0.020 at L=8 β=16 p=0.032 [stored
seed: 0.013], 0.025 at L=6 p=0.041 [stored: 0.013]; vs 0.075, p=0.19 at β=4). (3) The v77 "β≥12
unmeasurable" boundary is retracted — the 0.40-vs-1.50 disagreement was intra- vs inter-cluster
spacing; note added atop MU_PERIOD_RESULT.md. (4) The naive levels∪midpoints law killed at L=6
(p=0.33); flip trajectories convergent (1.988→2; one family ≈ 1+ln4/β); the L=6 core set
{0.94,1.09,1.79,1.99} external-time-independent (three (to,ti) pairs; max drift 0.025; the
2(to+ti)=1.8 coincidence killed by its own discriminator). (5) Cross-geometry orientation transfer
is bimodal: 79–87% within the multiplicity-matched cluster, 32–47% against the odd-multiplicity
geometry — positions universal, multiplicities residue-dependent. (6) Method provenance: the round
applied the KT-RG method (IS/IS-NOT, Phase-0, escalation ladder, discriminator tests) per user
direction; three lessons banked in #90.

**Reproduce.** `cd 08_2d_interacting && python3 resonance_regime.py` → level-attraction p<0.05;
cross-geometry p<0.05 at both L; midpoint kill; external-time independence; bimodal transfer; live
engine core-flip check; "resonance-regime self-test ... PASS" (~30 s). The survey scripts (fine-grid
batteries, flow, toti discriminator) are documented in RESONANCE_REGIME_RESULT.md.

**Scope (honest).** Axis lines, n=3; flip counts fluctuate run-to-run at β≥20 while stable core
positions recur; the universal limit set is characterized but not identified (open program:
degeneracy-weighted ΔE/Δk with ln g/β corrections).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
