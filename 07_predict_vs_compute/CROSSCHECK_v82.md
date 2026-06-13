# CROSSCHECK_v82 — the two-class structure: the prediction fails, the statics appear

**Claims.** (1) Phase-0 catch: deg(ε=2, L=8) = 39 exactly (hand-count 63 corrected by the script
before firing); the on-record prediction was a pair at 2 ± ln(39)/2β = 2 ± 1.832/β. (2) Verdict:
falsified as universal — windowed trajectories (grid 0.0125, NT=120, β=12–28, two geometries) show
no flips at the predicted positions; c = ln(deg)/2 is demoted to a one-level fit (L=6 ε=1).
(3) The two-class structure: Class I (Δk=1) flight pairs converging to levels (v81) with central
pinned flips at the level confirmed at L=8 (2.05→1.99→1.98); Class II (Δk=2) β-STATIC crossings at
specific level-pair midpoints — the L=8 lower-window flip is flat at 1.819±0.009 across β=12–24,
matching (0.828+2.828)/2 = 1.828 within 0.009; late-β statics at 2.121 = (1.414+2.828)/2 and
2.293 = (2+2.586)/2 within grid+jitter; window-edge registrations excluded as a documented
artifact class. (4) Retro-cleanup: v80's L=8 "1.81 cluster" was this Class-II static; the midpoint
law resurrects selectively. (5) Open, sharply posed: the residue-pair sign condition (the L=6
half-integer statics are suppressed — v80's own kill, p=0.33) and the Class-I c-formula.

**Reproduce.** `cd 08_2d_interacting && python3 level2_structure.py` → static flatness and
midpoint match; the fired prediction's failure; central flips; edge-excluded midpoint matches;
live-engine static at β=20; "level2-structure self-test ... PASS" (~30 s).

**Scope (honest).** L=8 level-2 region + the v81 L=6 corpus; two geometries; β=28 multiplicity
splitting flagged; upper statics appear only at large β; both open derivations named.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
