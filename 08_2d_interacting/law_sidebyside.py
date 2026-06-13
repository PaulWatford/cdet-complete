"""law_sidebyside.py (v94; STATUS REVISED v95) -- THE SIDE-BY-SIDE.
[v95 revision, degree_bound.py: the menu-vs-flatness tension below is DISSOLVED -- the corrected
menu contains 24/13 = 1.84615 (q = 13), 0.26 sigma from the constant reading, whose 1/(13 beta)
approach is nearly flat. The "degree bound 6" conjecture below was wrong (it is 7 = 2n+1), and
"13/7/15/8 removed structurally" does not happen. Status: open among {13/7, 24/13}, 11/6
disfavored.]
THE SIDE-BY-SIDE: both prediction surfaces updated with the v93
law (and the 13/7 competitor line), parity-locked, then tested out-of-sample against fresh
brute-force honest measurements with predictions FROZEN TO DISK before any scan ran.

THE SETUP. Surrogate side: surr_static_l6_deep_law/alt (C, ~ns) and the atlas mirrors
static_l6_deep_law/alt (Python) -- parity verified at 1e-15 across six betas inside the
csurrogate gate. Brute-force side: the honest multi-draw dense protocol (7-point grid, 4 draws
x NT=2048, inter-draw errors, in-window local quadratic + bootstrap). Frozen predictions
(written to disk first): law 11/6 + 2.67/(6b) -> z(44) = 1.8434, z(52) = 1.8419; competitor
13/7 - 3.21/(7b) -> z(44) = 1.8467, z(52) = 1.8483.

THE MEASUREMENTS:
    beta=30: z = 1.8138 +/- 0.0037  -- the SCOPE DEMONSTRATION: beta=30 is inside the v92
             crossover window (law floor beta ~ 36); both lines miss by >> 5 sigma, exactly as
             the scope says they must. (Also caught and fixed a harness bug: the quadratic's
             root selection must be restricted to the bracketing window.)
    beta=44: z = 1.8510 +/- 0.0076  -- law 1.0 sigma, competitor 0.6 sigma
    beta=52: z = 1.8527 +/- 0.0052  -- law 2.1 sigma, competitor 0.8 sigma

THE VERDICT (the six-point honest pool, beta = 36-56):
    out-of-sample only:      11/6 chi2 = 5.4 / 2, 13/7 chi2 = 1.0 / 2  -> ~9:1 for 13/7;
    v93 frozen test (36/40): ~80:1 for 11/6;
    NET: the v93 identification is REOPENED -- it does not survive out-of-sample.
    Six-point fits: 11/6 refit ln r = +3.11(50), chi2 4.79/5; 13/7 refit ln r = -2.98(58),
    chi2 1.58/5; CONSTANT a = 1.8467 +/- 0.0021, chi2 2.37/5. All acceptable; model selection
    indecisive. The constant reading puts the chord sqrt(2+sqrt2) at 0.5 sigma and BOTH menu
    rationals at 5-6.5 sigma -- in tension with the exponent-balance menu if z is truly flat.

THE DECISIVE THEORY QUESTION RAISED (queue head): the degree bound. v93 used weight <= 8 (4x4
matrices x 2 spins); but at order n = 3 each spin contributes THREE g0 factors, plausibly
bounding weights at <= 6 -- which would remove 13/7 and 15/8 from the menu structurally and put
the law itself in tension with a flat z. Re-derive the bound from the C_V structure; if weight
<= 6 holds and z stays flat at higher precision, the law needs a new term (or the chord needs a
mechanism the field theorem currently forbids). Freeze-then-predict did its job twice in a row:
first selecting 11/6 (v93), then unselecting it (v94).
"""
import numpy as np

FROZEN = {"law": {30: 1.848167, 32: 1.847240, 44: 1.843447, 52: 1.841891},
          "alt": {30: 1.841857, 32: 1.842813, 44: 1.846721, 52: 1.848319}}
NEW = {30.0: (1.8138, 0.0037), 44.0: (1.8510, 0.0076), 52.0: (1.8527, 0.0052)}
POOL6 = {36: (1.8450, 0.0030), 40: (1.8457, 0.0046), 44: (1.8510, 0.0076),
         48: (1.846, 0.009), 52: (1.8527, 0.0052), 56: (1.8407, 0.0103)}


def fits():
    B = np.array(sorted(POOL6)); Z = np.array([POOL6[b][0] for b in B])
    E = np.array([POOL6[b][1] for b in B])
    out = {}
    for nm, mu, q in (("11/6", 11 / 6, 6), ("13/7", 13 / 7, 7)):
        be = (Z - mu) * q * B; berr = E * q * B; w = 1 / berr**2
        bb = float(np.sum(w * be) / np.sum(w)); sb = float(1 / np.sqrt(np.sum(w)))
        out[nm] = (bb, sb, float(np.sum(((be - bb) / berr)**2)))
    w = 1 / E**2
    a = float(np.sum(w * Z) / np.sum(w)); sa = float(1 / np.sqrt(np.sum(w)))
    out["const"] = (a, sa, float(np.sum(((Z - a) / E)**2)))
    return out


def _selftest():
    ok = True
    c44l = abs(NEW[44.0][0] - FROZEN["law"][44]) / NEW[44.0][1]
    c44a = abs(NEW[44.0][0] - FROZEN["alt"][44]) / NEW[44.0][1]
    c52l = abs(NEW[52.0][0] - FROZEN["law"][52]) / NEW[52.0][1]
    c52a = abs(NEW[52.0][0] - FROZEN["alt"][52]) / NEW[52.0][1]
    chi_l, chi_a = c44l**2 + c52l**2, c44a**2 + c52a**2
    lr = float(np.exp((chi_l - chi_a) / 2))
    print(f"out-of-sample vs frozen: 11/6 chi2 {chi_l:.1f}, 13/7 chi2 {chi_a:.1f} -> "
          f"{lr:.0f}:1 for 13/7 (gates: chi_l > 4, chi_a < 2, LR in [4, 30])")
    ok = ok and chi_l > 4 and chi_a < 2 and 4 <= lr <= 30
    f = fits()
    print(f"six-point fits: 11/6 ln r {f['11/6'][0]:+.2f}({f['11/6'][1]:.2f}) chi2 "
          f"{f['11/6'][2]:.2f}/5; 13/7 ln r {f['13/7'][0]:+.2f}({f['13/7'][1]:.2f}) chi2 "
          f"{f['13/7'][2]:.2f}/5; const {f['const'][0]:.4f}({f['const'][1]:.4f}) chi2 "
          f"{f['const'][2]:.2f}/5 -- all acceptable: REOPENED (gates)")
    ok = ok and f["11/6"][2] < 11 and f["13/7"][2] < 11 and f["const"][2] < 11 \
        and abs(f["const"][0] - 1.8467) < 0.001
    chord = float(np.sqrt(2 + np.sqrt(2)))
    sc = abs(chord - f["const"][0]) / f["const"][1]
    s11 = abs(11 / 6 - f["const"][0]) / f["const"][1]
    print(f"under the constant reading: chord at {sc:.1f} sigma, 11/6 at {s11:.1f} sigma -- the "
          f"menu-vs-flatness tension (gate: sc < 1.5, s11 > 4)")
    ok = ok and sc < 1.5 and s11 > 4
    smin = min(abs(NEW[30.0][0] - FROZEN[k][30]) / NEW[30.0][1] for k in ("law", "alt"))
    print(f"scope demonstration at beta=30: nearest line {smin:.0f} sigma away (gate > 5 -- the "
          f"law floor at beta ~ 36 is real, both lines correctly inapplicable)")
    ok = ok and smin > 5
    print("side-by-side self-test (frozen scoring; six-point fits; tension; scope):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
