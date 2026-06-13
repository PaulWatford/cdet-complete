#!/usr/bin/env python3
"""
dimer_efficiency.py  (v24)  --  QUANTITATIVE efficiency gain of the scheme change, on the exactly-
solvable 2-site Hubbard dimer (the simplest lattice with both hopping t and interaction U, so both
expansion schemes are non-trivial and there is an exact answer to validate against).

Two-engine methodology: the engine_exp sandbox, anchored on an exact result. Here the anchor is the
dimer ground-state energy, whose closed form E0 = (U - sqrt(U^2 + 16 t^2)) / 2 is verified against
direct ED of the half-filled 2-site Hubbard (matches to 1e-9). This is the engine's strong-coupling
question in miniature: the engine's bare series IS the expansion in U, and on the dimer that series
has the same divergence the lattice engine hits at strong coupling.

The two schemes:
  - BARE (the engine's current scheme): expand in U around U=0. Radius of convergence = 4t. Converges
    only for U < 4t (weak coupling).
  - ATOMIC (the scheme change, the engine ships G_exact_atom as the reference): expand in the hopping
    t around the atomic limit, with the full local U kept exactly. Radius = U/4. Converges only for
    t < U/4, i.e. U > 4t (strong coupling).
The radii are reciprocals (4t and U/4): the schemes are COMPLEMENTARY and tile the (U,t) plane with
a crossover at U = 4t.

Cost model: each perturbative order n costs ~3^n in the connected-determinant recursion, and the
order needed to reach accuracy eps is N_eps = ceil(ln eps / ln rho), rho = (target)/(radius). So the
cost is ~3^(N_eps), and the efficiency gain of one scheme over the other is 3^(N_bare - N_atomic).

QUANTITATIVE RESULT (eps = 1e-6, t = 1):
  U/t    bare              atomic            gain
   1     N=6  (3^6=729)     diverge           bare-only (weak coupling)
   2     N=14 (3^14=4.8M)   diverge           bare-only
   4     diverge            diverge           crossover (both marginal -- needs resummation, v23)
   6     diverge            N=24 (3^24=2.8e11) INF: bare impossible, atomic possible
   8     diverge            N=16 (3^16=4.3e7)  INF
  12     diverge            N=10 (3^10=59049)  INF
  16     diverge            N=8  (3^8=6561)    INF
  32     diverge            N=6  (3^6=729)     INF
Validation at U/t=8: exact E0 = -0.472136; bare 12-order sum = +126 (diverged); atomic 20-order
sum = -0.472136 (exact).

READING THE EFFICIENCY GAIN. In the strong-coupling regime we operate in (U/t >= 4), the bare engine
expansion DIVERGES -- it cannot reach the answer at ANY order, so its cost is effectively infinite.
The atomic scheme converges, and its cost 3^(N_atomic) DROPS rapidly as the coupling strengthens
(3^24 -> 3^16 -> 3^10 -> 3^8 -> 3^6 at U/t = 6,8,12,16,32). So the gain is not a modest constant
factor: it is the difference between an impossible calculation and a feasible one, and the feasible
cost gets cheaper the deeper into strong coupling you go. The one hard region is the crossover
U ~ 4t, where BOTH simple expansions are marginal and a resummation (Pade, v23) or hybrid is needed.
"""
import itertools
import mpmath as mp

mp.mp.dps = 40


def dimer_E0_ED(U, t):
    """Exact ground-state energy of the half-filled 2-site Hubbard by direct ED (Sz=0, N=2)."""
    orbs = [(0, 1), (1, 1), (0, -1), (1, -1)]
    states = list(itertools.combinations(range(4), 2))
    idx = {s: i for i, s in enumerate(states)}
    import numpy as np
    H = np.zeros((len(states), len(states)))
    for s in states:
        o = set(s); i = idx[s]
        for site in (0, 1):
            up = orbs.index((site, 1)); dn = orbs.index((site, -1))
            if up in o and dn in o:
                H[i, i] += U
        for spin in (1, -1):
            a = orbs.index((0, spin)); b = orbs.index((1, spin))
            for (p, q) in [(a, b), (b, a)]:
                if p in o and q not in o:
                    full = sorted(o); sp = (-1) ** full.index(p)
                    rem = [x for x in full if x != p]
                    sc = (-1) ** sorted(rem + [q]).index(q)
                    H[idx[tuple(sorted(rem + [q]))], i] += -t * sp * sc
    return float(np.linalg.eigvalsh(H)[0])


def E0(U, t):
    return (U - mp.sqrt(U * U + 16 * t * t)) / 2


def N_eps(scheme, U, t, eps=mp.mpf('1e-6'), Nmax=60):
    ex = E0(U, t)
    coeffs = mp.taylor(lambda u: E0(u, t), 0, Nmax) if scheme == 'bare' \
        else mp.taylor(lambda tt: E0(U, tt), 0, Nmax)
    var = U if scheme == 'bare' else t
    s = mp.mpf(0)
    for n in range(Nmax + 1):
        s += coeffs[n] * var ** n
        if n >= 2 and abs(s - ex) < eps * abs(ex):
            return n
    return None


def main():
    print("Quantitative efficiency: bare vs atomic expansion on the dimer (exact anchor)\n")
    print("Closed form E0 = (U - sqrt(U^2+16t^2))/2 verified vs ED:")
    for U, t in [(2, 1), (4, 1), (8, 1)]:
        cf = float(E0(mp.mpf(U), mp.mpf(t)))
        print("  U=%d t=%d: ED=%.6f  closed=%.6f  match=%s"
              % (U, t, dimer_E0_ED(U, t), cf, abs(dimer_E0_ED(U, t) - cf) < 1e-9))
    print("\nbare radius = 4t ; atomic radius = U/4 (reciprocal -> complementary, crossover U=4t)")
    print("cost ~ 3^N ; eps=1e-6 ; t=1\n")
    print("  U/t | bare              | atomic            | gain")
    t = mp.mpf(1)
    for Ur in [1, 2, 4, 6, 8, 12, 16, 32]:
        U = mp.mpf(Ur); Nb = N_eps('bare', U, t); Na = N_eps('atomic', U, t)
        bs = "diverge" if Nb is None else "N=%-2d 3^%d=%d" % (Nb, Nb, 3 ** Nb)
        as_ = "diverge" if Na is None else "N=%-2d 3^%d=%d" % (Na, Na, 3 ** Na)
        if Nb is None and Na is not None:
            gain = "INF (bare impossible)"
        elif Na is None and Nb is not None:
            gain = "bare-only (weak)"
        elif Nb is not None and Na is not None:
            gain = "3^(%d-%d)" % (Nb, Na)
        else:
            gain = "crossover (resummation)"
        print("  %3d | %-17s | %-17s | %s" % (Ur, bs, as_, gain))
    print("\nIn the strong-coupling regime (U/t>=4) the bare engine series DIVERGES (infinite cost);")
    print("the atomic scheme converges, and its cost 3^N drops as coupling strengthens. The gain is")
    print("qualitative (impossible -> possible), cheapest deep in strong coupling. The crossover")
    print("U~4t is hard for both simple schemes -- there a resummation (Pade, v23) is the handle.")


if __name__ == '__main__':
    main()
