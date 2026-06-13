# CROSSCHECK_v49 — contour deformation / covariate (null on the wall) + best-methods consolidation

**Claim 1 (deformation is null on the sign).** On the genuine v48 integrand (2×2, levels {−4,0,0,+4},
β=4, U=4, μ=0.5, externals 0.7/0.2), the sign/variance-optimal contour amplitude is the **real axis**
(A=0 in every kink-pinned sector), integral invariant to 0.0e+00. Within each sector R=1.000; the deficit
is discrete between sectors. n=2 reproduces the v48 wall (|R₂| 0.82 shell / 0.04 Hartree).
Reproduce: `cd 08_2d_interacting && python3 contour_deformation.py`.

**Claim 2 (covariate is null; ceiling).** The deformation family's optimal variance-minimising combination
gives ×1.00; the deformed real part is rigid to 1e-15 (toy control: real part moves by 1.4, so the
deformation is live). Control variates reduce variance, never R → prefactor only. Same script.

**Claim 3 (best methods verified).** `python3 08_2d_interacting/best_methods.py` → all PASS:
shifted reference (bare diverges radius 1.0 / shifted converges radius 2.64, K=11 err 1.07e-5);
complex-μ contour derivative extraction matches the direct shift to 5.87e-14; free-baseline control
variate weak-U range reduction ×8.4 (U=0.5) → ×1.5 (U=4).

**Port validation.** `python3 08_2d_interacting/cdet_port.py` → max|general − validated ring port| =
0.00e+00 (so the v49 experiments run on a bit-identical copy of the frozen engine's connected determinant).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; `cdet_order` constants
bit-identical (−0.5082750022348369  0.44040518398732875).

Honest status: v49 is a clean **negative** result on the sign wall (the plundered contour tool does not
cross it, with a structural reason) plus a **positive** consolidation of the three verified, axis-distinct
accelerations. No claim crosses the Troyer–Wiese wall.
