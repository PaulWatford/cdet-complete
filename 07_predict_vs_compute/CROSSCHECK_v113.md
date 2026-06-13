# CROSSCHECK_v113 — the "single de-confined mode" sharpening: real channel, but it saturates

**Claims.** (1) ξ₂ < ξₙ is true: ξₙ = levelₙ−μ puts level 2 (the probe) closest to μ=1.845
(ξ₂ = 2−μ = 0.155), smaller than every level above μ — the phase response c1 is carried by this
single channel (= v112). (2) The literal c1 = Σₙ aₙ e^(−ξₙβ) is falsified: it predicts |c1| decay
of e^(0.155·96) ≈ 2.9×10⁶ over β=24→120; measured drop is 1.66× (effective rate 0.0046). (3) The
level-2 propagator saturates: ∫₀^β exp(−ξ₂τ)dτ → 1/ξ₂ = 6.45, a rate-0 factor — so integrated c1
is a power law, not an exponential mode. (4) gap (2−μ) = de-confinement range 1/(2−μ) ≈ 6.5 and the
limit z(∞)=2, not a β-rate.

**Reproduce.** `cd 08_2d_interacting && python3 spectral_channel_test.py` (gap ordering, exp-form
test, saturation; self-test PASS).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
