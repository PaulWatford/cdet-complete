# CROSSCHECK_v111 — z(∞) resolved: the bare probe level z=2; the menu was a ln(β)/β approach

**Claims.** (1) On the clean 9-point flow (β=24–120), the exponential-gap model ln(|c1|/A)=ρβ+q
(→ a sub-2 menu rational) is rejected at χ²=622/7. (2) The power-law model ln(|c1|/A)=p·ln β+q
(→ z(∞)=2) fits (χ²=37/7, residuals 0.003 in z); the general fit gives z(∞)=1.991(2). (3) Both A
(~β^−2.8) and |c1| (~β^−0.54) are power-law dominated (rates ≈ 0), so their ratio is β^2.3 and
z(β)=2−2.3·ln β/β → 2. (4) The menu rationals (11/6…17/9) are finite-β crossings of a ln(β)/β
approach, not asymptotes.

**Reproduce.** `cd 08_2d_interacting && python3 deep_beta_asymptote.py` (model comparison +
power-law fits; self-test PASS). Grid data from `cdet_stable_engine` (`./cse grid …` float64 24–64;
`./cse_ld grid …` long double 80–120).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
