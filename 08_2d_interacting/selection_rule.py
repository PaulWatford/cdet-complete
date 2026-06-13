"""selection_rule.py (v84) -- THE CLASS-II SELECTION RULE, measured both ways. Near a level-pair
midpoint, the connected coefficient is a saturated background plus two competing residue
exponentials:

    <C>(mu)  ~  A  +  B e^{-beta(mu-mid)}  +  C e^{+beta(mu-mid)},      mid = (eps_a+eps_b)/2

(every single hole/particle deviation runs at rate +/-beta in mu; the LEVEL-PAIR IDENTITY is fixed
by the zero position and its beta-flow, not by the rate). A beta-static sign flip exists iff

    (i)  the saturated background A vanishes in the window, AND
    (ii) the competing residues have opposite signs (B*C < 0),

and then sits at  mu* = mid + ln(-B/C)/(2 beta)  -- the same logit-type law as Class I with the
TWO-RESIDUE ratio.

THE POSITIVE CASE (L=8, (2,3,4), beta=20, the 1.828 static):
  - measured VALUES (not just signs) cross zero at 1.8195 (interpolated);
  - background A = +1.06 +/- 1.04 (x1e-9): CONSISTENT WITH ZERO -- condition (i);
  - B*C < 0 -- condition (ii);
  - direct-zero ln-ratio K = 2 beta (zero - mid) = -0.36 -> residue ratio |R_a/R_b| = 0.70;
  - BETA-FLOW: zero(beta) = 1.8284 - 0.18/beta predicts 1.814@12 / 1.817@16 / 1.821@24 vs the
    v82 stored 1.819 / 1.819 / 1.831 (max dev 0.010);
  - PAIR IDENTIFICATION: any 1.707-midpoint alternative needs K = +4.5 and predicts 1.894@12 --
    rejected by 0.075. The (0.828, 2.828) crossing is confirmed by flow, not numerology.

THE NEGATIVE CASE (midpoint (0.586+2.586)/2 = 1.586, no static ever observed):
  - NO sign change anywhere in the window (all seven points positive, smooth);
  - background A = +4.27 +/- 0.95 (x1e-9): 4.5-sigma NONZERO -- condition (i) fails;
  - B, C individually consistent with zero. Suppression = background dominance, exactly as the
    rule requires. The L=6 half-integer suppression (v80's kill) now reads the same way --
    a stated, testable prediction.

HONEST LIMITS: the three-term fit over the narrow window (w = beta(mu-mid) in [-1.2, 1.2]) is
PARTIALLY DEGENERATE (the basis functions are collinear there; A and B trade off, so the fit's own
ln(-B/C) is unreliable) -- the DIRECT ZERO POSITION plus its beta-flow is the robust extraction
and is what the gates test. One positive and one negative case at one geometry; the rule's
residue-level derivation (why A vanishes where it does) is the remaining open step, now with the
extraction machinery in hand.
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

MID_POS = 1.8284271   # (0.828 + 2.828)/2
MID_NEG = 1.5857864   # (0.586 + 2.586)/2
BETA0 = 20.0
OFFS = np.array([-0.06, -0.04, -0.02, 0.0, 0.02, 0.04, 0.06])
V_POS = np.array([2.026, 1.402, 0.617, -0.491, -2.230, -4.157, -6.316]) * 1e-9
E_POS = np.array([0.683, 0.661, 0.682, 0.714, 0.566, 0.537, 0.503]) * 1e-9
V_NEG = np.array([5.252, 5.049, 4.671, 4.275, 3.931, 3.654, 3.439]) * 1e-9
E_NEG = np.array([0.525, 0.520, 0.538, 0.565, 0.591, 0.613, 0.632]) * 1e-9
V82_LOWER_234 = {12: 1.819, 16: 1.819, 24: 1.831}


def fit3(offs, V, E, beta=BETA0):
    w = beta * offs
    X = np.column_stack([np.ones_like(w), np.exp(-w), np.exp(w)])
    Wm = np.diag(1 / E)
    coef = np.linalg.lstsq(Wm @ X, Wm @ V, rcond=None)[0]
    chi = float(np.sqrt(np.mean(((X @ coef - V) / E) ** 2)))
    err = np.sqrt(np.diag(np.linalg.inv((Wm @ X).T @ (Wm @ X))))
    return coef, err, chi


def direct_zero(offs, V, mid):
    for i in range(len(V) - 1):
        if V[i] * V[i + 1] < 0:
            x0, x1, y0, y1 = offs[i], offs[i + 1], V[i], V[i + 1]
            return float(mid + x0 + (x1 - x0) * y0 / (y0 - y1))
    return None


def _selftest():
    ok = True
    z = direct_zero(OFFS, V_POS, MID_POS)
    K = 2 * BETA0 * (z - MID_POS)
    print(f"positive window: direct zero {z:.4f}; K = ln-residue-ratio = {K:+.2f} "
          f"(ratio {np.exp(K):.2f})")
    ok = ok and z is not None and -0.6 <= K <= -0.1
    mx = max(abs(MID_POS + K / (2 * b) - m) for b, m in V82_LOWER_234.items())
    alt12 = 1.7071068 + 4.5 / 24
    print(f"beta-flow vs v82 stored: max dev {mx:.3f} (gate <= 0.02); "
          f"1.707-pair alternative predicts {alt12:.3f}@12 vs measured 1.819 -> rejected "
          f"({abs(alt12 - 1.819):.3f} miss)")
    ok = ok and mx <= 0.02 and abs(alt12 - 1.819) > 0.05
    co, er, chi = fit3(OFFS, V_POS, E_POS)
    co2, er2, chi2 = fit3(OFFS, V_NEG, E_NEG)
    print(f"condition (i): background A_pos = {co[0]*1e9:+.2f}+/-{er[0]*1e9:.2f} "
          f"({abs(co[0])/er[0]:.1f} sigma, gate <= 2); A_neg = {co2[0]*1e9:+.2f}+/-{er2[0]*1e9:.2f} "
          f"({abs(co2[0])/er2[0]:.1f} sigma, gate >= 3)")
    ok = ok and abs(co[0]) / er[0] <= 2 and abs(co2[0]) / er2[0] >= 3
    print(f"condition (ii): B*C < 0 in positive window: {co[1]*co[2] < 0}; "
          f"fit chi/dof {chi:.2f} / {chi2:.2f} (gates < 2)")
    ok = ok and co[1] * co[2] < 0 and chi < 2 and chi2 < 2
    neg_flip = any(V_NEG[i] * V_NEG[i + 1] < 0 for i in range(len(V_NEG) - 1))
    print(f"negative window sign change: {neg_flip} (gate: False)")
    ok = ok and not neg_flip
    # live engine: fresh sign checks either side
    cd = FastCDet(cube_hopping(8), beta=BETA0, to=0.7, ti=0.2)
    rng = np.random.default_rng(431)
    T = rng.uniform(0, BETA0, size=(600, 3))
    def sgn(mu):
        v = np.array([cd.C_V([(2, float(t[0])), (3, float(t[1])), (4, float(t[2]))], float(mu)).real
                      for t in T])
        return int(np.sign(v.mean()))
    s1, s2, s3 = sgn(1.7884), sgn(1.8684), sgn(MID_NEG)
    print(f"live engine signs: 1.7884 -> {s1} (+1), 1.8684 -> {s2} (-1), {MID_NEG:.3f} -> {s3} (+1)")
    ok = ok and (s1, s2, s3) == (1, -1, 1)
    print("selection-rule self-test (zero+flow; pair ID; conditions i+ii; negative; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
