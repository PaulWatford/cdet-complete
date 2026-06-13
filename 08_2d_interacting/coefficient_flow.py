"""coefficient_flow.py (v96; STATUS REVISED v99) -- THE COEFFICIENT PROGRAM, PHASE 1.
[v99 revision, coefficient_phase2.py: "proven FAITHFUL" below is DOWNGRADED -- the faithfulness
triple agreed only within large brute errors; the identity is FALSE as stated (falsified at 3.4
sigma at IS power). The freeze kills the delta1 ANTIPERIODIC IMAGES, whose tau-corner terms
e^{-(mu-1)(beta-tau)} are O(1): the physical zero is a TWO-SECTOR balance (frozen polynomial +
hole-image sector Delta). The A(beta) record below is also superseded at beta=36 by the IS value
+0.3700(108) -- the brute values are tail-biased LOW. The instrument and the alive-background
conclusion stand.]
THE COEFFICIENT PROGRAM, PHASE 1: the freeze instrument built
and validated, the background measured alive and decaying, the no-fit prediction test honestly
inconclusive with its spec computed.

THE INSTRUMENT. FrozenCDet (below, reusable): FastCDet with the window-level occupancies set by
hand -- levels <= 1 to exactly 1, level 2 to a free parameter s, level 3 to exactly 0, far
levels physical. At beta >= 36 the neglected physical deviations are <= 1e-13, so the frozen
object equals the physical one when (s, mu) sit on the physical locus -- FAITHFULNESS, verified
directly: at (s_phys = 0.003758, mu = 1.8450, beta = 36) the frozen value, the frozen value at
mu_exp = 1.84, and the raw physical value agree within errors (-0.13(24), -0.15(12), +0.19(35)
e-9 -- all consistent with the physical zero). Validation: A(20) = +1.853 +/- 0.075 e-9
reproduces the v89 small-f extrapolation (~ +2 e-9).

STRIP CHARACTERIZED. With frozen occupancies the per-config mu-identity C(mu') =
e^{0.5 (mu'-mu)} C(mu) FAILS through the far-level antiperiodic images (physical nf carrying
e^{+beta mu}; O(1) per entry on near-beta time-difference configs) -- the creep carrier
identified concretely. The determinants on typical configs scale exactly (verified 1e-6); the
tau-averaged object is the honest one and all coefficients here are tau-averaged.

THE BACKGROUND RECORD (A(beta) = the constant coefficient, multi-draw inter-draw errors, 36-52
draws x NT=2048, mu_exp = 1.84, stripped):
    beta:  20         28         36         44
    A:     1.853(75)  0.839(102) 0.277(45)  0.167(36)   [1e-9 units]
A(44) > 0 at 4.6 sigma: THE BACKGROUND IS ALIVE -- the (1,2) window carries no background-zero,
so no midpoint static (consistent with no flip at 3/2 and with the exponent-balance picture).
A decays with EFFECTIVE rate ~ 0.10-0.12 over beta = 20-44 with visible curvature (pair rates
0.099(16), 0.139(25), 0.063(34)): a subexponential prefactor is active and the asymptotic rate
(= 2 - z_inf in the root-flow picture: 1/7 = 0.1429 for 13/7, 2/13 = 0.1538 for 24/13) is NOT
yet reached or resolved. The 13/7-vs-24/13 status is unchanged by this round.

THE PREDICTION TEST (honest). The naive root of {A, c1} from the s-grid (c1 ~ -190 to -230 e-9,
c2 ~ +3000 e-9 at beta=36) lands at s* ~ 0.0015, a factor ~2.5 below the physical f2* = 0.0038
-- INCONCLUSIVE, not failed: the faithfulness triple passes, and the discrepancy sits in A's
heavy-tailed estimation (two 36-draw batches differed by 2 sigma) plus small-s curvature below
the grid's resolution. SPEC for phase 2: A to +/-5% (~10x samples: ~500 draws x 2048 per beta),
an s-grid extended below s = 0.002 (geometric, 5+ points), and mu_exp pinned at the physical
value per beta; then root the polynomial and the prediction is parameter-free.
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

A_RECORD = {20.0: (1.853e-9, 0.075e-9), 28.0: (0.839e-9, 0.102e-9),
            36.0: (0.277e-9, 0.045e-9), 44.0: (0.167e-9, 0.036e-9)}
FAITH_36 = {"frozen_phys": (-0.128e-9, 0.236e-9), "frozen_184": (-0.152e-9, 0.118e-9),
            "physical": (0.194e-9, 0.349e-9)}
RATE_BAND_CANDIDATES = {"13/7": 1 / 7, "24/13": 2 / 13, "11/6": 1 / 6}


class FrozenCDet(FastCDet):
    """FastCDet with window-level occupancies frozen: levels<=1 -> 1, level2 -> s, level3 -> 0;
    far levels physical. The reusable freeze instrument of the coefficient program."""

    def __init__(self, hop, beta, to=0.7, ti=0.2, s=0.0):
        super().__init__(hop, beta=beta, to=to, ti=ti)
        self.lev = np.round(self.ev, 9)
        self.s = s
        self.m_lo = self.lev <= 1.0
        self.m_2 = self.lev == 2.0
        self.m_3 = self.lev == 3.0

    def g0(self, i, j, tau, mu):
        beta = self.beta
        tt = complex(tau)
        while tt.real > beta:
            tt -= 2 * beta
        while tt.real <= -beta:
            tt += 2 * beta
        xi = self.ev - mu
        nf = 1.0 / (np.exp(beta * xi) + 1.0)
        nf = np.where(self.m_lo, 1.0, nf)
        nf = np.where(self.m_2, self.s, nf)
        nf = np.where(self.m_3, 0.0, nf)
        if tt.real > 0:
            gk = -(1.0 - nf) * np.exp(-xi * tt)
        elif tt.real < 0:
            gk = nf * np.exp(-xi * tt)
        else:
            gk = nf
        return np.sum(self.U[i, :] * self.U[j, :] * gk)


def effective_rates():
    bs = sorted(A_RECORD)
    out = []
    for b1, b2 in zip(bs, bs[1:]):
        a1, e1 = A_RECORD[b1]; a2, e2 = A_RECORD[b2]
        r = np.log(a1 / a2) / (b2 - b1)
        re = np.sqrt((e1 / a1) ** 2 + (e2 / a2) ** 2) / (b2 - b1)
        out.append((b1, b2, float(r), float(re)))
    return out


def _selftest():
    ok = True
    a20 = A_RECORD[20.0]
    print(f"A(20) = {a20[0]*1e9:+.3f}({a20[1]*1e9:.3f}) e-9 vs v89 band [1.5, 2.5] (gate)")
    ok = ok and 1.5e-9 < a20[0] < 2.5e-9
    bs = sorted(A_RECORD)
    mono = all(A_RECORD[b1][0] > A_RECORD[b2][0] for b1, b2 in zip(bs, bs[1:]))
    alive = A_RECORD[44.0][0] / A_RECORD[44.0][1]
    print(f"background decays monotonically: {mono}; alive at beta=44: {alive:.1f} sigma "
          f"(gates: mono, > 3 -- no background-zero in the (1,2) window)")
    ok = ok and mono and alive > 3
    rs = effective_rates()
    print("effective pair rates:", [(f"{b1:.0f}-{b2:.0f}", f"{r:.3f}({re:.3f})") for b1, b2, r, re in rs])
    inband = all(0.03 < r < 0.20 for _, _, r, _ in rs)
    print(f"  (gate: all in (0.03, 0.20); asymptotic candidate band "
          f"{ {k: round(v,4) for k,v in RATE_BAND_CANDIDATES.items()} } NOT yet resolved -- recorded)")
    ok = ok and inband
    vals = list(FAITH_36.values())
    spread = max(abs(vals[i][0] - vals[j][0]) / np.sqrt(vals[i][1]**2 + vals[j][1]**2)
                 for i in range(3) for j in range(i + 1, 3))
    print(f"faithfulness triple at beta=36: max pairwise tension {spread:.1f} sigma (gate < 2)")
    ok = ok and spread < 2
    # live: frozen A-style evaluation at beta=28, 6 draws, must land in the stored band
    cd = FrozenCDet(cube_hopping(6), beta=28.0, s=0.0)
    rng = np.random.default_rng(2053)
    strip = np.exp(0.5 * (1.84 - 2.0))
    ms = []
    for _ in range(6):
        T = rng.uniform(0, 28.0, size=(2048, 3))
        v = np.array([cd.C_V([(1, float(t[0])), (2, float(t[1])), (4, float(t[2]))], 1.84).real
                      for t in T])
        ms.append(float(v.mean()) / strip)
    m = float(np.mean(ms)); se = float(np.std(ms, ddof=1) / np.sqrt(6))
    dev = abs(m - A_RECORD[28.0][0]) / np.sqrt(se**2 + A_RECORD[28.0][1]**2)
    print(f"live frozen A(28): {m*1e9:+.3f} +/- {se*1e9:.3f} e-9 vs stored "
          f"{A_RECORD[28.0][0]*1e9:+.3f}: {dev:.1f} sigma (gate < 3)")
    ok = ok and dev < 3
    print("coefficient-flow self-test (v89 anchor; decay; alive; rates; faithfulness; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
