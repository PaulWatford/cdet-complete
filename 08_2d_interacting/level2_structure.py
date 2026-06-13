"""level2_structure.py (v82) -- the no-free-parameter test FIRED at L=8 level 2: the ln(deg)/2
candidate FAILS as a universal formula -- and the failure exposes the second mechanism class.
The resonance-regime flip set has TWO populations:

  CLASS I  (Delta-k = 1):  flight pairs  mu*_(+/-) = eps +/- c_eps/beta  converging to LEVELS
           (proved at L=6 level 1, v81; central pinned flips at the levels confirmed at BOTH L);
  CLASS II (Delta-k = 2):  beta-STATIC crossings at specific level-pair MIDPOINTS
           mu* = (eps_a + eps_b)/2  --  position beta-independent by construction (Delta-E/Delta-k).

THE FIRED PREDICTION AND ITS FAILURE. On record before measuring: if c = ln(deg)/2 universally,
L=8 level 2 (deg = 39 EXACTLY -- a Phase-0 catch: the hand-count said 63, the script said 39)
hosts a pair at 2 +/- 1.832/beta. Measured (windowed trajectories, grid 0.0125, NT=120,
beta 12-28, two geometries): NO such pair. The candidate is FALSIFIED AS UNIVERSAL; it stands as
the L=6-level-1 fit (0.4%) whose generality died on contact with new data -- exactly what a
no-free-parameter prediction is for.

WHAT THE DATA SHOWS INSTEAD (L=8, level-2 region):
  - lower window: a flip FLAT at ~1.82 across beta = 12-24 (std ~ 0.01) -- not in flight;
    1.828 = (0.828 + 2.828)/2: a Class-II static. This is also what the v80 "1.81 cluster" was.
  - central window: pinned flip at the level (2.05 -> 1.99 -> ~1.98, both geometries) -- the same
    central structure as L=6.
  - upper window: late-beta flips at ~2.09-2.12 and ~2.23-2.33, matching the statics
    2.121 = (1.414 + 2.828)/2 and 2.293 = (2 + 2.586)/2 within grid+jitter.
  - beta = 28 shows splitting (multiplicity noise), flagged; window-EDGE registrations (a flip
    landing on the final grid midpoint of a window) are a documented artifact class, excluded.

THE SELECTION-RULE PUZZLE (open, sharply posed): at L=6 the Class-II positions are half-integers
-- and v80's test KILLED them (p = 0.33): the statics are RESIDUE-SUPPRESSED at L=6 axis lines
while prominent at L=8. Which crossings actually flip = a sign condition on residue pairs;
lattice- and geometry-dependent. Deriving it joins the queue with the Class-I residue ratio.

HONEST SCOPE: level-2 region of L=8 + the v81 L=6 corpus; two geometries per measurement;
midpoint identifications within grid 0.0125 + flip jitter ~0.02; Class-I c-formula now OPEN
(ln(deg)/2 demoted to a one-level fit); upper-window statics appear only at large beta
(residue-weight thresholds, presumably).
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

# stored L=8 level-2-region trajectories (beta -> flips), grid 0.0125, NT=120
LOWER_234 = {12: [1.819], 16: [1.819], 20: [1.806], 24: [1.831], 28: [1.781, 1.819, 1.856]}
CENTRAL_234 = {12: [2.049], 16: [2.011], 20: [1.999], 24: [1.986], 28: [1.986]}
UPPER_134 = {24: [2.116, 2.229, 2.341], 28: [2.191]}
UPPER_234 = {16: [2.341], 24: [2.341], 28: [2.091, 2.329]}
STATICS_L8 = {1.828427: ("0.828+2.828", "/2"), 2.121320: ("1.414+2.828", "/2"),
              2.292893: ("2.000+2.586", "/2")}
DEG_L8_LEVEL2 = 39
FIRED_PREDICTION_C = float(np.log(39) / 2)   # 1.832 -- failed as universal


def _selftest():
    ok = True
    # 1. the static: flat across beta (Class II)
    prim = [v[0] for b, v in sorted(LOWER_234.items()) if b <= 24]
    sd = float(np.std(prim)); mid = 1.828427
    print(f"Class-II static at L=8: lower-window primary flips {prim}; std {sd:.3f} (gate <= 0.02); "
          f"mean {np.mean(prim):.3f} vs (0.828+2.828)/2 = {mid:.3f} (gate within 0.035)")
    ok = ok and sd <= 0.02 and abs(np.mean(prim) - mid) <= 0.035
    # 2. the fired prediction fails: no flip near 2 - 1.832/beta at beta = 16, 24
    miss = True
    for b in (16, 24):
        pred = 2 - FIRED_PREDICTION_C / b
        allf = LOWER_234.get(b, []) + CENTRAL_234.get(b, [])
        if any(abs(f - pred) <= 0.04 for f in allf):
            miss = False
    print(f"fired prediction (pair at 2 +/- ln(39)/2beta): no matching flip at beta = 16/24 -> "
          f"falsified-as-universal: {miss}")
    ok = ok and miss
    # 3. central pinned at the level
    cen = [v[0] for b, v in sorted(CENTRAL_234.items())]
    print(f"central flips {cen}: all within 0.06 of level 2: {all(abs(c - 2) <= 0.06 for c in cen)}")
    ok = ok and all(abs(c - 2) <= 0.06 for c in cen)
    # 4. upper statics match within tolerance where present (window-edge flips excluded:
    #    a flip registered within one grid step of the window boundary is a boundary artifact)
    HI = 2.35
    cand = [f for F in list(UPPER_134.values()) + list(UPPER_234.values()) for f in F
            if HI - f > 0.015]
    hits = sum(1 for f in cand if any(abs(f - m) <= 0.045 for m in STATICS_L8))
    print(f"upper-window flips (edge-excluded) matching a static midpoint within 0.045: "
          f"{hits}/{len(cand)} (gate >= half)")
    ok = ok and hits * 2 >= len(cand)
    # 5. live engine: the static reproduces at beta = 20
    cd = FastCDet(cube_hopping(8), beta=20.0, to=0.7, ti=0.2)
    rng = np.random.default_rng(373)
    mus = np.round(np.arange(1.77, 1.8801, 0.0125), 5)
    s = [int(np.sign(np.mean([cd.C_V([(k, float(rng.uniform(0, 20.0))) for k in (2, 3, 4)], float(m)).real
                              for _ in range(100)]))) for m in mus]
    F = [float((mus[i] + mus[i + 1]) / 2) for i in range(len(s) - 1) if s[i] * s[i + 1] < 0]
    hit = any(abs(f - 1.828) <= 0.035 for f in F)
    print(f"live engine (beta=20 window): flips {[round(f, 3) for f in F]} -> static within 0.035: {hit}")
    ok = ok and hit
    print("level2-structure self-test (static; falsification; central; midpoints; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
