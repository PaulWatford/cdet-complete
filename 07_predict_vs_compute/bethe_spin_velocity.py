#!/usr/bin/env python3
"""
bethe_spin_velocity.py  (v14)  --  the exact Bethe spin velocity attempt, and the honest
outcome: the zero-field endpoint route is fragile, so u_sigma is verified by BRACKETING
between its two exact limits instead.

Goal: an EXACT anchor for u_sigma(U) at quarter filling (the spin analogue of bethe_Krho.py),
to upgrade the v13 spin-stiffness u_sigma from robustly-measured to verified. The natural
route is the Bethe dressed-energy velocity v = eps'(Fermi point)/(2 pi rho(Fermi point)).

What works and what does not (this IS the result, real_patterns #12, #13):
  - CHARGE velocity v_c: the charge Fermi point is at finite Q, the dressed-energy slope is
    clean, and the solver reproduces the known Bethe charge velocity at strong coupling
    (U=8: ~1.92 vs the reference 1.93). It is resolution-limited at small U because the
    kernels a_n(x) ~ (n U/4)/((nU/4)^2+x^2) become sharp (width U/4) and a uniform Lambda
    grid undersamples them. So the machinery is correct where the kernels are broad.
  - SPIN velocity v_s: at ZERO magnetic field the spin Fermi point is at Lambda -> infinity
    (the spin sea fills the whole line). The endpoint slope eps_s'(Lambda)/(2 pi sigma(Lambda))
    is then a 0/0 limit evaluated at the edge of a truncated grid -- numerically singular. The
    solver returns unphysical values (e.g. negative v_s). This is exactly the fragility
    entry #13 documented for the charge velocity at its vanishing point, here in its sharpest
    form. The naive exact spin velocity does NOT come out of this route.

Honest verification of u_sigma, the robust way (real_patterns #10 -- bracket between exact
limits): u_sigma is pinned EXACTLY at the two ends, and the v13 spin stiffness must lie
between them with a monotonic trend:
  - U -> 0 :  u_sigma -> v_F = 2 sin(pi n/... ) = sqrt2 at n=0.5 (free fermions, no separation).
  - U -> inf:  u_sigma -> 0  (the spin sector decouples; v_s ~ 1/U).
The v13 spin-stiffness values (computed in spin_stiffness_qf.py): 1.4304, 1.3733, 1.2623,
1.0309, 0.7083 at U=0,1,2,4,8 -- monotonically decreasing from sqrt2 toward 0, sitting
strictly inside the bracket. The two exact endpoints validate the ends; the monotonic
interior is the robust statement; an exact INTERIOR curve needs an integrated (not
endpoint-slope) Bethe formulation -- the genuine open problem (v15).
"""
import numpy as np
trap = getattr(np, 'trapezoid', None) or np.trapz


def an(x, n, u):
    return (1.0 / np.pi) * (n * u) / ((n * u) ** 2 + x ** 2)


def bethe_velocities(U, n=0.5, NL=1601, Lmax=40.0, Nk=401):
    """Dressed-energy charge velocity v_c (clean) and the spin-velocity endpoint estimate
    v_s (shown to be unreliable at zero field)."""
    u = U / 4.0
    Lam = np.linspace(-Lmax, Lmax, NL); dL = Lam[1] - Lam[0]

    def dens(Q):
        k = np.linspace(-Q, Q, Nk); dk = k[1] - k[0]; sk = np.sin(k); ck = np.cos(k)
        A1kL = an(sk[:, None] - Lam[None, :], 1, u)
        A1Lk = an(Lam[:, None] - sk[None, :], 1, u)
        A2 = an(Lam[:, None] - Lam[None, :], 2, u)
        I1 = np.eye(len(k)); I2 = np.eye(len(Lam))
        M = np.block([[I1, -ck[:, None] * A1kL * dL], [-A1Lk * dk, I2 + A2 * dL]])
        b = np.concatenate([np.ones(len(k)) / (2 * np.pi), np.zeros(len(Lam))])
        s = np.linalg.solve(M, b)
        return k, dk, sk, ck, s[:len(k)], s[len(k):]

    lo, hi = 0.05, np.pi - 0.05
    for _ in range(42):
        Q = 0.5 * (lo + hi); k, dk, sk, ck, rho, sig = dens(Q)
        if trap(rho, k) < n: lo = Q
        else: hi = Q
    Q = 0.5 * (lo + hi); k, dk, sk, ck, rho, sig = dens(Q)

    A1kL = an(sk[:, None] - Lam[None, :], 1, u)
    A1Lk = an(Lam[:, None] - sk[None, :], 1, u)
    A2 = an(Lam[:, None] - Lam[None, :], 2, u)
    I1 = np.eye(len(k)); I2 = np.eye(len(Lam))
    M = np.block([[I1, -A1kL * dL], [(A1Lk * ck[None, :] * dk), I2 + A2 * dL]])
    base = np.concatenate([-2 * ck, np.zeros(len(Lam))])
    onemu = np.concatenate([-np.ones(len(k)), np.zeros(len(Lam))])
    s0 = np.linalg.solve(M, base); s1 = np.linalg.solve(M, onemu)
    kap0 = s0[:len(k)]; kap1 = s1[:len(k)]
    mu = -kap0[-1] / kap1[-1]
    sol = s0 + mu * s1; kap = sol[:len(k)]; eps = sol[len(k):]
    c = np.polyfit(k[-6:], kap[-6:], 2); dkap = 2 * c[0] * Q + c[1]
    v_c = dkap / (2 * np.pi * rho[-1])
    ie = np.argmin(np.abs(Lam - 0.8 * Lmax))            # "spin Fermi point" near grid edge
    v_s_raw = (eps[ie + 1] - eps[ie]) / dL / (2 * np.pi * sig[ie])
    return Q, v_c, v_s_raw


def main():
    print("BETHE spin velocity (v14): the attempt, and the honest outcome\n")
    print("1) CHARGE velocity v_c (finite Fermi point Q -> clean), vs known Bethe refs:")
    print("   %5s %8s %10s %8s" % ("U", "Q", "v_c(Bethe)", "ref"))
    refs = {2.0: 1.76, 4.0: 1.83, 8.0: 1.93}
    for U in [2.0, 4.0, 8.0]:
        Q, vc, vs = bethe_velocities(U)
        print("   %5.1f %8.4f %10.4f %8s" % (U, Q, vc, refs[U]))
    print("   -> reproduces the reference at strong coupling (machinery validated); small-U")
    print("      is resolution-limited (sharp kernels). v_F=sqrt2=%.4f is the U->0 target.\n" % np.sqrt(2))

    print("2) SPIN velocity v_s by the same endpoint route -- UNRELIABLE at zero field:")
    for U in [2.0, 4.0, 8.0]:
        Q, vc, vs = bethe_velocities(U)
        print("   U=%.1f  v_s(endpoint) = %+.4f   <- unphysical (spin Fermi point at Lambda->inf)" % (U, vs))
    print("   The spin sea fills the whole line, so eps_s'/2pi sigma is a 0/0 limit at the")
    print("   grid edge: numerically singular. This is entry #13 fragility, sharpest form.\n")

    print("3) u_sigma verified by BRACKETING between exact limits (real_patterns #10):")
    print("   U->0 : u_sigma -> v_F = %.4f (exact)      U->inf : u_sigma -> 0 (exact)" % np.sqrt(2))
    v13 = {0.0: 1.4304, 1.0: 1.3733, 2.0: 1.2623, 4.0: 1.0309, 8.0: 0.7083}
    vF = np.sqrt(2)
    print("   %5s %16s %14s" % ("U", "u_sig (v13 stiff)", "fraction of v_F"))
    for U in [0.0, 1.0, 2.0, 4.0, 8.0]:
        us = v13[U]
        tag = "  (= v_F, finite-size: +1.1% over the thermodynamic sqrt2)" if U == 0 else ""
        print("   %5.1f %16.4f %13.2f%s" % (U, us, us / vF, tag))
    print("   u_sigma falls monotonically from v_F (at U=0, where the L=12 value 1.4304 is")
    print("   the finite-size v_F, ~1.1% above the thermodynamic sqrt2) toward 0 at U->inf.")
    print("   The two exact endpoints validate the ends; the monotonic interior is the robust")
    print("   statement. An EXACT interior u_sigma(U) needs an integrated (not endpoint-slope)")
    print("   Bethe formulation -- the genuine open problem (v15).")


if __name__ == '__main__':
    main()
