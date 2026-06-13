# CROSSCHECK_v156 — consolidation of the v148–155 arc

**Claims.** A single health gate (`consolidation_v156.py`, ~1s) re-proves the whole current state: (1) cross-model
invariants hold (surrogate == production route for SU(N) c₁,n₁; surrogate addition pole == python; fast-minors
connected determinant == numpy det); (2) every capability added since v147 is live and tied to an exact anchor —
the UI control plane (cdet_lab/cdet_shell/cdet_study) and the SU(N) EoS arc (weak n₀=free density v152, strong
two-point v153, 2D k-integral n₁=−0.5116 v154, 2D n₂ Hartree a₂D=0.005622 v155). Nothing new is asserted.

**Reproduce.** `cd 08_2d_interacting && python3 consolidation_v156.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
