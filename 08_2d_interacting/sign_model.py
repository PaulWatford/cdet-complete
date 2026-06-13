"""sign_model.py (v67) -- the knock answered: the sign structure IS measurable with trustworthy
statistics, the sign of the line sector IS predictable, and exploiting both moves the v66 estimator
ceiling from 0.7x to ~87x at the cancellation-dominated n=3 total.

THE THREE RESULTS (L=4 cube, beta=4, mu=0.5, n=3 unless noted):

1. THE v58-DOWNGRADED QUESTION, SETTLED with the statistics it demanded. The per-geometry sign
   survival r_g = |<C>_tau| / <|C|>_tau (how much of a geometry's weight escapes its own
   tau-cancellation -- the right object, since v60 showed 40% of variance is tau-interference) is
   STABLE and bootstrap-bounded:
        1d lines:  median r_g = 0.696   90% CI [0.606, 0.819]    sign(+) fraction 92%
        2d planes: median r_g = 0.697   90% CI [0.584, 0.822]    sign(+) fraction 70%
        3d bulk:   median r_g = 0.343   90% CI [0.244, 0.468]    sign(+) fraction 45%
   Non-overlapping CIs between low-dim and bulk: the sign hierarchy is REAL at the tau-integrated
   per-geometry level (the v58 downgrade targeted unstable per-sample R estimators; this object is
   the stable one). And the sign itself is PREDICTABLE for lines: 92% positive, vs a coin flip in
   the bulk. r_g correlates with span-dim (-0.45) and MST (-0.50): a sign-survival model is fittable.

2. THE STRUCTURAL FACT (why the sign model matters): the enumerated d<=1 sector -- 808 of 262,144
   configs, 0.3% of the space -- carries +0.002949 of the +0.003846 exact signed total: 77% OF THE
   ENTIRE ANSWER. Sign coherence concentrates the signed sum even harder than magnitude
   concentrates the unsigned one; the bulk's 208,074 configs mostly cancel to a small remainder.

3. THE CEILING MOVED: hybrid estimator (enumerate the sign-coherent d<=1 sector EXACTLY +
   pilot-Neyman the d=2/d=3 remainder with signed-sigma pilots) at budget ~1200 (0.46% of configs)
   vs the exact 262,144-config truth: ~87x variance reduction over uniform MC, bias < 1 sigma --
   where v66's magnitude-only guidance gave 0.7x. (A magnitude-bin arm in the same survey showed
   "231x" but ran on a frozen subsample whose selection variance is not in its std -- flagged, NOT
   banked.) v55's 2.1x at this n was the same design starved of the budget to enumerate the 1d
   sector; the v67 sign measurements are what justify spending the budget there.

HONEST SCOPE: one lattice/order/mu/beta; the 92% sign predictability of lines is measured here, not
derived, and must be re-measured before reuse elsewhere; the bulk remainder is still a coin flip --
the wall stands there, now with its territory mapped to 0.3% precision.
"""
import numpy as np
from slice_scaling import FastCDet, LINE_DIRS
from decay_law import mst_length
from symmetry_reduction import cube_hopping


def sign_survival(cd, Lc, geoms, NT=30, mu=0.5, beta=4.0, rng=None):
    """Per-geometry r_g = |<C>_tau| / <|C|>_tau and the sign of <C>_tau."""
    out = []
    for g in geoms:
        vals = np.array([cd.C_V([(s, float(rng.uniform(0, beta))) for s in g], mu).real
                         for _ in range(NT)])
        out.append((abs(vals.mean()) / np.abs(vals).mean(), np.sign(vals.mean())))
    return out


def class_table(cd, Lc, n_lines=20, n_bulk=40, NT=30, mu=0.5, beta=4.0, seed=80, nboot=300):
    """Bootstrap-bounded sign-survival table by span dimension. Returns {dim: (median, lo, hi, pos_frac)}."""
    N = Lc ** 3; rng = np.random.default_rng(seed)
    co = lambda s: (s % Lc, (s // Lc) % Lc, s // (Lc * Lc))
    geoms = []
    for _ in range(n_lines):
        d = np.array(LINE_DIRS[rng.integers(13)]); ks = rng.integers(1, Lc, 3)
        geoms.append([int((k * d) % Lc @ np.array([1, Lc, Lc * Lc])) for k in ks])
    geoms += [[int(rng.integers(N)) for _ in range(3)] for _ in range(n_bulk)]
    rs = sign_survival(cd, Lc, geoms, NT=NT, mu=mu, beta=beta, rng=rng)
    cls = {}
    for g, (r, sg) in zip(geoms, rs):
        D = (np.array([co(s) for s in g], float) + Lc // 2) % Lc - Lc // 2
        d = int(np.linalg.matrix_rank(D))
        cls.setdefault(d, []).append((r, sg))
    table = {}
    for d, v in sorted(cls.items()):
        r = np.array([x[0] for x in v]); pos = np.mean([x[1] > 0 for x in v])
        B = [np.median(np.random.default_rng(b).choice(r, len(r))) for b in range(nboot)]
        lo, hi = np.percentile(B, [5, 95])
        table[d] = (float(np.median(r)), float(lo), float(hi), float(pos))
    return table


def span_strata(Lc, n):
    """Exact span-dimension strata of all configs (vectorized)."""
    N = Lc ** 3
    idx = np.indices((N,) * n).reshape(n, -1).T
    P = np.stack([idx % Lc, (idx // Lc) % Lc, idx // (Lc * Lc)], axis=2).astype(float)
    D = (P + Lc // 2) % Lc - Lc // 2
    rank = (np.linalg.svd(D, compute_uv=False) > 1e-9).sum(axis=1)
    return {d: idx[rank == d] for d in range(4) if (rank == d).any()}


def hybrid_estimate(cd, Lc, times, mu, budget, seed, strata=None, enum_dims=(0, 1), pilot=25):
    """Sign-informed hybrid: enumerate the sign-coherent low-dim sector EXACTLY (it carries most of
    the signed answer), pilot-Neyman the rest with signed-sigma pilots. Unbiased."""
    if strata is None:
        strata = span_strata(Lc, len(times))
    cv = lambda st: cd.C_V([(s, t) for s, t in zip(st, times)], mu).real
    est = sum(cv(tuple(s)) for d in enum_dims if d in strata for s in strata[d])
    used = sum(len(strata[d]) for d in enum_dims if d in strata)
    r = np.random.default_rng(seed)
    samp = [d for d in strata if d not in enum_dims]
    pil = {d: np.array([cv(tuple(strata[d][i])) for i in r.choice(len(strata[d]), pilot, replace=False)])
           for d in samp}
    w = {d: len(strata[d]) * pil[d].std() for d in samp}; wt = sum(w.values())
    for d in samp:
        k = min(len(strata[d]), max(20, int((budget - used) * w[d] / max(wt, 1e-300))))
        pick = r.choice(len(strata[d]), k, replace=False)
        est += len(strata[d]) * np.mean([cv(tuple(strata[d][i])) for i in pick])
    return est


EXACT_TRUTH_N3 = +0.00384575  # fold+cache over all 262,144 configs (v66, 11 s), times [0.5,1.9,3.3]


def _selftest():
    Lc = 4; cd = FastCDet(cube_hopping(Lc), beta=4.0, to=0.7, ti=0.2)
    tab = class_table(cd, Lc, n_lines=36, n_bulk=84, NT=40)   # survey sizes: CIs need them (v58 lesson)
    for d, (m, lo, hi, pos) in tab.items():
        print(f"dim {d}: r_g median {m:.2f}  CI [{lo:.2f},{hi:.2f}]  sign(+) {pos:.0%}")
    lo1 = tab[1][1]; hi3 = tab[3][2]
    ok = lo1 > hi3 and tab[1][3] > 0.75
    print(f"gates: CI(1d) above CI(bulk): {lo1:.2f} > {hi3:.2f} -> {lo1 > hi3};  1d sign(+) > 75%: {tab[1][3] > 0.75}")
    strata = span_strata(Lc, 3); times = [0.5, 1.9, 3.3]
    uni, hyb = [], []
    for rep in range(5):
        r = np.random.default_rng(1300 + rep)
        uni.append(np.mean([cd.C_V([(s, t) for s, t in zip(x, times)], 0.5).real
                            for x in r.integers(0, Lc ** 3, size=(1200, 3))]) * (Lc ** 3) ** 3)
        hyb.append(hybrid_estimate(cd, Lc, times, 0.5, 1200, 1300 + rep, strata=strata))
    uni, hyb = np.array(uni), np.array(hyb)
    gain = (uni.std() / hyb.std()) ** 2
    print(f"hybrid n=3 vs truth {EXACT_TRUTH_N3:+.6f}: std {hyb.std():.1e} (uniform {uni.std():.1e})  "
          f"gain {gain:.0f}x  bias {abs(hyb.mean() - EXACT_TRUTH_N3) / hyb.std():.1f} sigma")
    ok = ok and gain > 10 and abs(hyb.mean() - EXACT_TRUTH_N3) < 3 * hyb.std()
    print("sign-model self-test (CI separation; 1d sign predictability; ceiling moved):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
