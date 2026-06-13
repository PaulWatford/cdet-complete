# CROSSCHECK_v107 — the assembled root flow: z(∞) from the rate difference

**Claims.** (1) Measured clean on the stable engine + MoM (uniform grid β=24/32/40/48):
A(β)=1.328(217)/0.357(125)/0.119(28)/0.051(23) (fast) and c1(β)=−319.8(69.9)/−193.8(49.5)/
−195.4(20.7)/−172.2(16.0) (slow). (2) Leading static s\*=A/|c1| → z(∞)=2−(ρ_A−ρ_c1); with MC
error propagation ρ_A=0.1406(158), ρ_c1=0.0225(95) → **z(∞)_leading = 1.8818(184)**. (3) This is
above the lower menu: 24/13 (1.9σ) and 13/7 (1.3σ) disfavoured; 15/8=1.875 (0.4σ) and 17/9=1.889
(0.4σ) consistent — 15/8, declared dead in v94/95 on naive data, is resurrected. (4) Internal
consistency: the leading-order finite-β flow sits ~0.03 below the robust pool — the v100 cross-term
— so the measured-full-static and assembled-leading+cross routes agree, both rising to ~1.88. (5)
Limits: leading order, 4 points/series, 10–40% rate errors; robust claim is ρ_A ≫ ρ_c1 and the
lower menu disfavoured by two independent methods.

**Reproduce.** `cd 08_2d_interacting && python3 deep_beta_resummation.py` (channels; known-rate;
assembled z_inf; PASS ~5 s).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
