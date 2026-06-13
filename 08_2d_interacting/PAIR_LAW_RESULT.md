# The pair law (v81): the limit set identified — flips converge to the levels as ε ± c_ε/β

**The measurement** (windowed trajectory flows: grid 0.0125, NT=120, β=12→28, two geometries,
L=6 around level ε=1):

| trajectory | r (limit) | c | rms |
|---|---|---|---|
| (1,2,4) lower | 1.047 | −1.97 | 0.006 |
| (1,2,4) upper | 1.004 | **+1.79** | **0.004** |
| (1,3,5) lower | 1.019 | −1.83 | 0.001 |
| (1,3,5) upper | 0.959 | +2.50 | 0.027 (the noisy outlier) |

**The law:** μ\*± = ε ± c_ε/β — the resonance-regime flip positions converge **to the
single-particle levels**, two-sidedly, as a flip pair tightening like 1/β. The candidate-set hunt
of v80 is over: **the limit set is the spectrum**, and every "midpoint" ever sighted (L=6 *and* the
L=8 0.707/1.000/1.828 coincidences) was a pair partner in flight. This retro-explains v80's level
attraction, the geometry-independent universal set, and the intra-cluster spacing scale (2c_ε/β).

**The candidate arrangement (stated as candidate, not proved):** c = ln(deg(ε))/2. The L=6
degeneracy of ε=1 is exactly 36, and ln(36)/2 = ln 6 = **1.792** — a 0.4% hit on the cleanest fit,
inside the pooled spread (|c|pooled = 2.02 ± 0.3). Forward mechanism sketch: each flip is a
crossing of two Boltzmann families differing by one particle *at the level*; μ\* = ε +
ln(g_ratio)/(βΔk); degeneracy enters the residue ratio; the symmetric pair is the particle-side
and hole-side crossings. Deriving the exact ratio (and the ½) is the open forward-proof step.

**Honest residuals.** Level 2's partners are grid-pinned (motion per β-step < the 0.0125 grid) and
its window conflated partners at β=12 — an analysis trap caught and recorded (per-window min-flip
mixes the pair when both enter); consistent with limit 2 within ~0.04, not fit-grade. The (1,3,5)
upper fit is the outlier (early-β multiplicity jitter). Flip *counts* still fluctuate run-to-run at
β≥20; the recurring flip *positions* are what the law governs.

**The prediction it makes (falsifiable):** at any L and any level, the pair tightens as
ln(deg)/2β — e.g., L=8's ε=2 (its degeneracy computable exactly) fixes that pair's flight path
with no free parameters.

Reproduce: `python3 pair_law.py` (gates: four fits with r within 0.06 of the level, pair-symmetric
signs, c in range; the ln(36)/2 candidate within pooled spread; a live-engine partner check at
β=24; PASS, ~30 s). Frozen engine untouched (194/194).
