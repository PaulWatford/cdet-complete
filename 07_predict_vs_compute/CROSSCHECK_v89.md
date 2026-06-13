# CROSSCHECK_v89 — the deep partner: identification, closures, and the creep in position

**Claims.** (1) Level-2's residue polynomial at L=6 ((1,2,4), β=20, small-f-weighted grid,
NT=4096) has three roots: 0.0116 / 0.4437 / 0.9504 (c = −4.44 / −0.23 / +2.95); the curve refits
at χ/dof ≈ 0. (2) Identifications: the unclassified ~1.8 object (v85 gate D) = the deep lower
partner (f\*=0.0116, Class I); v80's dangling "2.2 family" = the upper partner (predictions
2.185/2.148/2.123 vs the stored v80 flow 2.188/2.138/2.112, devs 0.003–0.011); the central root
matches v81 at β≥16 with max dev 0.010. (3) The v85 "c-drift" is quantified as sign-scan noise:
through the deep crossing |p| ≈ 0.4–5e-9 vs the v81 NT=120 sem ≈ 3.2e-9 — signs noise-dominated
over ±0.04. (4) Root-count varies by level (3 vs level-1's 2), per the multiplicity law. (5) The
designed value-level β-transfer at β=14 missed (measured zero ≈1.768 vs predicted 1.683): the deep
root's pure logit law is large-β scoped, with Δ(β) = +0.114@12, +0.086@14, +0.034@16, +0.003@28 —
monotone, ~e^(−0.3β) — the adjacent level-1 comb's β-compensated contamination at the ~1e-9
cancellation floor: the v83 creep measured in μ-position for the first time; the larger-|p| roots
show no measurable departure. (6) The decay constant is empirical; deriving the contamination's
residue structure joins the queue.

**Reproduce.** `cd 08_2d_interacting && python3 deep_partner.py` → stored-curve refit (three
matched roots); the upper/central match tables; the monotone scoped-law deviation; the noise
quantification; a live value-scan bracketing the deep zero; "deep-partner self-test ... PASS"
(~30 s).

**Scope (honest).** One geometry; the β=24 v81 point remains a sign-noise outlier; Δ's decay
constant not derived.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
