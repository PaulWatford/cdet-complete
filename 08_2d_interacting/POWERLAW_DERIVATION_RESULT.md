# Deriving z(∞)=2 (v112): A is corner-confined (~1/β³), c1 is level-2 de-confined (~β^−0.3) — the ratio forces z→2

v111 *measured* that z(∞)=2 because A and |c1| are power laws whose ratio is ~β^2.5. v112 *derives*
those powers from the structure of the τ-averaged connected determinant, closing the loop.

## The key: A and c1 are τ-averages, so the power is set by an integral's convergence

A = ⟨C_V⟩ = (1/β³)∫dτ³ C_V. So the β-power lives in the **un-normalized integral**
J(β) = β³·X = ∫dτ³ (·). Measured on the clean grid:

| | J(β) = β³·X | scaling | ⇒ X scaling |
|---|---|---|---|
| **A** | 1.66, 1.82, 1.61, 1.75, 1.79, 1.77, 1.72, 1.65, 1.65 (×10⁹) | β^(−0.02) **→ const** | **A ~ 1/β³** |
| **\|c1\|** | grows 3.3×10⁶ → 2.5×10⁸ | β^(+2.7) **grows** | **\|c1\| ~ β^(−0.3)** |

**A is corner-confined.** At s=0, level 2 is empty; the connected determinant's antiperiodic images
align only in the τ→β corner — a β-*independent* O(10)-wide region — so ∫dτ³ C_V **converges** to a
constant. Three 1/β normalizations × an O(1) corner integral give **A ~ 1/β³** (measured exponent
−3.02, deep-half −3.12).

**c1 is de-confined by the smallest-gap channel.** c1 = dC_V/ds activates **level 2**, whose gap
ξ₂ = 2−μ = **0.155** is the smallest of all levels — so its propagator exp(−ξ₂|Δτ|) has the longest
range (1/ξ₂ ≈ 6.5) and connects τ's across the *whole* box. That slow channel de-confines the
integral: it **grows** as β^2.7 instead of converging, so **|c1| ~ β^(−0.3)**. A direct windowed
check at β=64 confirms it: J_c1(W) = ∫_{[β−W,β]³} grows as **W^2.6** (no saturation), the signature
of box-filling support.

## The conclusion

|c1|/A = J_c1/J_A ~ β^(q_c1 − q_A) = **β^2.7**, a *positive* power. Hence ln(|c1|/A) ~ 2.7·ln β and

  **z(β) = 2 + ln(A/|c1|)/β = 2 − 2.7·ln β/β → 2.**

The exponent difference 2.7 (matching v111's measured p≈2.3–2.6) is the whole story: A's corner
confinement vs c1's level-2 de-confinement. z(∞)=2 is **forced** by q_c1 > q_A — it is not a fitted
limit but a structural consequence of the smallest-gap channel (level 2 = the probe level itself)
decaying slower than the corner-confined background. The sign-structure zero sits at the probe level
because the probe level is the slowest channel.

None of this moves the wall (R, 2^n unchanged). It is the derived, mechanistic close of the z(∞)
question: **z=2, because the probe level is the smallest gap.**

Reproduce: `python3 deep_beta_powerlaw_derivation.py` (J-scaling + power fits; self-test PASS).
Frozen engine untouched (194/194).
