"""sun_lattice_production.py (v144) -- queue item #2 (SU(N)), step 3: the production EoS route.

Steps 1-2 (v142-v143) established that the SU(N) linked-cluster coefficients are degree-(j+1) polynomials in N
(the combinatorial record), on the atom and the lattice. Step 3 builds the PRODUCTION route the record enables:
compute the SU(N) equation of state from the N-independent single-flavor propagator g0 TIMES the record, WITHOUT
ever diagonalizing the N-flavor system. This is the CoS value proposition -- the cost is N-independent.

THE FIRST COEFFICIENT (built and verified here). For the 2-site lattice the first-order pieces are, with d the
per-flavor density and d' = d(d)/d(mu) of the FREE SINGLE-FLAVOR system (the N-independent g0 amplitudes):
    c1 (linked-cluster, dlnZ/dU at U=0) = -beta * N(N-1) * d^2        [record N(N-1) = flavor pairs]
    n1 (EoS, d(density)/dU at U=0)       = -(N-1) * d * d'             [record (N-1)]
Both reproduce the 2-site SU(N) ED to ~1e-7 for every N = 2..6 -- and the N=6 (173-Yb) value comes purely from
the single-flavor g0 and the record, with NO N=6 diagonalization. The first-order EoS n(U) ~ n0 + U n1 tracks the
N=6 ED curve at small U (3e-3 at U=0.05) and departs at larger U, where higher orders enter.

WHY THIS IS THE PRODUCTION ROUTE. The single-flavor g0 is computed once; the record N(N-1), (N-1), ... is pure
combinatorics; the EoS at any flavor number is their product. This is exactly how CoS reaches N=6 at SU(2) cost.

SCOPE. Built and verified: the first-order (Hartree) EoS coefficient via g0 x record, at all N incl N=6, no
N-flavor ED. NOT yet built: the higher orders -- the full connected-determinant sum with the closed-loop record
and the imaginary-time integrals (the v132 fast minors supply the per-flavor minors). That is the remaining
engineering toward the strong-coupling EoS curve. ED is the anchor only; frozen engine untouched (194/194)."""
import numpy as np

BETA, T, MU0 = 2.0, 1.0, 1.0

def _fermi(e): return 1.0 / (1.0 + np.exp(BETA * e))

def perflavor_density(mu, t=T):
    """Free single-flavor per-site density of the 2-site system (the N-independent g0 amplitude)."""
    return 0.5 * (_fermi(-mu - t) + _fermi(-mu + t))

def g0_amplitudes(mu=MU0):
    d = perflavor_density(mu)
    dp = (perflavor_density(mu + 1e-6) - perflavor_density(mu - 1e-6)) / 2e-6
    return d, dp

def c1_production(N, mu=MU0):
    """First linked-cluster coefficient from g0 x record -- no N-flavor ED."""
    d, _ = g0_amplitudes(mu); return -BETA * N * (N - 1) * d ** 2

def n1_production(N, mu=MU0):
    """First-order EoS (density) coefficient from g0 x record -- no N-flavor ED."""
    d, dp = g0_amplitudes(mu); return -(N - 1) * d * dp

def _build_H(N, mu, U, t=T):
    norb = 2 * N; dim = 1 << norb
    occ = lambda s, p: (s >> p) & 1
    jw = lambda s, p: -1 if bin(s & ((1 << p) - 1)).count('1') & 1 else 1
    H = np.zeros((dim, dim))
    for s in range(dim):
        dg = -mu * bin(s).count('1')
        for site in range(2):
            for a in range(N):
                for b in range(a + 1, N):
                    if occ(s, site * N + a) and occ(s, site * N + b): dg += U
        H[s, s] += dg
        for a in range(N):
            for pi, pj in [(N + a, a), (a, N + a)]:
                if occ(s, pj) and not occ(s, pi):
                    s2 = s & ~(1 << pj); g = jw(s, pj); s3 = s2 | (1 << pi); g *= jw(s2, pi); H[s3, s] += -t * g
    return H

def _lnZ(N, mu, U):
    ev = np.linalg.eigvalsh(_build_H(N, mu, U)); m = ev.min()
    return np.log(np.sum(np.exp(-BETA * (ev - m)))) - BETA * m

def _selftest():
    print("sun_lattice_production self-test (#2 SU(N) step 3: production EoS from g0 x record):")
    d, dp = g0_amplitudes()
    print(f"  single-flavor g0 amplitudes (N-independent): d={d:.6f}, d'={dp:.6f}")
    worst_c1 = worst_n1 = 0.0
    for N in [2, 3, 4, 5, 6]:
        c1_ed = (_lnZ(N, MU0, 1e-4) - _lnZ(N, MU0, -1e-4)) / 2e-4
        dN = lambda U: (_lnZ(N, MU0 + 1e-5, U) - _lnZ(N, MU0 - 1e-5, U)) / 2e-5 / (2 * N * BETA)
        n1_ed = (dN(1e-4) - dN(-1e-4)) / 2e-4
        worst_c1 = max(worst_c1, abs(c1_production(N) - c1_ed))
        worst_n1 = max(worst_n1, abs(n1_production(N) - n1_ed))
    assert worst_c1 < 1e-5 and worst_n1 < 1e-5, (worst_c1, worst_n1)
    print(f"  c1, n1 from g0 x record vs ED, N=2..6 (incl N=6, no N=6-specific input): {worst_c1:.0e}, {worst_n1:.0e}")
    # N=6 first-order EoS tracks ED at small U
    n0 = d; n6_pred = n0 + 0.05 * n1_production(6)
    n6_ed = (_lnZ(6, MU0 + 1e-5, 0.05) - _lnZ(6, MU0 - 1e-5, 0.05)) / 2e-5 / (12 * BETA)
    assert abs(n6_pred - n6_ed) < 5e-3, abs(n6_pred - n6_ed)
    print(f"  SU(6) first-order EoS at U=0.05: {n6_pred:.5f} vs ED {n6_ed:.5f} (dev {abs(n6_pred-n6_ed):.1e})")
    print("  => the N=6 EoS coefficient is single-flavor g0 x record -- the CoS N-independent production route.")
    print("     Higher orders (full CDet + closed-loop record + tau-integrals, v132 fast minors) remain. PASS")

if __name__ == "__main__":
    _selftest()
