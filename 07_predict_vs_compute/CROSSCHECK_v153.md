# CROSSCHECK_v153 — reaching strong coupling: SU(N) EoS by two-point resummation

**Claims.** (1) The strong-coupling anchor is the atomic limit (m₀ = t=0 SU(N) atom density, the v142 atom record,
single-site, no 2-site diagonalization); m₀(N), m₁(N) are smooth in N → record-predictable. (2) A two-point Padé
[2/2] (3 weak + 2 strong) is stable (no spurious pole in the physical window; higher orders are not). (3) The
record-predicted SU(6) EoS — using only N≤5 data, no SU(6) diagonalization — matches direct SU(6) ED across the
whole coupling range, hitting U/t=2.3 (the Kozik benchmark) at 2.4% and worst <5% to U=4. (4) The SU(N) EoS is now
record-predicted weak→strong: weak end from the lattice record (v152), strong end from the atom record (v142).

**Reproduce.** `cd 08_2d_interacting && python3 sun_eos_strong.py` (self-test, N≤5, ~2s). N=6 table in
SUN_EOS_STRONG_RESULT.md.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
