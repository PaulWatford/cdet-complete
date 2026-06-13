# Integration #3, step 4 — exact 1PI coefficients, and a correction to v136 (v137)

This step computes the **exact** self-energy coefficients and, in doing so, **corrects an overclaim in v136**.

## The correction (retraction)

v136 claimed the 1PI self-energy series has a much larger convergence radius than the connected-G series
(R_Σ ≈ 1.76 vs R_G ≈ 0.80, "2.2× larger", "reaches strong coupling the bare series can't"). **That was
wrong.** v136 extracted σ_n by a Cauchy contour on Σ(U) at radius rS ≈ 1.0–1.5 — but that contour **encloses
Σ's own singularity near |U| ≈ 0.8**, so the extracted numbers were not Taylor coefficients. They gave a
bounded-but-wrong (~1e-1) result that *looked* like convergence past R_G but wasn't. Retracted.

## What is actually true

The **exact** σ_n come from the Dyson coefficient recursion (no contour):

  a_n = connected-G coefficients (a₀=G₀);  σ_n = a_n/G₀² − (1/G₀) Σ_{m=1}^{n-1} σ_m a_{n-m}.

These reproduce the ED self-energy to **1.9e-9 at U=0.3**, 6e-5 at U=0.5 — a correct, exact deliverable. Their
decay gives the true radii (lowest Matsubara):

| | from coefficient decay |
|---|---|
| R_G (from \|a_n\|^{1/n}) | ≈ 0.73 |
| R_Σ (from \|σ_n\|^{1/n}) | ≈ 0.84 |

So **R_Σ ≈ R_G** — no significant radius advantage for the Hubbard atom (a marginal ~15% is within the
asymptotic drift, nothing like 2.2×).

## What the Šimkovic–Kozik advantage actually is

Not a larger bare-series radius (at least not here). It is **(i) efficiency** — computing Σ directly via the
irreducible recursion avoids forming and inverting the full connected G — and **(ii) lower MC variance** of
the irreducible series. Reaching strong coupling past the bare-series radius needs **resummation** (Padé /
conformal mapping) or action-shift tricks, which apply to G and Σ alike. This is the honest framing.

## What still stands

Unaffected by this correction: **z(∞) = the free addition pole** (v133); **the interacting addition energy =
ε + ReΣ**, ED-verified (v134); **the diagrammatic Σ converges to ED within its radius** (v135). Those remain
correct. Only v136's radius-advantage claim is retracted, and the exact σ_n recursion replaces the flawed
contour proxy.

ED is the anchor only; frozen engine untouched (194/194). Reproduce: `python3 self_energy_irreducible.py`.
