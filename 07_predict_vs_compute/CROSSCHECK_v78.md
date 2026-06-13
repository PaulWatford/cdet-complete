# CROSSCHECK_v78 — the Matsubara comb: the μ-period's analytic origin

**Claims.** (1) Cancellation lemma (rigorous, any order): explicit e^{μτ} factors cancel per
determinant; all μ-dependence enters via Fermi factors; ⟨C⟩_τ is exactly rational in z=e^{βμ} with
poles only at z=−e^{βε_k}<0 — μ-poles on Matsubara combs μ=ε_k+i(2m+1)π/β at uniform height π/β.
(2) Staircase falsification: the literal charge-staircase predicts +β slope steps in ln|⟨C⟩| at
flips; measured slopes 0.03–0.33β, steps ±0.2β — falsified (this corrects our own v77 reading and
the outside heuristic). (3) Direct detection: complex-μ continuation validated (zero-imag exact;
Cauchy–Riemann 6e-4); at a level, |⟨C⟩(μ₀+iy)| rises 3.9e6-fold as y→0.77 (π/β=0.785); between
levels ×12; contrast 3e5. (4) Mechanism: comb-limited sign structure derives the 1/β scaling and
the R/L-independence; q≈1 = nearest-comb dominance (matches the drift 1.12→0.98); "charge 1" = the
z-degree of each Fermi denominator; π = the antiperiodicity phase. (5) Refined open item: the
exact constant (≈π/β vs O(π/β)) as a zero-statistics question. Reading note added atop
MU_PERIOD_RESULT.md.

**Reproduce.** `cd 08_2d_interacting && python3 fugacity_structure.py` → continuation consistency,
Cauchy–Riemann, comb contrast >1e4, staircase slopes flat; "fugacity-structure self-test ... PASS"
(~40 s). Precision curves and the slope analysis are documented in FUGACITY_STRUCTURE_RESULT.md.

**Scope (honest).** Lemma exact for the free-propagator CDet integrand; probes at n=3, one
geometry, β=4 comb scan (β=6 staircase too); continuation validated internally (zero-imag +
Cauchy–Riemann), not against an independent exact construction.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875). The complex-μ probe runs through the Python port only.
