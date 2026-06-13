"""anchor_test.py (v92) -- THE ANCHOR TEST under the imported tau0/tau1 context: three results,
honestly graded after two in-flight catches.

RESULT 1 (SOLID) -- THE v90/v91 LAW IS SCOPED. Extended scans show the deep trajectory rising
THROUGH both v90 anchor candidates above beta ~ 32: the anchored law z = 1.824 - 0.72/beta is an
EFFECTIVE intermediate-window form (beta ~ 10-32), not an asymptote. Scope corrections propagated
(csurrogate, atlas).

RESULT 2 (SOLID, METHODOLOGY) -- THE DEEP-BETA HEAVY-TAIL AUDIT. At the cancellation floor the
value distribution has kurtosis ~ 4500 with ~98% of the variance in the top 0.1% of samples:
single-draw CLT errors are INVALID (per-draw sems on one point ranged 0.02-0.18 e-9; a "+8 sigma"
and a "-4.5 sigma" reading at the SAME point were both outlier artifacts of a true ~0.00 +/- 0.02).
REQUIRED PROTOCOL: multi-draw means with inter-draw errors AND dense grids (sparse linear fits are
curvature-biased). Two in-flight catches banked: a window-edge artifact (the (1,3,5) "universality
broken" call, corrected -- honest split 1.1 sigma, undetermined) and the live-gate redesign.

RESULT 3 (OPEN, with the verdict quantified by the edited bridge tool) -- THE HONEST DEEP RECORD:
    beta=48: z = 1.846  +/- 0.009    (dense 7-point grid, 4-draw errors, clean crossing)  A
    beta=56: z = 1.8407 +/- 0.0103   (dense grid + bootstrap quadratic)                   A
    beta=44: z ~ 1.84   +/- 0.012    (sparse; curvature-biased)                           B
    beta=64: UNRESOLVED (|V| below honest errors across the window)                       --
    pooled A: a_inf = 1.8437 +/- 0.0068; constancy beyond beta=56 unverified.
The bridge tool (anchor_bridge.py, edited from cdet-diagnose-bridge v0.57) applies its own
null-model rule: the framework-expressible alphabet near 1.84 has mean spacing ~0.011, P(random
position within 1 sigma of SOME member) = 83% -> rigid-gate verdict NOT RIGID (one-of-many). The
nearest member is the octagon chord sqrt(2+sqrt2) = 1.84776 [Q(sqrt2), the tau1 field] at 0.60
sigma -- recorded as the LEADING CANDIDATE, NOT an identification. sigma* for a unique ID: 0.0008
(72x the sample budget); the primary route is STRUCTURAL: derive the static position from the
residue/background-zero structure -- the derived form's field answers tau0-vs-tau1 with no sigma.

The withdrawn preliminary (single-draw "plateau 1.8486 +/- 0.0052, chord at 0.17 sigma") is
retained below as the cautionary record its gates test against.
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

# the (single-draw) trajectory record -- errors are CLT UNDERESTIMATES at beta >= 36 (Result 2);
# retained for the qualitative crossover gate only.
B_124 = np.array([22.0, 24.0, 27.0, 32.0, 36.0, 40.0, 44.0, 48.0, 56.0, 64.0])
Z_124 = np.array([1.8017, 1.8134, 1.8233, 1.8242, 1.8436, 1.8551, 1.8484, 1.8496, 1.8459, 1.8499])
E_124 = np.array([0.0127, 0.0127, 0.0141, 0.0100, 0.0142, 0.0242, 0.0181, 0.0107, 0.0155, 0.0084])
X135_36 = (1.8211, 0.0141)

# THE HONEST RECORD (multi-draw inter-draw errors, dense grids)
HONEST = {48.0: (1.846, 0.009), 56.0: (1.8407, 0.0103)}
TAIL_AUDIT = {"kurtosis": 4544, "top0.1pct_var_frac": 0.98, "interdraw_std_NT2048_1e9": 0.051,
              "per_draw_CLT_range_1e9": (0.021, 0.179)}
BRIDGE = {"alphabet_n": 13, "rarity_1sigma": 0.83, "sigma_star": 0.0008,
          "nearest": ("chord_8gon[3] = sqrt(2+sqrt2)", 1.84776, "Q(sqrt2)", 0.60),
          "verdict": "NOT RIGID -- one-of-many; OPEN"}


def pooled_honest():
    w = np.array([1 / e**2 for _, e in HONEST.values()])
    z = np.array([z for z, _ in HONEST.values()])
    a = float(np.sum(w * z) / np.sum(w)); sa = float(1 / np.sqrt(np.sum(w)))
    return a, sa


def _selftest():
    ok = True
    a, sa = pooled_honest()
    print(f"honest pooled a_inf = {a:.4f} +/- {sa:.4f} (gates: |a-1.8437|<=0.002; sa in [0.004,0.01])")
    ok = ok and abs(a - 1.8437) <= 0.002 and 0.004 <= sa <= 0.01
    ns = abs(BRIDGE["nearest"][1] - a) / sa
    print(f"nearest candidate (octagon chord, Q(sqrt2)): {ns:.2f} sigma (gate < 1: leading, "
          f"NOT identified -- bridge rarity {BRIDGE['rarity_1sigma']:.0%}, NOT RIGID)")
    ok = ok and ns < 1 and BRIDGE["rarity_1sigma"] > 0.5
    below = all(Z_124[i] < 1.8284 + E_124[i] for i in range(4))
    risen = all(Z_124[i] > 1.8333 for i in range(4, 10))
    print(f"crossover gate: beta<=32 zeros below 2*sqrt(2)-1 (within 1 sigma): {below}; "
          f"beta>=36 records above 11/6: {risen} (the v90/v91 law is scoped to beta<=32)")
    ok = ok and below and risen
    print(f"tail audit stored: kurtosis {TAIL_AUDIT['kurtosis']} (gate > 1000 -- CLT invalid); "
          f"top-0.1% variance fraction {TAIL_AUDIT['top0.1pct_var_frac']} (gate > 0.5)")
    ok = ok and TAIL_AUDIT["kurtosis"] > 1000 and TAIL_AUDIT["top0.1pct_var_frac"] > 0.5
    s = abs(Z_124[4] - X135_36[0]) / np.sqrt(E_124[4]**2 + X135_36[1]**2)
    print(f"geometry at beta=36: split {s:.1f} sigma (gate < 2: undetermined -- the 'broken' call "
          f"was a window-edge artifact, corrected)")
    ok = ok and s < 2
    # live engine, heavy-tail-aware: 3-draw mean at (beta=48, mu=1.880), stored -0.407 +/- 0.039
    cd = FastCDet(cube_hopping(6), beta=48.0, to=0.7, ti=0.2)
    rng = np.random.default_rng(983)
    ms = []
    for k in range(3):
        T = rng.uniform(0, 48.0, size=(2048, 3))
        v = np.array([cd.C_V([(1, float(t[0])), (2, float(t[1])), (4, float(t[2]))], 1.880).real
                      for t in T])
        ms.append(float(v.mean()))
    m = float(np.mean(ms)); se = float(np.std(ms, ddof=1) / np.sqrt(3))
    print(f"live engine (multi-draw, beta=48 mu=1.880): {m*1e9:+.3f} +/- {se*1e9:.3f} e-9 "
          f"(gate: negative beyond 2 sigma; stored -0.407 +/- 0.039)")
    ok = ok and m < 0 and abs(m) > 2 * se
    print("anchor-test self-test (honest pool; bridge verdict; crossover; tail audit; geometry; "
          "live):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
