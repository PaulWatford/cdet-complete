"""resonance_regime.py (v80) -- the KT-review round: the chain I closed too early, reopened and
mostly proved. The v77 "beta >= 12 unmeasurable" boundary is RETRACTED AS A BOUNDARY: it was the
RESONANCE REGIME announcing itself. Found by applying the KT-RG method (IS/IS-NOT on the discarded
beta=12 disagreement; Phase-0 on the q-drift; the escalation ladder on the limit-set hunt) at the
user's direction -- multiple effects superposed, exactly as predicted.

THE TWO-REGIME LAW (two independent significant statistics, frozen nulls):
  THERMAL regime (small beta): geometry-dependent offsets, spacing ~ pi/beta-ish.
    Phase-0 reversal en route: the fine grid (0.025) gives beta=4 median spacing 0.625 (q ~ 1.26)
    -- the banked 0.70 was coarse-grid inflated; the sub-pi/beta deviation is REAL and larger than
    banked, with two spacing populations visible already at beta=4.
  RESONANCE regime (large beta): flips ATTRACT TO LEVELS (mean-distance ratio vs uniform null:
    0.87 / 0.86 / 0.71-0.84 / 0.79 at beta = 4/8/12/16; p = 0.025 at beta = 12 and 16 in
    independent runs) and become GEOMETRY-INDEPENDENT (cross-geometry median nearest-flip
    distance 0.020 at L=8 beta=16, p = 0.032; 0.025 at L=6, p = 0.041; vs 0.075 / p = 0.19 at
    beta=4). The old beta=12 "0.40 vs 1.50 disagreement" = intra- vs inter-cluster spacing --
    both real ("more than one effect").

THE UNIVERSAL LIMIT SET (characterized; identification open with a concrete program):
  - the naive levels-plus-midpoints law was KILLED at L=6 (sparse-spectrum discriminator, p=0.33);
  - flip trajectories vs beta are stable/convergent: 1.988 -> level 2 exactly; one family flows as
    1 + c/beta with c ~ 1.39 ~ ln 4 (log-degeneracy-correction candidate);
  - the core set {0.94, 1.09, 1.79, 1.99} at L=6 is EXTERNAL-TIME-INDEPENDENT (stationary under
    (to,ti) = (0.7,0.2)/(1.1,0.3)/(0.5,0.1)) -- pure spectrum/integrand structure; the pretty
    2(to+ti) = 1.8 coincidence was killed by its own discriminator (FM-5 caught in the act);
  - open program: degeneracy-weighted multi-particle crossing energies Delta-E/Delta-k with
    ln(g)/beta corrections.

THE UNLOCK (the orientation channel's offset bottleneck, restructured): in the resonance regime
the flip POSITIONS are geometry-free, so calibration transfers across geometries -- but the
MULTIPLICITY (single vs double crossing) is geometry-dependent (residues), making naive transfer
BIMODAL: 79-87% within the multiplicity-matched cluster, anti-phased (32-47%) against the
odd-multiplicity geometry. Refined channel: transfer the position set + resolve multiplicities
with a few parity anchors -- well-specified engineering.

HONEST SCOPE: axis lines, n=3; statistics from 4-geometry batteries at grid 0.025-0.05, NT 50-100;
estimator reliability at beta >= 20 fluctuates run-to-run (flip COUNTS vary; the stable core
positions recur); limit-set identification open.
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

# stored flip tables (grid 0.025, NT=80, edge flips > 2.95 dropped)
FLIPS_L8_B16 = {"123": [0.26, 0.49, 0.74, 1.41, 1.49, 1.71, 2.04, 2.81],
                "134": [0.31, 0.76, 0.96, 1.36, 1.81, 1.99, 2.54, 2.81],
                "234": [0.44, 0.71, 1.06, 1.44, 1.81, 2.04, 2.54, 2.74, 2.81, 2.91],
                "124": [0.46, 0.71, 0.91, 1.44, 1.79, 2.01, 2.56, 2.71]}
FLIPS_L6_B16 = {"123": [0.69, 1.01, 1.11, 1.44, 1.51, 1.66, 1.99],
                "234": [0.34, 0.44, 0.91, 1.11, 1.74, 2.01, 2.84],
                "135": [0.94, 1.11, 1.74, 1.99, 2.21, 2.86],
                "124": [0.21, 0.91, 1.11, 1.71, 2.01, 2.26]}
CORE_L6 = [0.94, 1.09, 1.79, 1.99]   # external-time-independent core (toti discriminator)
TOTI_TABLE = {(0.7, 0.2): [0.938, 1.087, 1.788, 1.988],
              (1.1, 0.3): [0.962, 1.062, 1.788, 1.988],
              (0.5, 0.1): [0.938, 1.087, 1.812, 1.988]}
LEV_L8 = np.array([0.0, 0.586, 0.828, 1.414, 2.0, 2.586, 2.828])


def mean_dist_to(points, targets):
    return float(np.mean([np.min(np.abs(np.array(targets) - p)) for p in points]))


def perm_p_closer(points, targets, lo=0.2, hi=2.95, n=10000, seed=2):
    rng = np.random.default_rng(seed)
    m = mean_dist_to(points, targets); k = len(points)
    nulls = [mean_dist_to(rng.uniform(lo, hi, k), targets) for _ in range(n)]
    return float(np.mean(np.array(nulls) <= m))


def cross_geometry_stat(sets):
    ds = []; keys = list(sets)
    for g in keys:
        others = np.array(sorted(sum((list(sets[h]) for h in keys if h != g), [])))
        for f in sets[g]:
            ds.append(float(np.min(np.abs(others - f))))
    return float(np.median(ds))


def cross_geometry_p(sets, lo=0.2, hi=2.95, n=20000, seed=7):
    rng = np.random.default_rng(seed)
    obs = cross_geometry_stat(sets); sizes = [len(v) for v in sets.values()]
    cnt = 0
    for _ in range(n):
        rs = {i: list(rng.uniform(lo, hi, k)) for i, k in enumerate(sizes)}
        if cross_geometry_stat(rs) <= obs:
            cnt += 1
    return cnt / n


def transfer_accuracy(flips_a, flips_b, lo=0.2, hi=2.95):
    grid = np.arange(lo, hi + 1e-9, 0.005)
    sf = lambda F: np.array([(-1) ** sum(1 for f in F if g > f) for g in grid])
    return float(np.mean(sf(flips_a) == sf(flips_b)))


def _selftest():
    ok = True
    allf = sum(FLIPS_L8_B16.values(), [])
    p_lev = perm_p_closer(allf, LEV_L8)
    print(f"level attraction (L=8, beta=16, stored): p = {p_lev:.4f} (gate < 0.05)")
    ok = ok and p_lev < 0.05
    p8 = cross_geometry_p(FLIPS_L8_B16); p6 = cross_geometry_p(FLIPS_L6_B16)
    print(f"cross-geometry universality: L=8 p = {p8:.4f}, L=6 p = {p6:.4f} (gates < 0.05)")
    ok = ok and p8 < 0.05 and p6 < 0.05
    naive = sorted(set([0.5, 1.0, 1.5, 2.0, 2.5]))
    p_mid = perm_p_closer(sum(FLIPS_L6_B16.values(), []), naive)
    print(f"naive midpoint law at L=6: p = {p_mid:.4f} (gate > 0.1 -- the kill reproduced)")
    ok = ok and p_mid > 0.1
    drift = max(max(abs(np.array(v) - np.array(TOTI_TABLE[(0.7, 0.2)]))) for v in TOTI_TABLE.values())
    print(f"core-set external-time independence: max drift {drift:.3f} (gate <= 0.05)")
    ok = ok and drift <= 0.05
    accs = [transfer_accuracy(FLIPS_L8_B16[a], FLIPS_L8_B16[b])
            for a in ("134", "234", "124") for b in ("134", "234", "124") if a != b]
    print(f"transfer within multiplicity-matched cluster: min {min(accs):.0%} (gate >= 0.75); "
          f"vs the odd geometry: {transfer_accuracy(FLIPS_L8_B16['123'], FLIPS_L8_B16['134']):.0%} (bimodal)")
    ok = ok and min(accs) >= 0.75
    # live engine gate: the L=6 core flips near 0.94 / 1.09 reproduce in a short window
    cd = FastCDet(cube_hopping(6), beta=20.0, to=0.7, ti=0.2)
    rng = np.random.default_rng(353)
    mus = np.round(np.arange(0.85, 1.2001, 0.025), 4)
    s = [int(np.sign(np.mean([cd.C_V([(k, float(rng.uniform(0, 20.0))) for k in (1, 2, 4)], float(m)).real
                              for _ in range(60)]))) for m in mus]
    F = [float((mus[i] + mus[i + 1]) / 2) for i in range(len(s) - 1) if s[i] * s[i + 1] < 0]
    hit = sum(1 for c in (0.94, 1.09) if any(abs(f - c) <= 0.06 for f in F))
    print(f"live engine: core flips found in window {[round(f, 2) for f in F]} -> {hit}/2 within 0.06")
    ok = ok and hit == 2
    print("resonance-regime self-test (attraction; universality; kills; independence; transfer; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
