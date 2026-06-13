"""shell_fold.py (v75) -- the L=6 shell fold: first exact signed totals at 10,077,696-config scale
(both fillings), the Friedel rings at L=6, the v70 pilot validated -- and a wrap-collinearity
DISCOVERY that corrected our own sector definition on the way in.

THE WRAP DISCOVERY (correction banked; the standing wrap-safe rule now extends to DEFINITIONS).
Min-image collinearity is ILL-DEFINED on even-L tori: the line through (5,1,0) at L=6 wraps through
the antipode, where the min-image convention flips signs -- {0, (5,1,0), (3,3,0)} IS collinear
((3,3,0) = 3 x (5,1,0) mod 6) but its min-image rows are not parallel. Consequences:
  - the per-config min-image rank classifier is NOT orbit-consistent;
  - the v67/v70 "rank<=1 sector" was the min-image-parallel SUBSET of the true torus-line sector.
THE CORRECT DEFINITION: a config is sector iff all its sites lie on a common cyclic line through
the origin (generator-mask test) -- manifestly group-invariant. Corrected sectors:
    L=4: 1,618 configs (was 808), exact sum +0.003165 = 82% of the exact total (was 77%)
    L=6: 16,950 configs = 0.17% (was 3,774); construction and fold classification agree exactly.
The old numbers were TRUE statements about a smaller, wrap-blind subset; notes added to the v67/v70
docs.

THE FOLD (240,464 orbit reps of 10,077,696 configs; ~25 min of evaluation, both fillings per rep):
    FIRST EXACT L=6 TOTALS (times [0.5, 1.9, 3.3]):
        mu=0.5: total -2.498377e-3    TRUE sector -1.055844e-3 (42%)
        mu=1.5: total -2.224768e-3    TRUE sector +4.842304e-4 (sector OPPOSES the total: -22%)
    The v70 pilot (-2.3e-3 +/- 4.5e-3) is VALIDATED dead-on. The mu=0.5 total is negative -- the
    phase flip vs L=4 (+0.00385) holds for the full total, not just the sector. At L=6 the sector
    carries less of the answer (42% vs 82% at L=4) and can oppose it: the remainder grows in
    relative importance with size -- the sign problem scaling faster than the machinery, again.

THE RINGS AT L=6 (remainder = NOT-sector, exact shell sums): oscillation persists -- 2 sign changes
per filling at unit bins (patterns [--+---] at mu=0.5, [-+----] at mu=1.5), and at half-unit bins
the node positions are mu-DEPENDENT (mu=0.5: ~3.0, 4.5, 5.5, ...; mu=1.5: ~3.5, 4.0, 5.0, ...).
HONEST VERDICT on the period: spacings are irregular (0.5-1.5) at this size/binning -- the right
SCALE relative to the frozen pi/k_F ~ 1.1-1.2 (continuum estimate), but the period is NOT resolved.
The mu-period theory item stays open with new constraints; named refinement path: MST is a crude
radial coordinate for a 3-body object (per-leg extent was cleaner in v68).
"""
import numpy as np
import itertools
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping, cube_point_stabilizer


def line_masks(Lc):
    """M[u, s] = site s lies on the cyclic line through generator u (origin included)."""
    N = Lc ** 3
    M = np.zeros((N, N), dtype=bool)
    for u in range(1, N):
        p = np.array([u % Lc, (u // Lc) % Lc, u // (Lc * Lc)])
        s = np.zeros(3, int); M[u, 0] = True
        for k in range(1, Lc):
            s = (s + p) % Lc
            M[u, int(s[0] + Lc * (s[1] + Lc * s[2]))] = True
    return M


def true_sector(Lc):
    """The WRAP-SAFE coherent sector: all ordered triples lying on a common cyclic line."""
    N = Lc ** 3; M = line_masks(Lc)
    lines = set()
    for u in range(1, N):
        lines.add(tuple(sorted(np.nonzero(M[u])[0].tolist())))
    fam = set()
    for pts in lines:
        for t in itertools.product(pts, repeat=3):
            fam.add(t)
    fam.add((0, 0, 0))
    return sorted(fam)


def classify_true_rank1(site_triples, M):
    """Group-invariant sector membership for an array of (a, b, c) site triples."""
    a, b, c = site_triples[:, 0], site_triples[:, 1], site_triples[:, 2]
    out = np.zeros(len(a), bool)
    chunk = 60000
    for s in range(0, len(a), chunk):
        e = min(s + chunk, len(a))
        out[s:e] = (M[:, a[s:e]] & M[:, b[s:e]] & M[:, c[s:e]]).any(axis=0)
    out |= (a == 0) & (b == 0) & (c == 0)
    return out


# ---- exact tables from the fold (times [0.5, 1.9, 3.3]) ----
L4_TRUE_SECTOR = {"count": 1618, "sum_mu05": +0.003165, "share": 0.82}
L6_TRUE_SECTOR_COUNT = 16950
L6_TOTALS = {"mu05": -2.498377e-3, "mu15": -2.224768e-3,
             "sector_mu05": -1.055844e-3, "sector_mu15": +4.842304e-4}
RING_TABLE_L6 = {  # remainder shell sums, unit bins [0,3.5,4.5,5.5,6.5,7.5,inf)
    "mu05": [-9.366e-5, -5.388e-4, +1.150e-4, -2.022e-4, -3.225e-4, -4.002e-4],
    "mu15": [-6.874e-4, +5.434e-4, -9.475e-4, -4.490e-4, -1.083e-3, -8.508e-5]}
NODES_L6 = {"mu05": [3.0, 4.5, 5.5, 6.0, 6.5], "mu15": [3.5, 4.0, 5.0, 5.5, 8.0]}


def _selftest():
    ok = True
    fam4 = true_sector(4); fam6_n = len(true_sector(6))
    print(f"true sector counts: L=4 {len(fam4)} (expect 1618)   L=6 {fam6_n} (expect 16950)")
    ok = ok and len(fam4) == 1618 and fam6_n == 16950
    cd = FastCDet(cube_hopping(4), beta=4.0, to=0.7, ti=0.2)
    times = [0.5, 1.9, 3.3]
    S = sum(cd.C_V([(s, t) for s, t in zip(g, times)], 0.5).real for g in fam4)
    print(f"L=4 true sector exact sum: {S:+.6f} (expect +0.003165); share {100 * S / 0.00384575:.0f}%")
    ok = ok and abs(S - 0.003165) < 2e-5
    # group-invariance of the wrap-safe classifier on sampled L=6 orbits
    M = line_masks(6); G = np.array(cube_point_stabilizer(6, cube_hopping(6)), dtype=np.int64)
    rng = np.random.default_rng(3); inv_ok = True
    for _ in range(25):
        t = rng.integers(0, 216, 3)
        members = np.array([[g[t[0]], g[t[1]], g[t[2]]] for g in G])
        flags = classify_true_rank1(members, M)
        inv_ok = inv_ok and (flags.all() or (~flags).all())
    print(f"group-invariance over 25 sampled orbits x 48 members: {inv_ok}")
    ok = ok and inv_ok
    # stored-table arithmetic: sector + sum(shells) == total, both fillings
    for mu, sk in (("mu05", "sector_mu05"), ("mu15", "sector_mu15")):
        lhs = L6_TOTALS[sk] + sum(RING_TABLE_L6[mu])
        print(f"{mu}: sector + shells = {lhs:+.6e} vs total {L6_TOTALS[mu]:+.6e}  "
              f"diff {abs(lhs - L6_TOTALS[mu]):.1e}")
        ok = ok and abs(lhs - L6_TOTALS[mu]) < 2e-6
    print("shell-fold self-test (wrap-safe sector; L=4 sum; invariance; table arithmetic):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
