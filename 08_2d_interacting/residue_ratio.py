"""residue_ratio.py (v83) -- THE RESIDUE RATIO TIED DOWN. The Class-I flight constants are
derived: near a level eps at large beta,

    <C>_tau(mu) * e^{-(to-ti)(mu-eps)}  =  p( f_eps(mu) )        (the RESIDUE POLYNOMIAL)

with p a low-degree polynomial whose coefficients are tau-integrated residue combinations, and
since f(mu) = 1/(1+e^{beta(eps-mu)}):

    mu*_(flip)(beta) = eps + logit(f*) / beta,     f* = the roots of p in (0,1).

THE FLIGHT CONSTANTS c ARE LOGITS OF RESIDUE-POLYNOMIAL ROOTS. Everything in the resonance
regime's Class I follows: the pair = two roots straddling 1/2; the central pinned flip = a root
near 1/2; per-geometry MULTIPLICITY = the root count (residue-dependent); the beta-flow is the
logit map -- the polynomial itself is beta-independent.

THE EVIDENCE (L=6, level eps=1, beta=20 extraction; v80/v81 measurements as targets):
  1. STRUCTURE: the curve over the full crossing region fits a degree-4..6 polynomial in f at
     chi/dof ~ 1 (3-time object, NT=4096 common-random-times); a 2-time slice version fit to
     60x BELOW the noise floor. Lemma-grounded: all mu-dependence is through occupancies
     (v78 cancellation lemma), up to the smooth external e^{(to-ti)mu} factor (stripped).
  2. BETA-TRANSFER (the derivation-grade test): the polynomial extracted ONCE at beta=20
     predicts the (1,2,4) flip positions at beta = 12,16,20,24,28 with NO refitting:
     median |offset| = 0.014 (~one v81 grid step), max 0.023.
  3. MULTIPLICITY: (1,2,3) has a root at 0.447 (near 1/2) -> predicted central flip at 0.987
     (beta=16), measured 1.01; (1,2,4) and (1,3,5) have p(1/2) != 0 (10 sigma / 2.4 sigma) ->
     central flips correctly ABSENT.
  4. ROOTS: (1,2,4): 0.235 / 0.832 (c = -1.18 / +1.60); (1,3,5): 0.190 / 0.828
     (c = -1.45 / +1.57); (1,2,3): 0.447 / 0.939 (the 0.939 edge root carries inflated
     uncertainty -- its beta=16 prediction 1.171 vs measured 1.11 is the one marginal
     comparison, flagged).

WHERE RESIDUES CREEP IN (the honest mechanism finding): the naive single-level occupancy freeze
(SCDet: replace f_eps by a free s, freeze everything else at mu=eps) matches the direct curve
EXACTLY at s=1/2 and breaks down away from it -- even flipping sign -- because the connected
object sits at a ~1e-8 cancellation floor where the ADJACENT combs' exponentially-suppressed-
but-beta-compensated residues contribute at the same order. The polynomial must be extracted
through the direct curve via the logit map (which the lemma justifies); the failed shortcut is
documented as the boundary of the single-level truncation.

RETRO-CLEANUP: v81's fitted c's (-1.97/+1.79) were fit-basis artifacts (the r-offset/c trade in
linear-in-1/beta fits); the root logits are the fundamental constants and position-by-position
agreement is the honest comparison. The ln(36)/2 = 1.79 coincidence is resolved as accidental --
explaining v82's falsification.

HONEST SCOPE: one level (L=6, eps=1), three geometries, n=3, axis lines; extraction at beta=20
(adjacent-comb backgrounds ~e^{-beta gap} compensated -- at much smaller beta the polynomial
picture blurs into the thermal regime); the edge-root comparison marginal; Class II statics and
the selection rule remain separate open items.
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

EPS, BETA0 = 1.0, 20.0
S_GRID = np.linspace(0.03, 0.97, 17)
S_GRID13 = np.linspace(0.03, 0.97, 13)
# stored extracted curves (x 1e6), 3-time average, e^{-(to-ti)(mu-eps)} stripped
P_124 = np.array([0.0030, 0.0060, 0.0054, 0.0022, -0.0027, -0.0084, -0.0140, -0.0186, -0.0217,
                  -0.0226, -0.0211, -0.0173, -0.0115, -0.0045, 0.0022, 0.0066, 0.0062]) * 1e-6
E_124 = np.array([0.0002, 0.0003, 0.0004, 0.0005, 0.0007, 0.0008, 0.0009, 0.0010, 0.0011,
                  0.0011, 0.0012, 0.0012, 0.0012, 0.0011, 0.0009, 0.0008, 0.0007]) * 1e-6
ROOTS = {"124": (0.235, 0.832), "135": (0.190, 0.828), "123": (0.447, 0.939)}
V81_124 = {12: (0.879, 1.151), 16: (0.929, 1.114), 20: (0.954, 1.101),
           24: (0.954, 1.076), 28: (0.979, 1.064)}


def fit_residue_poly(S, P, E, deg=6):
    co = np.polyfit(S, P, deg, w=1 / E)
    chi = float(np.sqrt(np.mean(((np.polyval(co, S) - P) / E) ** 2)))
    roots = sorted(x.real for x in np.roots(co) if abs(x.imag) < 1e-8 and 0.03 < x.real < 0.97)
    return co, chi, roots


def predict_flips(roots, beta, eps=EPS):
    return [eps + float(np.log(f / (1 - f))) / beta for f in roots]


def _selftest():
    ok = True
    co, chi, roots = fit_residue_poly(S_GRID, P_124, E_124)
    print(f"stored (1,2,4) curve: chi/dof {chi:.2f} (gate < 2); roots {[round(r, 3) for r in roots]} "
          f"(gate: two roots straddling 0.5)")
    ok = ok and chi < 2 and len(roots) == 2 and roots[0] < 0.5 < roots[1]
    # beta-transfer gate
    mx = 0.0
    for b, meas in V81_124.items():
        pred = predict_flips(roots, b)
        mx = max(mx, max(abs(p - m) for p, m in zip(pred, meas)))
    print(f"beta-transfer (no refitting), max |pred - measured| over beta=12..28: {mx:.3f} (gate <= 0.035)")
    ok = ok and mx <= 0.035
    # multiplicity gate
    cen = {g: any(0.40 < r < 0.55 for r in R) for g, R in ROOTS.items()}
    print(f"central-root presence: {cen} (gate: 123 True, 124/135 False -- matches measured central flips)")
    ok = ok and cen["123"] and not cen["124"] and not cen["135"]
    # live engine: sign pattern (+,-,+) of the curve at s = 0.1 / 0.5 / 0.95 for (1,2,4)
    cd = FastCDet(cube_hopping(6), beta=BETA0, to=0.7, ti=0.2)
    rng = np.random.default_rng(411)
    T = rng.uniform(0, BETA0, size=(700, 3))
    sg = []
    for s in (0.10, 0.50, 0.95):
        mu = EPS + np.log(s / (1 - s)) / BETA0
        v = np.array([cd.C_V([(1, float(t[0])), (2, float(t[1])), (4, float(t[2]))], float(mu)).real
                      for t in T])
        sg.append(int(np.sign(v.mean())))
    print(f"live engine signs at s = 0.1/0.5/0.95: {sg} (gate: [+1, -1, +1] -- the two-crossing structure)")
    ok = ok and sg == [1, -1, 1]
    print("residue-ratio self-test (structure; beta-transfer; multiplicity; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
