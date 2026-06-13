# Mechanism closure (v63): the two-coefficient law locks the concentration within 1.27×

**The chase.** v62 left a ~4× residual: distance × flat-2× channeling composed to only ~16× of the
measured ~75× class gap. The question pre-registered for v63: does channeling **compound with
length**? Lockdown gate pre-set before the run: frozen prediction within **2×** of the measured
75.5×.

**Finding 1 — channeling compounds.** The paired line/bent ratio grows with matched MST: ~1.6× at
ℓ=3 → ~2.7× at ℓ=4 in the survey run (self-test seeds: 1.26× → 3.28×). Fit c ≈ +0.5 per unit
collinear length. The v62 "~2×" was the average over a growing function.

**Two traps caught on the way (banked as lessons):**
1. **Spurious credit** — a first ℓ_coll definition let a *single* vertex count as a line with the
   external, handing bulk configs channeling credit for their longest leg (double-counting
   distance). Corrected: a direction group needs ≥2 vertices.
2. **Multicollinearity** — in a joint fit, the line family has ℓ_coll ≡ MST identically, so the
   regression zeroed c and inflated b. Cure: **clean identification** — measure each coefficient
   where the other cannot contaminate it.

**The lockdown result (L=6, β=4, μ=0.5, n=3):**

| quantity | value | identified from |
|---|---|---|
| b (distance) | **0.537** (R²=0.16) | bulk-only regression (ℓ_coll = 0 exactly) |
| c (channeling) | **+0.583** /unit collinear length | paired line/bent matched-MST contrast (n=10; distance cancels per pair) |
| frozen composition | exp(0.537×3.00 + 0.583×4.24) = **59×** | class medians (1d: MST 4.24, ℓ_coll 4.24; bulk: 7.24, 0) |
| measured | **75.5×** | v60 session, τ-averaged class medians |
| **agreement** | **1.27× — LOCKED** (gate was 2×) | |

**Honest scope.** Two coefficients identified on independent subsets, validated against one held-out
number; one lattice/order/μ/β; b's R² is low (per-config scatter = the τ-interference already
quantified at 40% in v60); c rests on 10 matched pairs. A semi-quantitative mechanism law with
*measured* coefficients, not a first-principles derivation. **Closed:** *where* the universal
concentration comes from — distance decay compounded with length-growing 1d channeling, modulated by
τ-interference. **Open:** *why* c ≈ 0.5–0.6 (a propagator calculation not yet attempted).

Reproduce: `python3 mechanism_closure.py` (gates: b∈(0.3,0.9), c>0.25, composition within 2×,
compounding monotone; PASS, ~3 min). Frozen engine untouched (194/194).
