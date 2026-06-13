# What governs where the signed weight lives (v68)

**The answer, measured:** signed weight = (magnitude envelope) × (sign-coherence decay) × (a
filling-controlled phase).

**1. Magnitude envelope** — the v63 law: distance (b=0.537) + length-compounding channeling
(c=0.583), modulated by τ-interference (40% of variance). Where the *unsigned* weight is.

**2. Sign coherence has its own, longer decay scale.** Fitting ln r_g vs MST: **ξ_s ≈ 3.0** — about
3× the magnitude's effective decay (1.9) and the bare propagator (0.9). Binned medians: r_g 0.73
(MST<4) → 0.40 (4–6) → 0.21 (≥6). **Sign coherence outlives weight** — the compact sector is not
just heavy, it is disproportionately sign-ordered. This is why the signed answer concentrates even
harder (77% in 0.3% of configs, v67) than the unsigned one.

**3. The orientation is a filling-controlled phase — not parity.**
- **Parity falsified:** the product of sublattice signs predicts orientation at 50% (μ=0.5) and 59%
  (μ=0, the PH point itself) — coin flip both times. (Suspected mechanism for the μ=0 failure: the
  v54 equal-time dressing; suspected, not shown.)
- **The flip:** extent-3 axis lines at L=6 are **94% negative at μ=0.5 and 75–100% positive at
  μ=1.5** (extent-4 at μ=1.5: 100% positive, r_g=0.81). Same geometries, opposite orientation —
  the phase moves with the filling: the Friedel/k_F signature. This also resolves the apparent
  contradiction between L=4 lines (92% positive) and L=6 lines (negative at μ=0.5): different
  k-grids, different phase — supporting the phase picture, period not yet fitted.
- **Coherence, not positivity, is the invariant:** at matched MST 3–4, compact configs of *any*
  class are orientation-coherent (lines 85%, bulk 72%).

**Why v67 worked, restated correctly:** enumerating the compact line sector captures most of the
signed answer not because that sector is positive, but because it is *coherent* — its phase is
deterministic enough that its contributions add, while the bulk's phases scramble. (A correction of
this turn's own interim framing, on the record: "compact ⇒ positive" was wrong; "compact ⇒
coherent" is what the data says.)

**Honest scope.** The phase law is qualitative (flip with μ; coherence at small extent; ξ_s
measured) but not quantitative — no fitted oscillation period vs k_F yet; 16 geometries per extent
cell; one β. **The quantitative phase law is the open theory item** — fitting the orientation's
period against the free-fermion k_F(μ) would turn this from a mechanism into a formula.

Reproduce: `python3 sign_governance.py` (gates: coherence |2f−1|>0.4 at both fillings; orientation
flip between μ=0.5 and 1.5; ξ_s>1.5; PASS, ~2 min). Frozen engine untouched (194/194).
