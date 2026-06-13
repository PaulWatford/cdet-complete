# The deep partner (v89): the ~1.8 object identified, two anomalies closed, the creep measured in position

> **REVISED (v90, the two-window cross-check):** the deep zero's β-flow is NOT logit — value-level
> measurements across β = 10–28 select an ANCHORED, GEOMETRY-INDEPENDENT trajectory
> z = 1.824(±0.022) − 0.72(±0.34)/β (cross-geometry devs 0.001–0.011), a third instance of the
> static class. The f\*=0.0116 root remains a true property of the β=20 polynomial, but the deep
> tail is itself β-dependent (the creep contaminates the small-f extraction). The Δ(β) "decay" in
> this document was an artifact of a β=20-anchored baseline. The anchor identity (2√2−1 vs 11/6)
> is open. See CREEP_CROSSCHECK_RESULT.md.

**One extraction, three trajectories.** Level-2's residue polynomial at L=6 ((1,2,4), β=20,
small-f-weighted grid, NT=4096) resolves **three roots**:

| f\* | c = logit | identity | verification |
|---|---|---|---|
| 0.0116 | −4.44 | **the unclassified ~1.8 object** = the deep lower partner (Class I) | β=28 dev 0.003; large-β scoped (below) |
| 0.4437 | −0.23 | the central flip | β≥16 max dev 0.010 vs v81 |
| 0.9504 | +2.95 | **v80's dangling "2.2 family"** = the upper partner | v80 flow 2.188/2.138/2.112 vs 2.185/2.148/2.123: devs 0.003–0.011 |

**The v85 anomaly dissolves quantitatively:** through the deep root's crossing region |p| ≈
0.4–5e-9 while the v81 sign scans (NT=120) carried sem ≈ 3.2e-9 — sign estimates were
noise-dominated over a ±0.04 window, which is exactly the observed "c-drift" scatter. And level 2
carries **three roots vs level 1's two** — root count varies by level, as the multiplicity law
requires.

**The designed miss, banked as measurement.** A value-level β-transfer of the deep root at β=14
found no zero at the predicted 1.683 (measured ≈1.768): the pure logit law for the *deep* root is
**large-β scoped**. The deviation Δ(β) = measured − predicted = +0.114@12, +0.086@14, +0.034@16,
+0.003@28 — monotone, decaying ~e^(−0.3β). Mechanism: the deep root sits at the ~1e-9 cancellation
floor where the adjacent level-1 comb's β-compensated contamination grows as β drops — **the v83
creep, now measured in μ-position for the first time.** The central and upper roots (larger-|p|
crossings) show no departure at measurable size.

**Honest scope.** One geometry; the β=24 v81 point remains a sign-noise outlier; the decay
constant (~0.3) is empirical, not derived; the contamination's own residue structure is the next
derivable object.

Reproduce: `python3 deep_partner.py` (gates: stored-curve refit with three matched roots;
upper/central match tables; the monotone scoped-law deviation with β=28 ≤ 0.01; the noise
quantification; a live value-scan bracketing the deep zero; PASS, ~30 s). Frozen engine untouched
(194/194).
