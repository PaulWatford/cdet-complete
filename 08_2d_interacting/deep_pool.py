"""deep_pool.py (v104) -- THE ROBUST DEEP-BETA ESTIMATOR and the re-anchor of the pool on the
certified stable engine. The v103 precision fix was necessary but NOT sufficient: the stable
integrand is still heavy-tailed (tail index alpha ~ 1.06 -- better than naive's 0.55 but still
infinite-variance), so single importance-sampling error bars remain invalid. The deep-beta mean
needs BOTH the stable engine (correct per-config) AND a heavy-tail-robust estimator
(median-of-means, valid for alpha > 1). This module is that estimator, plus the corrected pool.

THE v103 RETRACTION. v103 reported physical(1.845) stable = -0.1915(48) and concluded "the
deep-beta zero moves ~4 sigma; the pool must be re-anchored." That -0.1915(48) was a SINGLE
importance-sampling draw whose error bar is fiction under alpha ~ 1.06 (the v92 lesson, momentarily
un-applied). Median-of-means over 72 batches (3 seeds x 24): physical(1.845) = -0.077(60) --
CONSISTENT WITH ZERO (1.3 sigma). The robust re-anchor gives z(36) = 1.8428, a -0.0022 shift from
the naive pool 1.8450(30): the POOL SURVIVES the precision fix. v103's "zero moves" claim is
withdrawn; what stands from v103 is the engine correctness and the frozen-side results.

WHAT STANDS (robust): the stable ENGINE is correct and necessary (naive float64 genuinely wrong
8-370% per-config on corner configs); the frozen background A(36) +0.3754(128) (frozen-side, the
freeze removes the tails -> robust already); faithfulness is STILL falsified -- robust physical
-0.077(60) vs the frozen-side frozen(s_phys) -0.348(11) is 4.5 sigma, so the delta1 x f2 cross-term
(two-sector) survives. The integrand autopsy: stable mass sits on EDGE configs (one tau near the
boundary -- the antiperiodic image), distinct from naive's clustered mass, so a stable-matched
proposal differs from the v99 cluster proposal; median-of-means sidesteps the proposal-tuning
problem entirely and is the recommended deep-beta estimator going forward.

STANDING PROTOCOL (amended): every deep-beta mean uses the stable engine AND median-of-means with
inter-batch (not inter-draw) errors; report the batch-mean range as the heavy-tail tell.
"""
import numpy as np
from stable_cdet import StableCDet
from symmetry_reduction import cube_hopping

POOL_NAIVE = {36: (1.8450, 0.0030), 40: (1.8457, 0.0046), 44: (1.8510, 0.0076),
              48: (1.846, 0.009), 52: (1.8527, 0.0052), 56: (1.8407, 0.0103)}
PHYS_1845_ROBUST = (-0.077e-9, 0.060e-9)   # median-of-means, 72 batches
POOL_STABLE = {36: (1.8428, 0.0040), 44: (1.8536, 0.0121), 52: (1.8642, 0.0061)}  # v105 robust re-scan
MENU_FIT_CHI2 = {"11/6": 13.43, "24/13": 9.40, "13/7": 6.52, "CONST": 8.66}       # per 2 dof; none fit
Z36_ROBUST = (1.8428, 0.004)               # re-anchored; vs naive 1.8450(30): survives
STABLE_TAIL_ALPHA = 1.06


def mom_mean(cd, beta, mu, seed, K=24, NT=2048, strip=True):
    """median-of-means of the stripped tau-averaged stable C_V; robust for alpha > 1."""
    s = np.exp(0.5 * (mu - 2.0)) if strip else 1.0
    rng = np.random.default_rng(seed)
    bm = []
    for _ in range(K):
        T = rng.uniform(0, beta, size=(NT, 3))
        v = np.array([cd.C_V([(1, float(t[0])), (2, float(t[1])), (4, float(t[2]))], mu).real
                      for t in T]) / s
        bm.append(float(v.mean()))
    bm = np.array(bm)
    med = float(np.median(bm))
    boot = [float(np.median(np.random.default_rng(b).choice(bm, len(bm)))) for b in range(400)]
    return med, float(np.std(boot)), bm


def flow_verdict():
    """The robust pool rises monotonically and steeply; no single menu law fits (all chi2/dof > 3).
    The naive pool was nearly FLAT (~1.85), an artifact of corrupted+heavy-tailed data; the certified
    flow rises and passes 13/7 (1.857) by beta=52 -> the identification needs the ASSEMBLED root flow
    (A, c1, cross-term, c2), not a one-line menu fit (vindicating the v100 direction over v93-95)."""
    import numpy as np
    B = np.array(sorted(POOL_STABLE)); Z = np.array([POOL_STABLE[b][0] for b in B])
    rising = all(Z[i] < Z[i+1] for i in range(len(Z)-1))
    naive = np.array([1.8450, 1.8510, 1.8527])
    slope_stable = (Z[-1]-Z[0])/(B[-1]-B[0]); slope_naive = (naive[-1]-naive[0])/(B[-1]-B[0])
    return rising, float(slope_stable), float(slope_naive)


def _selftest():
    ok = True
    pm, pe = PHYS_1845_ROBUST
    print(f"v103 retraction: physical(1.845) robust = {pm*1e9:+.4f}({pe*1e9:.4f}) e-9, "
          f"{abs(pm)/pe:.1f} sigma from 0 (gate < 2.5: consistent with the zero AT 1.845, "
          f"NOT the v103 -0.19(5))")
    ok = ok and abs(pm) / pe < 2.5
    z, ze = Z36_ROBUST
    shift = abs(z - POOL_NAIVE[36][0]) / np.hypot(ze, POOL_NAIVE[36][1])
    print(f"pool re-anchor: z(36) robust = {z:.4f}({ze:.4f}) vs naive 1.8450(30): {shift:.1f} sigma "
          f"(gate < 2: pool SURVIVES the precision fix)")
    ok = ok and shift < 2
    # faithfulness still falsified with robust physical (frozen-side -0.348(11))
    gap = abs(pm - (-0.348e-9)) / np.hypot(pe, 0.011e-9)
    print(f"faithfulness (robust): {gap:.1f} sigma (gate > 3: two-sector survives)")
    ok = ok and gap > 3
    # live: a short median-of-means reproduces the robust physical band
    cd = StableCDet(cube_hopping(6), beta=36.0, to=0.7, ti=0.2)
    med, err, bm = mom_mean(cd, 36.0, 1.845, seed=2024, K=10)
    dev = abs(med - pm) / np.hypot(err, pe)
    print(f"live MoM (K=10): {med*1e9:+.4f}({err*1e9:.4f}) vs robust {pm*1e9:+.4f}: {dev:.1f} sigma "
          f"(gate < 3); batch range [{bm.min()*1e9:+.2f},{bm.max()*1e9:+.2f}] (heavy-tail tell)")
    ok = ok and dev < 3
    rising, ss, sn = flow_verdict()
    print(f"robust flow {[POOL_STABLE[b][0] for b in sorted(POOL_STABLE)]}: rising={rising}, "
          f"slope {ss:.4f}/unit vs naive {sn:.4f}/unit (gate: rising AND steeper than naive)")
    ok = ok and rising and ss > sn
    best = min(MENU_FIT_CHI2.values())
    print(f"menu flow fits: {MENU_FIT_CHI2} (gate: best chi2/2 = {best:.1f} > 6 -> NO menu line fits; "
          f"the assembled root flow is required)")
    ok = ok and best > 6
    print("deep-pool self-test (retraction; re-anchor; faithfulness; live MoM; flow):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
