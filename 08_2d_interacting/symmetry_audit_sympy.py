"""Symbolic (sympy) audit of the symmetry-reduction module.

Numerics show the diagonal-swap permutation leaves C_V invariant at hopping t=1. This proves it
SYMBOLICALLY for ALL t: the stabilizer permutations of the external site commute with the hopping
matrix as an exact polynomial identity (P^T . H(t) . P - H(t) = 0). Since the engine's propagator
G0 is a function of H alone, a permutation that fixes H (and fixes the external site) fixes G0 on
every index, hence fixes every determinant entry, hence fixes C_V exactly -- for every t, mu, beta.
That is why fold_site_sum is exact to machine precision rather than approximately.

Requires sympy (audit-time only; the runtime module symmetry_reduction.py needs only numpy).
"""
import sympy as sp


def Pmat(perm):
    """Permutation matrix matching numpy's I[list(perm)]: row i is the perm[i]-th basis vector."""
    L = len(perm); M = sp.zeros(L, L)
    for i in range(L):
        M[i, perm[i]] = 1
    return M


def audit():
    t = sp.symbols('t', real=True, nonzero=True)
    # 2x2 torus hopping, symbolic in t (each connected pair contributes -2t on the torus)
    H = sp.Matrix([
        [0, -2 * t, -2 * t, 0],
        [-2 * t, 0, 0, -2 * t],
        [-2 * t, 0, 0, -2 * t],
        [0, -2 * t, -2 * t, 0]])

    # full automorphism group of H (all permutations fixing H as a symbolic identity)
    import itertools
    G = []
    for perm in itertools.permutations(range(4)):
        P = Pmat(perm)
        if sp.simplify(P.T * H * P - H) == sp.zeros(4, 4):
            G.append(perm)
    G0 = [p for p in G if p[0] == 0]   # stabilizer of external site 0

    print("SYMBOLIC AUDIT (sympy) -- symmetry proven for ALL hopping t, not just t=1")
    print(f"  symbolic automorphism group |G| = {len(G)}")
    print(f"  stabilizer of external site 0  |G_0| = {len(G0)}: {G0}\n")
    allzero = True
    for perm in G0:
        P = Pmat(perm)
        diff = sp.simplify(P.T * H * P - H)
        commute = sp.simplify(P * H - H * P)
        z1 = diff == sp.zeros(4, 4); z2 = commute == sp.zeros(4, 4)
        allzero = allzero and z1 and z2
        print(f"  perm {perm}:  P^T H P - H = 0 : {z1}    [P,H] = 0 : {z2}   (identity in t)")
    print("\n  => the symmetry, and therefore C_V-invariance and the exact site-fold,")
    print("     is a polynomial identity in the hopping -- holds for every t, mu, beta.")

    # 4x4: prove the column/row-slice reflections (and the rest of D4) for all t
    Lx = Ly = 4; L = 16
    co = lambda i: (i % Lx, i // Lx); ix = lambda x, y: (x % Lx) + Lx * (y % Ly)
    H4 = sp.zeros(L, L)
    for i in range(L):
        x, y = co(i)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            H4[i, ix(x + dx, y + dy)] += -t
    slice_ops = {'refl_leftright (COLUMN slice)': lambda x, y: (-x, y),
                 'refl_updown (ROW slice)': lambda x, y: (x, -y),
                 'rot90': lambda x, y: (-y, x), 'refl_diag': lambda x, y: (y, x)}
    print("\n  4x4 point-group slice operations (proven for all t):")
    for name, f in slice_ops.items():
        perm = [ix(*f(*co(i))) for i in range(L)]
        P = sp.zeros(L, L)
        for i in range(L):
            P[i, perm[i]] = 1
        z = sp.simplify(P.T * H4 * P - H4) == sp.zeros(L, L)
        allzero = allzero and z
        print(f"    {name:30s} P^T H P - H = 0 : {z}   fixes_site0={perm[0] == 0}")
    print("SYMBOLIC AUDIT:", "PASS" if allzero else "FAIL")
    return allzero


def audit_cube(L=2):
    """Prove the cube's 45-degree diagonal slices (axis swaps) commute with H(t) for all t.

    The identity is structural and size-independent (isotropic hopping is invariant under relabeling
    the x,y,z axes), so the small cube proves it for every cube size; the 4x4x4 fold is verified
    numerically in symmetry_reduction.py."""
    t = sp.symbols('t', real=True, nonzero=True)
    N = L ** 3
    co = lambda i: (i % L, (i // L) % L, i // (L * L))
    ix = lambda x, y, z: (x % L) + L * ((y % L) + L * (z % L))
    H = sp.zeros(N, N)
    for i in range(N):
        x, y, z = co(i)
        for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            H[i, ix(x + d[0], y + d[1], z + d[2])] += -t
    slices = {'swap y<->z (45-deg diagonal)': ((0, 2, 1), (1, 1, 1)),
              'swap x<->y (45-deg diagonal)': ((1, 0, 2), (1, 1, 1)),
              'swap x<->z (45-deg diagonal)': ((2, 1, 0), (1, 1, 1))}
    print(f"\nCUBE SYMBOLIC AUDIT ({L}x{L}x{L}, N={N}) -- 45-degree diagonal slices, all t:")
    allz = True
    for name, (perm, signs) in slices.items():
        f = lambda x, y, z, perm=perm, signs=signs: tuple(signs[k] * (x, y, z)[perm[k]] for k in range(3))
        p = [ix(*f(*co(i))) for i in range(N)]
        P = sp.zeros(N, N)
        for i in range(N):
            P[i, p[i]] = 1
        z = sp.simplify(P.T * H * P - H) == sp.zeros(N, N)
        allz = allz and z
        print(f"  {name:30s} P^T H(t) P - H(t) = 0 : {z}  fixes_site0={p[0] == 0}")
    print("CUBE SYMBOLIC AUDIT:", "PASS" if allz else "FAIL")
    return allz


if __name__ == "__main__":
    audit()
    audit_cube(2)
