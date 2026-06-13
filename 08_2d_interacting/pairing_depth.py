"""pairing_depth.py (v71) -- rotation item (a), run surrogate-first per the new standing mode:
does the orientation phase have finite pairing depth? ANSWER: NO -- and stronger: NO single free
determinant over the point set carries the phase at ANY depth, including complete.

THE EXPERIMENT (surrogate-side; engine used only for the orientation crosscheck cells). The free
4-point tau-integrated determinant model decomposes exactly into 24 permutation terms via Matsubara
cycle sums (each cycle: Sum_w Prod_legs G0(leg, i w_n); fermionic parity per permutation). Depth-k
predictor = sign of the sum of the k largest-magnitude terms. Frozen protocol identical to v69:
calibrate one global sign on the (L=6, mu=0.5, extent 3) cell, predict 7 other cells per-geometry.
PRE-REGISTERED GATES: (i) depth-2 (chain + leading exchange) >= 75%?  (ii) full depth (24) >= 75%?

RESULTS (both variants: all-times-integrated, and the engine-matched external-time-FIXED variant --
identical numbers):
    depth k :    1     2     4     24
    OOC mean:   46%   46%   63%   44%     (calibration cell: 93% at every depth)
Both pre-registered gates FAIL. The curve is non-monotonic and never reaches the gate; FULL depth is
no better than chance-ish. The v69 "determinant-level" conclusion SHARPENS: the phase is not in any
single determinant of free propagators over the geometry -- by elimination, it lives in the COUPLED
PRODUCT OF THE TWO SPIN DETERMINANTS integrated over SHARED vertex times (plus the connected/vacuum
subtraction) -- i.e., in the engine integrand itself. Consistent with v54 (the value channel's -1 is
a cross-spin dressing) and v60 (tau-interference, 40% of variance).

THE REDUCTION LADDER, COMPLETE (all frozen-protocol, all falsified):
    static parity (v68):                      50-59%
    static single-particle predictors (v69):  34%
    tau-integrated dominant chain (v69):      64%
    single free determinant, ANY depth (v71): <= 63%, full depth 44%
SURROGATE CONSEQUENCE (the question this rotation pass was asked in): no physics-reduced orientation
channel exists below the engine integrand. The only remaining surrogate route for orientation is a
LEARNED statistical channel (fit orientation vs geometry/mu/L directly) -- queued.

HONEST SCOPE: axis lines, n=3, one beta, 14 geometries/cell, 8 cells; "no single determinant" means
the free-propagator determinant over the n+1 points in both time conventions tested; exotic
dressed-propagator determinants untested.
"""
import numpy as np
import itertools
from symmetry_reduction import cube_hopping
from phase_law import measure_cell

BETA = 4.0


def Gw_table(Lc, mu, nw=200, beta=BETA):
    H = cube_hopping(Lc); w, V = np.linalg.eigh(H); xi = w - mu
    wn = (2 * np.arange(-nw, nw) + 1) * np.pi / beta
    return {r: np.array([np.sum(V[0, :] * V[r % Lc, :] / (1j * om - xi)) for om in wn])
            for r in range(Lc)}


def perm_terms(ks, gw, Lc, external_fixed=False, beta=BETA):
    """All 24 permutation terms of the free 4-point tau-integrated determinant model."""
    pts = [0] + sorted(ks); n = len(pts)
    terms = []
    for sg in itertools.permutations(range(n)):
        par = np.linalg.det(np.eye(n)[list(sg)])
        seen = [False] * n; val = 1.0
        for i in range(n):
            if seen[i]:
                continue
            cyc = []; j = i
            while not seen[j]:
                seen[j] = True; cyc.append(j); j = sg[j]
            legs = [abs(pts[cyc[a]] - pts[cyc[(a + 1) % len(cyc)]]) % Lc for a in range(len(cyc))]
            s = np.sum(np.prod([gw[l] for l in legs], axis=0)).real
            val *= (s / beta / beta if (external_fixed and 0 in cyc) else s / beta)
        terms.append(par * val)
    return np.array(terms)


def depth_sign(terms, k):
    order = np.argsort(-np.abs(terms))
    return np.sign(np.sum(terms[order[:k]]))


def frozen_depth_protocol(cells, cal, k, gws, data, external_fixed=False):
    pr = [depth_sign(perm_terms(list(ks), gws[(cal[0], cal[1])], cal[0], external_fixed), k)
          for ks, s in data[cal]]
    tr = [s for ks, s in data[cal]]
    SG = +1 if np.mean(np.array(pr) == tr) >= np.mean(np.array(pr) == -np.array(tr)) else -1
    ca = max(np.mean(np.array(pr) == tr), np.mean(np.array(pr) == -np.array(tr)))
    accs = []
    for c in cells:
        if c == cal:
            continue
        p = np.array([SG * depth_sign(perm_terms(list(ks), gws[(c[0], c[1])], c[0], external_fixed), k)
                      for ks, s in data[c]])
        t = np.array([s for ks, s in data[c]])
        accs.append(np.mean(p == t))
    return float(ca), float(np.mean(accs))


def _selftest():
    cells = [(6, 0.5, 3), (6, 0.5, 4), (6, 1.5, 3), (6, 1.5, 4), (4, 1.5, 3)]
    cal = (6, 0.5, 3)
    data = {c: measure_cell(*c) for c in cells}
    gws = {(Lc, mu): Gw_table(Lc, mu) for Lc in (4, 6) for mu in (0.5, 1.5)}
    ok = True
    for k in (2, 24):
        ca, oos = frozen_depth_protocol(cells, cal, k, gws, data)
        print(f"depth {k:>2}: calibration {ca:.0%}, out-of-calibration mean {oos:.0%}")
        ok = ok and ca > 0.8 and oos < 0.70
    ca_f, oos_f = frozen_depth_protocol(cells, cal, 24, gws, data, external_fixed=True)
    print(f"external-fixed variant, full depth: calibration {ca_f:.0%}, OOC {oos_f:.0%}")
    ok = ok and oos_f < 0.70
    print("pairing-depth self-test (ladder-complete negative reproduced: no depth crosses the gate):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
