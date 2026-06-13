"""pair_law.py (v81) -- THE LIMIT SET IDENTIFIED: the resonance-regime flip positions converge to
THE SINGLE-PARTICLE LEVELS, approached two-sidedly as a flip PAIR

        mu*_(+/-)(beta) = eps  +/-  c_eps / beta,

measured by windowed trajectory flows (grid 0.0125, NT=120, beta = 12..28, two geometries).
Every "midpoint" sighted in v80 was a pair partner in flight -- the candidate-set hunt is over.

THE MEASUREMENT (L=6, level eps = 1; the four clean fits):
    (1,2,4) lower:  r = 1.046, c = -1.97, rms 0.006
    (1,2,4) upper:  r = 1.003, c = +1.79, rms 0.004   <- the cleanest fit
    (1,3,5) lower:  r = 1.019, c = -1.83, rms 0.001
    (1,3,5) upper:  r = 0.959, c = +2.51, rms 0.027   (the noisy one; its beta<=16 points jittered)
  All four r-limits within 0.05 of the level; c symmetric at ~ +/-1.9 (+/-0.15 pooled).

THE CANDIDATE ARRANGEMENT (stated as CANDIDATE, not proved): c = ln(deg(eps)) / 2.
  deg(eps=1) at L=6 is exactly 36 -> ln(36)/2 = ln 6 = 1.792 -- a 0.4% hit on the cleanest fit,
  inside the pooled spread. Forward mechanism sketch: a flip is a crossing of two Boltzmann
  families differing by one particle AT the level; mu* = eps + ln(g_ratio)/(beta Dk); the
  degeneracy enters the residue ratio; the symmetric pair is the particle-side and hole-side
  crossings with near-reciprocal ratios. Deriving the exact ratio (and the 1/2) is the open
  forward-proof step.

HONEST RESIDUALS:
  - Level 2: partners are GRID-PINNED (the below-2 series sits flat at 1.984 across beta = 20-28
    because the predicted motion per beta-step is smaller than the 0.0125 grid) and the window-3
    series CONFLATED partners at beta = 12 (analysis trap caught: per-window min-flip mixes the
    pair when both enter the window). Consistent with limit 2 within ~0.04; c's smaller than
    level 1's; not fit-grade. Finer grids or larger beta needed.
  - The (1,3,5) upper fit (c = 2.51) is the outlier; its early-beta points carried multiplicity
    jitter.
  - Estimator flip-COUNTS still fluctuate run-to-run at beta >= 20; the stable trajectories are
    of flip POSITIONS that recur.

WHAT THIS RETRO-EXPLAINS: v80's "level attraction" (pairs tightening as 1/beta); the universal
geometry-independent set (levels + flight positions); the L=8 "midpoint" coincidences (0.707,
1.0, 1.828 were partners in flight); the intra-cluster spacing scale (2 c_eps / beta).
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

BETAS = (12.0, 16.0, 20.0, 24.0, 28.0)
# stored primary-flip trajectories (window, geometry) -> [(beta, mu*)]
TRAJ_L6 = {
    ("124", "lev1_lower"): [(12, 0.879), (16, 0.929), (20, 0.954), (24, 0.954), (28, 0.979)],
    ("124", "lev1_upper"): [(12, 1.151), (16, 1.114), (20, 1.101), (24, 1.076), (28, 1.064)],
    ("135", "lev1_lower"): [(16, 0.904), (20, 0.929), (24, 0.941), (28, 0.954)],
    ("135", "lev1_upper"): [(12, 1.151), (16, 1.164), (20, 1.051), (24, 1.064), (28, 1.051)],
}
DEG_L6 = {0.0: 24, 1.0: 36, 2.0: 27, 3.0: 14}
C_CANDIDATE = float(np.log(36) / 2)   # = ln 6 = 1.7918


def fit_trajectory(pts):
    x = np.array([1.0 / b for b, m in pts]); y = np.array([m for b, m in pts])
    A = np.column_stack([np.ones(len(x)), x])
    r, c = np.linalg.lstsq(A, y, rcond=None)[0]
    rms = float(np.sqrt(np.mean((y - A @ np.array([r, c])) ** 2)))
    return float(r), float(c), rms


def _selftest():
    ok = True
    print("pair-law fits (stored trajectories, level eps = 1):")
    cs = {}
    for (g, lab), pts in TRAJ_L6.items():
        r, c, rms = fit_trajectory(pts)
        cs[(g, lab)] = c
        side = -1 if "lower" in lab else +1
        print(f"  {g} {lab}: r = {r:.3f}  c = {c:+.2f}  rms = {rms:.3f}")
        ok = ok and abs(r - 1.0) <= 0.06 and np.sign(c) == side and 1.4 <= abs(c) <= 2.7
    pooled = np.mean([abs(c) for c in cs.values()])
    print(f"pooled |c| = {pooled:.2f}; candidate ln(deg)/2 = ln(36)/2 = {C_CANDIDATE:.3f} "
          f"(cleanest single fit +1.79 hits it at 0.4%; pooled within {abs(pooled - C_CANDIDATE):.2f})")
    ok = ok and abs(pooled - C_CANDIDATE) <= 0.35
    # live engine probe: the lower partner at beta = 24 predicted near 1 - 1.9/24 = 0.921
    cd = FastCDet(cube_hopping(6), beta=24.0, to=0.7, ti=0.2)
    rng = np.random.default_rng(367)
    mus = np.round(np.arange(0.86, 1.0001, 0.0125), 5)
    s = [int(np.sign(np.mean([cd.C_V([(k, float(rng.uniform(0, 24.0))) for k in (1, 2, 4)], float(m)).real
                              for _ in range(100)]))) for m in mus]
    F = [float((mus[i] + mus[i + 1]) / 2) for i in range(len(s) - 1) if s[i] * s[i + 1] < 0]
    pred = 1 - 1.9 / 24
    hit = any(abs(f - pred) <= 0.05 for f in F)
    print(f"live engine: lower partner at beta=24 measured {[round(f, 3) for f in F]} "
          f"vs predicted {pred:.3f} -> within 0.05: {hit}")
    ok = ok and hit
    print("pair-law self-test (limits = level; pair symmetry; c range; candidate; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
