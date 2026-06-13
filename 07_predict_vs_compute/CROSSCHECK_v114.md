# CROSSCHECK_v114 — z(∞)=2 is locked to the Fermi surface; non-Fermi probes are Fermi-forbidden

**Claims.** (1) The freeze generalizes to an arbitrary probe (engine `set_freeze` + grid arg 10).
(2) Background A is identical for probe=2 and probe=3 (s=0 leaves both windows empty). (3) probe=2
(Fermi surface): c1 finite/decaying (237→156, β=24–72), z→2. (4) probe=3: c1 diverges as exp(+2.72·β)
(3.8×10¹⁹→1.1×10⁷⁶) — a population inversion (level 3 occupied while level 2 empty), Fermi-forbidden.
(5) z(∞)=2 is locked to level 2 = the lowest empty level = the unique physical probe.

**Reproduce.** `cd 08_2d_interacting && python3 probe_generalization_test.py` (self-test PASS); the
divergence directly: `./cse grid 24 72 16 12 3072 31 0.002 0 3` (probe=3) vs `… 0 2` (probe=2).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875). Engine validates both builds (probe default 2).
