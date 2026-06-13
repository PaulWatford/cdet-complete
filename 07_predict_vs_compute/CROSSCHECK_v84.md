# CROSSCHECK_v84 — the Class-II selection rule: two conditions, measured both ways

**Claims.** (1) The model near a level-pair midpoint: ⟨C⟩(μ) ≈ A + B·e^{−β(μ−mid)} +
C·e^{+β(μ−mid)}; a β-static flip exists iff (i) A ≈ 0 in the window and (ii) B·C < 0, sitting at
μ\* = mid + ln(−B/C)/2β — the logit-type law with the two-residue ratio. (2) Mechanism-class
discrimination by slope probe first: ln|⟨C⟩| rates ≈ ±β in the static's window (not the shallow
±0.17β of nearest-level dominance). (3) Positive case (L=8, (2,3,4), β=20): value-level zero at
1.8196; K = −0.35 (residue ratio 0.70); A = 1.06±1.04 (1.0σ — condition i); B·C < 0 (condition
ii); β-flow zero(β) = 1.8284 − 0.18/β matches v82's stored positions at max dev 0.010; the
1.707-midpoint alternatives predict 1.895 at β=12 — rejected by 0.076; pair identity (0.828,
2.828) confirmed by flow. (4) Negative case (midpoint 1.586, no static ever observed): no sign
change; A = 4.27±0.95 (4.5σ nonzero — condition i fails); B, C consistent with zero — suppression
= background dominance. The L=6 half-integer suppression now reads identically (stated
prediction). (5) Honest: the three-term fit is partially degenerate over the narrow window
(collinear basis, A↔B trade-off); the direct zero + β-flow is the robust extraction and is what
the gates test; one geometry, one case each way; why A vanishes where it does is the remaining
residue-level derivation.

**Reproduce.** `cd 08_2d_interacting && python3 selection_rule.py` → direct zero + K range;
β-flow ≤ 0.02 vs v82 stored; alternative-pair rejection; background contrast (1.0σ vs 4.5σ);
B·C < 0; no negative-window flip; live-engine sign checks; "selection-rule self-test ... PASS"
(~35 s).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
