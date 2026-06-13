# Cross-check proof data (v16) — an EXACT spin velocity (half filling) validates the ED routes

The quarter-filling u_sigma has no closed form and the zero-field Bethe endpoint route is
singular (v14). But at HALF filling the spin velocity IS exactly known, so it serves as a
reference to validate the two ED routes and locate the quarter-filling u_sigma. Reproduce:
`python spin_velocity_exact_check.py`.

## Exact half-filling spin velocity (Lieb-Wu, zero field, n=1)
    v_s(U) = 2 I_1(2 pi/U) / I_0(2 pi/U)      (I_n = modified Bessel)
Validated by limits: U->0 -> 1.9984 ~ v_F = 2; U=8 -> 0.7305 vs 2pi/U = 0.7854 (the
Heisenberg value J=4/U, approached from below). Both correct -> the formula is trustworthy.

Stiffness prefactor is universal: half-fill U=0, L=10 gives pi(L/2)D_sigma = 2.033 ~ v_F=2
(same +1.6% finite size as quarter filling), so no refit across fillings.

## The two ED routes vs the exact value (half filling)
| U | exact | triplet (L10) | stiff (L6) | stiff (L10) | bracket | closer to |
|---|-------|---------------|------------|-------------|---------|-----------|
| 1 | 1.8331 | 1.6431 | 2.0448 | 1.9756 | yes | stiffness |
| 2 | 1.6399 | 1.2434 | 1.9175 | 1.8328 | yes | stiffness |
| 4 | 1.2263 | 0.6464 | 1.5266 | 1.4137 | yes | stiffness |
| 8 | 0.7305 | 0.3229 | 0.9022 | 0.8431 | yes | stiffness |

## Reading it
- At EVERY U the exact value is BRACKETED: triplet < exact < stiffness, and the exact value
  is CLOSER TO THE STIFFNESS. The bracket method (two independent ED routes around the truth)
  is thus validated against an exact reference, with the stiffness the better single estimate.
- The stiffness moves toward the exact value as L grows (L=6 -> L=10 decreases toward it),
  confirming it is the right observable with residual finite-size (log) corrections.
- The triplet runs far low at half filling because the half-filled spin sector carries the
  STRONGEST SU(2)_1 marginal correction, corrupting its U=0-calibrated dimension -- the same
  effect that made it ~10% low at quarter filling (v15), here in severe form. This confirms
  the v15 diagnosis with an exact reference.

## What it buys the quarter-filling u_sigma
The exact spin velocity lies between the triplet (v15) and stiffness (v13) routes, closer to
the stiffness -- DEMONSTRATED at half filling. Transferring: at quarter filling the exact
u_sigma is bracketed by [v15 triplet, v13 stiffness] and sits closer to v13. So v13 is a mild
overestimate, v15 a larger underestimate, the truth in between and nearer v13. The exact
quarter-filling CURVE still needs the general-n integrated Bethe solve, but its LOCATION is
now bounded on both sides with a known lean -- a real tightening of the v15 result.

## Status & next
EXACT-VALIDATED (v16): the spin velocity is known exactly at half filling (Bessel) and used
to validate the ED bracket and identify the stiffness as the better estimate; the quarter-
filling exact u_sigma is bracketed [v15, v13], closer to v13. OPEN: the exact quarter-filling
curve via the general-n integrated Bethe solve (the half-filling Bessel result is the
validator that solver must reproduce before being trusted at n=0.5). The u_sigma arc:
measure (v13) -> exact route fragile, bracket limits (v14) -> second ED route (v15) -> exact
half-filling reference validates the bracket and locates the truth (v16).
