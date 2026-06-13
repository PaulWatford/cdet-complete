#!/usr/bin/env python3
"""
doping_crossover.py  (v19)  --  the exact spin velocity vs the two ED routes across filling:
confirming v18 at a second doped point, and unifying the whole picture.

v18 found that at quarter filling (n=0.5) the EXACT u_sigma lies BELOW both ED routes (v13
stiffness, v15 triplet), correcting v16's transfer of the half-filling bracket. v19 tests that
at a SECOND doped filling -- n=0.833 (L=12, N=5,5, a closed shell) -- and assembles the exact-vs-
ED comparison across n = 0.5, 0.833, 1.0, with the exact spin velocity from the v18 plateau method
(validated against the half-filling Bessel curve to 0.1-0.2%).

The result is a clean crossover that unifies v16, v17, v18:
  - The STIFFNESS is ALWAYS an overestimate (above the exact at every filling) -- it carries a
    positive finite-size correction but no marginal correction.
  - The TRIPLET is above the exact when DOPED (an overestimate) but BELOW it at half filling --
    because the SU(2)_1 marginal correction (strongest at the commensurate point, v17) drags the
    triplet down, and only at n=1 does it over-correct past the exact.
  - So the EXACT lies BELOW BOTH ED routes in the doped regime (n=0.5 well below, n=0.833 just
    below the triplet) and BETWEEN them at half filling (triplet < exact < stiffness, v16).
The exact/triplet ratio rises smoothly toward 1 as n -> 1 from below, then the triplet collapses
(marginal correction) so the exact sits above it at half filling. The stiffness stays the upper
envelope throughout. This is the doping dependence of the finite-size corrections made explicit.

Honest scope: exact values are for U>=2 (small U is resolution-limited, the sharp-kernel wall,
v18). ED routes are L=12 (n=0.5, 0.833) and L=10 (n=1.0). The heavy ED values are tabulated in
ED_TAB (reproducible via stiff()/trip()); the exact Bethe is computed live. NOTE: a full run is
~4-5 min (nine dense Bethe solves); the printed table below is the captured result.

Captured result (this is what the script prints):
  n      U   EXACT   stiffness  triplet   exact/trip   position
  0.500  2  0.9512   1.2623    1.1327    0.840      below both
  0.500  4  0.8358   1.0309    0.9074    0.921      below both
  0.500  8  0.5847   0.7083    0.6251    0.935      below both
  0.833  2  1.4505   1.7668    1.5954    0.909      below both
  0.833  4  1.2334   1.4421    1.2410    0.994      below both
  0.833  8  0.8033   0.9376    0.8149    0.986      below both
  1.000  2  1.6399   1.8328    1.2434    1.319      between (above triplet, below stiffness)
  1.000  4  1.2263   1.4137    0.6464    1.898      between
  1.000  8  0.7305   0.8431    0.3229    2.262      between
"""
import numpy as np
import bethe_spin_velocity_integrated as bsi
import spin_stiffness_qf as ss
import predict_vs_compute as p


def vF(n):
    return 2 * np.sin(np.pi * n / 2)


def stiff(L, Nu, Nd, U, Phi=0.4):
    e0 = ss.E0_spinflux(L, Nu, Nd, U, 0.0)
    ep = ss.E0_spinflux(L, Nu, Nd, U, Phi)
    return np.pi * (L / 2) * 2 * (ep - e0) / Phi ** 2


def trip(L, Nu, Nd, U, dt0=None):
    if dt0 is None:
        e0, _ = p.ED(L, Nu, Nd).solve(0.0); e1, _ = p.ED(L, Nu + 1, Nd - 1).solve(0.0); dt0 = e1 - e0
    e0, _ = p.ED(L, Nu, Nd).solve(U); e1, _ = p.ED(L, Nu + 1, Nd - 1).solve(U)
    return vF((Nu + Nd) / L) * (e1 - e0) / dt0


# Heavy ED values, computed this session via stiff()/trip() and tabulated so the script runs
# fast; reproduce with stiff(L,Nu,Nd,U), trip(L,Nu,Nd,U). n=0.833: L=12,N=5,5 (627k-dim solves);
# n=1.0: L=10,N=5,5 (the half-filling closed shell, from v16).
ED_TAB = {
    10/12: {2.0: (1.7668, 1.5954), 4.0: (1.4421, 1.2410), 8.0: (0.9376, 0.8149)},
    1.0:   {2.0: (1.8328, 1.2434), 4.0: (1.4137, 0.6464), 8.0: (0.8431, 0.3229)},
}


def main():
    Us = [2.0, 4.0, 8.0]
    print("Exact spin velocity vs the two ED routes, across filling (v19)\n")
    print("  n      U   EXACT   stiffness  triplet   exact/trip   position")
    for n, L, Nu, Nd in [(0.5, 12, 3, 3), (10/12, 12, 5, 5), (1.0, 10, 5, 5)]:
        dt0 = None
        if n == 0.5:
            e0, _ = p.ED(L, Nu, Nd).solve(0.0); e1, _ = p.ED(L, Nu + 1, Nd - 1).solve(0.0); dt0 = e1 - e0
        tab = ED_TAB.get(n if n == 1.0 else 10/12) if n != 0.5 else None
        for U in Us:
            ex = bsi.u_sigma_bethe(U, n)
            if tab is not None:
                s, t = tab[U]
            else:
                s = stiff(L, Nu, Nd, U); t = trip(L, Nu, Nd, U, dt0)
            pos = "below both" if ex < min(s, t) else ("between" if ex < max(s, t) else "above both")
            print("  %.3f  %.0f  %.4f   %.4f    %.4f    %.3f      %s"
                  % (n, U, ex, s, t, ex / t, pos))
        print()
    print("  Read: the STIFFNESS is always above the exact (always an overestimate). The TRIPLET")
    print("  is above the exact when doped but below it at half filling (the marginal correction,")
    print("  strongest at n=1, drags it past the exact). So the exact is BELOW BOTH ED routes in")
    print("  the doped regime and BETWEEN them at half filling -- one crossover unifying v16/v18.")
    print("  exact/triplet climbs 0.84->0.99 as n: 0.5->0.833, then the triplet collapses at n=1.")


if __name__ == '__main__':
    main()
