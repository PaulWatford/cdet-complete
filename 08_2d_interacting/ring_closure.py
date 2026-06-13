"""Ring-closure test (v61): the winding-phase hypothesis is FALSIFIED by a paired twist experiment --
and the unpaired version of the same experiment produced a 4x artifact first. Both are the result.

HYPOTHESIS (banked v60): the ~10x closed-line weight enhancement is ring-closure/winding coherence.
INTERVENTION: an ANTIPERIODIC twist along one axis -- |hopping| and all distances bit-identical
(sanity-checked), only the winding phase of loops along that axis changes. Frozen predictions:
distance laws say zero change; winding coherence says the twisted axis's lines are selectively
suppressed, and twisting y instead must MIRROR the effect onto y-lines.

WHAT HAPPENED (L=6, n=3, beta=4, mu=0.5):
  1. UNPAIRED first run (different tau draws per lattice): apparent x-line suppression 0.24x with
     y-lines at 0.74x -- looked like a clean 4x axis-selective effect.
  2. PAIRED rerun (SAME sites and SAME tau draws on every lattice; median of per-config ratios):
        class     twist-x/PBC   twist-y/PBC
        x-lines      0.93x         0.99x
        y-lines      1.14x         1.45x
        bulk         0.70x         0.73x
     No suppression. No mirror. The 4x was an UNPAIRED HEAVY-TAIL ARTIFACT -- the same estimator
     pathology documented since v58, caught by the paired design.
  3. VERDICT: the winding-phase form of ring closure is FALSIFIED -- maximally changing the closure
     phase leaves line weights within ~+/-40% and axis-blind. The ~10x line enhancement is
     CLOSURE-INDEPENDENT.

SURVIVING REFINED HYPOTHESIS (untested -- do not cite as result): 1d CHANNELING -- coherent
multi-bounce propagation along the line's short segments, which needs no winding and is therefore
twist-blind. Candidate v62 test: compare line configs against equally-compact NON-collinear configs
of identical MST in the decay metric.

LESSON (now thrice-earned): in heavy-tailed systems, PAIR every comparison -- same sites, same taus,
per-config ratios -- or the medians of independent samples will manufacture multi-x effects.
"""
import numpy as np
from slice_scaling import FastCDet


def cube_hop_twist(L, t=1.0, twist_axis=None):
    """Cubic torus hopping; if twist_axis is set, the wrap bonds on that axis get -t -> +t (APBC)."""
    co = lambda i: (i % L, (i // L) % L, i // (L * L))
    ix = lambda x, y, z: (x % L) + L * ((y % L) + L * (z % L))
    H = np.zeros((L ** 3, L ** 3))
    for i in range(L ** 3):
        x, y, z = co(i)
        for ax, d in [(0, (1, 0, 0)), (0, (-1, 0, 0)), (1, (0, 1, 0)),
                      (1, (0, -1, 0)), (2, (0, 0, 1)), (2, (0, 0, -1))]:
            nx, ny, nz = x + d[0], y + d[1], z + d[2]; sgn = 1.0
            if twist_axis == ax and ((ax == 0 and not 0 <= nx < L) or
                                     (ax == 1 and not 0 <= ny < L) or
                                     (ax == 2 and not 0 <= nz < L)):
                sgn = -1.0
            H[i, ix(nx, ny, nz)] += -t * sgn
    return H


def paired_ratio(cd_a, cd_b, configs, mu=0.5):
    """Median over configs of [tau-avg weight under cd_a] / [same under cd_b]; fully paired."""
    rs = []
    for sites, taus in configs:
        wa = np.mean([abs(cd_a.C_V(list(zip(sites, tt)), mu).real) for tt in taus])
        wb = np.mean([abs(cd_b.C_V(list(zip(sites, tt)), mu).real) for tt in taus])
        if wb > 0:
            rs.append(wa / wb)
    return float(np.median(rs))


def _selftest():
    Lc = 6; N = Lc ** 3; beta = 4.0
    rng = np.random.default_rng(13)
    idx = lambda p: int(p[0] % Lc + Lc * ((p[1] % Lc) + Lc * (p[2] % Lc)))
    def mk(axis, ng=14, NT=20):
        out = []
        for _ in range(ng):
            ks = rng.integers(1, Lc, 3)
            sites = [idx((int(a), 0, 0)) for a in ks] if axis == 0 else [idx((0, int(a), 0)) for a in ks]
            out.append((sites, [[float(rng.uniform(0, beta)) for _ in range(3)] for _ in range(NT)]))
        return out
    Hp = cube_hop_twist(Lc); Hx = cube_hop_twist(Lc, twist_axis=0)
    print("sanity |H_PBC| == |H_APBC-x| elementwise:", np.allclose(np.abs(Hp), np.abs(Hx)))
    ok = np.allclose(np.abs(Hp), np.abs(Hx))
    cdP = FastCDet(Hp, beta=beta, to=0.7, ti=0.2); cdX = FastCDet(Hx, beta=beta, to=0.7, ti=0.2)
    rx = paired_ratio(cdX, cdP, mk(0)); ry = paired_ratio(cdX, cdP, mk(1))
    print(f"paired median ratios under twist-x:  x-lines {rx:.2f}x   y-lines {ry:.2f}x")
    # gates: NO multi-x axis-selective suppression (both within [0.4, 2.5]) -- the falsification itself
    ok = ok and 0.4 < rx < 2.5 and 0.4 < ry < 2.5
    print("ring-closure self-test (winding-phase falsification reproduced):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
