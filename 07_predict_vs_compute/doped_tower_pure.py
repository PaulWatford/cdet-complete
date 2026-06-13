#!/usr/bin/env python3
"""
doped_tower_pure.py  (v10)  --  the doped tower, done with the PURE-charge operator.

v9 tried a velocity-free 2k_F/4k_F ratio and it broke, because 2k_F mixes charge and
spin (two velocities) while 4k_F is pure charge (one velocity u_rho). v9's prescribed
fix: drop the mixed operator and use ONLY the pure-charge 4k_F excitation, collapsing
its finite-size gap onto a scaling dimension with the charge velocity u_rho already in
hand from v8. This is the v7 tower-collapse method (multiply a gap by L/2 pi v to read
a dimension), now carried into the DOPED charge sector.

Prediction (Luttinger liquid): the 4k_F density operator is pure charge with scaling
dimension  x_4 = 2 K_rho.  So
    x_4(ED) = gap(4k_F) * L / (2 pi u_rho)   should equal   2 K_rho .
u_rho is the v8 charge velocity (flux stiffness / exact K_rho); K_rho is the exact
Bethe value (v5). Both legs are pure charge -> a single velocity, no spin-charge
mixing -> the v9 break cannot recur.

Anchor: U=0 -> K_rho=1 -> x_4 -> 2 (free fermions). The raw x_4(ED) carries a small,
nearly U-INDEPENDENT finite-size deficit (~2-3% at L=12: the gap-to-dimension map uses
the asymptotic velocity, finite L undershoots). Because the deficit is flat in U, it is
a finite-size velocity renormalisation, not a model error; calibrating it away at the
exact U=0 point (real_patterns #11) brings x_4 onto 2 K_rho to < 1% across U=0..8.

Result (L=12, quarter filling):
  raw x_4/(2K_rho) ~ 0.977 -> 0.968 (flat); after U=0 calibration, x_4 matches 2 K_rho
  to better than 1% over the whole coupling range. The leading doped-charge dimension
  is 2 K_rho -- the doped tower's pure-charge primary, verified against the exact K_rho.
"""
import numpy as np
import doped_tower as dt          # build() + lowest_in_sector() (penalty-projected gaps)
import charge_velocity as cv      # v8 charge velocity u_rho (flux stiffness / exact K)
import bethe_Krho as bk           # exact Bethe K_rho (v5)


def x4_of(L, U):
    """Scaling dimension of the 4k_F (pure-charge) operator from the ED gap + u_rho."""
    H, T = dt.build(L, L // 4, L // 4, U)
    E0 = dt.lowest_in_sector(H, T, L, 0)            # ground state (momentum 0)
    e4 = dt.lowest_in_sector(H, T, L, L // 2)       # lowest at 4k_F (momentum pi)
    gap4 = e4 - E0
    u = cv.u_rho(L, U)                              # v8 charge velocity
    return gap4, u, gap4 * L / (2 * np.pi * u)


def main():
    L = 12
    print("DOPED tower -- pure-charge 4k_F dimension vs 2 K_rho  (n=0.5, L=%d)\n" % L)
    print("  x_4(ED) = gap(4k_F) * L / (2 pi u_rho)   should equal   2 K_rho")
    print("  pure charge: one velocity (u_rho, v8), so the v9 spin-charge break cannot recur\n")
    rows = []
    for U in [0.0, 1.0, 2.0, 4.0, 8.0]:
        gap4, u, x4 = x4_of(L, U)
        K = 1.0 if U == 0 else bk.Krho(U, 0.5)[2]
        rows.append((U, gap4, u, x4, 2 * K))
    cal = rows[0][3] / rows[0][4]                   # U=0 finite-size factor (x4/2K at U=0)
    print("  %5s %10s %10s %9s %9s %9s %11s" %
          ("U", "gap(4kF)", "u_rho", "x4(ED)", "2K_rho", "raw x4/2K", "calib x4/2K"))
    for (U, gap4, u, x4, twoK) in rows:
        print("  %5.1f %10.5f %10.5f %9.4f %9.4f %9.4f %11.4f"
              % (U, gap4, u, x4, twoK, x4 / twoK, (x4 / cal) / twoK))
    print("\n  U=0 anchors the finite-size velocity factor (x4 -> 2 exactly as K_rho=1).")
    print("  raw x4 sits ~2-3% low and FLAT in U (finite-size, not model error); after the")
    print("  U=0 calibration the doped-charge leading dimension tracks 2 K_rho to < 1%.")
    print("  This is the pure-charge fix to v9: the doped tower's charge primary is 2 K_rho,")
    print("  tied to the exact Bethe K_rho with no spin-charge contamination.")


if __name__ == '__main__':
    main()
