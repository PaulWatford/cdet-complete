# Cross-check proof data (v9) — doped tower probe & the spin-charge-separation break

The doped charge sector at quarter filling (n=0.5), the step v7 flagged. A
deliberately velocity-free probe was tried; it produced a clean BREAK whose
direction and size identify spin-charge separation. Reproduce: `python doped_tower.py`.

## Hypothesis (single charge velocity)
Luttinger liquid, SU(2) so K_sigma = 1:
  - 2k_F density operator dimension  x_2 = (1 + K_rho)/2
  - 4k_F density operator dimension  x_4 = 2 K_rho
If one velocity u_rho governed both finite-size gaps, the ratio would be velocity-free:
  R(L) = gap(4k_F)/gap(2k_F) -> x_4/x_2 = 4 K_rho/(1 + K_rho).

## Exact anchor — U=0 must give R=2 (free fermions, K_rho=1)
L=12, quarter filling (N_up=N_dn=3), closed shell, ground-state momentum 0.
gap(2k_F)=0.73205, gap(4k_F)=1.46410, R=2.00000. Momentum identification and gap
extraction are correct to all printed digits (cross-checked against an independent
full-spectrum momentum resolution; both give the same gaps).

## Result — R(ED) vs the single-velocity prediction (L=12)
| U | gap(2k_F) | gap(4k_F) | R(ED) | 4K/(1+K) | K_rho(exact) |
|---|-----------|-----------|-------|----------|--------------|
| 0 | 0.73205 | 1.46410 | 2.0000 | 2.0000 | 1.0000 |
| 1 | 0.66218 | 1.44615 | 2.1839 | 1.8954 | 0.9006 |
| 2 | 0.60865 | 1.40847 | 2.3141 | 1.8006 | 0.8187 |
| 4 | 0.52897 | 1.32846 | 2.5114 | 1.6633 | 0.7118 |
| 8 | 0.43714 | 1.22421 | 2.8005 | 1.5257 | 0.6166 |

K_rho is the exact Bethe value from bethe_Krho.py (v5).

## Reading the break (the point of the cross-check)
R(ED) RISES with U; 4K/(1+K) FALLS. The hypothesis is wrong, and wrong in a way
that is itself a measurement:
- The 4k_F operator is PURE CHARGE — its gap is set by u_rho alone.
- The 2k_F operator carries BOTH charge and spin — its gap is (2 pi/L)(u_rho·x_rho +
  u_sigma·x_sigma), a MIX of the two velocities.
- So the ratio is not velocity-free unless u_rho = u_sigma. At U=0 they coincide
  (= v_F), which is exactly why the anchor is clean. As U grows the velocities split
  (u_sigma slows toward ~2pi/U scales, u_rho speeds up: cf v6, v8), the 2k_F gap is
  dragged down by the slower spin velocity, the 4k_F gap is not, and R rises.
- The monotonic rise of R(ED) is therefore a direct, parameter-free SIGNATURE of
  spin-charge separation, anchored to its exact zero (no separation) at U=0.

## The corrected probe (v10 open item)
Use a ratio of two PURE-CHARGE gaps, both governed by u_rho only, so a single
velocity genuinely cancels: 4k_F (x = 2 K_rho) against the charge-current / flux
excitation (the D_c sector already built for the v8 charge stiffness). That ratio
should isolate 4 K_rho/(...) with the exact-anchor discipline intact.

## Status
Velocity-free 2k_F/4k_F ratio: anchored EXACT at U=0; at U>0 it cleanly fails the
single-velocity hypothesis and the failure quantifies spin-charge separation. This
is a negative-with-diagnosis (real_patterns #9), and it specifies the corrected
pure-charge probe rather than leaving an open "needs bigger lattice".
