# The U-axis rational lead, pursued to its boundary (v146)

v141 found the **atom** self-energy is rational in U at fixed density (geometric recurrence → [2/1] closed form
→ 15 digits) and left a lead: does the **lattice** (skeleton) self-energy inherit a rational structure? This
pursues that lead and finds its boundary — with a clean reason.

## The theorem (why the atom is rational)

Σ(iω;U) is rational in U **iff the many-body eigenvalues E_k(U) are linear in U**. For the atom the interaction
U·n↑n↓ is **diagonal** in the occupation basis (= the energy basis), so E_k(U) = E_k(0) + U·(double occupation)
— linear. Linear eigenvalues ⇒ the Green's-function poles move linearly ⇒ G and Σ are rational in U. (At fixed
density; the grand-canonical nd(U) was the v140 non-rationality, removed by fixing density in v141.)

## The boundary (why the lattice is not)

With hopping, the kinetic term does **not** commute with the interaction, so the interaction is not diagonal in
the energy basis and the eigenvalues become **algebraic** in U (roots of a U-dependent characteristic
polynomial), not linear.

| criterion | atom | dimer (2-site) |
|---|---|---|
| ‖[H_kin, H_int]‖ | **0** (interaction diagonal) | **1.4** (≠0) |
| eigenvalues vs U | linear | algebraic |
| Σ(U) | rational | algebraic (branch points) |
| constant-coeff recurrence residual | ~1e-4 | **0.21** (fails) |

So the lattice self-energy is an **algebraic** function of U with branch-point singularities — not rational.

## Consequence

The exact 15-digit **rational** route is confined to the **atom / local self-energy** (the Hubbard-I /
DMFT-atomic object — still the Mott-physics driver, so the route is useful where the self-energy is local). The
full lattice self-energy is algebraic: still a closed form in principle (it satisfies a finite polynomial
equation), but not rational, and its branch points cap simple resummation — Padé reaches past the radius (turns a
1e6 divergence at U=3 into O(1)) but not to 15 digits; conformal/algebraic methods are the lattice tool.

## Net — the two axes differ

The rational structure is **exact along N** (the record, v145 — polynomial, constant-coefficient recurrence) and
**along U only locally** (the atom, v141). Along U the lattice is **algebraic**, not rational, because hopping
makes the eigenvalues nonlinear in U. That is the boundary of the U-axis rational lead.

Reproduce: `python3 rational_lattice_boundary.py`. ED is the anchor only; frozen engine untouched (194/194).
