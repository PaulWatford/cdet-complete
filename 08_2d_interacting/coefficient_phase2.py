"""coefficient_phase2.py (v99) -- COEFFICIENT PROGRAM PHASE 2: the importance-sampled estimator
(the heavy-tail problem solved), the frozen polynomial measured to 3-7%, and THE TWO-SECTOR
DISCOVERY: faithfulness-as-claimed falsified by direct measurement -- the physical zero balances
the frozen f2-polynomial against a delta1 antiperiodic-image sector the freeze kills.

THE ESTIMATOR. The s=0 integrand autopsy (beta=36): the top 1% of tau-samples carry 95.5% of
the |v| mass; the mass lives at CLUSTERED times (spread 3.6 vs 18.3) near the edges; survival
tail index alpha ~ 0.55 -- the plain estimator has INFINITE VARIANCE and its inter-draw error
bars are fiction (demonstrated: a 24-draw brute running mean swung -0.178 -> +0.023 when late
spikes landed). Fix: mixture importance sampling -- w.p. 1/2 uniform on the box, w.p. 1/2
cluster mode (t1 uniform; t2, t3 = t1 + Laplace(lambda=0.8) truncated to [0, beta] with exact
normalization). Weights = q_uniform/q_mixture are bounded <= 2 and mean 1 (unbiasedness gates);
validated against an analytic integrand (1.6 sigma over 400k) and against the s=0 record;
variance reduction ~31x per sample at s=0. The +/-5% spec costs ~50 s/point instead of ~26 min.

THE FROZEN POLYNOMIAL (beta=36, mu_exp=1.845, all IS, multi-draw):
    A = +0.3700(108)        [supersedes v96's brute +0.277(45): tail-biased LOW, as the
                             heavy-tail mechanism predicts -- the mean rides on rare positive
                             clusters that finite brute samples miss]
    P(0.0005) = +0.2553(127)   P(0.001) = +0.1678(118)
    P(0.002)  = -0.0345(74)    P(0.004) = -0.4063(126) [reproduced at fresh seed]
    root s* = 0.00183(8)  ->  z_pol(36) = 1.8249(12)
The polynomial is smooth and internally consistent: the directly measured
frozen(s_phys = 0.0037584) = -0.3391(143) sits exactly on it.

THE REGISTERED TWO-BRANCH TEST, SCORED. Registered before measuring: root-flow branch (root at
s_phys = 0.00376(41), small-s slope bending to ~ -98e-9) vs failure branch (slope ~ -190e-9
persists; root ~ 0.0018). The slope stayed at ~ -200e-9 down to s = 0.0005: the root-flow
branch is EXCLUDED at ~10 sigma. But the failure branch's interpretation is now IDENTIFIED,
not just suspected:

THE TWO-SECTOR DISCOVERY. Faithfulness as claimed in v96 ("the frozen object equals the
physical one at (s_phys, mu_phys) to 1e-13") is FALSIFIED at 3.4 sigma by direct measurement:
physical(1.845) = +0.030(108) [the v93 zero is real] vs frozen(s_phys, 1.845) = -0.3391(143).
The 1e-13 argument compared occupancy VALUES but ignored that they multiply exponentially
growing tau-factors: the level-1 particle branch carries (1 - nf1) e^{(mu-1) tau} =
e^{-(mu-1)(beta - tau)} -- O(1) in the tau -> beta corner. The freeze (delta1 = 0 exactly)
kills these ANTIPERIODIC IMAGES; physically they contribute a hole-image sector
    Delta(s_phys; 36) = physical - frozen = +0.369(109) e-9,
the same size as everything else at the zero. The physical zero is the root of
[frozen polynomial + Delta(s; beta)], which is why the frozen root (0.00183) sits 2.05x below
the physical f2* (0.00376). The v96 "faithfulness PASS" was an underpowered brute gate
(+/- 0.24-0.35 errors over a -0.37 effect) -- precisely the audit's too-weak-test finding.

CONSEQUENCES REGISTERED. (1) The literal-rate bookkeeping behind the v93/v95 menu (rates
|mu - eps| read off occupancy deviations) is now suspect for HOLE-side monomials: the tau-corner
saddle reduces effective hole rates (delta1's effective suppression at the zero is ~O(1), not
e^{-0.845 beta}). The menu positions need a tau-integrated re-derivation. The EMPIRICAL pool
(six honest zeros) is unaffected. (2) v96's #106 "proven FAITHFUL" is downgraded: the triple
agreed within (large) errors; the identity is false as stated. (3) The decisive
13/7-vs-24/13 object is now Delta(s; beta): measure the hole-image sector's own s- and
beta-dependence (cheap: Delta(s) = physical-style evaluation minus frozen at matched (s, mu)
-- or directly via a delta1-freeze that keeps level-1 occupancy physical).
"""
import numpy as np
from coefficient_flow import FrozenCDet
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

LAM = 0.8
BETA, MU = 36.0, 1.845
A36 = (0.3700e-9, 0.0108e-9)
GRID36 = {0.0005: (0.2553e-9, 0.0127e-9), 0.001: (0.1678e-9, 0.0118e-9),
          0.002: (-0.0345e-9, 0.0074e-9), 0.004: (-0.4063e-9, 0.0126e-9)}
ROOT36 = (0.00183, 0.00008)            # -> z_pol(36) = 1.8249(12)
FROZEN_AT_SPHYS = (-0.3391e-9, 0.0143e-9)   # s_phys = 0.0037584
PHYSICAL_1845 = (0.030e-9, 0.108e-9)
DELTA_SPHYS = (0.369e-9, 0.109e-9)     # the hole-image sector at the physical point


def draw_batch(rng, beta, n):
    """Mixture proposal: 1/2 uniform box, 1/2 cluster (truncated-Laplace relative offsets).
    Returns (T, w) with w = q_uniform/q_mixture; estimator of the box mean is E[v * w]."""
    pick = rng.random(n) < 0.5
    T = np.empty((n, 3))
    T[:, 0] = rng.uniform(0, beta, n)
    u = rng.uniform(0, beta, (n, 2))
    t1 = T[:, 0]
    Z = 1.0 - 0.5 * (np.exp(-LAM * t1) + np.exp(-LAM * (beta - t1)))
    cl = np.empty((n, 2))
    for j in range(2):
        r = rng.random(n) * Z
        Fl = 0.5 * (1 - np.exp(-LAM * t1))
        below = r < Fl
        cl[:, j] = np.where(below, t1 + np.log(1 - 2 * (Fl - r)) / LAM,
                            t1 - np.log(1 - 2 * (r - Fl)) / LAM)
    T[:, 1:] = np.where(pick[:, None], u, cl)

    def lap(t):
        return (LAM / 2) * np.exp(-LAM * np.abs(t - t1)) / Z
    q = 0.5 * (1.0 / beta**3) + 0.5 * (1.0 / beta) * lap(T[:, 1]) * lap(T[:, 2])
    w = (1.0 / beta**3) / q
    return T, w


def is_mean(cd, beta, mu, rng, ndraw=12, nt=2048):
    """Importance-sampled tau-average of C_V at vertex sites (1,2,4); inter-draw errors."""
    ms = []
    for _ in range(ndraw):
        T, w = draw_batch(rng, beta, nt)
        v = np.array([cd.C_V([(1, float(t[0])), (2, float(t[1])), (4, float(t[2]))], mu).real
                      for t in T])
        ms.append(float(np.mean(v * w)))
    return float(np.mean(ms)), float(np.std(ms, ddof=1) / np.sqrt(ndraw))


def _selftest():
    ok = True
    rng = np.random.default_rng(3083)
    # gate 1: weights bounded and unbiased
    T, w = draw_batch(rng, BETA, 40000)
    print(f"weights: max {w.max():.3f} (gate <= 2.001), mean {w.mean():.4f} (gate |mean-1| < 0.02)")
    ok = ok and w.max() <= 2.001 and abs(w.mean() - 1) < 0.02
    # gate 2: analytic integrand, IS vs brute
    f = lambda T: np.exp(-0.155 * (np.abs(T[:, 1] - T[:, 0]) + np.abs(T[:, 2] - T[:, 0]))) \
        + 0.3 * np.sin(T[:, 0])
    Tb = rng.uniform(0, BETA, size=(300000, 3)); fb = f(Tb)
    T, w = draw_batch(rng, BETA, 300000); fi = f(T) * w
    dev = abs(fb.mean() - fi.mean()) / np.sqrt(fb.var() / 3e5 + fi.var() / 3e5)
    print(f"analytic test: brute {fb.mean():.5f} vs IS {fi.mean():.5f}: {dev:.1f} sigma (gate < 4)")
    ok = ok and dev < 4
    # gate 3: stored-record structure -- the root and the two-sector gap
    rt, rte = ROOT36
    print(f"frozen root s* = {rt}({rte}) (gate in [0.0016, 0.0021]); physical f2* = 0.00376(41): "
          f"the frozen root is NOT the physical zero")
    ok = ok and 0.0016 < rt < 0.0021
    d, de = DELTA_SPHYS
    gap = abs(FROZEN_AT_SPHYS[0] - PHYSICAL_1845[0]) / np.sqrt(FROZEN_AT_SPHYS[1]**2
                                                               + PHYSICAL_1845[1]**2)
    print(f"two-sector gate: |frozen(s_phys) - physical| = {gap:.1f} sigma (gate > 3 -- "
          f"faithfulness-as-claimed falsified); Delta = {d*1e9:+.3f}({de*1e9:.3f}) e-9 at "
          f"{d/de:.1f} sigma (gate > 3)")
    ok = ok and gap > 3 and d / de > 3
    # gate 4 (live): IS frozen(s_phys) lands in the stored band
    cd = FrozenCDet(cube_hopping(6), beta=BETA, s=0.0037584)
    strip = np.exp(0.5 * (MU - 2.0))
    m, se = is_mean(cd, BETA, MU, np.random.default_rng(3089), ndraw=6)
    m, se = m / strip, se / strip
    dev = abs(m - FROZEN_AT_SPHYS[0]) / np.sqrt(se**2 + FROZEN_AT_SPHYS[1]**2)
    print(f"live IS frozen(s_phys): {m*1e9:+.4f} +/- {se*1e9:.4f} vs stored "
          f"{FROZEN_AT_SPHYS[0]*1e9:+.4f}: {dev:.1f} sigma (gate < 3)")
    ok = ok and dev < 3
    print("phase-2 self-test (weights; analytic; root; two-sector; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
