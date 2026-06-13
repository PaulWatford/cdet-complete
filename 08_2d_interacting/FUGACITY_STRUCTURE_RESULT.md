# The analytic origin of the μ-period (v78): the Matsubara comb, detected by complex-μ continuation

**The cancellation lemma (rigorous, load-bearing).** In every determinant det[g(τ_i−τ_j)] the
explicit e^{μτ} factors cancel term-by-term, and the CDet mask sums are determinants over shared
time sets — so all μ-dependence of ⟨C⟩_τ enters through the Fermi factors alone. Therefore
**⟨C⟩_τ is exactly a rational function of the fugacity z = e^{βμ}, with poles only at
z = −e^{βε_k} < 0** — equivalently, μ-poles on the Matsubara combs **μ = ε_k + i(2m+1)π/β**,
anchored at the levels, at uniform height π/β. (Exact at any order; the cancellation is
per-determinant.)

**The staircase falsification.** The literal "charge staircase" (adjacent fugacity powers
exchanging dominance — our v77 first reading and the simplest outside derivation) predicts slope
steps of +β in ln|⟨C⟩| at each sign flip. Measured: slopes flat (0.03–0.33β), steps ±0.2β —
**dead.** Every Fermi factor is degree-matched in z and saturates; the function lives in the
sigmoid-crossover regime.

**The direct detection.** The engine analytically continues in μ (zero-imag consistency exact;
Cauchy–Riemann residual 6e-4). Approaching the comb at β=4 (π/β=0.785): at a level (μ₀=2.000),
|⟨C⟩(μ₀+iy)| rises **3.9×10⁶-fold** by y=0.77; between levels (μ₀=1.700), ×12 (τ-noise-flat).
Contrast 3×10⁵. **The pole is there, exactly where the lemma puts it.**

**The mechanism (what Δμ\*=π/β means).** The real-axis sign structure is *comb-limited*: the
nearest singularities sit at uniform height π/β regardless of geometry or lattice — deriving the
1/β scaling **and** the R/L-independence in one stroke. q≈1 is nearest-comb dominance (higher combs
exponentially subdominant), consistent with the measured drift q: 1.12→0.98 with growing β.
"Charge 1" survives refined: it is the z-degree of each Fermi denominator; **π is the
antiperiodicity phase.** Open (honest): the exact constant — why the zero spacing is ≈π/β rather
than merely O(π/β) — is a zero-statistics question for high-degree negative-pole rational
functions; banked as the refined theory item. A reading note added to MU_PERIOD_RESULT.md.

Reproduce: `python3 fugacity_structure.py` (gates: continuation consistency; Cauchy–Riemann;
comb contrast >1e4; staircase slopes flat; PASS, ~40 s). Frozen engine untouched (194/194) — the
complex-μ probe runs through the Python FastCDet port; the C engine is unmodified.
