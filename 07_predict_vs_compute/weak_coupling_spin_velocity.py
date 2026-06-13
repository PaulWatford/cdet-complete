#!/usr/bin/env python3
"""
weak_coupling_spin_velocity.py  (v21)  --  the analytic small-U handle that bridges the v20
structural wall.

v20 established that exact quarter-filling u_sigma below U=2 is not cleanly extractable by the
dressed-energy route (no asymptotic plateau at low filling + small U). v21 confirms that the
NUMERICAL routes all fail there for real reasons -- and supplies the analytic handle v20 named as
the way through.

Why the numerical routes fail at quarter-filling small U (all checked):
  - Lambda->inf plateau (v18/v20): no plateau forms (the structural wall).
  - finite-field (finite-B) read: the velocity at the finite Fermi point is recipe-sensitive
    (crude endpoint vs linear fit disagree by ~2x), so it does not pin a value.
  - ED stiffness slope: gives c(1) ~ 0.025 vs the exact 0.159 -- the finite lattice (L<=12) does
    not resolve the weak-coupling slope at all.
Three independent confirmations that this is a genuine wall, not a coding issue.

The analytic handle (weak coupling / g-ology). The spin velocity to second order:
    u_sigma(n, U) = v_F(n) - U/(2 pi) - U^2/(16 pi^2) + O(U^3),   v_F(n) = 2 sin(pi n / 2).
The LEADING coefficient 1/(2 pi) is FILLING-INDEPENDENT: the on-site U is a contact interaction,
so the 2k_F backscattering amplitude g_1 = U is momentum- (hence filling-) independent, and in
u_sigma = v_F - g_1/(2 pi) the v_F cancels out of the coefficient.

Validation (half filling, where the exact Bessel curve 2 I_1(2pi/U)/I_0(2pi/U) is known):
  - (v_F - Bessel)/U -> 0.15915 = 1/(2 pi) as U->0 (0.15947, 0.15980, 0.16046 at U=0.05,0.1,0.2).
  - the two-term form matches Bessel to 3-4 digits at U=0.5, 1.0.
So both coefficients are confirmed exactly at half filling.

Quarter filling, leading order:
    u_sigma(0.5, U) = sqrt(2) - U/(2 pi) + O(U^2)  ->  1.335, 1.255 at U=0.5, 1.0,
which sits ABOVE the v20 quarter-filling peak lower bounds (1.077, 1.019) -- consistent.

Honest scope. The LEADING coefficient (1/(2pi)) is exact at half filling and filling-independent
by the contact-interaction argument, and the quarter-filling linear term is pinned by it. The U^2
coefficient is validated at half filling but is NOT shown to be filling-independent -- at quarter
filling the curvature is larger (from U=2: linear 1.096 vs exact 0.951), so the quarter formula is
reliable only to LEADING order (U <~ 1). The full exact quarter-filling small-U curve remains the
v20 structural wall; v21 bridges it to leading order, anchored and consistent, not papered.
"""
import numpy as np
from scipy.special import iv


def vF(n):
    return 2 * np.sin(np.pi * n / 2)


def u_sigma_bessel_half(U):
    x = 2 * np.pi / U
    return 2 * iv(1, x) / iv(0, x)


def u_sigma_weak(n, U, order=2):
    """Weak-coupling spin velocity; leading coeff filling-independent, validated at half filling."""
    val = vF(n) - U / (2 * np.pi)
    if order >= 2:
        val -= U ** 2 / (16 * np.pi ** 2)
    return val


def main():
    c = 1 / (2 * np.pi)
    print("Weak-coupling spin velocity: u_sigma(n,U) = v_F(n) - U/(2pi) - U^2/(16 pi^2) + ...\n")
    print("1) Leading coefficient is EXACT at half filling (slope of the Bessel curve):")
    print("   %6s %14s" % ("U", "(vF-Bessel)/U"))
    for U in [0.2, 0.1, 0.05, 0.02]:
        print("   %6.2f %14.5f" % (U, (2.0 - u_sigma_bessel_half(U)) / U))
    print("   -> 1/(2pi) = %.5f  (extrapolated U->0). Filling-independent: U is a contact" % c)
    print("      interaction, so g_1 = U is momentum-independent and v_F cancels.\n")

    print("2) Two-term form vs exact Bessel (half filling):")
    print("   %6s %12s %12s" % ("U", "weak(2)", "Bessel"))
    for U in [0.5, 1.0, 2.0]:
        print("   %6.2f %12.4f %12.4f" % (U, u_sigma_weak(1.0, U), u_sigma_bessel_half(U)))
    print()

    print("3) Quarter filling, leading order -- bridges the v20 structural wall:")
    print("   %6s %16s %20s" % ("U", "sqrt2 - U/(2pi)", "v20 peak (lower bnd)"))
    for U, pk in [(0.5, 1.077), (1.0, 1.019)]:
        print("   %6.2f %16.4f %20s" % (U, vF(0.5) - U / (2 * np.pi), "%.3f <= true (ok)" % pk))
    print("\n   Leading-order only (U <~ 1): the linear term is pinned (filling-independent, half-")
    print("   filling-exact); the U^2 curvature is larger at quarter filling and not derived. The")
    print("   exact full small-U curve there stays the v20 wall -- bridged to leading order here.")


if __name__ == '__main__':
    main()
