# Genericity of the sign-vs-convergence trade-off — the arc-closer (v56)

**The standing question (open since v48).** The shift's convergence optimum and sign optimum competed
in the one case measured. Is that tension generic, or does a filling exist where the
convergence-optimal reference lands ON the sign peak — both improving together?

**Method.** 2×2 cluster, U=4, τ=0.5. (a) Measure the sign landscape R₂(μ_ref) by sampling C_V
(U-independent, as proven earlier) at β=4 and β=8. (b) For each physical μ, find the
convergence-optimal shift α* by direct truncation-error minimization against the exact ED reference
(real-part metric), giving μ_ref_conv = μ − α*. (c) Compare μ_ref_conv against the sign peak.

**Result, β=4 (peak R₂=0.82 at μ_ref=0):** separation everywhere.

| μ | α* | μ_ref_conv | R₂ there | gap to peak |
|---|---|---|---|---|
| 0.0 | 1.50 | −1.50 | 0.15 | 1.50 |
| 0.5 | 1.50 | −1.00 | 0.01 | 1.00 |
| 1.0 | 2.00 | −1.00 | 0.01 | 1.00 |
| 1.5 | 0.00 | +1.50 | 0.40 | 1.50 |
| 2.0 | 0.50 | +1.50 | 0.40 | 1.50 |

**Result, β=8 (peak R₂=0.91 at μ_ref=0):** alignment exists — anchored at half filling.

| μ | α* | μ_ref_conv | R₂ there | gap |
|---|---|---|---|---|
| 0.0 | 1.50 | −1.50 | 0.14 | 1.50 |
| 1.5 | 1.00 | +0.50 | 0.89 | 0.50 |
| **2.0 (=U/2)** | **2.00** | **0.00** | **0.91** | **0.00** |

At half filling the alignment is **exact and mechanistic**: the Hartree shift α = U⟨n⟩/2 = U/2 maps
the reference to the particle-hole-symmetric point, which *is* the closed shell. The same symmetry
that makes half filling sign-free in the auxiliary-field formulation forces the two optima together
here. μ=1.5 (near half filling) sits on the peak's shoulder; the genuinely doped fillings stay
sharply separated at both temperatures.

**Correction on the record.** An earlier pass reported alignment at β=8, μ=1.0. That was a **metric
artifact**: the error used |complex residual| instead of the real part, and the near-degenerate α
landscape let the wrong winner surface. With the correct metric the landscape at these points is
unimodal and that alignment disappears. The full corrected α landscapes at μ=0.5 and μ=1.0 (β=8) show
unique optima at μ_ref=−1.0 and −0.5 (R₂≈0.08), i.e. separation. Caught because the module self-test
failed against the flawed sweep — the audit discipline doing its job.

**VERDICT (closing the v48→v56 arc).** The trade-off is **generic in the doped regime** — exactly
where the sign problem bites — with the optima separated by ~half a shell spacing or more. The one
robust both-at-once point is **half filling at low temperature**, where alignment is forced by
particle-hole symmetry: the same special point every sign-free structure in this program has pointed
back to. No new free lunch; one mechanism-understood alignment.

Honest scope: one cluster, one U (R₂ is U-independent; α_conv is not), one τ, α grid 0.5, K=8.
Reproduce: `python3 genericity_search.py` (gates both faces: exact half-filling alignment AND sharp
doped separation; PASS, ~90 s). Frozen engine untouched (194/194).
