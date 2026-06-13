"""creep_crosscheck.py (v90, ledger #100) -- THE CREEP CROSS-CHECKED BOTH WAYS, as directed:
the surrogate side (law baselines + pattern arrangement) and the brute-force side (value-level
zero measurement) run independently and compared. The comparison REWRITES the v89 reading.

BRUTE FORCE (value-level deep-zero locations, L=6 (1,2,4), beta = 10..28, NT=1536):
    beta:   10      12      14      16      18      20      24      28
    z:      1.750   1.774   1.787   1.765   1.790   1.781   1.791   1.820   (+/- 0.013-0.035)
  Model selection: pure logit z = 2 + L/beta FAILS (chi/dof 2.90; fitted L = -3.29 contradicts
  the extracted -4.44); the ANCHORED form z = a + b/beta fits at chi/dof 0.53 with
        a = 1.824 +/- 0.022,   b = -0.72 +/- 0.34.
  (Phase-0 note: the v89 Delta(beta) "decay" was an artifact of defining Delta against a baseline
  extracted AT beta=20 -- Delta(20) ~ 0 by construction; the right object is z(beta) itself.)

SURROGATE SIDE (arrangement + selectivity):
  - anchor candidates: 1.8284 = 2*sqrt(2) - 1 (0.2 sigma) -- THE SAME NUMBER AS THE L=8 STATIC,
    at a lattice whose integer spectrum contains no sqrt(2): a possible L-INDEPENDENT anchor;
    11/6 = 1.8333 (0.4 sigma) -- an L=6 Delta-k rational. UNRESOLVED at +/-0.022; discrimination
    needs anchor error <= 0.005 (queued).
  - slope b: consistent with ~ -1 (ln-residue-ratio scale); differs from the L=8 static's -0.18
    by 1.6 sigma (residue ratios are geometry/L-dependent -- allowed).
  - selectivity: position sensitivity to contamination ~ 1/(|p'(f*)| f*(1-f*)) orders the roots
    deep (0.32) > upper (0.70 raw but large-|p| protected) >> central (0.04) -- why only the
    extreme roots feel the floor.

THE DISCRIMINATOR (frozen before measuring): a spectrum-anchored static must be
GEOMETRY-INDEPENDENT; a per-geometry logit root must not. (1,3,5) value scans at beta = 12/20/28:
    predicted (universal): 1.764 / 1.788 / 1.798
    measured:              1.7631 +/- 0.027 / 1.7889 +/- 0.018 / 1.7874 +/- 0.013
    devs:                  0.001 / 0.001 / 0.011        -> UNIVERSALITY WINS.

THE REVISION (banked openly, note added to DEEP_PARTNER_RESULT): the ~1.8 deep object is NOT a
Class-I logit-root trajectory -- it is an anchored, geometry-independent object of the static
class, now seen at L=6 where naive midpoints were excluded; the f* = 0.0116 root remains a true
property of the beta=20 polynomial, but the level-2 polynomial's deep tail is itself
beta-dependent (the creep contaminates the small-f extraction), which is exactly why the logit
flow failed.

OPEN: the anchor identity (2*sqrt(2)-1 vs 11/6 -- needs +/-0.005); the slope's residue formula;
whether the L=8 and L=6 anchors are literally one object (an L-independent anchor would be new
physics for this program).
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

BETAS = np.array([10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 24.0, 28.0])
Z_124 = np.array([1.7497, 1.7736, 1.7873, 1.7648, 1.7899, 1.7813, 1.7908, 1.8201])
E_124 = np.array([0.0186, 0.0215, 0.0233, 0.0201, 0.0353, 0.0138, 0.0170, 0.0233])
X_135 = {12.0: (1.764, 1.7631, 0.0269), 20.0: (1.788, 1.7889, 0.0179),
         28.0: (1.798, 1.7874, 0.0133)}   # (predicted-universal, measured, err)
ANCHOR_CANDS = {"2*sqrt(2)-1 (= L=8 static)": 2 * np.sqrt(2) - 1, "11/6": 11 / 6}


def fit_models():
    W = np.diag(1 / E_124)
    X2 = np.column_stack([np.ones_like(BETAS), 1 / BETAS])
    co2 = np.linalg.lstsq(W @ X2, W @ Z_124, rcond=None)[0]
    chi2 = float(np.sqrt(np.mean(((X2 @ co2 - Z_124) / E_124) ** 2)))
    er2 = np.sqrt(np.diag(np.linalg.inv((W @ X2).T @ (W @ X2))))
    X1 = (1 / BETAS).reshape(-1, 1)
    co1 = np.linalg.lstsq(W @ X1, W @ (Z_124 - 2), rcond=None)[0]
    chi1 = float(np.sqrt(np.mean(((X1 @ co1 + 2 - Z_124) / E_124) ** 2)))
    return (float(co1[0]), chi1), (float(co2[0]), float(co2[1]), float(er2[0]), float(er2[1]), chi2)


def _selftest():
    ok = True
    (L1, chi1), (a, b, ea, eb, chi2) = fit_models()
    print(f"model selection: logit chi/dof {chi1:.2f} (gate > 2 -- rejected); "
          f"anchored chi/dof {chi2:.2f} (gate < 1.5); a = {a:.3f}+/-{ea:.3f}, b = {b:+.2f}+/-{eb:.2f}")
    ok = ok and chi1 > 2 and chi2 < 1.5
    for name, v in ANCHOR_CANDS.items():
        ns = abs(v - a) / ea
        print(f"   anchor candidate {name} = {v:.4f}: {ns:.1f} sigma (both must stay open, gate <= 1.5)")
        ok = ok and ns <= 1.5
    devs = {b_: abs(p - m) for b_, (p, m, e) in X_135.items()}
    print(f"cross-geometry discriminator devs: {devs} (gates <= 0.015/0.015/0.025) -> universality")
    ok = ok and devs[12.0] <= 0.015 and devs[20.0] <= 0.015 and devs[28.0] <= 0.025
    # live engine: a fresh value pair bracketing the (1,2,4) deep zero at beta=12 -- the
    # high-signal case (bracket values ~ +/-5-10e-9 >> sem; the low-signal (1,3,5)@20 case is
    # heavy-tail under-sampled at modest NT and lives in the stored scans instead)
    cd = FastCDet(cube_hopping(6), beta=12.0, to=0.7, ti=0.2)
    rng = np.random.default_rng(829)
    T = rng.uniform(0, 12.0, size=(1100, 3))
    vals = []
    for mu in (1.705, 1.845):
        v = np.array([cd.C_V([(1, float(t[0])), (2, float(t[1])), (4, float(t[2]))], float(mu)).real
                      for t in T])
        vals.append(float(v.mean()))
    print(f"live engine (1,2,4) beta=12 bracketing values x1e9: "
          f"{[round(x * 1e9, 2) for x in vals]} (gate: +,-)")
    ok = ok and vals[0] > 0 > vals[1]
    print("creep-crosscheck self-test (model selection; anchor brackets; universality; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
