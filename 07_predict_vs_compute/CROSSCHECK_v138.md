# CROSSCHECK_v138 — full consolidation of the integration program

**Claims.** (1) Three paths agree: surrogate-C == plane-wave-C (==stable @L6, 0.00e+00) == python on the
addition pole = lowest-empty level (worst 5e-10); fast minors == engine connected determinant (3e-15); exact
1PI σ_n == ED at U=0.3 (7e-8). (2) All v131–v137 advances live and self-testing. (3) Learnings: plane-wave
LD for deep cancellation; self-energy needs engine wire-in + resummation; fast-minors wire-in (#5); surrogate
could carry the Hartree shift. (4) README + QUICKSTART refreshed to the integration frontier.

**Reproduce.** `cd 08_2d_interacting && python3 consolidation_v138.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
