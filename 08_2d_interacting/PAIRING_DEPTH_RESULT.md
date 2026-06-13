# Pairing depth (v71): the phase has NO finite depth — no single free determinant carries it at all

**The question (rotation item a, run surrogate-first per the new standing mode):** does the
orientation phase emerge at finite pairing depth — chain + leading exchange, or a few terms more?
The candidate predictors are pure free-fermion arithmetic (Matsubara cycle sums over permutation
subsets of the free 4-point τ-integrated determinant); the engine's only role is the orientation
crosscheck cells. **Pre-registered gates:** (i) depth-2 ≥75%? (ii) full depth (all 24 pairings) ≥75%?

**Result — both gates FAIL, and the full-depth failure is the headline:**

| depth k | 1 | 2 | 4 | 24 (complete) |
|---|---|---|---|---|
| OOC mean | 46% | 46% | 63% | **44%** |

(Calibration cell: 93% at every depth — meaningless by itself, the v69 lesson.) The engine-matched
**external-time-fixed variant gives identical numbers.** The curve is non-monotonic and never
approaches the gate; the *complete* single free determinant predicts the orientation no better than
chance-ish.

**The sharpened conclusion.** v69 said "determinant-level." v71 says: not in *any single*
determinant of free propagators over the geometry. By elimination, the phase lives in the **coupled
product of the two spin determinants integrated over shared vertex times** (plus the
connected/vacuum subtraction) — i.e., in the engine integrand itself. This is consistent with v54
(the value channel's −1 is a cross-spin dressing) and v60 (τ-interference at 40% of variance).

**The reduction ladder, complete (all frozen-protocol, all falsified):**
static parity 50–59% (v68) → static single-particle predictors 34% (v69) → τ-integrated dominant
chain 64% (v69) → single free determinant at any depth ≤63%, full depth 44% (v71).

**Surrogate consequence (the frame this pass was asked in):** no physics-reduced orientation channel
exists below the engine integrand. The remaining surrogate route for orientation is a *learned*
statistical channel (fit orientation directly vs geometry/μ/L) — queued for a future surrogate pass.

**Honest scope.** Axis lines, n=3, one β, 14 geometries/cell, 8 survey cells; "no single
determinant" covers the free-propagator determinant in both time conventions tested;
dressed-propagator determinants untested.

Reproduce: `python3 pairing_depth.py` (gates: calibrations >80%; depth-2, depth-24, and
external-fixed full depth all OOC <70%; PASS, ~2 min). Frozen engine untouched (194/194).
