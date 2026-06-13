"""Universality of the slice hierarchy (v58): WEIGHT concentration is universal and robust;
the per-class SIGN hierarchy is estimator-fragile and is DOWNGRADED on the record.

Swept the hierarchy across order (n=2,3,4), temperature (beta=2,4,8), filling (mu=0,0.5,1.5) and the
observable on the L=6 cube, then re-measured with ROBUST statistics after a self-test failure exposed
heavy tails.

RESULT 1 -- WEIGHT UNIVERSALITY (the strong claim; robust and seed-stable):
  The 1d-line/bulk per-configuration weight ratio exceeds 10x in EVERY cell. Mean-based: 10x-223x.
  MEDIAN-based (heavy-tail robust): 11x-184x, seed-stable (e.g. beta=8: 66x/55x/61x across seeds
  11/42/77). Plus exactly universal in U by the banked theorem (C_V contains no U). The weight
  concentration is a property of propagator geometry. STANDS.

RESULT 2 -- SIGN HIERARCHY DOWNGRADED (the correction; the failed gate was the discovery):
  The v54/v57 per-class sign claims used R = |mean|/mean|.|, which is dominated by rare large-|C|
  configurations: the SAME cell (L=6, beta=8) gave R(1d)=0.44 at 500 samples and 0.02 at 400 samples,
  same seed. The robust count-coherence S = |2 f_- - 1| is near the binomial floor (~0.035) in most
  cells: S(1d) 0.008-0.185, S(bulk) 0.007-0.055. HONEST STATUS: the weighted sign structure of the
  classes is REAL but NOT reliably measured at these sample sizes; the v57 statement "the sign
  hierarchy persists and narrows" is downgraded to OPEN, pending weighted-bootstrap error bars or
  much larger samples. (R remains the physically relevant quantity -- it weights by |C| -- but its
  estimator needs tail-aware statistics we have not yet built.)

LESSON: a ratio of means over a heavy-tailed distribution is not a measurement until its estimator
is shown stable; gate self-tests on robust statistics, and treat a failing gate as data.
"""
import numpy as np
from slice_scaling import FastCDet, LINE_DIRS
from symmetry_reduction import cube_hopping


def cell_robust(Lc, n, beta, mu, nsamp=600, seed=11, to=0.7, ti=0.2):
    """One cell with robust statistics: (median weight ratio 1d/bulk, S_1d, S_bulk, R_1d, R_bulk)."""
    N = Lc ** 3; cd = FastCDet(cube_hopping(Lc), beta=beta, to=to, ti=ti)
    rng = np.random.default_rng(seed)
    idx = lambda p: int(p[0] % Lc + Lc * ((p[1] % Lc) + Lc * (p[2] % Lc)))
    v1 = []
    for _ in range(nsamp):
        d = np.array(LINE_DIRS[rng.integers(len(LINE_DIRS))]); ks = rng.integers(1, Lc, size=n)
        v1.append(cd.C_V([(idx(k * d), float(rng.uniform(0, beta))) for k in ks], mu).real)
    v3 = []
    while len(v3) < nsamp:
        sites = [int(rng.integers(N)) for _ in range(n)]
        P = np.array([[s % Lc, (s // Lc) % Lc, s // (Lc * Lc)] for s in sites], float)
        D = (P + Lc // 2) % Lc - Lc // 2
        if np.linalg.matrix_rank(D) == min(3, n):
            v3.append(cd.C_V([(s, float(rng.uniform(0, beta))) for s in sites], mu).real)
    v1, v3 = np.array(v1), np.array(v3)
    S = lambda v: abs(2 * np.mean(v < 0) - 1)
    R = lambda v: abs(v.mean()) / np.abs(v).mean()
    return (np.median(np.abs(v1)) / np.median(np.abs(v3)), S(v1), S(v3), R(v1), R(v3))


def _selftest():
    ok = True
    print("gate 1: median weight ratio universal across a temperature flip (beta=2 and beta=8):")
    for beta in (2.0, 8.0):
        mr, s1, s3, r1, r3 = cell_robust(6, 3, beta, 0.5, nsamp=500)
        print(f"  beta={beta}: median ratio {mr:.0f}x   S(1d)={s1:.3f} S(bulk)={s3:.3f}   "
              f"[non-robust R: {r1:.2f}/{r3:.2f}]")
        ok = ok and mr > 10
    print("gate 2: seed stability of the median ratio (beta=8, seeds 42, 77):")
    ratios = []
    for sd in (42, 77):
        mr, *_ = cell_robust(6, 3, 8.0, 0.5, nsamp=500, seed=sd)
        ratios.append(mr); print(f"  seed {sd}: median ratio {mr:.0f}x")
    ok = ok and all(r > 10 for r in ratios) and max(ratios) / min(ratios) < 2.0
    print("(the R columns above are printed as the fragility warning, not gated -- see docstring)")
    print("slice-universality self-test (robust weight universality, seed-stable):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
