"""sector_estimator.py (v70) -- the sign model folded into the surrogate layer as SCALABLE EXACT
MACHINERY, plus an exact-variance methodology that corrected one of our own banked claims.

THE FOLD-IN. The v67/v68 sign findings become algorithmic at any lattice size:
  1. The coherent (rank<=1) sector is POLYNOMIALLY SMALL BY CONSTRUCTION and directly constructible
     from direction classes in O(N^2) -- no enumeration of the N^3 config space. Sizes: 808 of
     262,144 at L=4 (0.31%); 3,774 of 10,077,696 at L=6 (0.037%).
  2. Per-config rank classification is O(1) and vectorizes: EXACT strata counts over all 10,077,696
     L=6 configs in ~6 s (rank<=1: 3,774 / rank2: 902,136 / rank3: 9,171,786).
  3. Estimator: exact sector sum + signed-sigma pilot-Neyman over rank2/rank3. Unbiased, with a
     principled error bar, at any L.
  The sign-survival channel r_pred (ln r_g ~ a - MST/xi_s + ...; OOS R2 = 0.32, implied xi_s = 2.2
  vs the 3.0 measured in v68) is banked as the surrogate's sign channel; its role here is
  conceptual -- it is WHY the rank<=1 sector is the right thing to enumerate.

THE CORRECTION (banked openly, per protocol). Exact second moments -- computable by the same orbit
fold that computes exact sums, since C is group-invariant -- give every design's variance EXACTLY:
     uniform (B=1200, L=4):   exact std 1.08e-2   (measured across seed sets: 2.75e-3 ... 3.0e-2!)
     v67 design:              exact std 4.30e-3   (v67 measured 2.9e-3)
     TRUE GAIN: ~6x.  The banked v67 figure of 87-110x was INFLATED by a lucky-high uniform
     baseline; today's seed set was lucky-LOW by 4x in the opposite direction. v67's structural
     facts (77% of the signed total in the sector; the CIs; coherence) are UNTOUCHED -- only the
     gain factor corrects, 87-110x -> ~6x exact.
Exact noise decomposition: 96% of uniform's E[C^2] sits in the rank<=1 sector's rarity (the single
all-external config alone: 34%); the bulk carries 4%. Removing the sector exactly is what works;
nothing magnitude-based can compress the remaining sign-driven bulk noise (v66's theorem, again).

NEW STANDING RULE (bought with this correction): in heavy-tailed systems, estimator comparisons
must be exact-moment-based wherever exact moments are computable; rep-spread comparisons of
heavy-tailed estimators are not measurements.

L=6 DEMONSTRATION (10M-config scale, ~4,600 evaluations = 0.045%): exact sector sum = -5.87e-4 --
NEGATIVE, the mu=0.5 orientation flip of v68 appearing in exact arithmetic (L=4 sector: positive).
Total estimate -2.3e-3 +/- 4.5e-3: the error bar exceeds the value -- at L=6 the bulk noise
dominates the signed total. Honest reading: the machinery scales; the sign problem scales faster.
"""
import numpy as np
import itertools
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping, cube_point_stabilizer


def rank1_family(Lc):
    """The full coherent sector (rank<=1 configs incl. external-coincident), via direction classes."""
    N = Lc ** 3
    co = lambda s: np.array([s % Lc, (s // Lc) % Lc, s // (Lc * Lc)], float)
    mi = lambda v: (v + Lc // 2) % Lc - Lc // 2
    dirs = {}
    for s in range(1, N):
        d = mi(co(s)); d = d / np.linalg.norm(d)
        key = tuple(np.round(d, 5)); key = min(key, tuple(-x for x in key))
        dirs.setdefault(key, []).append(s)
    fam = set()
    for sites in dirs.values():
        pts = [0] + sites
        for t in itertools.product(pts, repeat=3):
            if any(x != 0 for x in t):
                fam.add(t)
    fam.add((0, 0, 0))
    return sorted(fam)


def exact_sector_sum(cd, Lc, times, mu):
    fam = rank1_family(Lc)
    return sum(cd.C_V([(s, t) for s, t in zip(g, times)], mu).real for g in fam), fam


def exact_strata_counts(Lc, chunk=600000):
    """EXACT rank-stratum counts over all N^3 configs, vectorized (no evaluations)."""
    N = Lc ** 3
    mi = lambda v: (v + Lc // 2) % Lc - Lc // 2
    n1 = n2 = n3 = 0
    for start in range(0, N ** 3, chunk):
        ids = np.arange(start, min(start + chunk, N ** 3))
        T = np.stack([ids // (N * N), (ids // N) % N, ids % N], axis=1)
        D = mi(np.stack([T % Lc, (T // Lc) % Lc, T // (Lc * Lc)], axis=-1).astype(np.float32))
        c01 = np.cross(D[:, 0], D[:, 1]); c02 = np.cross(D[:, 0], D[:, 2]); c12 = np.cross(D[:, 1], D[:, 2])
        r1 = (np.abs(c01).max(1) < 1e-4) & (np.abs(c02).max(1) < 1e-4) & (np.abs(c12).max(1) < 1e-4)
        det = np.einsum('ij,ij->i', D[:, 0], np.cross(D[:, 1], D[:, 2]))
        r3 = np.abs(det) > 1e-4
        n1 += int(r1.sum()); n3 += int(r3.sum()); n2 += len(ids) - int(r1.sum()) - int(r3.sum())
    return n1, n2, n3


def exact_moments_L4(cd, times, mu):
    """Exact per-stratum first/second moments at L=4 via orbit fold (C is group-invariant)."""
    Lc = 4; N = 64
    G = np.array(cube_point_stabilizer(Lc, cube_hopping(Lc)))
    idx = np.indices((N,) * 3).reshape(3, -1).T
    code = lambda T: (T[:, 0].astype(np.int64) * N + T[:, 1]) * N + T[:, 2]
    best = np.full(len(idx), np.iinfo(np.int64).max, dtype=np.int64)
    for g in G:
        best = np.minimum(best, code(g[idx]))
    reps, cnt = np.unique(best, return_counts=True)
    co = lambda s: np.stack([s % Lc, (s // Lc) % Lc, s // (Lc * Lc)], axis=-1).astype(float)
    S1 = np.zeros(4); S2 = np.zeros(4); NN = np.zeros(4)
    for r, c in zip(reps, cnt):
        tr = (int(r) // (N * N), (int(r) // N) % N, int(r) % N)
        v = cd.C_V([(s, t) for s, t in zip(tr, times)], mu).real
        D = (co(np.array(tr)) + Lc // 2) % Lc - Lc // 2
        d = int(np.linalg.matrix_rank(D))
        S1[d] += c * v; S2[d] += c * v * v; NN[d] += c
    return S1, S2, NN


def exact_design_stds(S1, S2, NN, budget=1200, pilots=50):
    """Exact stds of: uniform; v67 design (enum d<=1 + Neyman d2/d3); sector+uniform-rest."""
    Ntot = NN.sum(); tot = S1.sum()
    varC = S2.sum() / Ntot - (tot / Ntot) ** 2
    sd_uni = Ntot * np.sqrt(varC / budget)
    m = np.where(NN > 0, S1 / np.maximum(NN, 1), 0)
    s2 = np.where(NN > 0, S2 / np.maximum(NN, 1) - m ** 2, 0); sd = np.sqrt(np.maximum(s2, 0))
    n_en = int(NN[0] + NN[1]); rest = budget - n_en - pilots
    sd_v67 = np.sqrt((NN[2] * sd[2] + NN[3] * sd[3]) ** 2 / rest)
    nrest = Ntot - n_en
    m_r = (S1[2] + S1[3]) / nrest; v_r = (S2[2] + S2[3]) / nrest - m_r ** 2
    sd_sc = np.sqrt(nrest ** 2 * v_r / (budget - n_en))
    return sd_uni, sd_v67, sd_sc


def pilot_neyman_estimate(cd, Lc, times, mu, n_pilot=400, seed=2000):
    """Unbiased signed-total estimate at scale: exact sector + pilot-Neyman rank2/rank3."""
    S_sec, fam = exact_sector_sum(cd, Lc, times, mu)
    n1, n2, n3 = exact_strata_counts(Lc)
    assert n1 == len(fam), "sector construction vs classification mismatch"
    N = Lc ** 3; rng = np.random.default_rng(seed)
    mi = lambda v: (v + Lc // 2) % Lc - Lc // 2
    def draw(target, k):
        vals = []
        while len(vals) < k:
            g = rng.integers(0, N, 3)
            D = mi(np.stack([g % Lc, (g // Lc) % Lc, g // (Lc * Lc)], axis=-1).astype(float))
            cr = max(np.abs(np.cross(D[0], D[1])).max(), np.abs(np.cross(D[0], D[2])).max(),
                     np.abs(np.cross(D[1], D[2])).max())
            det = abs(np.dot(D[0], np.cross(D[1], D[2])))
            r = 1 if cr < 1e-4 else (3 if det > 1e-4 else 2)
            if r == target:
                vals.append(cd.C_V([(s, t) for s, t in zip(g, times)], mu).real)
        return np.array(vals)
    p2 = draw(2, n_pilot); p3 = draw(3, n_pilot)
    est = S_sec + n2 * p2.mean() + n3 * p3.mean()
    err = np.sqrt(n2 ** 2 * p2.var() / len(p2) + n3 ** 2 * p3.var() / len(p3))
    return est, err, S_sec, (n1, n2, n3)


RPRED_ROLE = ("sign-survival channel ln r_g ~ a - MST/xi_s + c*l_coll + d*dim; OOS R2 = 0.32, "
              "implied xi_s = 2.2 (v68 measured 3.0); role: identifies the coherent sector as the "
              "enumeration target -- not used as a numerical weight")


def _selftest():
    times = [0.5, 1.9, 3.3]; mu = 0.5
    cd4 = FastCDet(cube_hopping(4), beta=4.0, to=0.7, ti=0.2)
    S, fam = exact_sector_sum(cd4, 4, times, mu)
    print(f"L=4 sector: {len(fam)} configs, exact sum {S:+.6f} (reference +0.002949)")
    ok = len(fam) == 808 and abs(S - 0.002949) < 2e-5
    S1, S2, NN = exact_moments_L4(cd4, times, mu)
    print(f"exact total {S1.sum():+.8f} (reference +0.00384575, match {abs(S1.sum() - 0.00384575):.1e})")
    ok = ok and abs(S1.sum() - 0.00384575) < 1e-7
    su, sv, ss = exact_design_stds(S1, S2, NN)
    gain = (su / sv) ** 2
    print(f"EXACT design stds (B=1200): uniform {su:.2e}, v67-design {sv:.2e} (TRUE gain {gain:.0f}x; "
          f"banked 87-110x CORRECTED), sector+uniform-rest {ss:.2e}")
    ok = ok and su > 8e-3 and 3 <= gain <= 12
    cd6 = FastCDet(cube_hopping(6), beta=4.0, to=0.7, ti=0.2)
    S6, fam6 = exact_sector_sum(cd6, 6, times, mu)
    print(f"L=6 sector: {len(fam6)} configs, exact sum {S6:+.3e} -- sign flip vs L=4: {S * S6 < 0}")
    ok = ok and len(fam6) == 3774 and S * S6 < 0
    print("sector-estimator self-test (sector exact; moments exact; corrected gain; L=6 flip):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
