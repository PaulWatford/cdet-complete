# CROSSCHECK_v152 — SU(N) step 5: the record-predicted EoS curve in U

**Claims.** (1) The per-flavor density U-series is extracted to K=8 for small N via a complex-U contour on the
2-site reference. (2) The record predicts the N=6 series from N≤5 (polynomial-in-N fit per order), with leading
coeffs n0,n1,n2 to 1e-4..1e-3 — no SU(6) diagonalization. (3) Padé[3/3] resummation of the predicted N=6 series
matches direct SU(6) ED to ~1–2% out to U≈1.2 (10× the bare radius ~0.16). (4) Strong coupling needs conformal
resummation (the v146 algebraic boundary). NET: EoS exactly N-predictable; U-reach set by the branch point.

**Reproduce.** `cd 08_2d_interacting && python3 sun_eos_curve.py` (self-test, N≤5, ~40s). Full N=6 validation
table in SUN_EOS_CURVE_RESULT.md.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
