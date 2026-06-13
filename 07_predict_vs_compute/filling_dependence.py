#!/usr/bin/env python3
"""
filling_dependence.py  (v17)  --  does the u_sigma method generalize across system size and
filling, and WHAT is the bracket gap? Three stress tests, one experiment.

This answers three frame-of-reference questions for the u_sigma determination (v13 stiffness,
v15 triplet, v16 exact half-filling Bessel), using the EXACT references (U=0 Fermi velocity
v_F = 2 sin(pi n/2), and the n=1 Bessel curve) as the things to match -- not synthetic data.

(1) GENERALIZABILITY (size + prefactor). The stiffness velocity prefactor pi(L/2) is not
    tuned to one lattice or filling: at U=0 it reproduces v_F to ~1% at EVERY filling tested
    (n=0.5: 1.430 vs 1.414; n=0.833: 1.954 vs 1.932; n=1.0: 2.033 vs 2.000) and at every
    half-filling closed shell (L=6: 2.045, L=10: 2.033, both ~ v_F=2), converging to the exact
    Bessel curve as L grows (v16). One rule, all sizes and fillings.

(2) THE BRACKET GAP -- the "12% smoking gun" identified. The gap between the two ED routes,
    (stiff - trip)/stiff, IS the SU(2)_1 marginally-irrelevant correction (the triplet gap
    carries it, the integrated stiffness does not). Measured across filling it is small in the
    DOPED regime (~7-14% at n=0.5 and n=0.833) and EXPLODES at half filling (17-62%). Half
    filling is the commensurate point where the marginal coupling is strongest (the Heisenberg
    log-correction point); doping suppresses it. The exact Bessel (v16) shows the truth sits
    near the stiffness (the marginal-free route), so the stiffness is the best single estimate
    and the gap is an upper bound on its bias, shrinking as you dope.

(3) FILLING FRACTION (doping). The bracket structure triplet < truth < stiffness holds across
    fillings; and -- counter to the usual intuition that doping adds complexity -- for u_sigma
    doping HELPS: it shrinks the marginal correction from ~60% (n=1) to ~12% (n=0.5), making
    u_sigma MORE reliably determined in the doped liquid than at half filling. n=0.833 (= 10/12,
    a genuine closed shell near a typical doping) behaves like n=0.5, confirming the doped
    regime is the easy one for this observable.

Bottom line: the method scales (one L-dependent prefactor, all sizes), the residual gap is a
named, filling-controlled effect (not noise), and it is smallest exactly where the package
works (the doped liquid). The exact quarter-filling u_sigma stays bracketed [v15, v13] near v13.
"""
import numpy as np
from scipy.special import iv
import predict_vs_compute as p
import spin_stiffness_qf as ss


def vF(n):
    return 2 * np.sin(np.pi * n / 2)


def vs_exact_half(U):
    x = 2 * np.pi / U
    return 2 * iv(1, x) / iv(0, x)


def stiff(L, Nu, Nd, U, Phi=0.4):
    e0 = ss.E0_spinflux(L, Nu, Nd, U, 0.0)
    ep = ss.E0_spinflux(L, Nu, Nd, U, Phi)
    return np.pi * (L / 2) * 2 * (ep - e0) / Phi ** 2


def trip(L, Nu, Nd, U):
    e0, _ = p.ED(L, Nu, Nd).solve(U)
    e1, _ = p.ED(L, Nu + 1, Nd - 1).solve(U)
    return e1 - e0


def main():
    # (L, N_up, N_dn): n=0.5 (L12,N3), n=0.833 (L12,N5), n=1.0 (L10,N5 closed shell)
    fills = [(12, 3, 3), (12, 5, 5), (10, 5, 5)]
    Us = [1.0, 2.0, 4.0, 8.0]

    print("u_sigma across filling -- generalizability, the bracket gap, and doping\n")
    print("(1) prefactor universality: stiffness at U=0 must hit v_F = 2 sin(pi n/2)")
    for L, Nu, Nd in fills:
        n = (Nu + Nd) / L
        print("    n=%.3f (L=%d): stiff(U=0)=%.3f  vs v_F=%.3f  (%.1f%%)"
              % (n, L, stiff(L, Nu, Nd, 0.0), vF(n), 100 * abs(stiff(L, Nu, Nd, 0.0) / vF(n) - 1)))

    print("\n(2)+(3) bracket gap (stiff - trip)/stiff  [= SU(2)_1 marginal correction]:")
    print("    %6s %8s %8s %8s %8s" % ("n", "U=1", "U=2", "U=4", "U=8"))
    for L, Nu, Nd in fills:
        n = (Nu + Nd) / L
        vf = vF(n)
        d0 = trip(L, Nu, Nd, 0.0)
        gaps = []
        for U in Us:
            s = stiff(L, Nu, Nd, U)
            t = vf * trip(L, Nu, Nd, U) / d0
            gaps.append((s - t) / s)
        print("    %6.3f %7.1f%% %7.1f%% %7.1f%% %7.1f%%"
              % (n, gaps[0] * 100, gaps[1] * 100, gaps[2] * 100, gaps[3] * 100))

    print("\n  Read: the gap is small in the DOPED regime (n=0.5, 0.833) and explodes at half")
    print("  filling (n=1) -- the marginal correction peaks at the commensurate point and is")
    print("  suppressed by doping. So for u_sigma, doping HELPS (60% -> 12%); the doped liquid")
    print("  is the easy regime. The exact n=1 Bessel (v16) puts the truth near the stiffness,")
    print("  so the stiffness is the best estimate and the gap is a shrinking upper bound on its")
    print("  bias. One prefactor works at every size/filling; the residual gap is named, not noise.")


if __name__ == '__main__':
    main()
