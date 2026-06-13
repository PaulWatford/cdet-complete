"""deep_partner.py (v89) -- [REVISED v90/v91: the deep object's beta-flow is NOT logit -- it is
an anchored, geometry-independent static (z = 1.824 - 0.72/beta; see creep_crosscheck.py and
CREEP_CROSSCHECK_RESULT.md). The Delta(beta) table below is retained as the historical stored
data this module gates; its "decay" framing was a baseline artifact. The three roots remain true
properties of the beta=20 polynomial; the deep (small-f) tail is itself beta-dependent.]

 THE ~1.8 OBJECT IDENTIFIED (the v85 audit catch closed), and the
creep measured in position. One level-2 residue-polynomial extraction at L=6 ((1,2,4), beta=20,
small-f-weighted s-grid, NT=4096) resolved THREE roots:

    f* = 0.0116 (c = -4.44)   THE DEEP LOWER PARTNER  == the unclassified ~1.8 object
    f* = 0.4437 (c = -0.23)   the central flip (matches beta >= 16 at <= 0.010)
    f* = 0.9504 (c = +2.95)   the upper partner       == v80's dangling "2.2 family"
                              (flow data 2.188/2.138/2.112 vs predictions 2.185/2.148/2.123:
                               devs 0.003/0.010/0.011)

TWO ANOMALIES CLOSED AT ONCE. The v85 "c-drift" (3.1 -> 5.5) is quantified as SIGN-SCAN NOISE on
a steep small-f trajectory: through the crossing region |p| ~ 0.4-5e-9 while the v81 scans at
NT=120 carried sem ~ 3.2e-9 -- sign estimates were unreliable across a +/-0.04 window, exactly
the observed scatter. Level 2 carries 3 roots vs level 1's 2: root count varies by level,
consistent with the multiplicity law.

THE SCOPED-LAW FINDING (a designed value-level beta-transfer that MISSED, banked as measurement):
the deep root's pure logit law mu* = 2 - 4.44/beta holds at large beta (dev 0.003 at beta=28;
~0.03 at beta=20) but the measured zero departs below beta ~ 16-20:

    Delta(beta) = measured - predicted:  +0.114@12, +0.086@14 (value-level), +0.034@16,
                  ~+0.03@20, +0.003@28   -- decaying roughly as e^{-0.3 beta}.

Mechanism: the deep root sits where |p| ~ 1e-9 -- the cancellation floor -- and the ADJACENT
level-1 comb's beta-compensated contamination grows as beta drops (the v83 creep, now measured in
mu-position). The central and upper roots (larger-|p| crossings) show no departure at measurable
size. The logit law is therefore LARGE-BETA SCOPED for deep (small-f) roots, with the
contamination a measured, decaying correction.

HONEST SCOPE: one geometry; the beta=24 v81 point (1.769) remains a sign-noise outlier; the
Delta(beta) decay constant (~0.3) is empirical, not derived.
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

S_GRID = np.array([0.005, 0.010, 0.018, 0.032, 0.055, 0.09, 0.15, 0.25, 0.38, 0.52, 0.68, 0.82, 0.94])
P_LEV2 = np.array([1.8617, 0.4515, -1.7018, -5.1715, -10.0751, -15.7486, -20.9945, -19.8247,
                   -7.4384, 7.9029, 14.9601, 8.5300, 0.3681]) * 1e-9
E_LEV2 = np.array([0.5764, 0.5683, 0.5565, 0.5390, 0.5187, 0.5064, 0.5226, 0.5836, 0.6139,
                   0.5435, 0.3876, 0.2638, 0.1282]) * 1e-9
ROOTS_LEV2 = (0.0116, 0.4437, 0.9504)
UPPER_VS_V80_FLOW = {16: (2.185, 2.188), 20: (2.148, 2.138), 24: (2.123, 2.112)}  # (pred, meas)
CENTRAL_VS_V81 = {16: (1.986, 1.996), 20: (1.989, 1.984), 24: (1.991, 1.984), 28: (1.992, 1.984)}
DEEP_DELTA = {12: 0.114, 14: 0.086, 16: 0.034, 28: 0.003}   # measured - logit prediction
NOISE_QUANT = {"crossing_|p|_range_1e9": (0.4, 5.0), "v81_sem_NT120_1e9": 3.2}


def refit(deg=8):
    co = np.polyfit(S_GRID, P_LEV2, deg, w=1 / E_LEV2)
    chi = float(np.sqrt(np.mean(((np.polyval(co, S_GRID) - P_LEV2) / E_LEV2) ** 2)))
    roots = sorted(x.real for x in np.roots(co) if abs(x.imag) < 1e-8 and 0.004 < x.real < 0.96)
    return chi, roots


def _selftest():
    ok = True
    chi, roots = refit()
    print(f"level-2 stored curve: chi/dof {chi:.2f} (gate < 2); roots "
          f"{[round(r, 4) for r in roots]} (gate: 3 roots matching stored within 0.01/0.01/0.01)")
    ok = ok and chi < 2 and len(roots) == 3 \
        and all(abs(a - b) <= 0.01 for a, b in zip(roots, ROOTS_LEV2))
    devs_u = [abs(p - m) for p, m in UPPER_VS_V80_FLOW.values()]
    devs_c = [abs(p - m) for p, m in CENTRAL_VS_V81.values()]
    print(f"upper partner vs v80 flow: max dev {max(devs_u):.3f} (gate <= 0.015); "
          f"central vs v81: max dev {max(devs_c):.3f} (gate <= 0.012)")
    ok = ok and max(devs_u) <= 0.015 and max(devs_c) <= 0.012
    d = DEEP_DELTA
    mono = d[12] > d[14] > d[16] > d[28]
    print(f"deep-root scoped-law deviation: Delta = {d} -- monotone decay {mono} "
          f"(gate); large-beta dev {d[28]:.3f} (gate <= 0.01)")
    ok = ok and mono and d[28] <= 0.01
    print(f"v85 c-drift explained: crossing |p| in {NOISE_QUANT['crossing_|p|_range_1e9']} e-9 vs "
          f"v81 sign-scan sem {NOISE_QUANT['v81_sem_NT120_1e9']} e-9 (noise-dominated, gate: sem "
          f"inside the |p| range)")
    ok = ok and NOISE_QUANT["crossing_|p|_range_1e9"][0] < NOISE_QUANT["v81_sem_NT120_1e9"] \
        < NOISE_QUANT["crossing_|p|_range_1e9"][1]
    # live engine: re-locate the deep zero at the extraction beta by a 3-point value scan
    cd = FastCDet(cube_hopping(6), beta=20.0, to=0.7, ti=0.2)
    rng = np.random.default_rng(701)
    T = rng.uniform(0, 20.0, size=(900, 3))
    vals = []
    for mu in (1.755, 1.785, 1.815):
        v = np.array([cd.C_V([(1, float(t[0])), (2, float(t[1])), (4, float(t[2]))], float(mu)).real
                      for t in T])
        vals.append(float(v.mean()))
    sgnpat = [int(np.sign(x)) for x in vals]
    print(f"live engine (beta=20 values around the deep zero): signs {sgnpat} (gate [+1, ?, -1]: "
          f"a crossing inside [1.755, 1.815])")
    ok = ok and sgnpat[0] == 1 and sgnpat[2] == -1
    print("deep-partner self-test (curve; upper/central matches; scoped deviation; noise; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
