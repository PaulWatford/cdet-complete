# CROSSCHECK_v160 — conformal-Borel resummation (order axis)

**Claims.** (1) Web-grounded: CDet's frontier is perturbative order (~10–13 coeffs), not lattice size (works in the
thermodynamic limit); the bare-U series is capped by a complex-U branch point (v146). (2) Conformal-Borel keyed to
the Borel singularity (|t_c|≈1.05, complex → Borel-summable) beats plain Padé[4/4] on the SU(N) EoS by ~4× at U=0.6
and ~2× at U=1.0, validated vs ED. (3) Honest ceiling: reliable strong coupling needs the large-order/instanton
structure or the v153 two-point bridge — the fragile U≈2.5 result is NOT claimed. (4) Frozen reference untouched.

**Reproduce.** `cd 08_2d_interacting && python3 sun_eos_conformal.py` (~3s).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
