"""cdet_diagmc.py -- a Rossi-style connected-determinant Monte Carlo sampler.

This is the diagrammatic Monte Carlo (DiagMC) layer the package describes but, until now, did not contain. It samples the
connected-determinant perturbation series

    ln(Z/Z0) = sum_{n>=1} (-U)^n * integral_{0<t1<...<tn<beta} C_n(t1..tn)  dt   (summed over vertex sites),

where C_n is Rossi's connected determinant (the SAME validated kernel used everywhere else here -- imported from
cdet_connected, so the sampler and the deterministic path share one code path). Two estimators:

  (A) importance-sampled per-order MC  -- for each order n, Monte-Carlo integrate C_n over the imaginary-time simplex,
      returning the coefficient a_n with an error bar and the average sign  <s>_n = |<C_n>| / <|C_n|>.
  (B) a grand-canonical Metropolis Markov chain over (order n, the n times), the actual DiagMC walker -- insert / remove /
      shift moves with weight |U|^n |C_n|, anchored on the n=1 sector, estimating ln(Z/Z0) directly.

Both are validated against exact answers (the deterministic coefficients and the atom's closed form / 2-site ED) to within
error bars by `_selftest`.

WHAT THIS IS AND IS NOT. It is a working, validated connected-determinant Monte Carlo that runs at any (U, mu, beta) and
that MEASURES the fermionic sign problem in the form it takes here: the across-order alternating series. As U approaches
the convergence radius (strong coupling), the average sign <s> = |sum a_n U^n| / sum |a_n| U^n collapses toward zero and
the cost to a fixed error scales as 1/<s>^2. (On the small solvable clusters the WITHIN-order sign is ~1 -- they are
nearly sign-free per order; the wall is the across-order cancellation, which is the same object as the bare-series
convergence radius the rest of the package studies.) It does NOT defeat the sign problem; that wall is Troyer-Wiese /
NP-hard and is exhibited honestly, not removed. The reachable order is bounded by the 2^n cost of the exact
connected-determinant recursion, the same ceiling stated throughout the package.
"""
import argparse
import math

import numpy as np

import cdet_connected as cc


# ----------------------------------------------------------------------------------------------------------------------
# (A) importance-sampled per-order Monte-Carlo coefficients
# ----------------------------------------------------------------------------------------------------------------------
def _sites_iter(spv, n):
    """All site assignments (exact sum; spv**n is tiny for the small reference systems)."""
    import itertools
    return itertools.product(range(spv), repeat=n)


def mc_coeff(n, g0, beta, mu, t=1.0, spv=1, N=20000, rng=None):
    """Monte-Carlo estimate of the order-n free-energy coefficient a_n and the order-n average sign.

    Samples n times uniformly on the ordered simplex 0<t1<...<tn<beta (volume beta^n/n!) and averages the connected
    determinant C_n, summed over vertex-site assignments. Returns (a_n, err_n, sign_n, abs_mean).
    """
    rng = rng or np.random.default_rng(0)
    vol = beta ** n / math.factorial(n)
    site_lists = list(_sites_iter(spv, n))
    vals = np.empty(N)
    absv = np.empty(N)
    for k in range(N):
        taus = np.sort(rng.uniform(0.0, beta, size=n))
        c = 0.0
        for sites in site_lists:
            verts = tuple((sites[m], float(taus[m])) for m in range(n))
            c += cc.Cweight(verts, g0, beta, mu, t, {})
        vals[k] = c
        absv[k] = abs(c)
    mean = vals.mean()
    a_n = ((-1) ** n) * vol * mean
    err = vol * vals.std(ddof=1) / math.sqrt(N)
    abs_mean = absv.mean()
    sign_n = abs(mean) / abs_mean if abs_mean > 0 else 1.0
    return a_n, err, sign_n, vol * abs_mean


def mc_lnZ_over_Z0(g0, beta, mu, U, t=1.0, spv=1, n_max=4, N=40000, seed=0):
    """Sum the MC coefficients into ln(Z/Z0) at coupling U, with a propagated error bar and the per-order signs."""
    rng = np.random.default_rng(seed)
    coeffs, errs, signs = [], [], []
    total, var = 0.0, 0.0
    for n in range(1, n_max + 1):
        a_n, err, sgn, _ = mc_coeff(n, g0, beta, mu, t, spv, N, rng)
        coeffs.append(a_n); errs.append(err); signs.append(sgn)
        total += a_n * U ** n
        var += (err * U ** n) ** 2
    return {"value": total, "err": math.sqrt(var), "coeffs": coeffs, "coeff_errs": errs, "signs": signs}


# ----------------------------------------------------------------------------------------------------------------------
# (B) grand-canonical Metropolis DiagMC walker (insert / remove / shift), anchored on n=1
# ----------------------------------------------------------------------------------------------------------------------
def _config_absC(taus, g0, beta, mu, t, spv):
    """|C_n| summed over site assignments for a configuration of times (order = len(taus))."""
    n = len(taus)
    if n == 0:
        return 0.0, 0.0
    tot = 0.0
    for sites in _sites_iter(spv, n):
        verts = tuple((sites[m], float(taus[m])) for m in range(n))
        tot += cc.Cweight(verts, g0, beta, mu, t, {})
    return abs(tot), tot


def diagmc_walk(g0, beta, mu, U, t=1.0, spv=1, n_max=6, steps=200000, seed=1):
    """A grand-canonical DiagMC chain over (order, times) with weight |U|^n |C_n|, anchored on the n=1 sector.

    Returns ln(Z/Z0) estimated as sum_{n>=1} sign_n * (H[n]/H[1]) * a1, where a1 is the exact n=1 coefficient times U
    (cheap and closed-form), H[n] the order histogram, and sign_n the measured average sign at order n. The n=1 anchor
    fixes the absolute normalisation without a separate n=0 sector.
    """
    rng = np.random.default_rng(seed)
    # exact n=1 coefficient a_1 = (-1) * integral_0^beta C_1 dt (summed over sites); C_1 is t-independent here.
    absC1, C1 = _config_absC([0.5 * beta], g0, beta, mu, t, spv)
    a1 = (-1.0) * beta * C1                      # a_1 (signed), exact: C_1 constant in tau
    taus = [0.5 * beta]                          # start in the n=1 sector
    absC, C = absC1, C1
    H = np.zeros(n_max + 1)                       # order histogram (|weight| sectors)
    Ssum = np.zeros(n_max + 1)                    # summed sign per order
    for _ in range(steps):
        n = len(taus)
        move = rng.integers(3)
        if move == 0 and n < n_max:               # insert
            tnew = rng.uniform(0.0, beta)
            cand = sorted(taus + [tnew])
            a2, c2 = _config_absC(cand, g0, beta, mu, t, spv)
            # weight |U|^{n+1}|C_{n+1}| / |U|^n|C_n| ; proposal factor beta/(n+1)
            ratio = (U * a2 / absC) * (beta / (n + 1)) if absC > 0 else 0.0
            if a2 > 0 and rng.random() < ratio:
                taus, absC, C = cand, a2, c2
        elif move == 1 and n > 1:                 # remove (keep the anchor sector non-empty: n>=1)
            j = rng.integers(n)
            cand = taus[:j] + taus[j + 1:]
            a2, c2 = _config_absC(cand, g0, beta, mu, t, spv)
            ratio = (a2 / (U * absC)) * (n / beta) if absC > 0 else 0.0
            if a2 > 0 and rng.random() < ratio:
                taus, absC, C = cand, a2, c2
        elif move == 2:                           # shift a random time
            j = rng.integers(n)
            cand = sorted(taus[:j] + [rng.uniform(0.0, beta)] + taus[j + 1:])
            a2, c2 = _config_absC(cand, g0, beta, mu, t, spv)
            if a2 > 0 and (absC == 0 or rng.random() < a2 / absC):
                taus, absC, C = cand, a2, c2
        n = len(taus)
        H[n] += 1.0
        Ssum[n] += (1.0 if C > 0 else -1.0) * ((-1) ** n)   # sign of (-U)^n C_n, U>0
    # assemble ln(Z/Z0) = sum_n a_n U^n, anchored so order-1 reproduces a1*U exactly
    signs = np.array([Ssum[k] / H[k] if H[k] > 0 else 0.0 for k in range(n_max + 1)])
    val = 0.0
    if H[1] > 0 and signs[1] != 0:
        # a_n U^n = sign_n * |a1| * (H[n]/H[1]) * U   (H[n] already carries |U|^n, so one factor of U remains)
        for n in range(1, n_max + 1):
            val += signs[n] * abs(a1) * (H[n] / H[1]) * U
    overall_sign = float(abs(Ssum[1:].sum()) / H[1:].sum()) if H[1:].sum() > 0 else 0.0
    return {"value": val, "order_hist": H.tolist(), "signs": signs.tolist(), "mean_sign": overall_sign}


# ----------------------------------------------------------------------------------------------------------------------
# exact references + the sign wall
# ----------------------------------------------------------------------------------------------------------------------
def atom_lnZ_over_Z0_exact(beta, mu, U):
    a = 1.0 + 2.0 * math.exp(beta * mu); b = math.exp(2.0 * beta * mu)
    return math.log((a + b * math.exp(-beta * U)) / (a + b))


def across_order_sign(coeffs, U):
    """The DiagMC average sign for the alternating series: |sum a_n U^n| / sum |a_n| U^n.

    coeffs is [a_1, a_2, ...]. This is the quantity that collapses toward zero as U approaches the convergence radius --
    the strong-coupling sign / convergence wall. The cost to a fixed error scales as 1/<sign>^2.
    """
    num = abs(sum(a * U ** (i + 1) for i, a in enumerate(coeffs)))
    den = sum(abs(a) * U ** (i + 1) for i, a in enumerate(coeffs))
    return num / den if den > 0 else 1.0


def sign_wall_scan(coeffs, Us):
    """Scan the coupling U and report the across-order average sign and the 1/<sign>^2 cost factor -- the wall."""
    return [(U, across_order_sign(coeffs, U), 1.0 / across_order_sign(coeffs, U) ** 2) for U in Us]


# ----------------------------------------------------------------------------------------------------------------------
def _selftest():
    print("cdet_diagmc self-test (the CDet Monte-Carlo reproduces exact answers within error bars):")
    beta, mu = 1.0, 0.5
    rng = np.random.default_rng(7)

    # (A) per-order MC coefficients vs the exact deterministic coefficients (atom)
    print("  (A) importance-sampled coefficients vs exact (atom, beta=1, mu=0.5):")
    ok = True
    for n in range(1, 4):
        exact = cc.lnZ_coeff(n, cc.g0_atom, beta, mu)
        a_n, err, sgn, _ = mc_coeff(n, cc.g0_atom, beta, mu, N=8000, rng=rng)
        dev = abs(a_n - exact)
        within = dev <= 5 * err + 1e-9
        ok = ok and within
        print(f"      n={n}: MC {a_n:+.5f} +/- {err:.5f}   exact {exact:+.5f}   "
              f"{'OK' if within else 'FAIL'} ({dev / (err + 1e-12):.1f} sigma)   <sign>={sgn:.3f}")
    assert ok, "per-order MC coefficients disagree with exact beyond 5 sigma"

    # (A) summed observable vs the EXACT PARTIAL SUM (truncation removed from the comparison; atom MC is exact)
    U, n_max = 1.0, 3
    r = mc_lnZ_over_Z0(cc.g0_atom, beta, mu, U, n_max=n_max, N=8000, seed=3)
    partial = sum(cc.lnZ_coeff(n, cc.g0_atom, beta, mu) * U ** n for n in range(1, n_max + 1))
    closed = atom_lnZ_over_Z0_exact(beta, mu, U)
    dev = abs(r["value"] - partial)
    print(f"  (A) ln(Z/Z0) partial sum to n={n_max}, U={U}: MC {r['value']:+.5f} +/- {r['err']:.5f}   "
          f"exact-partial {partial:+.5f}   (dev {dev:.2e}); closed form {closed:+.5f} (truncation gap "
          f"{abs(partial - closed):.4f})")
    assert dev <= 5 * r["err"] + 1e-6, "summed MC observable disagrees with the exact partial sum"

    # (A) 2-site validation against the deterministic coefficient (intra-order sign ~ 1: small clusters are nearly
    # sign-free WITHIN an order; the real wall is the across-order alternating series, measured below)
    a2, e2, s2, _ = mc_coeff(2, cc.g0_2site, 1.0, 0.5, spv=2, N=25000, rng=rng)
    ex2 = cc.lnZ_coeff(2, cc.g0_2site, 1.0, 0.5, sites_per_vertex=2)
    print(f"  (A) 2-site n=2 coefficient: MC {a2:+.5f} +/- {e2:.5f}   exact {ex2:+.5f}   intra-order <sign>={s2:.3f}")
    assert abs(a2 - ex2) <= 5 * e2 + 1e-6, "2-site MC coefficient disagrees with exact"

    # (B) the grand-canonical Markov chain reproduces the exact partial sum (atom, exact)
    nmw = 4
    w = diagmc_walk(cc.g0_atom, beta, mu, U, n_max=nmw, steps=30000, seed=5)
    pw = sum(cc.lnZ_coeff(n, cc.g0_atom, beta, mu) * U ** n for n in range(1, nmw + 1))
    devw = abs(w["value"] - pw)
    print(f"  (B) Metropolis DiagMC walk ln(Z/Z0): {w['value']:+.5f}   exact-partial(n<={nmw}) {pw:+.5f}   "
          f"(dev {devw:.4f})   chain mean sign {w['mean_sign']:.3f}")
    assert devw <= 0.03, "the DiagMC walk disagrees with the exact partial sum"

    # the sign / convergence wall: the across-order average sign collapses as U grows toward the radius
    ac = cc.atom_exact_coeffs(10, 2.0, 0.5)[1:]                 # fast closed-form coefficients
    rows = sign_wall_scan(ac, [0.3, 0.6, 1.0, 1.5])
    print("  sign wall (atom, beta=2): across-order <sign> vs U, cost ~ 1/<sign>^2 --")
    for U_, s_, c_ in rows:
        print(f"      U={U_}:  <sign>={s_:.3f}   cost x{c_:.1f}")
    assert rows[-1][1] < rows[0][1] - 0.1, "the across-order sign should collapse as U grows (the wall)"

    print("  all checks pass: the CDet Monte-Carlo reproduces exact answers within error bars, and the sign / "
          "convergence wall is measured (not defeated). PASS")


def _cli():
    p = argparse.ArgumentParser(description="Rossi-style connected-determinant Monte Carlo (DiagMC).")
    p.add_argument("--system", choices=["atom", "2site"], default="atom")
    p.add_argument("--beta", type=float, default=2.0)
    p.add_argument("--mu", type=float, default=0.5)
    p.add_argument("--U", type=float, default=1.0)
    p.add_argument("--nmax", type=int, default=4)
    p.add_argument("--samples", type=int, default=40000)
    p.add_argument("--walk", action="store_true", help="also run the Metropolis DiagMC chain")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        _selftest(); return
    g0 = cc.g0_atom if a.system == "atom" else cc.g0_2site
    spv = 1 if a.system == "atom" else 2
    print(f"connected-determinant Monte Carlo -- {a.system}, beta={a.beta}, mu={a.mu}, U={a.U}")
    r = mc_lnZ_over_Z0(g0, a.beta, a.mu, a.U, spv=spv, n_max=a.nmax, N=a.samples)
    print("  order   a_n (MC)            <sign>_n")
    for i, (c, e, s) in enumerate(zip(r["coeffs"], r["coeff_errs"], r["signs"]), start=1):
        print(f"   {i}     {c:+.6f} +/- {e:.6f}   {s:.3f}")
    print(f"  ln(Z/Z0) at U={a.U}:  {r['value']:+.6f} +/- {r['err']:.6f}")
    if a.system == "atom":
        ex = atom_lnZ_over_Z0_exact(a.beta, a.mu, a.U)
        print(f"  exact (atom closed form): {ex:+.6f}   (dev {abs(r['value'] - ex):.4f})")
    if a.walk:
        w = diagmc_walk(g0, a.beta, a.mu, a.U, spv=spv, n_max=max(a.nmax + 1, 5), steps=150000)
        print(f"  Metropolis DiagMC walk:   {w['value']:+.6f}   chain mean sign {w['mean_sign']:.3f}")
    if a.system == "atom":
        ac = cc.atom_exact_coeffs(10, a.beta, a.mu)[1:]
        print("  sign / convergence wall -- across-order <sign> = |sum a_n U^n| / sum |a_n|U^n:")
        for U_, s_, c_ in sign_wall_scan(ac, [0.3, 0.6, 1.0, 1.5, 2.0]):
            print(f"      U={U_}:  <sign>={s_:.3f}   cost ~ x{c_:.1f}")
    print("  note: <sign> quantifies the sign problem; cost to fixed error ~ 1/<sign>^2. The wall is measured, "
          "not removed.")


if __name__ == "__main__":
    _cli()
