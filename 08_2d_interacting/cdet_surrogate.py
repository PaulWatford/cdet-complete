"""cdet_surrogate.py (v79) -- THE CONSOLIDATED SURROGATE. One integration layer carrying every
proven finding from the v66-v78 program, with each component's verified scope stated at the point
of use. This is the front door for no-brute-force prediction; cdet_best.py remains the front door
for exact computation.

WHAT IT COMPOSES (provenance in brackets):
  1. WRAP-SAFE SECTOR identification [v75 shell_fold]: a config is coherent-sector iff all sites
     share a cyclic line through the origin -- the group-invariant definition that corrected the
     v67/v70 wrap-blind subsets (true sectors: 1,618 carrying 82% at L=4; 16,950 at L=6).
  2. TRANSFERABLE MAGNITUDE model [v74 surrogate2]: 10 geometric features, linear ridge, calibrated
     at L=4, transferred to the target L with an 8-shot LINE intercept. TRANSFER ERROR, refined
     here (v79): median per-config error 1.8-2.7x across independent draws (pooled ~2.1x) -- the
     v74 single figure (1.81x) sits at the favorable end of draw-to-draw spread; per-class
     intercepts were hypothesized, TESTED, and REJECTED (offsets differ by only 0.16 ln units;
     the bulk offset estimate is noisier). In-distribution median ~1.7x; ceiling 0.95 -- residual
     signal is the tau-structure family.
     >> v87 REVISION: four independent draws give pooled median 2.31x with per-draw spread
     1.74-2.72x -- the earlier pooled figures (1.88x/2.1x) sat on the favorable side because the
     pool was dominated by one lucky draw; a calibration-seed contamination hypothesis for that
     draw was TESTED AND EXCLUDED (0/8 config overlap). Single fresh draws can reach ~2.7x;
     pooled multi-draw stays <= 2.6x.
  3. r_pred REGIME MAP [v74]: sign-survival is gradedly predictable only where coherence lives
     (within-rank OOS R2 +0.32 / +0.27 / -0.57 for rank 1/2/3); the deep bulk resists even graded
     prediction. The surrogate REPORTS the regime instead of pretending.
  4. ORIENTATION CHANNEL, period-based [v77 mu_period + v78 fugacity_structure]: orientation flips
     in mu with period ~ pi/(q beta), q ~ 1 (comb-limited: <C>_tau is exactly rational in the
     fugacity with Matsubara-comb poles at height pi/beta -- the mechanism behind both the 1/beta
     scaling and the R/L-independence). Calibrate flips on a mu-window, extend by the period.
     HONEST STATUS: at-the-bar (73-76% held-out across seeds; the residual is offset calibration);
     scoped to one-period horizons where it is strongest.

WHAT IT DOES NOT DO (the standing walls, unchanged): R(N, beta) still decays exponentially -- no
component crosses the sign problem; the deep-bulk orientation per geometry remains unpredictable
below the engine (v69/v71/v73); magnitude in-distribution R2 sits below its noise ceiling.
"""
import numpy as np
from slice_scaling import FastCDet, LINE_DIRS
from symmetry_reduction import cube_hopping
from shell_fold import line_masks, classify_true_rank1
from surrogate2 import feats2, ridge_cv, mag_dataset, REGIME_MAP, CEILINGS
from mu_period import (measure_line_signs, persistence_filter, flip_positions,
                       channel_predict, MUS)

BETA_WINDOW = (4.0, 8.0)        # where the period law is verified (v77)
PERIOD_Q = {4.0: 1.12, 6.0: 1.05, 8.0: 0.98}


class CDetSurrogate:
    """Consolidated no-brute-force predictor for n=3 CDet coefficients on cubic lattices."""

    def __init__(self, Lc, beta=4.0):
        self.Lc, self.beta = Lc, beta
        self.M = line_masks(Lc)
        self._w = None; self._mu_f = None; self._sd_f = None; self._off = 0.0

    # ---- magnitude (v74) ----
    def fit_magnitude(self, seed_train=130, seed_target=131, n_shot=8):
        X4, Y4 = mag_dataset(4, 40, 170, seed_train)
        self._mu_f = X4.mean(0); self._sd_f = X4.std(0) + 1e-9
        self._w = ridge_cv((X4 - self._mu_f) / self._sd_f, Y4)
        if self.Lc != 4:
            # 8-shot LINE intercept: line labels are the cleanest (per-class intercepts were
            # tested and rejected in v79 -- offsets differ by only ~0.16 ln units and the bulk
            # offset estimate is noisier)
            Xt, Yt = mag_dataset(self.Lc, n_shot, 0, seed_target)
            Z = (Xt - self._mu_f) / self._sd_f
            p = np.column_stack([np.ones(len(Z)), Z]) @ self._w
            self._off = float(np.mean(Yt - p))
        return self

    def predict_ln_magnitude(self, sites):
        assert self._w is not None, "call fit_magnitude() first"
        Z = (np.array(feats2(sites, self.Lc)) - self._mu_f) / self._sd_f
        return float(np.r_[1.0, Z] @ self._w + self._off)

    # ---- structure (v75 + v74) ----
    def classify(self, sites):
        t = np.array([sites], dtype=int)
        sector = bool(classify_true_rank1(t, self.M)[0])
        rank = int(feats2(sites, self.Lc)[2])
        return {"sector": sector, "rank": rank,
                "r_pred_regime_R2": REGIME_MAP.get(f"rank{rank}", None)}

    # ---- orientation channel (v77/v78), one-period horizon ----
    def orientation_profile(self, ks, NT=40, seed=179, mu_split=1.5):
        s = persistence_filter(measure_line_signs(self.Lc, ks, self.beta, NT=NT, seed=seed))
        pred, acc = channel_predict(s, self.beta, mu_split=mu_split)
        return {"signs_measured": s, "period": float(np.pi / self.beta),
                "heldout_accuracy": acc,
                "scope": "at-the-bar channel (73-76% across seeds, v77); comb mechanism v78"}

    def full_report(self, sites):
        rep = self.classify(sites)
        rep["ln_magnitude"] = self.predict_ln_magnitude(sites)
        rep["ceilings"] = CEILINGS
        return rep


def _selftest():
    ok = True
    sur = CDetSurrogate(6, beta=4.0).fit_magnitude()
    # 1. wrap-safe sector identification on known cases (v75)
    wrap_line = [int(5 + 6 * 1), int(3 + 6 * 3), int(4 + 6 * 2)]  # (5,1,0),(3,3,0),(4,2,0): one wrapped line
    bulk = [7, 100, 215]
    c1 = sur.classify(wrap_line); c2 = sur.classify(bulk)
    print(f"wrap-collinear line -> sector {c1['sector']} (expect True); bulk -> sector {c2['sector']} (expect False)")
    ok = ok and c1["sector"] and not c2["sector"]
    # 2. magnitude transfer on TWO independent draws + pooled median (mixtures declared)
    pred = lambda x: float(np.r_[1.0, (x - sur._mu_f) / sur._sd_f] @ sur._w + sur._off)
    Xs, Ys = mag_dataset(6, 15, 45, 131)        # draw A: 25% lines, n=60
    Xt, Yt = mag_dataset(6, 5, 15, 991)         # draw B: 25% lines, n=20
    eA = [abs(pred(x) - y) for x, y in zip(Xs, Ys)]
    eB = [abs(pred(x) - y) for x, y in zip(Xt, Yt)]
    mA, mB = float(np.exp(np.median(eA))), float(np.exp(np.median(eB)))
    mP = float(np.exp(np.median(eA + eB)))
    print(f"magnitude transfer (8-shot line intercept): draw A {mA:.2f}x, draw B {mB:.2f}x, "
          f"POOLED {mP:.2f}x (gate <= 2.6x)")
    ok = ok and mP <= 2.6
    # 3. orientation channel: one geometry, one-period horizon (honest v77 gates)
    rep = sur.orientation_profile((2, 3, 4))
    print(f"orientation channel: held-out accuracy {rep['heldout_accuracy']:.0%} "
          f"(gates: > 0.44 v73 baseline; >= 0.55), period {rep['period']:.3f}")
    ok = ok and rep["heldout_accuracy"] >= 0.55
    # 4. report integration
    fr = sur.full_report(wrap_line)
    print(f"full report keys: {sorted(fr.keys())}; regime for rank {fr['rank']}: {fr['r_pred_regime_R2']}")
    ok = ok and {"sector", "rank", "ln_magnitude"} <= set(fr.keys())
    print("consolidated-surrogate self-test (sector; transfer; orientation; report):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
