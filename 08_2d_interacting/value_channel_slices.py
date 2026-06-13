"""Value channel (particle-hole) identities and the slice-dimension decomposition.

TWO RESULTS, both computed (v54):

1. THE VALUE CHANNEL'S -1 IS REAL BUT DRESSED (particle-hole). On a bipartite lattice with
   sublattice signs eps_i, the engine propagator satisfies, exactly:
       off-diagonal / unequal time:  G(-mu)(i,j,tau) = -eps_i eps_j G(mu)(j,i,-tau)
       equal-time diagonal (0^-):    G(-mu)(i,i,0) + G(mu)(i,i,0) = 1   (completeness sum rule)
   i.e.  G(-mu) = -D_eps G(mu)^T D_eps + I|_equal-time.
   The transpose carries the -1 we hunted, but PH maps the 0^- equal-time convention to 0^+, and
   the difference is the identity on the equal-time diagonal = a contact/DENSITY counterterm (the
   v46 d/dmu object). Consequence (verified): NO bare per-configuration ratio C_V(V;-mu)/C_V(V;mu)
   is a constant -1 -- the -1 is an operator identity between observables (+mu <-> -mu, externals
   swapped, plus a counterterm tower), not a per-config cancellation at fixed mu. The sign wall is
   untouched; the doping reflection mu <-> -mu comes with computable counterterms.

2. WEIGHT AND SIGN CONCENTRATE ON LOW-DIMENSIONAL SLICES (the cube's slice hierarchy). Classifying
   cube configs by the dimension of the affine span of (external + vertices) under minimal-image
   torus displacements: 1d (line) configs carry ~18.5x their share of |weight|, 2d (plane) ~2.1x,
   full-3d only ~0.65x -- and the per-class sign quality R degrades sharply with dimension
   (~0.22 / 0.09 / 0.004 at n=3, mu=0.5). Locality appears as a slice hierarchy: configurations
   confined to lines/planes through the external dominate and carry the best sign. This points at
   slice-stratified evaluation (exact low-dim slices + sampled 3d remainder) as the next reduction.
"""
import numpy as np


def sublattice_signs(coords):
    """eps_i = (-1)^(sum of coordinates) for a bipartite hypercubic lattice."""
    return np.array([(-1) ** int(sum(c)) for c in coords])


def ph_identity_check(cdet, eps, L, beta, mu=0.5, nsamp=200, seed=1):
    """Verify the dressed PH identity on the engine propagator. Returns (err_diag, err_off0, err_off)."""
    err_diag = max(abs(cdet.g0(i, i, 0.0, -mu) + cdet.g0(i, i, 0.0, mu) - 1.0) for i in range(L))
    err_off0 = max(abs(cdet.g0(i, j, 0.0, -mu) + eps[i] * eps[j] * cdet.g0(j, i, 0.0, mu))
                   for i in range(L) for j in range(L) if i != j)
    rng = np.random.default_rng(seed); err_off = 0.0
    for _ in range(nsamp):
        i, j = int(rng.integers(L)), int(rng.integers(L))
        tau = float(rng.uniform(0.01, beta - 0.01))
        err_off = max(err_off, abs(cdet.g0(i, j, tau, -mu) + eps[i] * eps[j] * cdet.g0(j, i, -tau, mu)))
    return err_diag, err_off0, err_off


def span_dim(sites, coord, L, include=(0,)):
    """Dimension of the affine span of the given sites (plus `include`), minimal-image on the torus."""
    pts = [np.asarray(coord(s)) for s in tuple(include) + tuple(sites)]
    D = np.array([p - pts[0] for p in pts[1:]])
    if len(D) == 0:
        return 0
    D = (D + L // 2) % L - L // 2
    return int(np.linalg.matrix_rank(D))


def slice_decomposition(cdet, coord, L, N, n=3, mu=0.5, nsamp=2000, beta=4.0, seed=8):
    """Sampled decomposition of the site sum by slice dimension. Returns {dim: array of C_V values}."""
    rng = np.random.default_rng(seed); cls = {}
    for _ in range(nsamp):
        sites = [int(rng.integers(N)) for _ in range(n)]
        V = [(s, float(rng.uniform(0, beta))) for s in sites]
        d = span_dim(sites, coord, L)
        cls.setdefault(d, []).append(cdet.C_V(V, mu).real)
    return {d: np.array(v) for d, v in cls.items()}


def _selftest():
    from cdet_port import CDet
    from hubbard_ed import hop_2d_square
    from symmetry_reduction import cube_hopping
    ok = True
    print("1) dressed PH identity (the value channel's -1 + the equal-time counterterm):")
    for name, H, L, coords in [
            ("2x2 square", hop_2d_square(2, 2, 1.0), 4, [(i % 2, i // 2) for i in range(4)]),
            ("2x2x2 cube", cube_hopping(2), 8, [(i % 2, (i // 2) % 2, i // 4) for i in range(8)])]:
        cd = CDet(H, beta=4.0, to=0.7, ti=0.2)
        eps = sublattice_signs(coords)
        ed, e0, eo = ph_identity_check(cd, eps, L, 4.0)
        good = ed < 1e-12 and e0 < 1e-12 and eo < 1e-6
        ok = ok and good
        print(f"   {name}: diag sum-rule err {ed:.1e} | off-diag t=0 err {e0:.1e} | off-diag err {eo:.1e}"
              f"  -> {'PASS' if good else 'FAIL'}")
    print("2) slice classifier (cube, span through the external):")
    Lc = 4
    cdc = CDet(cube_hopping(Lc), beta=4.0, to=0.7, ti=0.2)
    co = lambda i: (i % Lc, (i // Lc) % Lc, i // (Lc * Lc))
    cases = {(0,): 0, (1,): 1, (1, 2): 1, (1, 4): 2, (1, 4, 16): 3}
    for sites, want in cases.items():
        got = span_dim(sites, co, Lc)
        ok = ok and (got == want)
        print(f"   sites {sites}: span dim {got} (expect {want})")
    print("value-channel + slices self-test:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
