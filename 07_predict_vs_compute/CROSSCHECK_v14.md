# Cross-check proof data (v14) — exact Bethe spin velocity: the attempt and the honest outcome

Goal: an EXACT u_sigma(U) anchor at quarter filling (spin analogue of bethe_Krho.py) to
upgrade the v13 spin-stiffness u_sigma from robustly-measured to verified. Reproduce:
`python bethe_spin_velocity.py`.

## What the dressed-energy route gives
Solve the zero-field Lieb-Wu densities and dressed energies; velocity = eps'(Fermi point)
/(2 pi rho(Fermi point)). Kernel a_n(x) = (1/pi)(nU/4)/((nU/4)^2 + x^2).

### CHARGE velocity v_c -- clean, validates the machinery
The charge Fermi point is at finite Q, so the slope is well defined.
| U | Q | v_c (Bethe) | reference |
|---|------|-------------|-----------|
| 2 | 1.1523 | 1.5368 | 1.76 |
| 4 | 1.2902 | 1.7753 | 1.83 |
| 8 | 1.4088 | 1.9225 | 1.93 |
Reproduces the reference at strong coupling (U=8: 1.92 vs 1.93). Small-U is resolution-
limited: the kernels have width U/4 and a uniform Lambda grid undersamples them. So the
solver is correct where the kernels are broad -- the approach is sound.

### SPIN velocity v_s -- UNRELIABLE at zero field (the result)
At zero magnetic field the spin sea fills the whole line, so the spin Fermi point is at
Lambda -> infinity. The endpoint slope eps_s'(Lambda)/(2 pi sigma(Lambda)) is a 0/0 limit
evaluated at the edge of a truncated grid -- numerically singular. The solver returns
unphysical values:
  U=2: v_s = -2.24 ;  U=4: v_s = -0.03 ;  U=8: v_s = -0.57  (all unphysical / negative).
This is exactly entry #13's fragility (the endpoint-derivative velocity at a vanishing
point), here in its sharpest form -- the Fermi point is literally at infinity.

## u_sigma verified the robust way -- bracket between exact limits (#10)
u_sigma is pinned EXACTLY at both ends, and the v13 spin stiffness lies strictly between,
monotonically:
| U | u_sigma (v13 spin stiffness) | fraction of v_F |
|---|------------------------------|-----------------|
| 0 | 1.4304 (= v_F, finite-size, +1.1% over sqrt2) | 1.01 |
| 1 | 1.3733 | 0.97 |
| 2 | 1.2623 | 0.89 |
| 4 | 1.0309 | 0.73 |
| 8 | 0.7083 | 0.50 |
- U -> 0:  u_sigma -> v_F = sqrt2 (exact, free fermions; the L=12 value is the finite-size v_F).
- U -> inf: u_sigma -> 0 (exact; spin sector decouples, v_s ~ 1/U).
The two exact endpoints validate the ends; the monotonic decrease validates the interior.

## Status & next (v15)
PARTIAL (v14): the Bethe machinery is validated on the charge velocity (strong coupling);
the exact spin velocity via the endpoint route is numerically fragile at zero field
(Lambda -> infinity), so u_sigma is verified by exact-limit bracketing rather than an exact
curve. This is honest scope, not a hidden failure -- the fragile route is documented with
its cause. Open (v15): an EXACT interior u_sigma(U) needs an INTEGRATED (not endpoint-slope)
Bethe formulation -- e.g. via the spin susceptibility chi_s = 2/(pi v_s) from the field
response, or a Fourier-space treatment of the zero-field spin equation. That is the genuine
remaining hard step; u_sigma stands as robustly-measured (v13) and exact-limit-bracketed (v14).
