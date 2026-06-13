"""bulk_remainder.py (v72) -- rotation item (c), surrogate-first: the incoherent bulk remainder is
NOT incoherent -- it is organized as mu-controlled ALTERNATING-SIGN MST SHELLS (Friedel rings in
configuration space). The frozen surrogate decay-model was FALSIFIED by the exact crosscheck; the
discovery is what the falsification exposed.

THE FROZEN PREDICTION (zero evaluations, banked before the crosscheck): signed content of the
rank>=2 remainder decays monotonically with MST -- compact shell (MST<4.5) >= 86 +/- 20 % of
|signed| content (G1); far bulk = "noise without signal" (G2). Model: N(l) * exp(-(b + 2/xi_s) l).

THE EXACT CROSSCHECK (orbit-fold moments binned by MST over rank>=2; L=4, times [0.5,1.9,3.3]):

    mu=0.5:  bin (MST)    0-3.5    3.5-4.5    4.5-5.5     5.5+      total
             signed sum  +0.000256 -0.000463  +0.001080  -0.000053  +0.000819 (= v70 reference)
             |s| share      13.8%     25.0%      58.3%      2.9%    inter-shell cancellation 2.3x
             noise share    15.9%     61.4%      20.5%      2.3%
    mu=1.5:  signed sum  -0.001469 -0.001889  -0.002065  +0.000322  -0.005101
             (pattern shifted; 6x larger net; cancellation only 1.13x -- more coherent, matching
              v68's higher r_g at mu=1.5)

BOTH GATES FAIL -- and the data says why: the binned signed sums ALTERNATE IN SIGN at mu=0.5 and the
whole pattern SHIFTS with mu (the frozen confirmation test: if these are phase rings, mu must move
them -- it did). The remainder's radial structure is governed by the orientation phase -- the exact
object that v69/v71 proved has no sub-engine formula. The dominant signed content sits MID-RANGE
(58% at MST 4.5-5.5 at mu=0.5), not in the compact shell; the noise concentrates at intermediate
MST (61-78% in the 3.5-4.5 bin, where N(l) x magnitude^2 peaks), and the far bulk is small in BOTH
signal and noise -- the "noise without signal" picture was wrong too.

THE ROTATION'S UNIFIED CONCLUSION (passes 1-3): every item ended at the same object. The sector
machinery (v70) works because the rank<=1 sector's phase is coherent; the phase has no formula below
the coupled two-spin integrand (v71); and the remainder's net is an alternating-shell sum the
surrogate cannot predict without an orientation channel (v72). The surrogate's missing channel is
now fully characterized: it is THE channel, and the only queued route to it is LEARNED, not derived.

HONEST SCOPE: L=4 exact (two mu values, one beta, fixed times); bin edges chosen before measurement;
shell alternation at other L computable by the same machinery but not yet run (L=6 fold is the
expensive item); the surrogate magnitude/noise predictions were directionally right (far bulk
negligible both ways) and radially wrong (oscillation, mid-range dominance).
"""
import numpy as np
from slice_scaling import FastCDet
from decay_law import mst_length
from symmetry_reduction import cube_hopping, cube_point_stabilizer

BINS = [(0, 3.5), (3.5, 4.5), (4.5, 5.5), (5.5, 99)]


def exact_remainder_shells(cd, Lc, times, mu, bins=BINS):
    """EXACT (orbit-fold) signed sums, second moments, counts per MST bin over the rank>=2
    remainder. Returns (S1, S2, NN) arrays over bins."""
    N = Lc ** 3
    G = np.array(cube_point_stabilizer(Lc, cube_hopping(Lc)))
    idx = np.indices((N,) * 3).reshape(3, -1).T
    code = lambda T: (T[:, 0].astype(np.int64) * N + T[:, 1]) * N + T[:, 2]
    best = np.full(len(idx), np.iinfo(np.int64).max, dtype=np.int64)
    for g in G:
        best = np.minimum(best, code(g[idx]))
    reps, cnt = np.unique(best, return_counts=True)
    co = lambda s: (s % Lc, (s // Lc) % Lc, s // (Lc * Lc))
    mi = lambda v: (v + Lc // 2) % Lc - Lc // 2
    S1 = np.zeros(len(bins)); S2 = np.zeros(len(bins)); NN = np.zeros(len(bins))
    for r, c in zip(reps, cnt):
        tr = (int(r) // (N * N), (int(r) // N) % N, int(r) % N)
        D = mi(np.stack([np.array(tr) % Lc, (np.array(tr) // Lc) % Lc,
                         np.array(tr) // (Lc * Lc)], axis=-1).astype(float))
        cr = max(np.abs(np.cross(D[0], D[1])).max(), np.abs(np.cross(D[0], D[2])).max(),
                 np.abs(np.cross(D[1], D[2])).max())
        if cr < 1e-4:
            continue
        l = mst_length([co(s) for s in tr], Lc)
        v = cd.C_V([(s, t) for s, t in zip(tr, times)], mu).real
        for i, (a, b) in enumerate(bins):
            if a <= l < b:
                S1[i] += c * v; S2[i] += c * v * v; NN[i] += c
                break
    return S1, S2, NN


# exact reference tables (L=4, times [0.5, 1.9, 3.3])
EXACT_SHELLS_MU05 = np.array([+0.000256, -0.000463, +0.001080, -0.000053])
EXACT_SHELLS_MU15 = np.array([-0.001469, -0.001889, -0.002065, +0.000322])
FROZEN_PREDICTION_FALSIFIED = ("G1 compact-shell share predicted 86 +/- 20 %, exact 39% (mu=0.5); "
                               "G2 'noise without signal' far bulk -- wrong: far bulk small in both")


def _selftest():
    cd = FastCDet(cube_hopping(4), beta=4.0, to=0.7, ti=0.2)
    times = [0.5, 1.9, 3.3]
    S05, _, _ = exact_remainder_shells(cd, 4, times, 0.5)
    print("mu=0.5 shells:", np.array2string(S05, precision=6),
          f" total {S05.sum():+.6f} (ref +0.000819)")
    ok = np.allclose(S05, EXACT_SHELLS_MU05, atol=2e-6) and abs(S05.sum() - 0.000819) < 2e-6
    alt = np.all(np.sign(S05) == np.array([1, -1, 1, -1]))
    print(f"alternating-sign shells at mu=0.5 (+,-,+,-): {alt}")
    ok = ok and alt
    S15, _, _ = exact_remainder_shells(cd, 4, times, 1.5)
    shifted = not np.all(np.sign(S15) == np.sign(S05))
    print("mu=1.5 shells:", np.array2string(S15, precision=6),
          f" total {S15.sum():+.6f} -- pattern shifted vs mu=0.5: {shifted}")
    ok = ok and np.allclose(S15, EXACT_SHELLS_MU15, atol=2e-6) and shifted
    compact = (abs(S05[0]) + abs(S05[1])) / np.abs(S05).sum()
    print(f"frozen-prediction falsification reproduced: compact |signed| share {compact:.0%} "
          f"(predicted 86 +/- 20) -> {'outside gate' if abs(compact * 100 - 86) > 20 else 'inside?!'}")
    ok = ok and abs(compact * 100 - 86) > 20
    print("bulk-remainder self-test (exact shells; alternation; mu-shift; falsification):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
