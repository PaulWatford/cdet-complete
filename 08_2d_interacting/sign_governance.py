"""sign_governance.py (v68) -- what governs where the SIGNED weight lives. Answer, measured:

    signed weight = (magnitude envelope) x (sign-coherence decay) x (a filling-controlled PHASE)

THE THREE COMPONENTS (L=4/6 cubes, n=3, beta=4):

1. MAGNITUDE ENVELOPE: the v63 law (distance b=0.537 + channeling c=0.583, tau-interference 40%).

2. SIGN COHERENCE HAS ITS OWN, LONGER DECAY SCALE: fitting ln r_g vs MST gives xi_s ~ 3.0 -- about
   3x the magnitude's effective decay (1.9) and the bare propagator (0.9). Binned medians: r_g 0.73
   (MST<4) -> 0.40 (4-6) -> 0.21 (>=6). Sign coherence OUTLIVES weight: the compact sector is not
   only heavy, it is disproportionately sign-ordered.

3. THE ORIENTATION IS A FILLING-CONTROLLED PHASE (Friedel-class), NOT PARITY:
   - PARITY FALSIFIED: the product of sublattice signs predicts the orientation at 50% (mu=0.5) and
     59% (mu=0, the PH point) -- coin flip both times. (The v54 equal-time dressing is the suspected
     reason it fails even at mu=0; suspected, not shown.)
   - THE FLIP: extent-3 axis lines at L=6 are 94% NEGATIVE at mu=0.5 and 81-100% POSITIVE at mu=1.5
     (extent 4 at mu=1.5: 100% positive, r_g=0.81). Same geometries, opposite orientation -- the
     phase moves with the filling, exactly the Friedel/k_F signature. It also resolves the apparent
     L=4-vs-L=6 contradiction (92% positive vs 94% negative lines): different k-grids, different
     phase -- supporting evidence for the phase picture, though the period is NOT yet fitted.
   - Matched-MST comparison: compact configs of ANY class are orientation-coherent (85%/72% at MST
     3-4); coherence -- not positivity -- is the invariant.

WHY v67 WORKED, restated correctly: enumerating the compact line sector captures 77% of the signed
answer not because that sector is positive, but because it is COHERENT -- its phase is deterministic
enough that its contributions add instead of cancelling, while the bulk's phases scramble.

HONEST SCOPE: the phase law is established qualitatively (flip with mu; coherence at small extent;
its own decay scale) but NOT quantitatively (no fitted oscillation period vs k_F); 16 geometries per
extent cell; parity's failure at mu=0 has a suspected but unproven mechanism. The quantitative phase
law is the open theory item.
"""
import numpy as np
from slice_scaling import FastCDet
from decay_law import mst_length
from symmetry_reduction import cube_hopping


def line_orientation(cd, Lc, extent, mu, n_geom=16, NT=24, beta=4.0, rng=None):
    """sign(+) fraction and median r_g for axis lines of given max extent through the external."""
    AX = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    idx = lambda p: int(p[0] % Lc + Lc * ((p[1] % Lc) + Lc * (p[2] % Lc)))
    ss, rs = [], []
    for _ in range(n_geom):
        d = np.array(AX[rng.integers(3)])
        ks = [extent] + list(rng.choice(np.arange(1, extent), 2, replace=False))
        g = [idx(k * d) for k in ks]
        v = np.array([cd.C_V([(s, float(rng.uniform(0, beta))) for s in g], mu).real for _ in range(NT)])
        ss.append(np.sign(v.mean())); rs.append(abs(v.mean()) / np.abs(v).mean())
    ss = np.array(ss)
    return float(np.mean(ss > 0)), float(np.median(rs))


def xi_sign(cd, Lc, n_geom=80, NT=30, mu=0.5, beta=4.0, seed=90):
    """Decay scale of sign coherence: fit ln r_g vs MST over a mixed ensemble."""
    from slice_scaling import LINE_DIRS
    N = Lc ** 3; rng = np.random.default_rng(seed)
    co = lambda s: (s % Lc, (s // Lc) % Lc, s // (Lc * Lc))
    geoms = []
    for _ in range(n_geom // 4):
        d = np.array(LINE_DIRS[rng.integers(13)]); ks = rng.integers(1, Lc, 3)
        geoms.append([int((k * d) % Lc @ np.array([1, Lc, Lc * Lc])) for k in ks])
    geoms += [[int(rng.integers(N)) for _ in range(3)] for _ in range(n_geom - len(geoms))]
    rg, ls = [], []
    for g in geoms:
        v = np.array([cd.C_V([(s, float(rng.uniform(0, beta))) for s in g], mu).real for _ in range(NT)])
        rg.append(abs(v.mean()) / np.abs(v).mean()); ls.append(mst_length([co(s) for s in g], Lc))
    A = np.polyfit(ls, np.log(np.maximum(rg, 1e-3)), 1)
    return -1 / A[0]


def _selftest():
    rng = np.random.default_rng(92)
    cd6 = FastCDet(cube_hopping(6), beta=4.0, to=0.7, ti=0.2)
    f05, r05 = line_orientation(cd6, 6, 3, 0.5, rng=rng)
    f15, r15 = line_orientation(cd6, 6, 3, 1.5, rng=rng)
    print(f"extent-3 axis lines: mu=0.5 sign(+) {f05:.0%} (r_g {r05:.2f})   mu=1.5 sign(+) {f15:.0%} (r_g {r15:.2f})")
    coher = abs(2 * f05 - 1) > 0.4 and abs(2 * f15 - 1) > 0.4
    flip = (f05 - 0.5) * (f15 - 0.5) < 0
    print(f"gates: coherent at small extent (both |2f-1|>0.4): {coher};  orientation FLIPS with mu: {flip}")
    cd4 = FastCDet(cube_hopping(4), beta=4.0, to=0.7, ti=0.2)
    xs = xi_sign(cd4, 4)
    print(f"sign-coherence decay scale xi_s = {xs:.2f}  (gate: > 1.5, i.e. longer than xi_eff_magnitude)")
    ok = coher and flip and xs > 1.5
    print("sign-governance self-test (coherence; mu-flip; xi_s outlives magnitude):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
