"""Derivation attempt (v59): can the universal weight concentration be PREDICTED from propagator
geometry? Protocol: derive, freeze, predict, then measure. OUTCOME: FALSIFIED at the quantitative
level -- recorded as the negative it is.

THE DERIVATION TESTED. Connected weight should decay exponentially with the length of the minimal
network connecting {external + vertices}: ln|C| ~ a - l/xi, giving class ratio
W_1d/W_bulk ~ exp((l_bulk - l_1d)/xi) -- exponential in L (the v57 data is exponential: ln-ratio
linear in L, slope ~0.41), with xi measured INDEPENDENTLY from the bare propagator.

WHAT THE MEASUREMENTS RETURNED (L=8 cube, beta=4, mu=0.5, n=3):
  1. Independent xi from tau-averaged |G| (axial r=1..3): xi = 0.91.
  2. Per-config law: regressing ln|C| on three candidate geometry variables over 900 random configs,
     MST length wins (R2=0.17, slope -0.51) over closed tour (0.12) and max external leg (0.01).
     BUT: the slope is HALF the prediction (-0.51 vs -1/xi = -1.10) -- effective decay length ~2*xi,
     unexplained -- and geometry explains only ~17-19% of the ln|C| variance.
  3. ZERO-FURTHER-PARAMETER prediction (slope frozen from L=8 randoms; class median MST lengths by
     pure geometry): predicted ratios 3x / 5x / 7x at L=4/6/8. MEASURED median ratios: 16x / 62x /
     30x. UNDER-PREDICTION by 5-10x => the single-variable law is FALSIFIED as the explanation of
     the concentration.
  4. Honest auxiliary finding: per-class median ratios fluctuate strongly across runs (L=8: 30x here
     vs 52-82x in v58) -- the 1d class is a MIXTURE (axis vs diagonal lines) with heavy tails; even
     medians wander with mixture proportions.

VERDICT (the screenshot's bar, applied honestly): prediction and measurement DISAGREE -- the line is
NOT crossed. The exponential FORM in L survives; minimal-connecting-length geometry is a real but
MINOR ingredient; the dominant mechanism of the universal concentration is still unidentified.
OPEN (v60): what carries the missing ~80% of variance -- candidates: line-class commensuration with
the free spectrum (1d sub-lattice shell effects), edge-count/compactness, tau-adjacency structure.
"""
import numpy as np
import itertools
from slice_scaling import FastCDet, LINE_DIRS
from symmetry_reduction import cube_hopping


def dmin(a, b, Lc):
    d = (np.array(a, float) - np.array(b, float) + Lc / 2) % Lc - Lc / 2
    return np.linalg.norm(d)


def mst_length(points, Lc, include_external=True):
    P = ([(0, 0, 0)] if include_external else []) + list(points)
    n = len(P); D = [[dmin(P[a], P[b], Lc) for b in range(n)] for a in range(n)]
    intree = [0]; tot = 0.0
    while len(intree) < n:
        best = (1e9, None)
        for a in intree:
            for b in range(n):
                if b not in intree and D[a][b] < best[0]:
                    best = (D[a][b], b)
        tot += best[0]; intree.append(best[1])
    return tot


def measure_xi(cd, Lc, mu=0.5, beta=4.0, nsamp=600, seed=1):
    """Independent propagator decay length (tau-averaged |G|, axial, wrap-safe range)."""
    rng = np.random.default_rng(seed)
    idx = lambda p: int(p[0] % Lc + Lc * ((p[1] % Lc) + Lc * (p[2] % Lc)))
    rs = [r for r in (1, 2, 3) if r < Lc / 2]
    g = [np.mean([abs(cd.g0(0, idx((r, 0, 0)), float(rng.uniform(0, beta)), mu)) for _ in range(nsamp)])
         for r in rs]
    return -1 / np.polyfit(rs, np.log(g), 1)[0]


def regression(cd, Lc, mu=0.5, beta=4.0, nsamp=600, seed=3):
    """Regress ln|C| on MST length over random configs. Returns (slope, R2)."""
    co = lambda s: (s % Lc, (s // Lc) % Lc, s // (Lc * Lc))
    rng = np.random.default_rng(seed); ls = []; lc = []
    for _ in range(nsamp):
        sites = [int(rng.integers(Lc ** 3)) for _ in range(3)]
        c = abs(cd.C_V([(s, float(rng.uniform(0, beta))) for s in sites], mu).real)
        if c > 1e-300:
            ls.append(mst_length([co(s) for s in sites], Lc)); lc.append(np.log(c))
    ls = np.array(ls); lc = np.array(lc)
    slope = np.polyfit(ls, lc, 1)[0]; r = np.corrcoef(ls, lc)[0, 1]
    return slope, r * r


def _selftest():
    Lc = 6; cd = FastCDet(cube_hopping(Lc), beta=4.0, to=0.7, ti=0.2)
    xi = measure_xi(cd, Lc)
    slope, R2 = regression(cd, Lc, nsamp=500)
    print(f"xi = {xi:.2f}   regression: slope={slope:.3f} (naive prediction {-1/xi:.3f})  R2={R2:.2f}")
    # geometry-only class medians -> frozen-slope prediction
    rng = np.random.default_rng(4)
    g1 = [mst_length([tuple((k * np.array(LINE_DIRS[rng.integers(13)])) % Lc) for k in rng.integers(1, Lc, 3)], Lc)
          for _ in range(2000)]
    g3 = []
    while len(g3) < 2000:
        sites = [tuple(rng.integers(0, Lc, 3)) for _ in range(3)]
        D = (np.array(sites, float) + Lc // 2) % Lc - Lc // 2
        if np.linalg.matrix_rank(D) == 3:
            g3.append(mst_length(sites, Lc))
    pred = np.exp(-slope * (np.median(g3) - np.median(g1)))
    idx = lambda p: int(p[0] % Lc + Lc * ((p[1] % Lc) + Lc * (p[2] % Lc)))
    v1 = [abs(cd.C_V([(idx(k * np.array(LINE_DIRS[rng.integers(13)])), float(rng.uniform(0, 4.0)))
                      for k in rng.integers(1, Lc, 3)], 0.5).real) for _ in range(400)]
    v3 = []
    while len(v3) < 400:
        sites = [int(rng.integers(Lc ** 3)) for _ in range(3)]
        P = np.array([[s % Lc, (s // Lc) % Lc, s // (Lc * Lc)] for s in sites], float)
        D = (P + Lc // 2) % Lc - Lc // 2
        if np.linalg.matrix_rank(D) == 3:
            v3.append(abs(cd.C_V([(s, float(rng.uniform(0, 4.0))) for s in sites], 0.5).real))
    meas = np.median(v1) / np.median(v3)
    print(f"frozen-slope prediction {pred:.0f}x  vs measured {meas:.0f}x   "
          f"(under-prediction x{meas / pred:.1f} = the falsification)")
    ok = (slope < 0) and (0.03 < R2 < 0.5) and (meas > 2 * pred)
    print("decay-law self-test (law direction real; quantitative prediction falsified):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
