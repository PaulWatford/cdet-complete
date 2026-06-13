"""Mechanism closure (v63): the two-coefficient law LOCKS the weight concentration within 1.27x.

THE RESIDUAL CHASE. After v62 the ledger read: distance + tau-interference + anisotropy + channeling
confirmed, winding falsified, and composing distance x (flat ~2x channeling) reached only ~16x of the
measured ~75x class gap. The chase asked: does channeling COMPOUND with length? It does -- the paired
line/bent ratio grows from ~1.6x at matched MST=3 to ~2.7x at MST=4 (c ~ +0.5 per unit length).

TWO METHODOLOGICAL TRAPS, CAUGHT ON THE WAY (both banked as lessons):
  1. SPURIOUS CREDIT: a first l_coll definition let a SINGLE vertex count as a "line" with the
     external, handing bulk configs channeling credit for their longest leg (double-counting
     distance). Channeling needs >=2 vertices sharing a direction.
  2. MULTICOLLINEARITY: in a joint fit ln W = a - b*MST + c*l_coll, the line family has
     l_coll == MST identically, so the regression cannot separate b from c (it zeroed c and inflated
     b). The cure is CLEAN IDENTIFICATION -- measure each coefficient where the other cannot
     contaminate it:
       b from BULK-ONLY regression (l_coll = 0 exactly; pure distance), and
       c from the PAIRED line/bent matched-MST contrast (distance cancels within each pair;
         c = median of ln(ratio)/delta_l_coll over pairs, identical tau draws per pair).

THE LOCKDOWN RESULT (L=6 cube, beta=4, mu=0.5, n=3; gate pre-set at 2x BEFORE the run):
    b (distance, bulk-only)              = 0.537   (R2 = 0.16; heavy tails, direction robust)
    c (channeling, paired contrast)      = +0.583 per unit collinear length   (n = 10 pairs)
    frozen composition at class medians (1d: MST 4.24, l_coll 4.24; bulk: MST 7.24, l_coll 0):
        exp(0.537 x 3.00 + 0.583 x 4.24) = 59x
    measured class ratio (v60 session, tau-averaged medians) = 75.5x
    agreement factor = 1.27  ->  LOCKED (within the pre-set 2x gate).

HONEST SCOPE: two coefficients identified on independent subsets and validated against ONE held-out
number; single lattice/order/mu/beta; b's R2 is low (the per-config scatter is the tau-interference
already quantified in v60); c rests on 10 matched pairs. This is a semi-quantitative mechanism law,
not a derivation from first principles -- the coefficients are measured, not predicted. What is now
closed: WHERE the universal concentration comes from (distance decay compounded with length-growing
1d channeling, modulated by tau-interference); what remains open: WHY c ~ 0.5-0.6 (a propagator
calculation nobody has done yet).
"""
import numpy as np
from slice_scaling import FastCDet
from channeling import families
from decay_law import mst_length
from symmetry_reduction import cube_hopping


def lcoll_line(sites, Lc):
    co = lambda s: (s % Lc, (s // Lc) % Lc, s // (Lc * Lc))
    return mst_length([co(s) for s in sites], Lc)


def lcoll_bent(sites, Lc):
    co = lambda s: (s % Lc, (s // Lc) % Lc, s // (Lc * Lc))
    xs = [co(s) for s in sites if co(s)[1] == 0 and co(s)[2] == 0]
    return mst_length(xs, Lc) if len(xs) >= 2 else 0.0


def identify_b(cd, Lc, n_bulk=40, NT=18, mu=0.5, beta=4.0, rng=None):
    """Distance coefficient from BULK-ONLY configs (l_coll = 0 exactly). Returns (b, R2)."""
    co = lambda s: (s % Lc, (s // Lc) % Lc, s // (Lc * Lc))
    X, Y = [], []
    while len(Y) < n_bulk:
        sites = [int(rng.integers(Lc ** 3)) for _ in range(3)]
        D = (np.array([co(s) for s in sites], float) + Lc // 2) % Lc - Lc // 2
        if np.linalg.matrix_rank(D) == 3:
            w = np.mean([abs(cd.C_V([(s, float(rng.uniform(0, beta))) for s in sites], mu).real)
                         for _ in range(NT)])
            Y.append(np.log(w)); X.append(mst_length([co(s) for s in sites], Lc))
    b = -np.polyfit(X, Y, 1)[0]
    return b, np.corrcoef(X, Y)[0, 1] ** 2


def identify_c(cd, Lc, NT=18, mu=0.5, beta=4.0, rng=None, per_key_cap=6):
    """Channeling coefficient from the PAIRED line/bent matched-MST contrast.
    Returns (c, n_pairs, per_key_ratio) -- per_key_ratio lets the compounding be checked."""
    pools = families(Lc)
    cs = []; per_key = {}
    for key in sorted(set(pools['line']) & set(pools['bent'])):
        ratios = []
        for sa, sb in list(zip(pools['line'][key], pools['bent'][key]))[:per_key_cap]:
            dl = lcoll_line(sa, Lc) - lcoll_bent(sb, Lc)
            if dl <= 0:
                continue
            taus = [[float(rng.uniform(0, beta)) for _ in range(3)] for _ in range(NT)]
            wa = np.mean([abs(cd.C_V(list(zip(sa, t)), mu).real) for t in taus])
            wb = np.mean([abs(cd.C_V(list(zip(sb, t)), mu).real) for t in taus])
            if wb > 0:
                cs.append(np.log(wa / wb) / dl); ratios.append(wa / wb)
        if ratios:
            per_key[key] = float(np.median(ratios))
    return float(np.median(cs)), len(cs), per_key


# class medians (geometry of the L=6 sampling protocol; see DECAY_LAW_RESULT / DUAL_MECHANISM_RESULT)
CLASS_MEDIANS_L6 = {"mst_1d": 4.24, "lcoll_1d": 4.24, "mst_bulk": 7.24, "lcoll_bulk": 0.0}
MEASURED_RATIO_L6 = 75.5  # tau-averaged class-median ratio, v60 session


def frozen_composition(b, c, med=CLASS_MEDIANS_L6):
    return float(np.exp(b * (med["mst_bulk"] - med["mst_1d"]) + c * (med["lcoll_1d"] - med["lcoll_bulk"])))


def _selftest():
    Lc = 6; cd = FastCDet(cube_hopping(Lc), beta=4.0, to=0.7, ti=0.2)
    rng = np.random.default_rng(35)
    b, r2b = identify_b(cd, Lc, rng=rng)
    print(f"b (distance, bulk-only, l_coll=0): {b:.3f}   R2={r2b:.2f}")
    c, npairs, per_key = identify_c(cd, Lc, rng=rng)
    print(f"c (channeling, paired matched-MST contrast): {c:+.3f}   (n={npairs} pairs)")
    ks = sorted(per_key)
    print(f"compounding check (per-key line/bent ratios): "
          + "  ".join(f"MST={k:.1f}: {per_key[k]:.2f}x" for k in ks))
    pred = frozen_composition(b, c)
    fac = max(pred, MEASURED_RATIO_L6) / min(pred, MEASURED_RATIO_L6)
    print(f"frozen composition = {pred:.0f}x   measured = {MEASURED_RATIO_L6}x   agreement factor = {fac:.2f}")
    compound_ok = len(ks) >= 2 and per_key[ks[-1]] > per_key[ks[0]]
    ok = (0.3 < b < 0.9) and (c > 0.25) and (fac < 2.0) and compound_ok
    print("mechanism-closure self-test (b, c identified cleanly; composition within the 2x gate; "
          "channeling compounds):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
