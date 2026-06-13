"""surrogate2.py (v74) -- magnitude and r_pred refinements, surrogate-first. Four findings, one of
them a scope correction of our own reporting.

1. MEASURE THE CEILING FIRST (new standing practice). Split-half label reliability:
       ln<|C|>_tau:  rho = 0.95 at NT=20  -> real headroom existed above the old 0.75
       ln r_g:       rho = 0.40 at NT=20, ~0.57 at NT=40 -> the old "weak" 0.32 was ~80% of what
                     its labels permitted -- mostly label noise, not model failure.

2. THE R^2-MIXTURE ARTIFACT (scope correction, banked). The v66 figure "OOS R2 = 0.75" was
   test-composition-flattered: a line-heavy test set has enormous between-class spread, which any
   model separating lines from bulk converts into high R2. On a standardized bulk-heavy split the
   same v1 model scores 0.55. The NUMBER was real; its INTERPRETATION was mixture-dependent.
   Standing protocol now: fixed-split comparisons + MEDIAN PER-CONFIG ERROR as co-headline
   (which was and remains ~1.7x, mixture-independent). Clarification note added to
   SURROGATE_RESULT.md.

3. MAGNITUDE v2 -- THE TRANSFERABLE SURROGATE (the real gain). Ten features (MST, lcoll, rank,
   sumpair, dmin, dmax, n_adj, aniso, vol^(1/3), lcoll2), ridge with proper CV, apples-to-apples on
   one split:
       L=4 in-distribution: v1 0.55 / v2 0.59 (a wash; med-err 1.66x vs 1.71x)
       L=4 -> L=6 TRANSFER (slopes frozen, intercept from 8 L=6 geometries):
           v1: R2 0.33, med-err 2.88x      v2: R2 0.57, med-err 1.81x
   The new features (dmax, anisotropy, adjacency, dmin) carry across lattice size; the old three do
   not. Quadratic interactions HURT transfer badly (extrapolation blowup) -- linear is the model.

4. THE r_pred REGIME MAP (the channel's true shape). Within-class OOS R2 with NT=40 labels:
       within rank-1 (coherent sector):   +0.32   -- genuinely graded (the xi_s decay is learnable)
       within rank-2 (near-coherent):     +0.27
       within rank-3 (deep bulk):         -0.57   -- STRICTLY unpredictable (worse than the mean)
   Sign-survival predictability lives exactly where coherence lives; the deep bulk is
   phase-governed and resists even graded prediction -- the orientation-channel closure (v73),
   now visible quantitatively in the survival channel. Earlier overall-R2 numbers were
   mixture-dependent blends of these regimes.

HONEST SCOPE: L=4 calibration + L=6 transfer, one beta/mu for the regime map; the 8-shot intercept
is a stated requirement of transfer, not hidden; in-distribution magnitude R2 (~0.59 vs ceiling
0.95) still leaves real geometry signal uncaptured -- plausibly the same tau-structure family as
the phase.
"""
import numpy as np
from slice_scaling import FastCDet, LINE_DIRS
from decay_law import mst_length
from symmetry_reduction import cube_hopping

BETA = 4.0
NAMES = ["MST", "lcoll", "rank", "sumpair", "dmin", "dmax", "n_adj", "aniso", "vol13", "lcoll2"]


def feats2(sites, Lc):
    co = lambda s: np.array([s % Lc, (s // Lc) % Lc, s // (Lc * Lc)], float)
    mi = lambda v: (v + Lc / 2) % Lc - Lc / 2
    pts = [np.zeros(3)] + [co(s) for s in sites]
    legs = [np.linalg.norm(mi(pts[i] - pts[j])) for i in range(4) for j in range(i + 1, 4)]
    mst = mst_length([tuple(co(s)) for s in sites], Lc)
    D = np.array([mi(co(s)) for s in sites])
    # v88 numerics correction: D is integer-valued by construction (min-image of integer coords),
    # so the determinant is an exact integer; np.linalg.det returns ~1e-13 noise for singular
    # configs (-> vol^(1/3) ~ 1e-5 instead of 0). Round to the exact integer. Effect on the
    # frozen trained weights is ~1e-4 ln units -- negligible against the 2.3x scope.
    vol = float(np.round(abs(np.linalg.det(D)))); rank = np.linalg.matrix_rank(D)
    groups = {}
    for s in sites:
        d = mi(co(s)); n = np.linalg.norm(d)
        if n < 1e-9:
            continue
        u = tuple(np.round(d / n, 5)); u = min(u, tuple(-x for x in u))
        groups.setdefault(u, []).append(tuple(co(s)))
    colls = sorted([mst_length(p, Lc) for p in groups.values() if len(p) >= 2], reverse=True)
    lc1 = colls[0] if colls else 0.0; lc2 = colls[1] if len(colls) > 1 else 0.0
    ext = [max(abs(mi(co(s))[a]) for s in sites) for a in range(3)]
    return [mst, lc1, float(rank), sum(legs), min(legs[:3]) if legs else 0, max(legs),
            sum(1 for l in legs if abs(l - 1) < 1e-6), max(ext) / max(mst, 1e-9),
            vol ** (1 / 3), lc2]


def ridge_cv(Z, Y, lams=(0.1, 0.3, 1, 3, 10, 30)):
    best = None
    for lam in lams:
        k = len(Y) // 5; errs = []
        for f in range(5):
            v = np.arange(f * k, (f + 1) * k); t = np.setdiff1d(np.arange(len(Y)), v)
            A = np.column_stack([np.ones(len(t)), Z[t]])
            w = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ Y[t])
            errs.append(np.mean((Y[v] - np.column_stack([np.ones(len(v)), Z[v]]) @ w) ** 2))
        if best is None or np.mean(errs) < best[1]:
            best = (lam, np.mean(errs))
    A = np.column_stack([np.ones(len(Y)), Z])
    return np.linalg.solve(A.T @ A + best[0] * np.eye(A.shape[1]), A.T @ Y)


def mag_dataset(Lc, n_lines, n_bulk, seed, NT=24, mu=0.5, beta=BETA):
    cd = FastCDet(cube_hopping(Lc), beta=beta, to=0.7, ti=0.2)
    rng = np.random.default_rng(seed)
    G = []
    for _ in range(n_lines):
        d = np.array(LINE_DIRS[rng.integers(13)]); ks = rng.integers(1, Lc, 3)
        G.append([int((k * d) % Lc @ np.array([1, Lc, Lc * Lc])) for k in ks])
    G += [[int(rng.integers(Lc ** 3)) for _ in range(3)] for _ in range(n_bulk)]
    X = np.array([feats2(g, Lc) for g in G])
    Y = np.array([np.log(np.mean([abs(cd.C_V([(s, float(rng.uniform(0, beta))) for s in g], mu).real)
                                  for _ in range(NT)])) for g in G])
    return X, Y


def r2(y, p):
    return 1 - np.sum((y - p) ** 2) / np.sum((y - y.mean()) ** 2)


CEILINGS = {"magnitude_NT20": 0.95, "r_g_NT20": 0.40, "r_g_NT40": 0.57}
REGIME_MAP = {"rank1": +0.32, "rank2": +0.27, "rank3": -0.57}


def _selftest():
    X4, Y4 = mag_dataset(4, 40, 170, 130)
    X6, Y6 = mag_dataset(6, 15, 45, 131)
    rng = np.random.default_rng(5); idx = rng.permutation(len(Y4)); tr, te = idx[:160], idx[160:]
    mu_f = X4[tr].mean(0); sd_f = X4[tr].std(0) + 1e-9
    Z4 = (X4 - mu_f) / sd_f; Z6 = (X6 - mu_f) / sd_f
    out = {}
    for name, cols in (("v1", [0, 1, 2]), ("v2", list(range(10)))):
        w = ridge_cv(Z4[tr][:, cols], Y4[tr])
        p6r = np.column_stack([np.ones(len(Y6)), Z6[:, cols]]) @ w
        off = np.mean(Y6[:8] - p6r[:8])
        out[name] = r2(Y6[8:], p6r[8:] + off)
        print(f"{name} transfer L=4 -> L=6 (8-shot intercept): R2 = {out[name]:.2f}")
    ok = out["v2"] - out["v1"] >= 0.10 and out["v2"] >= 0.45
    print(f"gates: v2 beats v1 by >=0.10 and v2 >= 0.45: {ok}")
    print(f"banked ceilings: {CEILINGS}; banked regime map (within-class r_pred): {REGIME_MAP}")
    print("surrogate-v2 self-test (transferable magnitude model):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
