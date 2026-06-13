# CROSSCHECK_v51 — the symmetry fold scales with the lattice point group (column/row slices)

**Claim (column/row slices fold, not cancel; fold grows with the point group).** On the 4×4 torus
the stabilizer of the external site is the full square point group D4, |G_0| = 8, including the
column-slice (left-right) and row-slice (up-down) reflections. Every element gives
C_V(σx)/C_V(x) = +1.000 to ~1e-10 (FOLD); none gives −1 (no CANCEL). Folding the L^n site sum by the
order-8 group is exact and gives 4.65× fewer C_V evaluations at n=2 and 6.15× at n=3 (→ |G_0| = 8 as
n grows), versus 2× on the 2×2.

**Reproduce (numeric).** `cd 08_2d_interacting && python3 symmetry_reduction.py` →
2×2 fold 1.60×/1.78×/1.88× (n=2/3/4) and 4×4 point-group fold 4.65× (n=2), both matching brute force
to ≤1e-15; self-tests print PASS.

**Reproduce (symbolic).** `python3 symmetry_audit_sympy.py` → the 2×2 stabilizer and the 4×4
column/row-slice reflections (and rot90, diag) all satisfy P^T·H(t)·P − H(t) = 0 as polynomial
identities in the hopping t; returns PASS. (sympy is audit-time only; runtime needs only numpy.)

**Scope (honest, unchanged).** Folds the L^n site-configuration space by the little group of the
external site, a saving that grows with lattice symmetry (2× → 8× → larger). Does NOT fold the Rossi
2ⁿ recursion and does NOT touch the physical sign — column/row slices are symmetries (orbit members
share the sign), not anti-symmetries.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; `cdet_order` constants
bit-identical (−0.5082750022348369  0.44040518398732875). The fold wraps the engine via the validated
`cdet_port.py` (bit-identical to the frozen ring port at 0.00e+00).
