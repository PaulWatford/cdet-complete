# CROSSCHECK_v59 — freeze-then-predict derivation attempt: FALSIFIED (banked negative)

**Claims.** (1) Independent propagator decay length ξ≈0.9 (τ-averaged |G|, axial, wrap-safe).
(2) ln|C| correlates with MST connecting length (best of three variables; R²≈0.15–0.17) but with
slope ≈ −0.5 to −0.64, about HALF the naive −1/ξ ≈ −1.1 (effective decay ~2ξ, unexplained).
(3) Freezing the regression slope and predicting class-median ratios by pure geometry under-predicts
the measured ratios by 3–10× (full run: predicted 3×/5×/7× vs measured 16×/62×/30× at L=4/6/8;
self-test at L=6: predicted 2× vs measured 6×). The single-variable decay law is falsified as the
explanation of the universal weight concentration. (4) Per-class medians fluctuate across runs (L=8:
30× vs 52–82×) — the 1d class is an axis/diagonal mixture; stratify by line type henceforth.

**Reproduce.** `cd 08_2d_interacting && python3 decay_law.py` → ξ, regression slope and R²,
frozen-slope prediction vs measurement with the under-prediction factor printed; gates: slope<0,
R²∈(0.03,0.5), measured > 2× predicted (the falsification itself); "decay-law self-test ... PASS"
(~2 min).

**Scope (honest).** n=3, one β/μ, MST as Steiner proxy; medians at 400–500 samples/class are still
mixture-sensitive. The negative is the result; the mechanism question is open (v60).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
