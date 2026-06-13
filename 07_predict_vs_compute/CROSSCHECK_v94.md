# CROSSCHECK_v94 — the side-by-side: parity-locked surfaces, frozen out-of-sample test, identification reopened

**Claims.** (1) Both surfaces carry the v93 law plus the 13/7 competitor with C↔Python parity at
1e-15 across six β (verified inside the csurrogate gate). (2) Out-of-sample predictions were
frozen to disk before measurement; the brute-force honest protocol then gave z(44) = 1.8510 ±
0.0076 and z(52) = 1.8527 ± 0.0052 → χ² 5.3 vs 1.0 — ~9:1 for 13/7 against the frozen 11/6 line,
reversing the v93 in-sample 80:1: the identification is **reopened**. (3) The six-point pool
(β=36–56) admits 11/6 (refit χ²/dof 0.96), 13/7 (0.32), and a constant 1.8467 ± 0.0021 (0.47);
the constant reading puts the octagon chord at 0.5σ and both menu rationals at 5–6.5σ — the
menu-vs-flatness tension, raising the degree bound (weight ≤ 6 at n=3?) as the decisive queued
item. (4) z(30) = 1.8138 ± 0.0037 demonstrates the law's scope floor: both lines miss by ≥8σ
inside the v92 crossover window, as they must. (5) A harness root-selection bug (quadratic root
outside the bracketing window) was caught at β=30 and fixed; the law's derivation, field
theorem, and L=8 verification stand unrevised.

**Reproduce.** `cd 08_2d_interacting && python3 law_sidebyside.py` (four gates: frozen scoring;
six-point fits; tension; scope; PASS <1 s); `python3 csurrogate.py` (parity + DEEPLAW);
`python3 resonance_atlas.py` (A–I); `python3 exponent_balance.py` (the v93 record, revised
header, still PASS).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
