"""Does the slice hierarchy survive scale? (v57) -- YES for weight (strengthening); sign persists, narrows.

The v54 hierarchy (weight and sign concentrate on low-dimensional slices through the external) was one
lattice at one size. Tested at L = 4, 6, 8 cubes (64 -> 512 sites), same protocol (n=3, mu=0.5, beta=4),
with TARGETED sampling of the rare 1d class (900 matched samples per class, noise floor sqrt(2/(pi n)) =
0.027):

    L   1d: mean|C| / R        bulk(3d): mean|C| / R     1d/bulk density ratio
    4   3.5e-06  / 0.652       1.1e-07  / 0.062          32x
    6   5.4e-07  / 0.366       7.3e-09  / 0.064          74x
    8   1.3e-07  / 0.244       8.1e-10  / 0.157          165x

FINDINGS (honest):
  1. The WEIGHT-DENSITY hierarchy survives and STRENGTHENS with system size: per-configuration weight
     on 1d lines through the external exceeds the 3d bulk by a factor that GROWS 32x -> 74x -> 165x.
     Uniform-sample d=2 concentration likewise grows (2.06x -> 3.35x -> 4.34x share-of-weight over
     share-of-configs). This is locality expressed as geometry: the propagator's decay makes
     high-dimensional (spread-out) configurations both tiny and numerous.
  2. The SIGN hierarchy persists at every size but NARROWS: 1d R decays 0.652 -> 0.366 -> 0.244 while
     the bulk sits at/near the statistical floor (0.06 at L=4,6). CAVEAT flagged, not hidden: the L=8
     bulk reads R=0.157, above the 0.027 floor -- possibly heavy-tail inflation of the ratio
     estimator; unresolved, recorded.
  3. REFINEMENT OF v54 ON THE RECORD: v54's per-class R at L=4 used uniform sampling (d=1 had only 12
     configs; R=0.224 was noise-dominated). Targeted sampling gives the well-measured value 0.652.

CONCEPTUAL READING (the theory-extraction claim this supports, stated carefully): the sign problem's
weight is concentrated in a geometrically identifiable low-dimensional sector that becomes MORE
dominant per-configuration as the lattice grows, and that sector carries the healthiest sign. The
diffuse bulk -- exponentially many, individually negligible, sign-incoherent -- is where the variance
lives. This is a measured geometric structure of configuration space, not yet a theory of it.

FastCDet: the engine propagator with the eigenmode loop vectorized -- validated against the
frozen-port-validated CDet to 4e-17 (self-test gate 1e-12), ~40x faster; what makes 512 sites
reachable. Frozen engine untouched.
"""
import numpy as np
from cdet_port import CDet


class FastCDet(CDet):
    """CDet with g0's eigenmode loop vectorized. Identical values (self-test gates < 1e-12)."""

    def g0(self, i, j, tau, mu):
        beta = self.beta; tt = complex(tau)
        while tt.real > beta:
            tt -= 2 * beta
        while tt.real <= -beta:
            tt += 2 * beta
        xi = self.ev - mu; nf = 1.0 / (np.exp(beta * xi) + 1.0)
        if tt.real > 0:
            gk = -(1.0 - nf) * np.exp(-xi * tt)
        elif tt.real < 0:
            gk = nf * np.exp(-xi * tt)
        else:
            gk = nf
        return np.sum(self.U[i, :] * self.U[j, :] * gk)


LINE_DIRS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1),
             (1, -1, 0), (1, 0, -1), (0, 1, -1), (1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]


def line_class_stats(cdet, Lc, nsamp=600, mu=0.5, beta=4.0, seed=9):
    """Targeted 1d sampling (vertices on a random line through the external) and matched bulk."""
    idx = lambda p: int(p[0] % Lc + Lc * ((p[1] % Lc) + Lc * (p[2] % Lc)))
    N = Lc ** 3; rng = np.random.default_rng(seed)
    v1 = []
    for _ in range(nsamp):
        d = np.array(LINE_DIRS[rng.integers(len(LINE_DIRS))])
        ks = rng.integers(1, Lc, size=3)
        v1.append(cdet.C_V([(idx(k * d), float(rng.uniform(0, beta))) for k in ks], mu).real)
    v3 = []
    while len(v3) < nsamp:
        sites = [int(rng.integers(N)) for _ in range(3)]
        P = np.array([[s % Lc, (s // Lc) % Lc, s // (Lc * Lc)] for s in sites], float)
        D = (P + Lc // 2) % Lc - Lc // 2
        if np.linalg.matrix_rank(D) == 3:
            v3.append(cdet.C_V([(s, float(rng.uniform(0, beta))) for s in sites], mu).real)
    v1, v3 = np.array(v1), np.array(v3)
    stat = lambda v: (np.abs(v).mean(), abs(v.mean()) / np.abs(v).mean())
    return stat(v1), stat(v3)


def _selftest():
    import sys; sys.path.insert(0, '.')
    from symmetry_reduction import cube_hopping
    # gate 1: FastCDet identical to the validated CDet
    H = cube_hopping(4); a = CDet(H, beta=4.0, to=0.7, ti=0.2); b = FastCDet(H, beta=4.0, to=0.7, ti=0.2)
    rng = np.random.default_rng(0); worst = 0.0
    for _ in range(40):
        n = int(rng.integers(1, 4)); V = [(int(rng.integers(64)), float(rng.uniform(0, 4))) for _ in range(n)]
        worst = max(worst, abs(a.C_V(V, 0.5) - b.C_V(V, 0.5)))
    print(f"FastCDet vs validated CDet: max diff = {worst:.2e}")
    ok = worst < 1e-12
    # gate 2: the hierarchy at two sizes -- density ratio grows, 1d sign beats bulk
    rows = {}
    for Lc in (4, 6):
        cd = FastCDet(cube_hopping(Lc), beta=4.0, to=0.7, ti=0.2)
        (m1, r1), (m3, r3) = line_class_stats(cd, Lc)
        rows[Lc] = (m1 / m3, r1, r3)
        print(f"L={Lc}: density ratio 1d/bulk = {m1 / m3:.0f}x   R(1d)={r1:.2f}  R(bulk)={r3:.2f}")
    floor = np.sqrt(2 / (np.pi * 600))
    ok = ok and rows[6][0] > rows[4][0] and all(rows[L][1] > rows[L][2] + floor for L in (4, 6))
    print("slice-scaling self-test (ratio grows with L; 1d sign beats bulk):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
