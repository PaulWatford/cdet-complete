# CROSSCHECK_v52 — 45-degree slices of the cube; the fold scales with dimension

**Claim (cube 45-degree diagonal slices fold; O_h gives a bigger fold).** On the 4×4×4 cubic torus the
stabilizer of the external site is the full cube point group O_h, |G_0| = 48 (signed permutations of
the three axes), of which 40 are 45-degree diagonal slices (axis swaps). Every diagonal slice gives
C_V(σx)/C_V(x) = +1.000 to ~1e-10 (FOLD); none gives −1 (no CANCEL). Folding the N^n site sum (N=64)
by the order-48 group is exact (match 5.2e-15) and gives 18.62× fewer C_V evaluations at n=2, climbing
toward |G_0| = 48 as n grows.

**Reproduce (numeric).** `cd 08_2d_interacting && python3 symmetry_reduction.py` → prints the 2×2 fold,
the 4×4 D4 fold (4.65× at n=2), and the 4×4×4 cube O_h fold (|G_0| = 48, 18.62× at n=2), all matching
brute force to ≤5e-15; self-tests print PASS (~20 s).

**Reproduce (symbolic).** `python3 symmetry_audit_sympy.py` → the 2×2/4×4 slice operations and the
cube 45-degree diagonal slices (axis swaps) all satisfy P^T·H(t)·P − H(t) = 0 as polynomial identities
in the hopping t; both SYMBOLIC AUDIT and CUBE SYMBOLIC AUDIT print PASS. (The cube identity is proven
on the small cube and is size-independent — isotropic hopping is invariant under relabeling the axes.)

**The pattern.** The redundancy fold equals the order of the little group of the external site, and it
grows with both size and dimension: 2× (2×2 square) → 8× (4×4 square, D4) → 48× (4×4×4 cube, O_h).
Exact at every step, proven for all t.

**Scope (honest, unchanged).** Folds the N^n site-configuration space; does NOT fold the Rossi 2ⁿ
recursion and does NOT touch the physical sign. The 45-degree slices are symmetries (orbit members
share the sign), not anti-symmetries.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; `cdet_order` constants
bit-identical (−0.5082750022348369  0.44040518398732875). The fold wraps the engine via the validated
`cdet_port.py` (bit-identical to the frozen ring port at 0.00e+00).
