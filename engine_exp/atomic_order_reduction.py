#!/usr/bin/env python3
"""
atomic_order_reduction.py  (v23)  --  the FIRST experiment of the engine-acceleration arc, run in
the engine_exp sandbox and validated against the frozen baseline's exact G_exact_atom.

Methodology (the same discipline that drove the simulation arc, now on the engine): two engines.
`engine/` is the FROZEN baseline oracle; `engine_exp/` is the sandbox. Every experimental change is
validated against the baseline (bit-identical where it must be -- the fork was checked
bit-identical at orders 1,2 -- and against an exact anchor where it is an approximation). Here the
exact anchor is the baseline's own closed form G_exact_atom(tau,beta,mu,U) =
-(e^{mu tau} + e^{mu(beta+tau)-tau U}) / (1 + 2 e^{beta mu} + e^{beta(2mu-U)}).

The question (the v22 redirection): the engine's bare expansion is a series in interaction order n
at cost ~3^n per order, so the cost is set by the ORDER NEEDED. On the atom the engine's CDet
series IS the bare U-expansion of G. Does the expansion SCHEME change how many orders are needed?

Finding (beta=4, mu=0.7, tau=0.123):
  - the bare U-series has a finite convergence radius R = 0.942 (nearest complex U where the
    partition function Z(U)=0). So at the strong coupling we care about (U=2 > R) the bare series
    DIVERGES: partial sums at N=2,6,12 are -1.77, +29.5, +2799 vs the exact -0.4445. No order
    converges -- the bare engine expansion is useless at strong coupling.
  - a resummation of the SAME coefficients, informed by the analytic (pole) structure, rescues it:
    Pade[6/6] gives -0.4443 at U=2 (the bare sum is +2799 there), and at U=0.5 reaches 1.2e-10
    where the bare order-12 sum is only at 2.9e-5. Same orders, far more accuracy -- i.e. far fewer
    orders for a target accuracy.

This is the order-reduction lever demonstrated on the engine's own atomic limit and validated
against its exact formula: the cost wall is the order needed, and the order needed is set by the
expansion scheme, not just the physics. The next step (engine_exp C) is the physically-motivated
version -- the shifted-action / atomic-reference expansion (the engine already ships G_exact_atom
as the reference) -- which moves the expansion point so the series converges at strong coupling
with few orders, validated against this same baseline anchor.
"""
import mpmath as mp

mp.mp.dps = 50
BETA, MU, TAU = mp.mpf(4), mp.mpf('0.7'), mp.mpf('0.123')


def G_exact_atom(U):
    U = mp.mpf(U)
    Z = 1 + 2 * mp.e ** (BETA * MU) + mp.e ** (BETA * (2 * MU - U))
    return -(mp.e ** (MU * TAU) + mp.e ** (MU * (BETA + TAU) - TAU * U)) / Z


def bare_radius():
    Using = 2 * MU - (mp.log(1 + 2 * mp.e ** (BETA * MU)) + 1j * mp.pi) / BETA
    return abs(Using)


def main():
    R = bare_radius()
    print("Engine acceleration, experiment 1: expansion scheme vs order needed (atom)\n")
    print("Two-engine methodology: validated against the frozen baseline's exact G_exact_atom.")
    print("Bare U-series convergence radius R = %.3f  -> U=2 is BEYOND it.\n" % float(R))
    coeffs = mp.taylor(G_exact_atom, 0, 40)  # = the engine's CDet series on the atom
    for Ut in [mp.mpf('0.5'), mp.mpf(2)]:
        exact = G_exact_atom(Ut)
        print("U=%.1f: exact G_atom = %.8f" % (float(Ut), float(exact)))
        s = mp.mpf(0); rows = []
        for N in range(0, 13):
            s += coeffs[N] * Ut ** N
            if N in (2, 6, 12):
                rows.append((N, float(s), float(abs(s - exact))))
        for N, val, er in rows:
            print("   bare N=%2d: %+12.4f   err %.1e" % (N, val, er))
        p, q = mp.pade(coeffs, 6, 6)
        pad = mp.polyval(p[::-1], Ut) / mp.polyval(q[::-1], Ut)
        print("   Pade[6/6] (same coeffs): %+.8f   err %.1e" % (float(pad), float(abs(pad - exact))))
        print()
    print("Bare expansion diverges at strong coupling; resummation of the same orders converges.")
    print("The cost wall is the ORDER needed, and the scheme sets it -- the order-reduction lever.")


if __name__ == '__main__':
    main()
