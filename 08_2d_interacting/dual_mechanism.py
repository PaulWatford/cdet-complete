"""Dual-mechanism hunt (v60): tau-interference CONFIRMED as the second component; anisotropy real
but insufficient; a ~10x closed-line enhancement remains unexplained (ring-closure hypothesis banked).

Following the v59 falsification, the hypothesis tested: the concentration law fails as a SINGLE
mechanism because two (or more) operate together. Three rounds, all freeze-then-predict or direct
variance accounting:

ROUND 1 -- more geometric variables (REJECTED): adding d_min, axis-alignment count, rank, and
  tau-gap to MST raises R2 only 0.178 -> 0.198 (all five combined). No second geometric variable.

ROUND 2 -- tau-interference as mechanism 2 (CONFIRMED): variance decomposition at fixed sites shows
  WITHIN-geometry (tau-only) fluctuation = 39% of total var(ln|C|) -- the v49 zero-crossing
  interference. Integrating tau out (regressing ln<|C|>_tau per geometry) DOUBLES the geometric law:
  R2 = 0.18 -> 0.48, slope -0.69. The per-sample scatter that buried v59's law was largely tau noise.
  BUT the frozen prediction of the tau-averaged class ratio still fails: predicted 8.7x vs measured
  75.5x at L=6. And the stratified 1d class exposed the anomaly: BODY-DIAGONAL lines (longest MST,
  5.20) are as heavy as AXIS lines (MST 3.00) and 3.4x heavier than face-diagonals -- weight does not
  follow Euclidean distance within the class.

ROUND 3 -- propagator anisotropy as mechanism 2b (REAL BUT INSUFFICIENT): measured decay lengths per
  Euclidean unit: xi = 0.90 (axis), 1.21 (face-diag), 1.20 (body-diag) -- diagonals decay ~35%
  slower, and one body-diagonal step carries almost the weight of one axis step. Folding this into an
  anisotropic decay-metric MST does NOT close the gap (R2 0.32; frozen prediction 6.8x vs 75.5x).

VERDICT: the dual structure is real -- (geometry) x (tau-interference) -- and accounting for it
doubles the explanatory power; but a persistent ~10x enhancement of CLOSED-LINE configurations over
the bulk survives every distance-based law. BANKED HYPOTHESIS (v61): on the torus the 1d lines are
closed RINGS (periodic 1d sub-chains with discrete spectra); ring-closure/winding coherence -- which
no tree/decay metric can express -- is the candidate third component. (Rhymes with the v41 shell
physics.) Untested; do not cite as a result.
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping


def variance_decomposition(cd, Lc, n_geom=60, n_tau=25, mu=0.5, beta=4.0, seed=5):
    """Share of var(ln|C|) that is WITHIN-geometry (tau-only), plus per-sample vs tau-avg R2 on MST."""
    from decay_law import mst_length
    co = lambda s: (s % Lc, (s // Lc) % Lc, s // (Lc * Lc))
    rng = np.random.default_rng(seed)
    all_ln, win, avg_ln, mst = [], [], [], []
    for _ in range(n_geom):
        sites = [int(rng.integers(Lc ** 3)) for _ in range(3)]
        vals = np.array([abs(cd.C_V([(s, float(rng.uniform(0, beta))) for s in sites], mu).real)
                         for _ in range(n_tau)])
        lv = np.log(np.maximum(vals, 1e-300))
        all_ln.extend(lv); win.append(lv.var())
        avg_ln.append(np.log(vals.mean())); mst.append(mst_length([co(s) for s in sites], Lc))
    all_ln = np.array(all_ln); avg_ln = np.array(avg_ln); mst = np.array(mst)
    share = np.mean(win) / all_ln.var()
    r_avg = np.corrcoef(mst, avg_ln)[0, 1] ** 2
    # per-sample R2: pair each tau draw with its geometry's MST
    per = np.repeat(mst, n_tau)
    r_per = np.corrcoef(per, all_ln)[0, 1] ** 2
    return share, r_per, r_avg


def anisotropy(cd, Lc, mu=0.5, beta=4.0, nsamp=300, seed=7):
    """Decay length per Euclidean unit along axis vs face-diagonal."""
    idx = lambda p: int(p[0] % Lc + Lc * ((p[1] % Lc) + Lc * (p[2] % Lc)))
    rng = np.random.default_rng(seed); out = {}
    for name, d in [("axis", (1, 0, 0)), ("face", (1, 1, 0))]:
        dv = np.array(d)
        kmax = int(np.floor((Lc / 2 - 0.01) / max(abs(x) for x in d)))  # wrap-safe: stay short of the antipode
        steps = list(range(1, max(kmax, 2) + 1))[:3]
        g = [np.mean([abs(cd.g0(0, idx(k * dv), float(rng.uniform(0, beta)), mu)) for _ in range(nsamp)])
             for k in steps]
        eu = np.array(steps) * np.linalg.norm(dv)
        out[name] = -1 / np.polyfit(eu, np.log(g), 1)[0]
    return out


def _selftest():
    Lc = 6; cd = FastCDet(cube_hopping(Lc), beta=4.0, to=0.7, ti=0.2)
    share, r_per, r_avg = variance_decomposition(cd, Lc)
    print(f"tau-interference share of var(ln|C|) = {share:.0%}   (mechanism 2; gate 15-65%)")
    print(f"MST law R2: per-sample {r_per:.2f}  ->  tau-averaged {r_avg:.2f}   (gate: averaged > per-sample)")
    cd8 = FastCDet(cube_hopping(8), beta=4.0, to=0.7, ti=0.2)   # anisotropy needs the longer wrap-safe range
    xi = anisotropy(cd8, 8)
    print(f"anisotropy (L=8): xi_axis={xi['axis']:.2f}  xi_face={xi['face']:.2f}   (gate: face > axis by >10%)")
    ok = (0.15 < share < 0.65) and (r_avg > r_per) and (xi['face'] > 1.10 * xi['axis'])
    print("dual-mechanism self-test (tau share, averaging gain, anisotropy):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
