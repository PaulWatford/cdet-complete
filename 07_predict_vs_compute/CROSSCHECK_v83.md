# CROSSCHECK_v83 — the residue ratio: c = logit of the residue-polynomial roots

**Claims.** (1) The law, lemma-grounded: near a level ε at large β,
⟨C⟩_τ(μ)·e^{−(to−ti)(μ−ε)} = p(f_ε(μ)) with p a low-degree polynomial (residue coefficients), so
Class-I flips sit at μ\* = ε + logit(f\*)/β, f\* = roots of p in (0,1). Pair = roots straddling ½;
central flip = root near ½; multiplicity = root count. (2) Structure verified: χ/dof ≈ 1 fits over
the full crossing region (3-time object, NT=4096 common random times); a 2-time slice fit 60×
below its noise floor. (3) β-transfer: the β=20-extracted polynomial predicts the (1,2,4) flips at
β=12–28 with no refitting; median offset 0.014, max 0.022 (≈1–2 measurement grid steps).
(4) Multiplicity across three geometries: (1,2,3)'s root at 0.447 → central flip predicted 0.987
vs measured 1.01; (1,2,4)/(1,3,5) have p(½)≠0 at 10σ/2.4σ → central flips correctly absent.
(5) The creep located: the single-level occupancy freeze (SCDet) matches the direct curve exactly
at s=½ and breaks down (sign-flipping) away from it — adjacent-comb residues contribute at the
connected object's ~1e-8 cancellation floor at the same order; extraction must go through the
direct curve via the logit map. (6) Retro-cleanup: v81's fitted c's were fit-basis artifacts; root
logits are the fundamental constants; the ln(36)/2 coincidence resolved as accidental. (7) Two
Phase-0 catches recorded: the 2-time-slice ≠ 3-time-object mismatch (Q0.2), and the s=½
machine-match isolating bug-vs-truncation in one diff.

**Reproduce.** `cd 08_2d_interacting && python3 residue_ratio.py` → stored-curve refit (χ/dof,
straddling roots), the β-transfer gate (≤0.035), the three-geometry multiplicity pattern, and a
live-engine sign-pattern check (+,−,+); "residue-ratio self-test ... PASS" (~40 s). Extraction
scripts documented in RESIDUE_RATIO_RESULT.md.

**Scope (honest).** One level (L=6, ε=1), three geometries, n=3, axis lines, extraction at β=20;
the (1,2,3) edge root marginal; Class-II statics and the selection rule open (same machinery
applies).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
