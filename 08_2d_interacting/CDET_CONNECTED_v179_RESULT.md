# Tier 0: the connected-determinant recursion, implemented and validated

**Why.** The suite had been, by its own description, a validation harness *around* a frozen engine — it never actually
implemented the connected determinant (CDet), the method (Rossi, PRL 119, 045701, 2017) the whole package is named for.
This closes that gap: a faithful low-order CDet, proven correct on cases with a known answer.

**What CDet is.** At perturbation order n the n interaction vertices sit at fixed (site, τ) positions. The sum of *all*
diagrams (connected + disconnected) at those positions is a determinant per spin; for the spin-symmetric Hubbard vertex
the full weight is `D(V) = det M(V)^2` with `M(V)_{ab} = G0(vertex_a, vertex_b)`. The *connected* weight is extracted by
Rossi's recursion, marking one vertex v*:

>   `C(V) = D(V) − Σ_{ v* ∈ S ⊊ V }  C(S) · D(V∖S)`.

This is the exact inverse of the linked-cluster identity `D(V) = Σ_{partitions P of V} Π_{B∈P} C(B)`. The free-energy
series follows from `ln(Z/Z0) = Σ_n (−U)^n/n! ∫ C`, so the `U^n` coefficient is `(−1)^n` times the integral of `C` over
the ordered-τ simplex (C is symmetric in the vertices).

**Validation (three gates, all pass).**
1. **Recursion combinatorics (exact, no quadrature).** `D(V) = Σ_partitions Π C(B)` at random vertex positions, n=2..5
   — worst deviation **2e-16**. The bug-prone heart is correct to machine precision.
2. **Atom.** The lnZ U-series, orders 1..5, against the closed form `ln(1 + 2e^{βμ} + e^{−βU+2βμ})` — worst dev **6e-17**.
3. **2-site Hubbard lattice.** The lnZ U-series, orders 1..3, against exact diagonalization — order 1 **1e-12**, order 2
   **2e-12**, order 3 **1e-9** (the last limited by the ED Taylor fit, not by CDet).

**What this is — and is not.** It is a correct CDet recursion (the connectedness extraction + the determinant weights +
the free-energy series) demonstrated on exactly-solvable systems, so the package now genuinely *implements* the method,
not merely validates an engine. It is **not** a contribution to the sign problem: it is deterministic and low-order. The
frontier — a Monte Carlo sampler pushed to high order in the strong-U, low-T, doped regime past the complex-U poles —
is Tier 2+ and remains unbuilt (see the v177 discussion and INDEX.md). This is the honest Tier 0: small, correct, and it
makes the existing claims true. Frozen reference engine untouched (194/194). `cdet_connected.py`, `cdet connected`.
