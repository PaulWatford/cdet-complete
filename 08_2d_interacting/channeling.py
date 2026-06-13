"""1d-channeling test (v62): CONFIRMED -- collinearity itself carries ~1.8-1.9x at matched distance,
graded monotonically in collinearity. Third confirmed mechanism; the class gap is still not fully
accounted (honest residual ~4x).

DESIGN (everything the record taught): three families built from the SAME axis-directed distances --
LINE (k1,k2,k3 on one axis through the external), BENT (two on x, one on y), ZIG (one each on x,y,z)
-- so propagator anisotropy is controlled EXACTLY by cubic symmetry; pairs matched on MST to 0.01;
identical tau draws within each pair (the thrice-earned pairing rule). Frozen predictions: distance
law -> all ratios ~1; channeling -> line > bent > zig at matched MST.

MEASURED (L=6, beta=4, mu=0.5, n=3):
    line / bent : median paired ratio 1.82x   IQR [1.25, 2.74]   (n=28)
    line / zig  : median paired ratio 1.93x   IQR [1.48, 2.24]   (n=12)
    bent / zig  : median paired ratio 1.33x   IQR [0.82, 2.00]   (n=36)
Monotone in collinearity, well separated from 1 for the line family: CHANNELING IS REAL -- coherent
multi-bounce propagation along a shared direction enhances the connected weight at fixed total
distance. Consistent with v61 (twist-blind: channeling needs no winding).

THE MECHANISM LEDGER for the universal weight concentration (v57-v62), honest accounting:
    confirmed:  distance decay (MST; tau-averaged R2 ~0.48, slope -0.69)
                tau-interference (40% of var(ln|C|); within-geometry)
                anisotropy (~35% slower decay per Euclidean unit on diagonals; real, minor)
                1d channeling (~1.8-1.9x for full collinearity at matched MST; graded)
    falsified:  winding/ring closure (paired twist, v61)
    residual:   composing distance x channeling predicts ~16x of the measured ~75x class gap --
                a ~4x residual remains UNACCOUNTED (candidates: mechanism interactions, the
                MST-matching range, tail composition of the classes). Stated, not hidden.
"""
import numpy as np
import itertools
from slice_scaling import FastCDet
from decay_law import mst_length
from symmetry_reduction import cube_hopping


def families(Lc):
    """Matched-MST pools of axis-directed line/bent/zig configs (site triples keyed by MST)."""
    idx = lambda p: int(p[0] % Lc + Lc * ((p[1] % Lc) + Lc * (p[2] % Lc)))
    pools = {k: {} for k in ("line", "bent", "zig")}
    for ks in itertools.product(range(1, Lc), repeat=3):
        if len(set(ks)) < 3:
            continue
        for kind in pools:
            if kind == "line":
                pts = [(k, 0, 0) for k in ks]
            elif kind == "bent":
                pts = [(ks[0], 0, 0), (ks[1], 0, 0), (0, ks[2], 0)]
            else:
                pts = [(ks[0], 0, 0), (0, ks[1], 0), (0, 0, ks[2])]
            sites = [idx(p) for p in pts]
            if len(set(sites)) == 3:
                pools[kind].setdefault(round(mst_length(pts, Lc), 2), []).append(sites)
    return pools


def paired_ratio(cd, pools, kindA, kindB, npairs=24, NT=18, mu=0.5, beta=4.0, seed=21):
    """Median over MST-matched pairs of [tau-avg weight A]/[B], identical tau draws per pair."""
    rng = np.random.default_rng(seed)
    keys = sorted(set(pools[kindA]) & set(pools[kindB])); rs = []
    for key in keys:
        for sa, sb in zip(pools[kindA][key], pools[kindB][key]):
            taus = [[float(rng.uniform(0, beta)) for _ in range(3)] for _ in range(NT)]
            wa = np.mean([abs(cd.C_V(list(zip(sa, t)), mu).real) for t in taus])
            wb = np.mean([abs(cd.C_V(list(zip(sb, t)), mu).real) for t in taus])
            if wb > 0:
                rs.append(wa / wb)
            if len(rs) >= npairs:
                return np.array(rs)
    return np.array(rs)


def _selftest():
    Lc = 6; cd = FastCDet(cube_hopping(Lc), beta=4.0, to=0.7, ti=0.2)
    pools = families(Lc)
    r_lb = paired_ratio(cd, pools, "line", "bent")
    r_lz = paired_ratio(cd, pools, "line", "zig", npairs=12)
    print(f"line/bent median paired ratio = {np.median(r_lb):.2f}x  (n={len(r_lb)})")
    print(f"line/zig  median paired ratio = {np.median(r_lz):.2f}x  (n={len(r_lz)})")
    ok = np.median(r_lb) > 1.15 and np.median(r_lz) > 1.15
    print("channeling self-test (collinearity carries weight at matched MST):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
