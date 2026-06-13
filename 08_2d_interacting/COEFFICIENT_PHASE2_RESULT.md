# Coefficient program phase 2 (v99): the heavy-tail problem solved, the frozen polynomial measured, and the two-sector discovery

**The estimator.** The s=0 integrand autopsy showed the top 1% of τ-samples carrying 95.5% of
the mass at clustered times, with survival tail index α ≈ 0.55 — the plain estimator has
infinite variance and fictional error bars (demonstrated: a 24-draw brute mean swung −0.178 →
+0.023 on late spikes). The mixture importance sampler (½ uniform + ½ truncated-Laplace
cluster mode, weights ≤ 2, mean 1) is validated analytically (0.5σ over 300k) and delivers
~31× variance reduction: the ±5% spec costs ~50 s/point instead of ~26 min.

**The frozen polynomial** (β=36, μ_exp = 1.845, all IS): A = +0.3700(108) — superseding v96's
tail-biased +0.277(45) — with the geometric grid P(0.0005…0.004) measured to 3–7% and the root
at **s\* = 0.00183(8) → z_pol(36) = 1.8249(12)**. Internally smooth: the directly measured
frozen(s_phys = 0.0037584) = −0.3391(143) sits exactly on it.

**The registered two-branch test, scored.** The root-flow branch (root at the physical
f₂\* = 0.00376(41)) is excluded at ~10σ — the small-s slope stays at ≈ −200 e-9 down to
s = 0.0005. The failure branch's "missing piece" is **identified**:

**The two-sector discovery.** v96's faithfulness claim is falsified at 3.4σ by direct
measurement: physical(1.845) = +0.030(108) — the v93 zero is real — vs frozen at the physical
point = −0.3391(143). The 1e-13 argument compared occupancy values but ignored their
exponentially growing coefficients: the level-1 particle branch (1−nf₁)e^((μ−1)τ) =
e^(−(μ−1)(β−τ)) is **O(1) in the τ→β corner**. The freeze (δ₁ = 0 exactly) kills these
antiperiodic images; physically they form a hole-image sector **Δ(s_phys; 36) = +0.369(109)
e-9** — the same size as everything else at the zero. The physical zero is the root of
[frozen polynomial + Δ(s; β)], which is why the frozen root sits 2.05× below the physical f₂\*.
The v96 "faithfulness PASS" was the underpowered gate the v98 audit flagged.

**Consequences registered.** (1) The literal-rate menu bookkeeping (v93/v95) is suspect for
hole-side monomials — the τ-corner saddle reduces effective hole rates; a τ-integrated
re-derivation is queued. The empirical pool is unaffected. (2) v96 #106 "proven FAITHFUL"
downgraded in-module. (3) The decisive 13/7-vs-24/13 object is now **Δ(s; β)** — the
hole-image sector's own s- and β-dependence, measurable by matched physical-minus-frozen
differences or a δ₁-retaining freeze.

Reproduce: `python3 coefficient_phase2.py` (weights; analytic; root; two-sector; live IS gates;
PASS ~80 s). Frozen engine untouched (194/194).
