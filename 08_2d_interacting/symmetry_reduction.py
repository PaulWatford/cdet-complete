"""Exact lattice-symmetry reduction of the connected-determinant site sum.

The connected weight C_V is invariant under any site permutation that (a) commutes with the
hopping matrix and (b) fixes the external site(s). Those permutations form the stabilizer group
G_0. They fold the discrete site-configuration sum into orbits: compute C_V once per orbit
representative, weight by the orbit size, and recover the EXACT same sum with |G_0|-fold fewer
evaluations.

This removes redundant computation ONLY. It does NOT touch the physical fermion sign: every member
of an orbit has the IDENTICAL value (and therefore the identical sign), so nothing cancels -- you
simply stop recomputing copies. Verified to machine precision.

For the 2x2 torus with the external on one site, |G_0| = 2 (a diagonal reflection), so the site
sum folds up to 2x (1.6x at n=2, ->2x as n grows). Larger clusters carry larger stabilizers (the
square point group is order 8, more once the external site is chosen to maximise it), so the fold
grows with the lattice's symmetry. The frozen engine is untouched; this wraps it.
"""
import itertools
from collections import defaultdict
import numpy as np


def symmetry_group(hop, tol=1e-9):
    """All site permutations P with P^T . hop . P = hop (the lattice automorphism group)."""
    L = hop.shape[0]; I = np.eye(L); G = []
    for perm in itertools.permutations(range(L)):
        P = I[list(perm)]
        if np.allclose(P @ hop @ P.T, hop, atol=tol):
            G.append(perm)
    return G


def stabilizer(group, fixed_sites):
    """Subgroup fixing every site in fixed_sites (the external legs of the observable)."""
    return [p for p in group if all(p[s] == s for s in fixed_sites)]


def square_point_stabilizer(Lx, Ly, hop, external=0, tol=1e-9):
    """Point-group operations about the external site that commute with hop.

    Generator-based (the eight square point operations: 4 rotations + 4 reflections), so it scales
    to large lattices with no L! enumeration. Returns the subset that commutes with hop AND fixes
    the external site -- i.e. the little group of the external. For a square lattice with the
    external on the origin this is up to D4 (order 8); the column/row-slice reflections live here.
    Index convention i = x + Lx*y; external assumed at the origin (site 0)."""
    if external != 0:
        raise NotImplementedError("point stabilizer is implemented for the origin (site 0)")
    L = Lx * Ly
    coord = lambda i: (i % Lx, i // Lx)
    idx = lambda x, y: (x % Lx) + Lx * (y % Ly)
    ops = [lambda x, y: (x, y), lambda x, y: (-y, x), lambda x, y: (-x, -y), lambda x, y: (y, -x),
           lambda x, y: (x, -y), lambda x, y: (-x, y), lambda x, y: (y, x), lambda x, y: (-y, -x)]
    G0 = []
    for f in ops:
        perm = tuple(idx(*f(*coord(i))) for i in range(L))
        P = np.eye(L)[list(perm)]
        if perm[0] == 0 and np.allclose(P @ hop @ P.T, hop, atol=tol):
            G0.append(perm)
    return G0


def cube_hopping(L, t=1.0):
    """Nearest-neighbour hopping on the L x L x L cubic torus (index i = x + L*y + L*L*z)."""
    N = L ** 3
    co = lambda i: (i % L, (i // L) % L, i // (L * L))
    ix = lambda x, y, z: (x % L) + L * ((y % L) + L * (z % L))
    H = np.zeros((N, N))
    for i in range(N):
        x, y, z = co(i)
        for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            H[i, ix(x + d[0], y + d[1], z + d[2])] += -t
    return H


def cube_point_stabilizer(L, hop, tol=1e-9):
    """O_h point operations (signed axis permutations) about the origin that commute with hop.

    The 45-degree diagonal slices of the cube are the axis-swap elements (a non-identity permutation
    of the x,y,z axes). On a 4x4x4 torus this returns the full O_h (order 48); on the 2x2x2 the axis
    reflections become trivial so it collapses to the axis-permutation subgroup (order 6). The slices
    fold the site sum like the square's column/row slices, only with a larger group."""
    import itertools as it
    N = L ** 3
    co = lambda i: (i % L, (i // L) % L, i // (L * L))
    ix = lambda x, y, z: (x % L) + L * ((y % L) + L * (z % L))
    G0 = []
    for perm in it.permutations(range(3)):
        for signs in it.product([1, -1], repeat=3):
            def f(x, y, z, perm=perm, signs=signs):
                c = (x, y, z); return tuple(signs[k] * c[perm[k]] for k in range(3))
            p = tuple(ix(*f(*co(i))) for i in range(N))
            P = np.eye(N)[list(p)]
            if p[0] == 0 and np.allclose(P @ hop @ P.T, hop, atol=tol):
                G0.append(p)
    return G0


def cv_cached(cdet, V, mu, cache):
    """C_V via the Rossi recursion with D_vac/D_corr MEMOIZED on the vertex SUBSET.

    D_vac and D_corr depend only on the subset of vertices (as a set), not on which configuration
    of the site sum is asking. Across an enumerated site sum at fixed times the same subsets recur
    massively (e.g. 6.7x at n=3 on 4x4), so caching them removes that recomputation exactly.
    `cache` is a dict carried across calls; keys are (kind, sorted vertex tuple)."""
    n = len(V); Nm = 1 << n; Dv = [None] * Nm; C = [None] * Nm
    for mask in range(Nm):
        key = (0, tuple(sorted(V[i] for i in range(n) if mask >> i & 1)))
        if key not in cache:
            cache[key] = cdet._Dvac([V[i] for i in range(n) if mask >> i & 1], mu)
        Dv[mask] = cache[key]
    for k in range(n + 1):
        for mask in range(Nm):
            if bin(mask).count("1") != k:
                continue
            key = (1, tuple(sorted(V[i] for i in range(n) if mask >> i & 1)))
            if key not in cache:
                cache[key] = cdet._Dcorr([V[i] for i in range(n) if mask >> i & 1], mu)
            val = cache[key]; sm = (mask - 1) & mask
            while True:
                if sm != mask:
                    val = val - C[sm] * Dv[mask ^ sm]
                if sm == 0:
                    break
                sm = (sm - 1) & mask
            C[mask] = val
    return C[Nm - 1]


def fold_site_sum_cached(cdet, times, group, mu, external_sites=(0,)):
    """fold_site_sum with subset memoization: orbit fold x determinant cache, both exact.

    Returns (total, n_unique_determinants, n_subset_evals_brute). The two reductions compose:
    the orbit fold cuts the configs evaluated, the cache cuts the determinants per config."""
    L = cdet.U.shape[0]; n = len(times)
    G0 = stabilizer(group, external_sites) if group and len(group[0]) == L else group
    orbits = defaultdict(list)
    for sites in itertools.product(range(L), repeat=n):
        orbits[min(tuple(p[s] for s in sites) for p in G0)].append(sites)
    cache = {}; total = 0.0
    for members in orbits.values():
        rep = members[0]
        total += cv_cached(cdet, [(s, t) for s, t in zip(rep, times)], mu, cache).real * len(members)
    return total, len(cache), (L ** n) * (2 ** n) * 2


def orbit_rep(sites, group):
    """Canonical representative of a site-tuple's orbit under the group."""
    return min(tuple(p[s] for s in sites) for p in group)


def fold_site_sum(cdet, times, group, mu, external_sites=(0,)):
    """EXACT sum of C_V over all L^n site assignments at fixed `times`, folded by `group`.

    Returns (total, n_reps, n_full). `total` equals the brute-force sum to machine precision;
    n_reps < n_full is the number of C_V evaluations actually performed (the saving).
    """
    L = cdet.U.shape[0]; n = len(times)
    G0 = stabilizer(group, external_sites)
    orbits = defaultdict(list)
    for sites in itertools.product(range(L), repeat=n):
        orbits[min(tuple(p[s] for s in sites) for p in G0)].append(sites)
    total = 0.0
    for members in orbits.values():
        rep = members[0]
        total += cdet.C_V([(s, t) for s, t in zip(rep, times)], mu).real * len(members)
    return total, len(orbits), L ** n


def _selftest():
    from cdet_port import CDet
    from hubbard_ed import hop_2d_square
    hop = hop_2d_square(2, 2, 1.0); cd = CDet(hop, beta=4.0, to=0.7, ti=0.2)
    G = symmetry_group(hop); G0 = stabilizer(G, (0,))
    print(f"symmetry group |G|={len(G)}; stabilizer of external site 0 |G_0|={len(G0)}: {G0}")
    ok = True
    for n in (2, 3, 4):
        times = list(np.linspace(0.3, 3.5, n))
        brute = sum(cd.C_V([(s, t) for s, t in zip(sites, times)], 0.5).real
                    for sites in itertools.product(range(4), repeat=n))
        folded, nreps, nfull = fold_site_sum(cd, times, G, 0.5)
        match = abs(brute - folded); ok = ok and match < 1e-12
        print(f"  n={n}: folded={folded:+.6f}  match={match:.1e}  "
              f"evals {nreps} vs {nfull}  ({nfull / nreps:.2f}x fewer)")
    print("symmetry-reduction self-test:", "PASS" if ok else "FAIL")

    # the fold scales with the lattice's point group: 4x4 -> full D4 (order 8)
    hop4 = hop_2d_square(4, 4, 1.0); cd4 = CDet(hop4, beta=4.0, to=0.7, ti=0.2)
    G0_4 = square_point_stabilizer(4, 4, hop4)
    print(f"4x4 lattice: point-group stabilizer of external site 0  |G_0| = {len(G0_4)} "
          f"(includes the column/row-slice reflections)")
    for n in (2,):
        times = list(np.linspace(0.3, 3.5, n))
        brute = sum(cd4.C_V([(s, t) for s, t in zip(st, times)], 0.5).real
                    for st in itertools.product(range(16), repeat=n))
        folded, nreps, nfull = fold_site_sum(cd4, times, G0_4, 0.5)
        m = abs(brute - folded); ok = ok and m < 1e-12
        print(f"  n={n}: folded={folded:+.6f}  match={m:.1e}  evals {nreps} vs {nfull}  ({nfull / nreps:.2f}x fewer)")
    print("4x4 point-group fold self-test:", "PASS" if ok else "FAIL")

    # 3D: the fold scales further with the cube point group (4x4x4 -> O_h, order 48)
    hopc = cube_hopping(4); cdc = CDet(hopc, beta=4.0, to=0.7, ti=0.2)
    G0c = cube_point_stabilizer(4, hopc)
    print(f"4x4x4 cube: point-group stabilizer of external site 0  |G_0| = {len(G0c)} "
          f"(O_h; the 45-degree diagonal slices fold here)")
    times = [0.3, 3.5]
    brute = sum(cdc.C_V([(s, t) for s, t in zip(st, times)], 0.5).real
                for st in itertools.product(range(64), repeat=2))
    folded, nreps, nfull = fold_site_sum(cdc, times, G0c, 0.5)
    m = abs(brute - folded); ok = ok and m < 1e-12
    print(f"  n=2: folded={folded:+.6f}  match={m:.1e}  evals {nreps} vs {nfull}  ({nfull / nreps:.2f}x fewer)")
    print("cube point-group fold self-test:", "PASS" if ok else "FAIL")

    # interior redundancy: subset memoization composes with the orbit fold (exact)
    times3 = [0.3, 1.9, 3.5]
    brute3 = sum(cd4.C_V([(s, t) for s, t in zip(st, times3)], 0.5).real
                 for st in itertools.product(range(16), repeat=3))
    tot, nuniq, nbrute = fold_site_sum_cached(cd4, times3, G0_4, 0.5)
    m3 = abs(brute3 - tot); ok = ok and m3 < 1e-12
    print(f"4x4 n=3 fold+cache: total={tot:+.8f}  match={m3:.1e}  "
          f"unique determinants {nuniq} vs {nbrute} brute subset evals  ({nbrute / nuniq:.1f}x fewer)")
    print("fold+cache composition self-test:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
