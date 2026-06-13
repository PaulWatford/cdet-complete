# CROSSCHECK_v56 — genericity closed: doped trade-off generic; exact alignment only at half filling

**Claim.** On the 2×2 (U=4, τ=0.5), the convergence-optimal reference μ_ref_conv = μ − α* (α* by
direct truncation-error minimization vs exact ED, REAL-part metric) is separated from the sign peak
at every doped filling — β=4: gaps ≥1.0, R₂ at the optimum 0.01–0.40 vs peak 0.82 (μ∈{0,0.5,1,1.5,2});
β=8: μ=0.0 gap 1.50 (R₂ 0.14) — and aligns EXACTLY only at half filling: β=8, μ=U/2=2.0 gives α*=2.0
→ μ_ref=0.0 = the sign peak (R₂=0.91, gap 0.00), forced by particle-hole symmetry (α_Hartree=U⟨n⟩/2=
U/2 maps the reference to the PH point = the shell); μ=1.5 sits on the shoulder (R₂=0.89, gap 0.50).

**Correction on the record.** An earlier sweep reported alignment at β=8, μ=1.0 — a metric artifact
(|complex residual| instead of the real part, in a near-degenerate α landscape). The module self-test
FAILED against that flawed sweep, which is how it was caught; corrected α landscapes at μ=0.5, 1.0 are
unimodal with optima at μ_ref=−1.0, −0.5 (R₂≈0.08), i.e. separation. Both the flaw and the fix are
banked (GENERICITY_RESULT.md, real_patterns #66).

**Reproduce.** `cd 08_2d_interacting && python3 genericity_search.py` → prints the β=8 R₂ profile
subset, the half-filling alignment (gap 0.00, R₂ within 0.1 of peak) and the doped separation
(gap >0.9, R₂ deficit >0.3); final line "genericity self-test ... PASS" (~90 s). Full sweep tables in
GENERICITY_RESULT.md.

**Scope (honest).** One cluster, one U (R₂ is U-independent — proven; α_conv is not), one τ, α grid
0.5, K=8. Extending to a larger cluster and second U is the v57 candidate.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875). Wraps the engine via validated `cdet_port.py` (0.00e+00).
