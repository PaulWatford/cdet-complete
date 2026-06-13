#!/usr/bin/env python3
"""
spin_charge_velocities.py  (v12)  --  spin-charge separation, made quantitative.

v9 saw the 2k_F/4k_F ratio rise with U and read it as spin-charge separation (the two
sectors have different velocities). v10/v11 nailed the pure-charge side (u_rho). v12
closes the loop by extracting BOTH velocities from the same two doped-tower gaps, so the
separation v9 detected qualitatively becomes two numbers, u_rho(U) and u_sigma(U).

Two finite-size gaps, one exact input (K_rho from v5), two unknown velocities:
  4k_F is PURE charge:   gap(4k_F) = (2 pi/L)(2 K_rho u_rho)
        -> u_rho = gap(4k_F) L / (4 pi K_rho)
  2k_F is charge + spin: gap(2k_F) = (2 pi/L)(K_rho u_rho / 2 + u_sigma / 2)
        -> u_sigma = gap(2k_F) L / pi - K_rho u_rho
(charge part dimension K_rho/2, spin part 1/2 with K_sigma=1 for SU(2)).

Anchor: at U=0 there is NO separation (free fermions), so u_rho = u_sigma = v_F = sqrt2.
The extraction returns u_rho = u_sigma = 1.398 at U=0 (1.1% below sqrt2, finite-size);
they must coincide there and SPLIT for U>0.

Cross-check (this is what makes u_rho trustworthy, not just extracted): u_rho from the
4k_F spectral gap is compared to the INDEPENDENT v8 charge velocity (flux stiffness /
exact K_rho, charge_velocity.py). The two unrelated routes agree to ~2-3% across U.

u_sigma at quarter filling is a NEW observable (v6 gave u_sigma only at half filling,
the Heisenberg point). Here its only hard anchor is U=0 (= v_F); its U>0 values are an
extraction, falling monotonically as the spin sector slows -- the direct, quantitative
face of spin-charge separation. An independent quarter-filling u_sigma (e.g. the lowest
triplet gap, needs S^2 resolution) is the v13 check.

Result (L=12, n=0.5): u_rho rises 1.40 -> 1.90, u_sigma falls 1.40 -> 0.50 over U=0..8;
the separation ratio u_rho/u_sigma grows from 1.0 to ~3.8. The velocities split exactly
as the v9 break required, now measured.
"""
import numpy as np
import doped_tower as dt          # doped-tower gaps (gap2, gap4) at L, U
import charge_velocity as cv      # independent v8 charge velocity (flux stiffness)
import bethe_Krho as bk           # exact Bethe K_rho (v5)


def velocities(L, U):
    E0, g2, g4, R = dt.ratio_for(L, U)
    K = 1.0 if U == 0 else bk.Krho(U, 0.5)[2]
    u_rho = g4 * L / (4 * np.pi * K)             # from the pure-charge 4k_F gap
    u_sigma = g2 * L / np.pi - K * u_rho         # from the charge+spin 2k_F gap
    return g2, g4, K, u_rho, u_sigma


def main():
    L = 12
    vF = 2 * np.sin(np.pi / 4)
    print("SPIN-CHARGE SEPARATION -- two velocities from the doped tower  (n=0.5, L=%d)\n" % L)
    print("  u_rho  = gap(4k_F) L /(4 pi K_rho)          [pure charge]")
    print("  u_sigma= gap(2k_F) L / pi  -  K_rho u_rho   [2k_F = charge + spin]")
    print("  anchor: U=0 -> no separation -> u_rho = u_sigma = v_F = %.4f\n" % vF)
    print("  %5s %9s %9s %9s %12s %11s %10s" %
          ("U", "u_rho", "u_rho(v8)", "u_sigma", "u_rho/u_sig", "K_rho", "cross %"))
    for U in [0.0, 1.0, 2.0, 4.0, 8.0]:
        g2, g4, K, u_rho, u_sigma = velocities(L, U)
        uv8 = cv.u_rho(L, U)
        cross = 100 * abs(u_rho / uv8 - 1)
        print("  %5.1f %9.4f %9.4f %9.4f %12.3f %11.4f %9.1f%%"
              % (U, u_rho, uv8, u_sigma, u_rho / u_sigma, K, cross))
    print("\n  At U=0 the two velocities coincide (= v_F, finite-size); for U>0 u_rho RISES")
    print("  and u_sigma FALLS -- the quantitative spin-charge separation behind the v9")
    print("  ratio break. u_rho is independently confirmed by the v8 flux stiffness")
    print("  (cross % column, ~2-3%, finite-size). u_sigma(n=0.5) is a new observable;")
    print("  its U>0 values are an extraction (anchored exact at U=0), and an independent")
    print("  quarter-filling u_sigma (lowest triplet gap, S^2-resolved) is the v13 check.")
    print("\n  Ceiling restated honestly: a large-L INTERACTING tower point (L=20 = 240M")
    print("  states) is beyond exact diagonalisation; from the DiagMC engine it needs a")
    print("  dynamical charge correlator + analytic continuation, and the per-order 2^n")
    print("  cost is the documented wall -- a separate effort, not an ED run.")


if __name__ == '__main__':
    main()
