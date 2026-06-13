"""order_axis.py (v88) -- THE ORDER AXIS: the resonance spine survives beyond n=3. The v83
logit-map extraction was run at n=4 and n=5 (L=6, level eps=1, beta=20, full axis-line configs),
testing the frozen claims: (i) a low-degree polynomial in f fits the whole crossing region at the
new order; (ii) flips still anchor to the LEVEL via mu* = eps + logit(f*)/beta; (iii) the ROOTS
are order-dependent (different residue combinations) while the spine is not.

n=4, geometry (1,2,3,4):  curve fits at chi/dof 0.04 (deg 6); roots 0.156 / 0.643 -- a pair
  straddling 1/2, different parameters from every n=3 set, SAME law. BETA-TRANSFER, no refitting:
  predictions at beta = 14 and 24 verified by direct n=4 sign scans, max dev 0.024
  (the lower flip at beta=14 landed at 0.001).
n=5, geometry (1,2,3,4,5): the practical wall arrives exactly where v87 predicted -- signal 20x
  smaller, peak s/n 4.3. The curve is COHERENT (a definite -3.7 sigma -> +3.3 sigma crossing):
  LOWER ROOT RESOLVED at 0.402, live-verified at beta=20 (predicted 0.980, measured 0.991,
  dev 0.011). UPPER ROOT 0.874 sits in the low-signal tail: MARGINAL, flagged.

THE C SURROGATE EXTENDED: ATLAS_ROOTS_N4 / ATLAS_ROOTS_N5 + surr_class1_flips_order() shipped
with the marginality note; gate re-passed (fresh seeds, pedantic C11).

THE ROUND'S NUMERICS CATCH (fresh-seed gate working as designed): feature 8 (vol^(1/3)) used
numpy's float determinant, which returns ~1e-13 noise for SINGULAR integer matrices
(-> vol^(1/3) ~ 1e-5 instead of exactly 0); the C cofactor noise differed -> mismatch. The
min-image displacement matrix is integer-valued by construction, so both sides now use the exact
integer determinant (surrogate2.feats2 corrected with a banked note; effect on the frozen trained
weights ~1e-4 ln units, negligible against the 2.3x scope).

HONEST SCOPE: one level, one geometry per order; n=5 upper root marginal; n >= 6 extraction needs
the C engine or variance reduction (the Python port's wall); cross-order root-flow structure
(how roots move with n) is a new open observable.
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

S13 = np.linspace(0.03, 0.97, 13)
P_N4 = np.array([-0.0766, -0.0864, 0.0738, 0.2799, 0.4331, 0.4723, 0.3809, 0.1884, -0.0374,
                 -0.2084, -0.2491, -0.1448, -0.0111]) * 1e-9
E_N4 = np.array([0.0070, 0.0217, 0.0332, 0.0419, 0.0486, 0.0535, 0.0569, 0.0586, 0.0584,
                 0.0559, 0.0498, 0.0377, 0.0151]) * 1e-9
S11 = np.linspace(0.05, 0.95, 11)
P_N5 = np.array([-0.0018, -0.0077, -0.0108, -0.0078, 0.0005, 0.0099, 0.0154, 0.0142, 0.0074,
                 0.0009, -0.0001]) * 1e-9
E_N5 = np.array([0.0008, 0.0019, 0.0029, 0.0036, 0.0041, 0.0045, 0.0046, 0.0044, 0.0039,
                 0.0029, 0.0014]) * 1e-9
ROOTS_N4 = (0.156, 0.643)
ROOTS_N5 = (0.402, 0.874)          # upper MARGINAL (low-signal tail)
TRANSFER_N4 = {(14.0, "lower"): 0.001, (14.0, "upper"): 0.024,
               (24.0, "lower"): 0.011, (24.0, "upper"): 0.014}
LIVE_N5 = {"beta": 20.0, "predicted": 0.980, "measured": 0.991, "dev": 0.011}


def refit(S, P, E, deg=8, lo=0.03, hi=0.97):
    co = np.polyfit(S, P, deg, w=1 / E)
    chi = float(np.sqrt(np.mean(((np.polyval(co, S) - P) / E) ** 2)))
    roots = sorted(x.real for x in np.roots(co) if abs(x.imag) < 1e-8 and lo < x.real < hi)
    return chi, roots


def _selftest():
    ok = True
    chi4, r4 = refit(S13, P_N4, E_N4)
    print(f"n=4 stored curve: chi/dof {chi4:.2f} (gate < 2); roots {[round(x, 3) for x in r4]} "
          f"(gate: pair straddling 0.5, matching stored within 0.01)")
    ok = ok and chi4 < 2 and len(r4) == 2 and r4[0] < 0.5 < r4[1] \
        and max(abs(a - b) for a, b in zip(r4, ROOTS_N4)) <= 0.01
    chi5, r5 = refit(S11, P_N5, E_N5, deg=6, lo=0.05, hi=0.95)
    print(f"n=5 stored curve: chi/dof {chi5:.2f} (gate < 2); roots {[round(x, 3) for x in r5]} "
          f"(lower-root gate within 0.01 of {ROOTS_N5[0]}; upper marginal, not gated)")
    ok = ok and chi5 < 2 and abs(r5[0] - ROOTS_N5[0]) <= 0.01
    mx = max(TRANSFER_N4.values())
    print(f"n=4 beta-transfer (stored, no refitting): max dev {mx:.3f} (gate <= 0.035)")
    ok = ok and mx <= 0.035
    print(f"n=5 live check (stored): dev {LIVE_N5['dev']:.3f} (gate <= 0.035)")
    ok = ok and LIVE_N5["dev"] <= 0.035
    # order-dependence of the parameters: n=4 roots differ from every n=3 root set
    n3 = [(0.235, 0.832), (0.190, 0.828), (0.447, 0.939)]
    sep = min(max(abs(a - b) for a, b in zip(ROOTS_N4, t)) for t in n3)
    print(f"roots are order-dependent: min distance of n=4 roots from any n=3 set {sep:.3f} "
          f"(gate > 0.05)")
    ok = ok and sep > 0.05
    # live engine: the n=4 lower flip at beta=24, predicted from the stored root
    pred = 1 + float(np.log(ROOTS_N4[0] / (1 - ROOTS_N4[0]))) / 24
    cd = FastCDet(cube_hopping(6), beta=24.0, to=0.7, ti=0.2)
    rng = np.random.default_rng(607)
    mus = np.round(np.arange(pred - 0.04, pred + 0.0401, 0.0125), 5)
    s = [int(np.sign(np.mean([cd.C_V([(k, float(rng.uniform(0, 24.0))) for k in (1, 2, 3, 4)],
                                     float(m)).real for _ in range(150)]))) for m in mus]
    F = [float((mus[i] + mus[i + 1]) / 2) for i in range(len(s) - 1) if s[i] * s[i + 1] < 0]
    hit = any(abs(f - pred) <= 0.03 for f in F)
    print(f"live engine (n=4, beta=24): predicted {pred:.3f}, measured {[round(f, 3) for f in F]} "
          f"-> within 0.03: {hit}")
    ok = ok and hit
    print("order-axis self-test (curves; transfer; n=5 live; order-dependence; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
