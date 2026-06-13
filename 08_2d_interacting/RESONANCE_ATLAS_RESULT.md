# The resonance atlas (v85): the consolidation — one spine, six audit gates, one honest catch

**What it is.** `resonance_atlas.py` integrates v80–v84 into one prediction surface: regime
classification (thermal / crossover / resonance at βΔε ≈ 8–12, empirical), Class-I flip prediction
from stored residue-polynomial roots (μ\* = ε + logit(f\*)/β), and Class-II static prediction with
the flow correction (μ\* = mid + K/2β, K = −0.355 for the 1.828 static). The unifying statement:
**every resonance-regime flip is a logit-type law μ\* = anchor + ln(ratio)/(qβ)** — Class I with
root odds at q=1, Class II with the two-residue ratio at q=2. Residues decide attendance.

**The integration audit (the self-test):**
- A. roots(1,3,5) predict the stored v81 trajectories: lower ≤ 0.006 at every β; upper ≤ 0.028
  excluding the v81-flagged β=16 jitter point.
- B. roots predict the v80 β=16 level-1-basin flips at ≤ 0.031 (the v83-flagged edge root excluded).
- C. selection-rule flow predicts the v82 static positions at ≤ 0.014.
- D. **The honest catch:** the L=6 ~1.8 flip is *unclassified* — its Class-I c drifts 3.1→5.5 and
  1.8 is neither an L=6 half-integer nor a third; likely two conflated trajectories (the v81
  window trap). Recorded on the open list, not swept under a law.
- E. Regime classification consistent with the v80 p-values (thermal at β=4, resonance at β=16).
- F. Live engine: the root-predicted (1,3,5) lower partner at β=24 (0.940) measured at 0.943.

**BEST_METHODS v85 edition** adds the arc's component table, the one-spine statement, and nine new
methodology rules (10–18), continuing the v79 nine.

**Open after consolidation:** the background-zero derivation; the unclassified ~1.8 object;
root-derived parity-anchor channel engineering; carried theory items.

Reproduce: `python3 resonance_atlas.py` (gates A–F; PASS, ~25 s). Frozen engine untouched
(194/194).
