"""phase_law.py (v69) -- the quantitative phase law, attempted under frozen protocol: TWO candidate
reductions FALSIFIED. The orientation of the signed weight is not reducible to static Friedel signs,
and not to the dominant chain diagram -- the phase appears to live at the determinant level.

THE TARGET. v68 established the phenomenology: the orientation of coherent (compact/line) geometries
is a filling-controlled phase (94% negative at mu=0.5 -> 75-100% positive at mu=1.5, same
geometries). The formula-grade question: can that phase be PREDICTED from objects cheaper than the
order-n determinant itself? Protocol: calibrate predictor choice + ONE global sign on a single cell
(L=6, mu=0.5, extent 3), freeze, predict every other (L, mu, extent) cell per-geometry.
Gate PRE-SET: >= 75% mean out-of-calibration accuracy.

CANDIDATE 1 -- STATIC FRIEDEL (tau-averaged single-particle predictors): per-leg sign products
(star P1, chain P2), the determinant of the tau-averaged propagator matrix over the point set (P3),
and the dominant permutation term with its parity (P4). All saturate the calibration cell (93%) and
COLLAPSE out of calibration: mean 34%, with anti-correlated cells (down to 7%). FALSIFIED,
diagnostically: <C>_tau averages the PRODUCT of propagators, not the product of averages -- the
static table cannot see the joint-tau interference that v60 measured at 40% of variance. (The
tau-averaged free sign pattern along the axis is ++-++ at ALL fillings tested -- it cannot even
represent the measured mu-flip.)

CANDIDATE 2 -- THE tau-INTEGRATED DOMINANT CHAIN (Matsubara loop sum over consecutive legs,
(1/beta) sum_n Prod_legs G0(leg, i w_n) -- full joint-tau structure, no determinants): calibration
93%, out-of-calibration mean 64% -- REAL partial signal (two cells at 100%/93%, both mu=1.5) but
FAILS the pre-set gate, with one cell anti-correlated (21%). The cell-dependent reversals are the
fingerprint of COMPETING PAIRINGS of opposite permutation parity: the chain alone carries part of
the phase; the exchange terms flip it in some cells.

THE STANDING CONCLUSION: the orientation phase is, as far as these reductions reach, an
interference effect at the level of the full determinant (the sum over all pairings with parities)
-- there may be no shortcut below the determinant for the SIGN, even though the MAGNITUDE has a
two-coefficient law (v63). That asymmetry -- magnitude lawful, phase irreducible -- is itself a
sharp, falsifiable characterization of where the sign problem's hardness sits in this
representation. The v68 phenomenology (coherence scale xi_s ~ 3; mu-controlled flip) stands
untouched; what failed is its reduction to single-particle formulas.

HONEST SCOPE: axis lines, n=3, one beta, 14 geometries/cell; "irreducible" means "both tested
reductions failed a frozen gate", not a proof; the full free-diagram sum (= the engine itself)
trivially reproduces the phase, so the open question is whether any object STRICTLY CHEAPER than
the determinant carries it.
"""
import numpy as np
import itertools
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

BETA = 4.0


def G0bar_table(Lc, mu, beta=BETA):
    """tau-averaged free propagator along an axis, r = 0..Lc-1 (min-image via r % Lc)."""
    H = cube_hopping(Lc); w, V = np.linalg.eigh(H); xi = w - mu
    taus = np.linspace(1e-3, beta - 1e-3, 160); occ = 1 / (1 + np.exp(beta * xi))
    tab = {}
    for r in range(Lc):
        amp = V[0, :] * V[r % Lc, :]
        Gt = np.array([-np.sum(amp * (1 - occ) * np.exp(-t * xi)) for t in taus])
        tab[r] = np.trapezoid(Gt, taus) / beta
    return tab


def Gw_table(Lc, mu, nw=120, beta=BETA):
    """free Matsubara propagator along an axis."""
    H = cube_hopping(Lc); w, V = np.linalg.eigh(H); xi = w - mu
    wn = (2 * np.arange(-nw, nw) + 1) * np.pi / beta
    return {r: np.array([np.sum(V[0, :] * V[r % Lc, :] / (1j * om - xi)) for om in wn])
            for r in range(Lc)}, wn


def static_predictors(ks, tab, Lc):
    """P1 star, P2 chain-of-gaps, P3 det of tau-averaged matrix, P4 dominant permutation x parity."""
    ks = sorted(ks); pts = [0] + ks
    P1 = np.sign(np.prod([tab[k % Lc] for k in ks]))
    gaps = [ks[0]] + [ks[i + 1] - ks[i] for i in range(len(ks) - 1)]
    P2 = np.sign(np.prod([tab[g % Lc] for g in gaps]))
    A = np.array([[tab[abs(a - b) % Lc] for b in pts] for a in pts])
    P3 = np.sign(np.linalg.det(A))
    best = None
    for sg in itertools.permutations(range(len(pts))):
        v = np.prod([A[i, sg[i]] for i in range(len(pts))])
        par = np.linalg.det(np.eye(len(pts))[list(sg)])
        t = par * v
        if best is None or abs(t) > abs(best):
            best = t
    return {1: P1, 2: P2, 3: P3, 4: np.sign(best)}


def chain_predictor(ks, gw, Lc, beta=BETA):
    """P5: fully tau-integrated closed chain (Matsubara loop)."""
    ks = sorted(ks); pts = [0] + ks
    legs = [abs(pts[i + 1] - pts[i]) % Lc for i in range(len(pts) - 1)] + [abs(pts[-1] - pts[0]) % Lc]
    return np.sign(np.sum(np.prod([gw[l] for l in legs], axis=0)).real / beta)


def measure_cell(Lc, mu, extent, n_geom=14, NT=22, seed=92, beta=BETA):
    cd = FastCDet(cube_hopping(Lc), beta=beta, to=0.7, ti=0.2)
    rng = np.random.default_rng(seed + 10 * extent + int(10 * mu) + Lc)
    AX = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    idx = lambda p: int(p[0] % Lc + Lc * ((p[1] % Lc) + Lc * (p[2] % Lc)))
    out = []
    for _ in range(n_geom):
        d = np.array(AX[rng.integers(3)])
        ks = [extent] + list(rng.choice(np.arange(1, extent), 2, replace=False))
        g = [idx(k * d) for k in ks]
        v = np.array([cd.C_V([(s, float(rng.uniform(0, beta))) for s in g], mu).real for _ in range(NT)])
        out.append((tuple(sorted(ks)), np.sign(v.mean())))
    return out


def frozen_protocol(cells, cal, predictor_fn, tabs):
    """Calibrate global sign on `cal`, predict all other cells. Returns (cal_acc, oos_mean, per_cell)."""
    data = {c: measure_cell(*c) for c in cells}
    pr = [predictor_fn(list(ks), tabs[(cal[0], cal[1])], cal[0]) for ks, s in data[cal]]
    tr = [s for ks, s in data[cal]]
    a_p = np.mean(np.array(pr) == tr); a_m = np.mean(np.array(pr) == -np.array(tr))
    SG = +1 if a_p >= a_m else -1
    per = {}
    for c in cells:
        if c == cal:
            continue
        p = np.array([SG * predictor_fn(list(ks), tabs[(c[0], c[1])], c[0]) for ks, s in data[c]])
        t = np.array([s for ks, s in data[c]])
        per[c] = float(np.mean(p == t))
    return max(a_p, a_m), float(np.mean(list(per.values()))), per


def _selftest():
    cells = [(6, m, e) for m in (0.5, 1.5) for e in (3, 4)] + [(4, 1.5, 3)]
    cal = (6, 0.5, 3)
    tabs_s = {(Lc, mu): G0bar_table(Lc, mu) for Lc in (4, 6) for mu in (0.5, 1.5)}
    ca_s, oos_s, _ = frozen_protocol(cells, cal, lambda ks, t, L: static_predictors(ks, t, L)[1], tabs_s)
    print(f"static (P1) frozen protocol: calibration {ca_s:.0%}, out-of-calibration mean {oos_s:.0%}")
    tabs_w = {(Lc, mu): Gw_table(Lc, mu)[0] for Lc in (4, 6) for mu in (0.5, 1.5)}
    ca_c, oos_c, _ = frozen_protocol(cells, cal, chain_predictor, tabs_w)
    print(f"chain  (P5) frozen protocol: calibration {ca_c:.0%}, out-of-calibration mean {oos_c:.0%}")
    # gates REPRODUCE THE FALSIFICATION: both calibrations high, both OOS below the 75% gate,
    # chain strictly better than static (the partial-signal ordering)
    ok = ca_s > 0.8 and ca_c > 0.8 and oos_s < 0.62 and oos_c < 0.75 and oos_c > oos_s
    print("phase-law self-test (double falsification reproduced; chain > static partial signal):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
