"""resonance_atlas.py (v85) -- THE CONSOLIDATION of the resonance-regime arc (v80-v84) into one
prediction surface, with the cross-component integration audit as its self-test. The arc:

  v80  THE TWO-REGIME LAW       thermal pi/beta winding (geometry-dependent offsets) crosses over
                                to a resonance regime: flips level-attracted (p = 0.025) and
                                geometry-independent (p = 0.013-0.041). The v77 "beta >= 12
                                unmeasurable" boundary RETRACTED. Empirical crossover at
                                beta * gap ~ 8-12.
  v81  THE PAIR LAW             Class-I flips converge to LEVELS two-sidedly, mu* = eps +/- c/beta.
  v82  THE TWO-CLASS STRUCTURE  the ln(deg)/2 candidate falsified at L=8; Class-II beta-STATIC
                                crossings at selected level-pair midpoints exposed.
  v83  THE RESIDUE RATIO        Class I derived: c = logit of residue-polynomial roots;
                                beta-transfer max 0.022; multiplicity = root count.
  v84  THE SELECTION RULE       Class II measured: static iff background ~ 0 AND opposite-sign
                                residues; mu* = mid + ln(-B/C)/(2 beta); pair identity by flow.

ONE SPINE: every resonance-regime flip is a logit-type law mu* = anchor + ln(ratio)/(q beta) --
Class I: anchor = a level, ratio = root odds f*/(1-f*), q = 1; Class II: anchor = a level-pair
midpoint, ratio = the two-residue ratio -B/C, q = 2. Residues decide attendance (root count;
the two conditions); positions are geometry-free, multiplicities are not.

THE INTEGRATION AUDIT (run as the self-test; all stored, plus one live check):
  A. roots(135) predict the stored v81 trajectories: lower <= 0.006 at every beta; upper <= 0.03
     except the v81-flagged beta=16 jitter outlier (0.066).
  B. roots predict the v80 beta=16 level-1-basin flips: <= 0.031 except the v83-flagged (1,2,3)
     edge root (0.061).
  C. selection-rule flow predicts the v82 static positions: <= 0.014.
  D. HONEST CATCH: the L=6 ~1.8 flip is UNCLASSIFIED -- its Class-I c drifts (3.1 -> 4.4), and
     1.8 is neither an L=6 half-integer (Delta-k=2) nor a third (Delta-k=3). Likely two conflated
     trajectories (the v81 window trap). On the open list, not swept under a law.

OPEN AFTER CONSOLIDATION: the background-zero derivation (why A vanishes where it does); the
unclassified L=6 ~1.8 object; root-derived parity-anchor channel engineering; carried items
(channeling c; PH quasi-exactness; the exact pi/beta constant).

v91 UPDATE (the v90 two-window correction propagated): the audit-catch object (gate D) is now
RESOLVED -- it is an ANCHORED, GEOMETRY-INDEPENDENT static (the third static-class instance):
z = 1.824(+/-0.022) - 0.72(+/-0.34)/beta, decided by a frozen cross-geometry discriminator (devs
0.001-0.011). The atlas gains the STATIC FAMILY (the L=8 flow static and the L=6 deep static)
and the corrected Class-I scope: the logit flow applies to mid-range roots; deep (small-f) roots
live at the cancellation floor where the polynomial tail is beta-dependent. Anchor identity open
(2*sqrt(2)-1 vs 11/6).
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping
import resonance_regime as _rr
import pair_law as _pl
import level2_structure as _l2
import residue_ratio as _rq
import selection_rule as _sr


class ResonanceAtlas:
    """The consolidated prediction surface for resonance-regime sign flips."""

    CROSSOVER_LO, CROSSOVER_HI = 8.0, 12.0   # empirical beta*gap window (v80)

    def __init__(self):
        self.roots = dict(_rq.ROOTS)             # L=6, level 1, per geometry
        z = _sr.direct_zero(_sr.OFFS, _sr.V_POS, _sr.MID_POS)
        self.static_K = 2 * _sr.BETA0 * (z - _sr.MID_POS)
        self.statics_l8 = sorted(_l2.STATICS_L8)
        self.l6_deep = (1.824, -0.72)   # v91 law; v92 SCOPE: beta in [10,32] only
        self.l6_deep_inf = 1.8437       # v92 honest measurement (beta 48-56, +/-0.0068)
        self.l6_deep_id = (11.0/6.0, 6, 2.67)  # v93: identified balance mu*=11/6, q=6, ln r (frozen test ~84:1)
        self.l6_deep_alt = (13.0/7.0, 7, -3.21)  # v94 competitor line (out-of-sample winner ~9:1)
        self.l6_deep_const = (1.8467, 0.0021)    # v94: the constant reading (chi2/dof 0.47)
        self.l6_deep_cand = (24.0/13.0, 13, 0.13)  # v95: the q=13 menu member -- the flat reading IS this

    def static_l6_deep_law(self, beta):
        mu, q, lnr = self.l6_deep_id
        return mu + lnr / (q * beta)

    def static_l6_deep_alt(self, beta):
        mu, q, lnr = self.l6_deep_alt
        return mu + lnr / (q * beta)

    def regime(self, beta, gap):
        x = beta * gap
        return "thermal" if x < self.CROSSOVER_LO else \
               ("crossover" if x < self.CROSSOVER_HI else "resonance")

    def class1_flips(self, geom, beta, eps=1.0):
        """Class-I predictions from stored residue-polynomial roots (L=6 level 1)."""
        return [eps + float(np.log(f / (1 - f))) / beta for f in self.roots[geom]]

    def class2_static(self, beta, mid=_sr.MID_POS):
        """The flow-corrected position of the measured L=8 static."""
        K = self.static_K if abs(mid - _sr.MID_POS) < 1e-6 else 0.0
        return float(mid + K / (2 * beta))

    def static_l6_deep(self, beta):
        """v91: the corrected L=6 deep-object law (anchored, geometry-independent; v90)."""
        a, b = self.l6_deep
        return float(a + b / beta)

    def predict(self, geom, beta):
        out = {"regime": self.regime(beta, 1.0), "class1_level1": self.class1_flips(geom, beta)}
        return out


def _selftest():
    ok = True
    atlas = ResonanceAtlas()
    # A. roots(135) vs stored v81 trajectories
    lo, up = atlas.roots["135"]
    cl, cu = np.log(lo / (1 - lo)), np.log(up / (1 - up))
    devs_l = [abs(1 + cl / b - m) for b, m in _pl.TRAJ_L6[("135", "lev1_lower")]]
    devs_u = [abs(1 + cu / b - m) for b, m in _pl.TRAJ_L6[("135", "lev1_upper")] if b != 16]
    print(f"A. roots->trajectories (135): lower max dev {max(devs_l):.4f} (gate <= 0.01); "
          f"upper max dev excl. flagged b16 {max(devs_u):.4f} (gate <= 0.03)")
    ok = ok and max(devs_l) <= 0.01 and max(devs_u) <= 0.03
    # B. roots vs v80 basin flips
    worst = 0.0
    for g in ("124", "135"):
        meas = [f for f in _rr.FLIPS_L6_B16[g] if 0.85 < f < 1.25]
        for f in atlas.class1_flips(g, 16):
            worst = max(worst, min(abs(f - m) for m in meas))
    print(f"B. roots->v80 basin flips (124/135): max dev {worst:.3f} (gate <= 0.035; "
          f"the 123 edge root excluded as v83-flagged)")
    ok = ok and worst <= 0.035
    # C. flow vs v82 statics
    mx = max(abs(atlas.class2_static(b) - F[0]) for b, F in _l2.LOWER_234.items() if b <= 24)
    print(f"C. flow->v82 statics: max dev {mx:.3f} (gate <= 0.02)")
    ok = ok and mx <= 0.02
    # D. the unclassified object is recorded
    cdrift = [(2 - m) * b for b, m in [(12, 1.744), (16, 1.756), (20, 1.806), (24, 1.769), (28, 1.844)]]
    print(f"D. unclassified L=6 ~1.8 object: c-drift {min(cdrift):.1f} -> {max(cdrift):.1f} "
          f"(non-constant confirmed; on the open list)")
    ok = ok and max(cdrift) - min(cdrift) > 0.8
    # E. regime classification consistency with v80 p-values
    cls = (atlas.regime(4, 1.0), atlas.regime(16, 1.0))
    print(f"E. regime(beta=4) = {cls[0]} (v80 p = 0.19), regime(beta=16) = {cls[1]} "
          f"(v80 p = 0.013-0.041) -- gates: thermal / resonance")
    ok = ok and cls == ("thermal", "resonance")
    # F. one live engine check: the (1,3,5) lower partner at beta=24, predicted from the root
    pred = atlas.class1_flips("135", 24)[0]
    cd = FastCDet(cube_hopping(6), beta=24.0, to=0.7, ti=0.2)
    rng = np.random.default_rng(367)
    mus = np.round(np.arange(pred - 0.04, pred + 0.0401, 0.0125), 5)
    s = [int(np.sign(np.mean([cd.C_V([(k, float(rng.uniform(0, 24.0))) for k in (1, 3, 5)], float(m)).real
                              for _ in range(100)]))) for m in mus]
    F = [float((mus[i] + mus[i + 1]) / 2) for i in range(len(s) - 1) if s[i] * s[i + 1] < 0]
    hit = any(abs(f - pred) <= 0.025 for f in F)
    print(f"F. live engine: predicted {pred:.3f}, measured {[round(f, 3) for f in F]} "
          f"-> within 0.025: {hit}")
    ok = ok and hit
    # G. (v91) the corrected deep-static law vs the v90 stored value-level zeros (its valid window)
    import creep_crosscheck as _cc
    devs = [abs(atlas.static_l6_deep(b) - z) for b, z in zip(_cc.BETAS, _cc.Z_124)]
    print(f"G. deep-static law vs v90 stored zeros (beta 10-28 window): max dev {max(devs):.3f} "
          f"(gate <= 0.025)")
    ok = ok and max(devs) <= 0.025
    # H. (v92) the honest deep-beta value vs the anchor-test HONEST record
    import anchor_test as _at
    devH = max(abs(z - atlas.l6_deep_inf) / e for z, e in _at.HONEST.values())
    print(f"H. honest deep-beta value (1.8437) vs the anchor-test honest record: max dev "
          f"{devH:.2f} sigma (gate <= 2)")
    ok = ok and devH <= 2
    # I. (v93) the identified exponent-balance law vs the full honest record
    import exponent_balance as _eb
    mu0, q0, lnr0 = atlas.l6_deep_id
    devI = max(abs(mu0 + lnr0/(q0*b) - z)/e for b,(z,e) in _eb.HONEST.items())
    print(f"I. exponent-balance law (11/6 + 2.67/(6 beta)) vs honest record: max dev "
          f"{devI:.2f} sigma (gate <= 1)")
    ok = ok and devI <= 1
    print("resonance-atlas integration audit (A-I):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
