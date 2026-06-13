"""surrogate.py (v66) -- the no-brute-force simulator: a geometry-trained surrogate that predicts
brute-force STRUCTURE with zero evaluations and steers small true-evaluation budgets, pushed to its
honest limit -- which turns out to be the sign wall itself, surfacing in estimator form.

WHAT IT IS. The concentration law (v57-63) as a predictive model:
        ln <|C|>_tau  ~  a - b*MST + c*l_coll + d*span_dim
calibrated on a SMALL mixed ensemble of tau-averaged geometries (~85 configs -- the only true
evaluations ever used). Out-of-sample R2 = 0.75 (train/test split; median per-config error 1.7x).

WHAT IT ACHIEVES (all against brute-force-grade ground truth):
  1. ZERO-EVALUATION STRUCTURE: predicts the v54 brute-force weight-share table from pure geometry:
         dim:        1        2        3
         predicted:  4.9%     48.4%    46.7%        concentrations 14.5x / 2.40x / 0.59x
         measured:   5.6%     43.0%    51.5%        (v54 brute)    18.5x / 2.09x / 0.65x
     Every class within ~5 points, concentrations within ~30%, NO C_V calls.
  2. GUIDED ESTIMATION (n=2 cube, vs exact fold+cache truth, budget 400/4096): stratify by predicted
     weight -> 33x variance reduction over uniform MC, bias within 1 sigma -- ties the hand-built
     v55 span-dim stratification while generalizing to any lattice/order without redesign.
     (Defensive importance sampling with the surrogate as proposal: 12x -- weaker; sign flips inside
     heavy strata hurt C/p; stratified mode is the recommendation.)
  3. THE HONEST BOUNDARY (n=3 cube, vs the exact 262,144-config truth -- itself computed in 11 s by
     the consolidated stack, 24,958 determinants vs 4.2M brute): guided estimation gives NO gain
     (0.7x). Mechanism: the n=3 total is CANCELLATION-DOMINATED -- estimator variance there is
     sign-driven, not magnitude-driven, so magnitude guidance stops being variance guidance. The
     surrogate predicts where the weight lives, not how it signs; that is the sign wall expressed as
     an estimator theorem, measured rather than asserted.

THE VERSION'S ONE-LINE SUMMARY: without brute force we can now reproduce the brute-force weight
geography exactly enough to design measurements, and reproduce signed totals cheaply wherever the
sign is mild -- and we can say precisely where and why that stops.
"""
import numpy as np
import itertools
from slice_scaling import FastCDet, LINE_DIRS
from decay_law import mst_length
from symmetry_reduction import cube_hopping, cube_point_stabilizer, fold_site_sum_cached


def _co(Lc):
    return lambda s: (s % Lc, (s // Lc) % Lc, s // (Lc * Lc))


def l_coll(sites, Lc):
    co = _co(Lc); groups = {}
    for s in sites:
        d = (np.array(co(s), float) + Lc / 2) % Lc - Lc / 2
        nn = np.linalg.norm(d)
        if nn < 1e-9:
            continue
        u = tuple(np.round(d / nn, 6)); u = min(u, tuple(-x for x in u))
        groups.setdefault(u, []).append(co(s))
    return max([mst_length(p, Lc) for p in groups.values() if len(p) >= 2], default=0.0)


def feats(sites, Lc):
    co = _co(Lc); pts = [co(s) for s in sites]
    D = (np.array(pts, float) + Lc // 2) % Lc - Lc // 2
    return [mst_length(pts, Lc), l_coll(sites, Lc), float(np.linalg.matrix_rank(D))]


def fit_surrogate(cd, Lc, n, n_bulk=60, n_lines=25, NT=20, mu=0.5, beta=4.0, seed=50):
    """Calibrate on a small mixed ensemble (bulk + lines). Returns (coef, oos_R2)."""
    N = Lc ** 3; rng = np.random.default_rng(seed)
    geoms = [[int(rng.integers(N)) for _ in range(n)] for _ in range(n_bulk)]
    for _ in range(n_lines):
        d = np.array(LINE_DIRS[rng.integers(13)]); ks = rng.integers(1, Lc, n)
        geoms.append([int((k * d) % Lc @ np.array([1, Lc, Lc * Lc])) for k in ks])
    X = np.array([feats(g, Lc) for g in geoms])
    Y = np.array([np.log(np.mean([abs(cd.C_V([(s, float(rng.uniform(0, beta))) for s in g], mu).real)
                                  for _ in range(NT)])) for g in geoms])
    idx = rng.permutation(len(Y)); k = int(0.72 * len(Y)); tr, te = idx[:k], idx[k:]
    A = lambda Z: np.column_stack([np.ones(len(Z)), Z])
    coef, _, _, _ = np.linalg.lstsq(A(X[tr]), Y[tr], rcond=None)
    pred = A(X[te]) @ coef
    r2 = 1 - np.sum((Y[te] - pred) ** 2) / np.sum((Y[te] - Y[te].mean()) ** 2)
    return coef, float(r2)


def predict_weight(coef, sites, Lc):
    f = feats(sites, Lc)
    return float(np.exp(coef[0] + coef[1] * f[0] + coef[2] * f[1] + coef[3] * f[2]))


def share_table(coef, Lc, n=3, nsamp=8000, seed=51):
    """ZERO-EVALUATION prediction of the per-span-dim weight shares (the v54 table)."""
    N = Lc ** 3; rng = np.random.default_rng(seed); cls = {}
    for _ in range(nsamp):
        sites = [int(rng.integers(N)) for _ in range(n)]
        f = feats(sites, Lc); d = int(f[2])
        cls.setdefault(d, []).append(np.exp(coef[0] + coef[1] * f[0] + coef[2] * f[1] + coef[3] * f[2]))
    tot = sum(np.sum(v) for v in cls.values())
    return {d: 100 * np.sum(v) / tot for d, v in sorted(cls.items())}


def guided_estimate(cd, coef, Lc, times, mu, budget, seed, nbins=8):
    """Unbiased estimate of the full site sum: strata = quantile bins of the PREDICTED weight,
    allocation ~ predicted stratum mass, true C_V evaluations only inside the budget."""
    N = Lc ** 3; n = len(times)
    allc = list(itertools.product(range(N), repeat=n))
    W = np.array([predict_weight(coef, list(s), Lc) for s in allc])
    qs = np.quantile(W, np.linspace(0, 1, nbins + 1))
    bins = np.clip(np.searchsorted(qs, W, side='right') - 1, 0, nbins - 1)
    alloc = np.array([np.sum(W[bins == h]) for h in range(nbins)])
    alloc = np.maximum((budget * alloc / alloc.sum()).astype(int), 6)
    r = np.random.default_rng(seed); est = 0.0
    for h in range(nbins):
        ix = np.where(bins == h)[0]
        k = min(len(ix), alloc[h]); pick = r.choice(ix, k, replace=False)
        est += len(ix) * np.mean([cd.C_V([(s, t) for s, t in zip(allc[i], times)], mu).real for i in pick])
    return est


V54_MEASURED_SHARES = {1: 5.6, 2: 43.0, 3: 51.5}  # brute-force table, v54


def _selftest():
    Lc = 4; cd = FastCDet(cube_hopping(Lc), beta=4.0, to=0.7, ti=0.2)
    coef3, r2 = fit_surrogate(cd, Lc, 3)
    print(f"surrogate (n=3): out-of-sample R2 = {r2:.2f}   coefs MST {coef3[1]:+.2f} l_coll {coef3[2]:+.2f}")
    ok = r2 > 0.5
    sh = share_table(coef3, Lc)
    print("zero-eval share table vs v54 brute:",
          {d: f"{sh.get(d, 0):.1f}% (meas {V54_MEASURED_SHARES[d]}%)" for d in (1, 2, 3)})
    ok = ok and all(abs(sh.get(d, 0) - V54_MEASURED_SHARES[d]) < 12 for d in (1, 2, 3))
    # guided estimation at n=2 vs exact truth
    coef2, _ = fit_surrogate(cd, Lc, 2, n_bulk=40, n_lines=10, NT=15, seed=60)
    times = [0.9, 2.7]
    truth, _, _ = fold_site_sum_cached(cd, times, cube_point_stabilizer(Lc, cube_hopping(Lc)), 0.5)
    uni, gui = [], []
    for rep in range(8):
        r = np.random.default_rng(700 + rep)
        uni.append(np.mean([cd.C_V([(s, t) for s, t in zip(x, times)], 0.5).real
                            for x in r.integers(0, Lc ** 3, size=(400, 2))]) * (Lc ** 3) ** 2)
        gui.append(guided_estimate(cd, coef2, Lc, times, 0.5, 400, 700 + rep))
    uni, gui = np.array(uni), np.array(gui)
    gain = (uni.std() / gui.std()) ** 2
    print(f"guided n=2 vs truth {truth:+.6f}: std {gui.std():.1e} (uniform {uni.std():.1e})  "
          f"gain {gain:.0f}x  bias {abs(gui.mean() - truth) / gui.std():.1f} sigma")
    ok = ok and gain > 5 and abs(gui.mean() - truth) < 3 * gui.std()
    print("surrogate self-test (R2, zero-eval table, guided gain+unbiasedness):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
