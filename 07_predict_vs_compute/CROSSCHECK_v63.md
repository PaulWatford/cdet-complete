# CROSSCHECK_v63 — mechanism closure: two-coefficient law locks the concentration at 1.27×

**Claims.** (1) Channeling compounds with length: paired line/bent ratio grows with matched MST
(~1.6× at ℓ=3 → ~2.7× at ℓ=4 in the survey; 1.26× → 3.28× at the self-test seeds). (2) Clean
identification on independent subsets: b = 0.537 from bulk-only regression (ℓ_coll = 0 exactly,
R²=0.16); c = +0.583 per unit collinear length from the paired line/bent matched-MST contrast (n=10,
distance cancels per pair, identical τ draws). (3) Frozen composition at the class medians
(1d: MST 4.24, ℓ_coll 4.24; bulk: 7.24, 0): exp(0.537×3.00 + 0.583×4.24) = 59× vs the measured
τ-averaged class ratio 75.5× → **agreement factor 1.27, within the gate pre-set at 2× before the
run.** (4) Two fitting traps caught and banked: spurious single-vertex collinearity credit
(direction groups need ≥2 vertices) and multicollinearity in the joint fit (ℓ_coll ≡ MST on the line
family zeroed c).

**Reproduce.** `cd 08_2d_interacting && python3 mechanism_closure.py` → b, c, per-key compounding
ratios, frozen composition and agreement factor; gates b∈(0.3,0.9), c>0.25, factor<2, compounding
monotone; "mechanism-closure self-test ... PASS" (~3 min). Narrative: MECHANISM_CLOSURE_RESULT.md.

**Scope (honest).** Semi-quantitative: coefficients measured (not derived), one lattice/order/μ/β,
b's R² low (the τ-interference scatter quantified in v60), c from 10 pairs, validated against one
held-out number. The open theory item is deriving c ≈ 0.5–0.6 from the propagator.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
