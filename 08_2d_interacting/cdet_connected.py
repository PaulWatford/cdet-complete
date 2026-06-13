"""cdet_connected.py (v179, Tier 0) -- the connected-determinant recursion, validated on exactly-solvable cases.

The rest of the suite is a validation harness *around* a frozen engine; it never actually implemented the connected
determinant (CDet) itself -- the trick (Rossi, PRL 119, 045701, 2017) of summing all connected diagram topologies at
fixed vertex positions via a determinant recursion. This module implements that recursion and proves it correct against
cases with a known answer. It is a faithful, gated implementation of CDet at low order on the atom and the 2-site lattice
-- not a contribution to the sign problem (the actual frontier is a Monte Carlo sampler at high order in the strong-U,
low-T, doped regime; see INDEX.md / the v177 discussion). What it does is make the suite honest: it now contains a
correct CDet, demonstrated on exactly-solvable systems.

THE RECURSION. At order n the n interaction vertices sit at fixed (site, tau) positions. The sum of ALL diagrams
(connected + disconnected) factorizes into a determinant per spin; for the spin-symmetric Hubbard vertex U n_up n_dn the
full weight is D(V) = det M(V)^2, with M(V)_{ab} = G0(vertex_a, vertex_b). The CONNECTED weight C(V) is extracted by
Rossi's recursion, marking one vertex v*:

        C(V) = D(V) - sum_{ v* in S subsetneq V } C(S) * D(V minus S).

This is the exact inverse of the linked-cluster identity D(V) = sum_{partitions P of V} prod_{B in P} C(B), which is the
combinatorial heart and is checked here to machine precision with no quadrature. The free-energy series then follows from
ln(Z/Z0) = sum_n (-U)^n / n! * integral C, i.e. the U^n coefficient is (-1)^n * integral over the ordered-tau simplex of
C (C is symmetric in the vertices).

VALIDATION (three gates):
  1. linked-cluster identity D(V) = sum_partitions prod C(B) at random positions, n=2..5 -> machine precision.
  2. atom lnZ U-series, orders 1..5, vs the closed form ln(1 + 2 e^{bmu} + e^{-bU+2bmu}) -> machine precision.
  3. 2-site Hubbard lnZ U-series, orders 1..3, vs exact diagonalization -> ~1e-6 (order 3 limited by the ED Taylor fit).
Frozen reference engine untouched.
"""
import itertools
import numpy as np
from numpy.polynomial.legendre import leggauss

# ----------------------------------------------------------------------------------------------------------------------
# free propagators. a vertex is (site, tau). G0 for one level eps; the atom is one site (eps=-mu), the 2-site uses
# bonding/antibonding levels eps_-/+ = -mu -/+ t with weights from phi_bond=(1,1)/rt2, phi_anti=(1,-1)/rt2.
# ----------------------------------------------------------------------------------------------------------------------
def _g_level(eps, tau, beta):
    f = 1.0 / (np.exp(beta * eps) + 1.0)
    if tau == 0.0:
        return f                                   # diagonal G0(0^-) = density
    if tau > 0:
        return -(1.0 - f) * np.exp(-eps * tau)
    return f * np.exp(-eps * tau)


def g0_atom(va, vb, beta, mu, t=1.0):
    return _g_level(-mu, va[1] - vb[1], beta)


def g0_2site(va, vb, beta, mu, t=1.0):
    ep, em = -mu - t, -mu + t
    gp = _g_level(ep, va[1] - vb[1], beta); gm = _g_level(em, va[1] - vb[1], beta)
    sign = 1.0 if va[0] == vb[0] else -1.0
    return 0.5 * (gp + sign * gm)


# ----------------------------------------------------------------------------------------------------------------------
# full weight D(V) = det(M)^2  and the connectedness recursion C(V)
# ----------------------------------------------------------------------------------------------------------------------
def Dweight(verts, g0, beta, mu, t=1.0):
    n = len(verts)
    if n == 0:
        return 1.0
    M = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            M[i, j] = g0(verts[i], verts[j], beta, mu, t)
    d = np.linalg.det(M)
    return d * d


def Cweight(verts, g0, beta, mu, t=1.0, memo=None):
    key = tuple(sorted(verts))
    if memo is None:
        memo = {}
    if key in memo:
        return memo[key]
    n = len(key)
    if n == 1:
        memo[key] = Dweight(key, g0, beta, mu, t); return memo[key]
    v = key[0]; rest = key[1:]
    tot = Dweight(key, g0, beta, mu, t)
    for r in range(n - 1):                          # proper subsets S containing v (S != V)
        for combo in itertools.combinations(rest, r):
            S = (v,) + combo
            comp = tuple(x for x in key if x not in S)
            tot -= Cweight(S, g0, beta, mu, t, memo) * Dweight(comp, g0, beta, mu, t)
    memo[key] = tot
    return tot


# ----------------------------------------------------------------------------------------------------------------------
# free-energy series:  U^n coefficient = (-1)^n * integral_{0<t1<...<tn<beta} C  (summed over site assignments)
# ----------------------------------------------------------------------------------------------------------------------
def lnZ_coeff(n, g0, beta, mu, t=1.0, sites_per_vertex=1, P=20):
    x, w = leggauss(P)
    tot = 0.0
    for sites in itertools.product(range(sites_per_vertex), repeat=n):
        def rec(k, upper, taus):
            if k == 0:
                verts = tuple((sites[m], taus[m]) for m in range(n))
                return Cweight(verts, g0, beta, mu, t, {})
            nodes = upper * (x + 1) / 2; wts = w * upper / 2; s = 0.0
            for nd, wt in zip(nodes, wts):
                s += wt * rec(k - 1, nd, taus + [nd])
            return s
        tot += rec(n, beta, [])
    return ((-1) ** n) * tot


# ---- reference answers --------------------------------------------------------------------------------------------
def atom_exact_coeffs(N, beta, mu):
    import mpmath as mp
    mp.mp.dps = 40
    a = 1 + 2 * mp.e ** (beta * mu); b = mp.e ** (2 * beta * mu)
    return [float(c) for c in mp.taylor(lambda U: mp.log(a + b * mp.e ** (-beta * U)), 0, N)]


def _set_partitions(c):
    c = list(c)
    if len(c) == 1:
        yield [c]; return
    first = c[0]
    for rest in _set_partitions(c[1:]):
        for i in range(len(rest)):
            yield rest[:i] + [[first] + rest[i]] + rest[i + 1:]
        yield [[first]] + rest


def ed_2site_coeffs(N, beta, mu, t=1.0):
    norb = 4; dim = 1 << norb
    occ = lambda s, p: (s >> p) & 1
    jw = lambda s, p: -1 if bin(s & ((1 << p) - 1)).count("1") & 1 else 1

    def H(U):
        Hm = np.zeros((dim, dim))
        for s in range(dim):
            d = 0.0
            for st in range(2):
                d += U * occ(s, st * 2) * occ(s, st * 2 + 1) - mu * (occ(s, st * 2) + occ(s, st * 2 + 1))
            Hm[s, s] += d
            for sp in range(2):
                a, b = sp, 2 + sp
                for (p, q) in [(a, b), (b, a)]:
                    if occ(s, p) and not occ(s, q):
                        s2 = s & ~(1 << p); g = jw(s, p); s3 = s2 | (1 << q); g *= jw(s2, q); Hm[s3, s] += -t * g
        return Hm
    Us = np.linspace(-0.12, 0.12, 11); ys = []
    for U in Us:
        ev = np.linalg.eigvalsh(H(U)); m = ev.min(); ys.append(np.log(np.exp(-beta * (ev - m)).sum()) - beta * m)
    return np.polyfit(Us, ys, 8)[::-1]


# ----------------------------------------------------------------------------------------------------------------------
def _selftest():
    print("cdet_connected self-test (Tier 0: the connected-determinant recursion, validated on solvable cases):")
    beta, mu = 2.0, 0.5

    # (1) linked-cluster identity D(V) = sum_partitions prod C(B) -- exact, no quadrature
    rng = np.random.default_rng(0); worst = 0.0
    for n in (2, 3, 4, 5):
        for _ in range(20):
            verts = [(0, x) for x in rng.uniform(0, beta, n)]; memo = {}
            D = Dweight(tuple(verts), g0_atom, beta, mu)
            s = sum(np.prod([Cweight(tuple(B), g0_atom, beta, mu, 1.0, memo) for B in P]) for P in _set_partitions(verts))
            worst = max(worst, abs(D - s))
    assert worst < 1e-11, worst
    print(f"  [1 recursion] linked-cluster identity exact for n=2..5 (worst dev {worst:.0e})")

    # (2) atom lnZ series vs the closed form, orders 1..5
    ex = atom_exact_coeffs(5, beta, mu); wa = 0.0
    for n, P in [(1, 20), (2, 20), (3, 16), (4, 12), (5, 10)]:
        cd = lnZ_coeff(n, g0_atom, beta, mu, 1.0, 1, P); wa = max(wa, abs(cd - ex[n]))
    assert wa < 1e-11, wa
    print(f"  [2 atom]      lnZ U-series orders 1..5 == closed form (worst dev {wa:.0e})")

    # (3) 2-site lattice lnZ series vs ED, orders 1..3
    edc = ed_2site_coeffs(3, beta, mu, 1.0)
    d1 = abs(lnZ_coeff(1, g0_2site, beta, mu, 1.0, 2, 20) - edc[1])
    d2 = abs(lnZ_coeff(2, g0_2site, beta, mu, 1.0, 2, 18) - edc[2])
    d3 = abs(lnZ_coeff(3, g0_2site, beta, mu, 1.0, 2, 12) - edc[3])
    assert d1 < 1e-6 and d2 < 1e-6 and d3 < 1e-4, (d1, d2, d3)
    print(f"  [3 2-site]    lnZ U-series vs ED: order1 {d1:.0e}, order2 {d2:.0e}, order3 {d3:.0e} (o3 ED-fit limited)")
    print("  => the connected-determinant recursion is correct on the atom and the 2-site lattice. This is a faithful")
    print("     low-order CDet, not a sign-problem result. Frozen engine untouched. PASS")


if __name__ == "__main__":
    _selftest()
