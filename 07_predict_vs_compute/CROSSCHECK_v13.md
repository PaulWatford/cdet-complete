# Cross-check proof data (v13) — u_sigma via spin stiffness (and it corrects v12)

v12 left u_sigma "extracted, not verified" (from the 2k_F gap). v13 measures it
independently via the SPIN STIFFNESS and they disagree for U>0 -- the cross-check
catches the v12 extraction. Reproduce: `python spin_stiffness_qf.py`.

## Method (pure-spin, integrated -- the robust kind)
Thread a SPIN flux: opposite Peierls phases for the two spins (up +Phi/L, down -Phi/L)
per bond. This twists the spin sector only. Then
    D_sigma = (L/2) d^2 E0/dPhi^2,   u_sigma = pi (L/2) D_sigma   (K_sigma = 1).
Ground-state energies only; no operator-dimension assumption (unlike v12's 2k_F formula).

## Implementation validation
At U=0 the spin twist and charge twist act identically on free fermions (up/down
symmetry), so spin-flux E0(Phi) must equal charge-flux E0(Phi): confirmed to all digits
(E0(0)=-10.928203, E0(0.4)=-10.922133 for both). Hence u_sigma(U=0) = u_rho(U=0) =
1.4304 with no free prefactor -- the method is calibrated by the exact free limit.

## Result (L=12, n=0.5)
| U | u_rho (v8 charge stiff) | u_sigma (spin stiff) | u_sigma (v12 gap) | u_rho/u_sigma | v12 error |
|---|-------------------------|----------------------|-------------------|---------------|-----------|
| 0 | 1.4304 | 1.4304 | 1.3981 | 1.000 | 2% |
| 1 | 1.5718 | 1.3733 | 1.1484 | 1.145 | 16% |
| 2 | 1.6896 | 1.2623 | 0.9799 | 1.338 | 22% |
| 4 | 1.8403 | 1.0309 | 0.7519 | 1.785 | 27% |
| 8 | 1.9582 | 0.7083 | 0.5007 | 2.765 | 29% |

## Reading it
- u_sigma(spin stiffness) and u_sigma(v12 gap extraction) AGREE at U=0 and DIVERGE to
  ~29% by U=8. The spin stiffness is the trustworthy route (integrated ground-state
  quantity, pure-spin twist, exact U=0 anchor); the v12 2k_F-gap decomposition
  gap(2k_F)=(2pi/L)(K_rho u_rho/2 + u_sigma/2) is NOT accurate at L=12 (marginal/log
  corrections of the SU(2) spin sector; asymptotic dimension not yet reached). So the
  v12 u_sigma numbers are SUPERSEDED by this row.
- With u_rho from the v8 CHARGE stiffness and u_sigma from the SPIN stiffness -- the
  SAME robust integrated route, charge vs spin twist -- spin-charge separation is now
  clean and consistent: the velocities coincide at U=0 (= v_F) and split with U,
  u_rho rising 1.43 -> 1.96, u_sigma falling 1.43 -> 0.71, ratio 1.0 -> 2.8.

## Status & next (v14)
ROBUSTLY-MEASURED (v13): u_sigma(n=0.5) via spin stiffness; exact U=0 anchor; supersedes
the v12 extraction; spin-charge separation now from one method on both legs. The v9 ->
v13 arc: detected (v9) -> pure-charge side verified (v10) -> finite-size-controlled (v11)
-> both velocities extracted (v12) -> spin side corrected by an independent robust
measurement (v13). Open (v14): an EXACT anchor for u_sigma at U>0 -- the Bethe-ansatz
spin (dressed-energy) velocity, the spin analogue of bethe_Krho.py -- to upgrade u_sigma
from robustly-measured to verified, as u_rho already is (v8 vs the Bethe charge velocity).
