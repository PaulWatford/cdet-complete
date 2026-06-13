# CROSSCHECK_v112 — deriving z(∞)=2: corner-confined A, level-2 de-confined c1

**Claims.** (1) A and c1 are τ-averages (A = (1/β³)∫dτ³ C_V), so the β-power lives in
J(β) = β³·X. (2) J_A → const (β^−0.02; deep-half β^−0.12) ⇒ A ~ 1/β³ (corner-confined: the s=0
images align only in a β-independent corner). (3) J_c1 ~ β^+2.7 ⇒ |c1| ~ β^−0.3 (de-confined by
the smallest-gap level-2 channel, ξ₂ = 2−μ = 0.155, longest-range propagator). (4) Windowed at
β=64: J_c1(W) ~ W^2.6, no saturation — box-filling support. (5) |c1|/A ~ β^2.7 forces
z(β) = 2 − 2.7·ln β/β → 2; z(∞)=2 because the probe level is the smallest gap.

**Reproduce.** `cd 08_2d_interacting && python3 deep_beta_powerlaw_derivation.py` (J-scaling + power
fits; self-test PASS). Grid data from `cdet_stable_engine`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
