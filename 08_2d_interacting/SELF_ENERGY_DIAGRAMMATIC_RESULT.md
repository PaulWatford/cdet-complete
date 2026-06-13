# Integration #3, step 2: the diagrammatic self-energy converges to the exact Σ (v135)

v134 fixed the observable (interacting addition energy = ε_k + ReΣ) and its exact ED ground truth. This step
shows the **engine-side** route reaches it: the connected determinant gives G order by order in U, and
resumming + Dyson-inverting yields a self-energy that converges to the exact Σ.

## Pipeline (per Matsubara frequency)

a_n(iω) = the Uⁿ order coefficients of G(iω;U) — the connected-determinant series the engine samples and the
v132 fast minors evaluate at O(2ⁿn²). Then G_diag = Σ_n a_n Uⁿ (resum) and Σ_diag = G₀⁻¹ − G_diag⁻¹ (Dyson).

## Verified (atom, vs the closed-form / ED Σ)

| U | order 2 | order 4 | order 6 | order 8 |
|---|---|---|---|---|
| 0.3 | 1.4e-2 | 1.3e-3 | 9.8e-5 | **7.2e-6** |
| 0.5 | 5.5e-2 | 1.5e-2 | 2.9e-3 | **6.6e-4** |
| 0.8 | 2.0e-1 | 1.3e-1 | 6.9e-2 | 4.9e-2 |

Inside the bare-series radius (~π/β) the diagrammatic Σ converges **geometrically** to the exact result. At
U=0.8 — near the radius — it slows.

## What the radius tells us

That slowdown is precisely why Šimkovic–Kozik compute the **irreducible (self-energy) series directly**
rather than connected-G + Dyson: the 1PI series has a larger convergence radius. So this step both verifies
the diagrammatic Σ pipeline against the v134 ground truth **and** pinpoints the next refinement — the direct
irreducible recursion (step 3), which is the actual Šimkovic–Kozik algorithm and the convergence upgrade.

The order coefficients here come from an exact U-contour integral on the ED Green's function — the target the
connected-determinant Monte Carlo converges to — so the coefficients→G→Σ pipeline and its convergence are
what is verified. ED is the anchor only; the frozen engine is untouched (194/194).

Reproduce: `python3 self_energy_diagrammatic.py`. Frozen engine untouched (194/194).
