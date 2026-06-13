"""learned_orientation.py (v73) -- the LEARNED orientation channel, attempted under the same frozen
discipline that killed every physics reduction: it fails too, for an identifiable structural reason.
The orientation channel is now CLOSED from both directions at this scope.

THE EXPERIMENT (surrogate-first; engine only for labels). Train on 9 cells (L=6; mu = 0.5, 1.0,
2.0; extent 3, 4, 5; 108 labeled line geometries), evaluate on ENTIRELY HELD-OUT cells: unseen
mu = 1.5 (all extents) AND unseen L = 4. Pre-set gate: >= 75% mean held-out accuracy -- the same bar
the physics ladder failed (best rung: chain, 64%).

TWO HYPOTHESIS CLASSES, SAME PROTOCOL, BOTH FAIL:
  L2-logistic on physics-informed features (ks, extent, mu, free filling n, trig in pi*n*k):
      train 74%, held-out mean 33% -- with consistent ANTI-prediction at unseen mu = 1.5
      (0% on one cell): the model interpolated the mu-trend smoothly between training fillings
      1.0 and 2.0, and the true orientation at 1.5 is anti-aligned with any smooth interpolant.
  Nonlinear MLP (24 hidden, harmonics m = 1, 2, pairwise interference features cos(pi n (k_i+-k_j))):
      train 74%, held-out mean 35%.

THE STRUCTURAL REASON: a PHASE WRAPS. Predicting orientation at an unseen mu requires the mu-period
of the wrap -- which is exactly the quantitative phase law that v69/v71 proved has no form below the
coupled two-spin engine integrand. The circle closes: to LEARN the channel across mu you need the
LAW; the law does not reduce. (The 74% train ceiling in both classes additionally indicates ~25%
in-distribution label-vs-feature mismatch at these sample sizes.)

THE ORIENTATION CHANNEL, CLOSED (at this scope), from both directions:
    derived:  parity 50-59% -> static 34% -> chain 64% -> full determinant 44%   (v68/69/71)
    learned:  linear-logistic 33% -> nonlinear MLP 35%                            (v73)
Remaining routes, named honestly: (i) dense mu-tabulation per target -- that is measurement, not
modeling; (ii) features computed from the engine integrand -- defeats the purpose; (iii) the
mu-period found analytically -- the open theory item. The surrogate's final boundary on orientation
is drawn and characterized.

HONEST SCOPE: axis lines, n=3, one beta, 12 geometries x 16 tau-draws per cell (some label noise
where r_g is small); two model classes tested -- not a proof over all learners, but the wrap
argument applies to any smooth interpolator over sparse mu samples.
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

BETA = 4.0


def measure_line_cell(Lc, mu, extent, n_geom=12, NT=16, seed=92, beta=BETA):
    cd = FastCDet(cube_hopping(Lc), beta=beta, to=0.7, ti=0.2)
    rng = np.random.default_rng(seed + 10 * extent + int(10 * mu) + Lc)
    AX = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    idx = lambda p: int(p[0] % Lc + Lc * ((p[1] % Lc) + Lc * (p[2] % Lc)))
    out = []
    for _ in range(n_geom):
        d = np.array(AX[rng.integers(3)])
        ks = [extent] + list(rng.choice(np.arange(1, extent), 2, replace=False))
        g = [idx(k * d) for k in ks]
        v = np.array([cd.C_V([(s, float(rng.uniform(0, beta))) for s in g], mu).real
                      for _ in range(NT)])
        out.append((sorted(ks), np.sign(v.mean())))
    return out


_NF = {}


def nfree(Lc, mu, beta=BETA):
    if (Lc, mu) not in _NF:
        w, _ = np.linalg.eigh(cube_hopping(Lc))
        _NF[(Lc, mu)] = float(np.mean(1 / (1 + np.exp(beta * (w - mu)))))
    return _NF[(Lc, mu)]


def featv(Lc, mu, ks):
    n = nfree(Lc, mu); k1, k2, k3 = ks
    f = [k1, k2, k3, k3, mu, n, k3 * n]
    for k in ks:
        f += [np.cos(np.pi * n * k), np.sin(np.pi * n * k)]
    return np.array(f, float)


def logistic_fit(X, y, lam=0.5, iters=200):
    Xb = np.column_stack([np.ones(len(X)), X]); w = np.zeros(Xb.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Xb @ w))
        g = Xb.T @ (p - y) + lam * np.r_[0, w[1:]]
        H = Xb.T @ (Xb * (p * (1 - p))[:, None]) + lam * np.eye(len(w)); H[0, 0] -= lam
        w -= np.linalg.solve(H + 1e-6 * np.eye(len(w)), g)
    return w


TRAIN_CELLS = [(6, m, e) for m in (0.5, 1.0, 2.0) for e in (3, 4, 5)]
HELDOUT_CELLS = [(6, 1.5, 3), (6, 1.5, 4), (6, 1.5, 5), (4, 0.5, 3), (4, 1.5, 3)]


def run_protocol(train_cells=TRAIN_CELLS, test_cells=HELDOUT_CELLS):
    rows = []
    for c in train_cells:
        for ks, s in measure_line_cell(*c):
            rows.append((c[0], c[1], ks, s))
    Xtr = np.array([featv(L, m, ks) for L, m, ks, s in rows])
    Ytr = np.array([s > 0 for L, m, ks, s in rows], float)
    mu_f = Xtr.mean(0); sd_f = Xtr.std(0) + 1e-9
    W = logistic_fit((Xtr - mu_f) / sd_f, Ytr)
    pred = lambda X: (1 / (1 + np.exp(-np.column_stack([np.ones(len(X)), (X - mu_f) / sd_f]) @ W))) > 0.5
    acc_tr = float(np.mean(pred(Xtr) == Ytr))
    accs = []
    for c in test_cells:
        d = measure_line_cell(*c)
        X = np.array([featv(c[0], c[1], ks) for ks, s in d])
        y = np.array([s > 0 for ks, s in d])
        accs.append(float(np.mean(pred(X) == y)))
    return acc_tr, accs


def _selftest():
    acc_tr, accs = run_protocol()
    print(f"learned channel (logistic): train {acc_tr:.0%}; held-out per cell "
          + " ".join(f"{a:.0%}" for a in accs) + f"; mean {np.mean(accs):.0%}")
    # gates REPRODUCE THE CLOSURE: pipeline works in-distribution (>65%) yet held-out FAILS the 75%
    # gate decisively (<60%) -- the wrap-interpolation failure
    ok = acc_tr > 0.65 and np.mean(accs) < 0.60
    print("learned-orientation self-test (channel closure reproduced: trains, does not transfer):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
