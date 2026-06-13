# The residue ratio (v83): the flight constants derived — c = logit of the residue-polynomial roots

**The law.** Near a level ε at large β, the τ-averaged connected coefficient with its smooth
external factor stripped is a **polynomial in the level's occupancy**:

> ⟨C⟩_τ(μ) · e^{−(to−ti)(μ−ε)} = p( f_ε(μ) ),  f(μ) = 1/(1+e^{β(ε−μ)})

so every Class-I flip sits at **μ\* = ε + logit(f\*)/β with f\* a root of p in (0,1)**. The
flight constants are logits of residue-polynomial roots; the pair = two roots straddling ½; the
central pinned flip = a root near ½; per-geometry multiplicity = the root count. The polynomial
is β-independent (its coefficients are τ-integrated residue combinations); the β-flow is purely
the logit map. Lemma-grounded: v78's cancellation lemma puts all μ-dependence in the occupancies.

**The evidence** (L=6, ε=1, extraction at β=20):
- **Structure:** the curve fits a degree-4–6 polynomial in f at χ/dof ≈ 1 over the full crossing
  region (3-time object, NT=4096 common random times); a 2-time slice version fit 60× below its
  noise floor.
- **β-transfer (the derivation-grade test):** the polynomial extracted *once* at β=20 predicts the
  (1,2,4) flips at β = 12, 16, 20, 24, 28 with no refitting — median offset 0.014, max 0.022.
- **Multiplicity:** (1,2,3)'s root at 0.447 predicts its central flip (0.987 vs measured 1.01);
  (1,2,4) and (1,3,5) have p(½) ≠ 0 at 10σ / 2.4σ — central flips correctly absent.
- **Roots:** (1,2,4): 0.235/0.832 (c = −1.18/+1.60); (1,3,5): 0.190/0.828 (−1.45/+1.57);
  (1,2,3): 0.447/0.939 (the edge root flagged — its β=16 prediction 1.171 vs measured 1.11 is the
  one marginal comparison).

**Where residues creep in** (the mechanism finding the round was named for): the naive
single-level freeze — replace f_ε by a free parameter, hold everything else at μ=ε — matches the
direct curve *exactly* at s=½ and breaks down away from it, even flipping sign. The connected
object sits at a ~1e-8 cancellation floor where the **adjacent combs'** exponentially-suppressed-
but-β-compensated residues contribute at the same order. The polynomial must be extracted through
the direct curve via the logit map; the failed shortcut is documented as the boundary of the
single-level truncation.

**Retro-cleanup.** v81's fitted c's (−1.97/+1.79) were fit-basis artifacts (the r-offset/c trade
in linear-in-1/β fits); the root logits are the fundamental constants. The ln(36)/2 coincidence is
resolved as accidental — explaining v82's falsification from the inside.

**Honest scope.** One level, three geometries, n=3, axis lines; extraction at β=20; the edge-root
comparison marginal; Class-II statics and the residue-pair selection rule remain open (the same
extraction machinery now applies to them).

Reproduce: `python3 residue_ratio.py` (gates: stored-curve refit χ/dof < 2 with straddling roots;
β-transfer max offset ≤ 0.035; multiplicity pattern across three geometries; live-engine sign
pattern (+,−,+); PASS, ~40 s). Frozen engine untouched (194/194).
