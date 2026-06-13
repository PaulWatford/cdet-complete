# CROSSCHECK_v146 — the U-axis rational lead, to its boundary

**Claims.** (1) Σ(iω;U) is rational in U iff the many-body eigenvalues are linear in U iff the interaction is
diagonal in the energy basis. Atom: ‖[H_kin,H_int]‖ = 0 (diagonal) → rational (15-digit, v141). (2) Dimer:
‖[H_kin,H_int]‖ = 1.4 ≠ 0 (hopping) → algebraic eigenvalues → Σ algebraic (branch points), not rational —
dimer Σ fails the constant-coeff recurrence (residual 0.21 vs atom ~1e-4). (3) So the 15-digit rational route is
atom/local (DMFT) only; the lattice needs conformal/algebraic resummation. Rational is exact along N (record,
v145) and along U only locally (atom, v141).

**Reproduce.** `cd 08_2d_interacting && python3 rational_lattice_boundary.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
