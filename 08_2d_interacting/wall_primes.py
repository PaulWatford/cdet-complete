"""wall_primes.py (v174) -- prime lattice sizes and the convergence wall: a number-theoretic sieve.

v173 showed the wall U_c(L) is a tide whose finite-size error is the curvature of the susceptibility peak times the
distance from the true peak q* to the nearest grid momentum. That grid-miss distance is a DIOPHANTINE quantity -- how
well the rational grid {k/L} approximates q*/2pi -- so lattice SIZE enters through its number theory:

  * COMPOSITE L (many divisors) provide dense rational approximants near low-denominator commensurate momenta, so they
    can land a grid point almost on q*  -> small miss -> wall captured -> tiny error.
  * PRIME L (no divisors but 1 and themselves) are commensuration-blind: they cannot represent any low-denominator
    momentum, so they systematically miss q* -> ride the UPPER envelope of the tide -> largest error.

So jumping the lattice through primes traces the worst-case wall; the error anti-correlates with the divisor count of L.

QUANTIFIED (beta=5, mu=-0.6, peak q*=(0.783,1.000)pi):
  - prime L deviate ~2.7x more from the TD wall than composite L;
  - this holds even WITHIN odd L (so it is deeper than the v173 even/odd parity);
  - corr(#divisors(L), |U_c-U_inf|) ~ -0.4  (more divisors -> better capture);
  - the whole effect is the v173 curvature law: corr(grid-miss(L)^2, |U_c-U_inf|) ~ +0.96.

FILLING DEPENDENCE. The sieve is sharp when q* sits near a low-denominator commensurate vector (good rational targets to
approximate); at a generic-irrational peak no small L approximates well and prime vs composite washes out. Pure
Diophantine approximation. The frozen reference engine is untouched.
"""
import numpy as np
import wall_vs_size as _w


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def n_divisors(n):
    return sum(1 for d in range(1, n + 1) if n % d == 0)


def true_peak(mu, beta=5.0, L=90):
    """continuum peak momentum q* (in pi units) from a large, highly-composite lattice."""
    _, q = _w.chi0_max(L, beta, mu)
    return np.array([2 * q[0] / L, 2 * q[1] / L])


def grid_miss(L, qstar):
    """min distance (pi units) from q* to the LxL momentum grid -- the Diophantine grid-miss of size L."""
    g = 2 * np.arange(L) / L
    dx = np.min(np.abs(((g - qstar[0] + 1) % 2) - 1))
    dy = np.min(np.abs(((g - qstar[1] + 1) % 2) - 1))
    return float(np.hypot(dx, dy))


def analyze(mu, beta=5.0, Ls=None):
    """deviations of U_c(L) from the TD wall, split by primality / divisor count / grid-miss."""
    if Ls is None:
        Ls = list(range(16, 61))
    qstar = true_peak(mu, beta)
    uc = {L: _w.wall(L, beta, mu)[0] for L in Ls}
    uinf = float(np.mean([uc[L] for L in Ls[-10:]]))
    dev = {L: abs(uc[L] - uinf) for L in Ls}
    pr = [L for L in Ls if is_prime(L)]; co = [L for L in Ls if not is_prime(L)]
    return {
        "qstar": qstar, "uinf": uinf, "dev": dev,
        "prime_dev": float(np.mean([dev[L] for L in pr])),
        "comp_dev": float(np.mean([dev[L] for L in co])),
        "corr_ndiv": float(np.corrcoef([n_divisors(L) for L in Ls], [dev[L] for L in Ls])[0, 1]),
        "corr_miss2": float(np.corrcoef([grid_miss(L, qstar) ** 2 for L in Ls], [dev[L] for L in Ls])[0, 1]),
        "primes": pr, "composites": co,
    }


def _selftest():
    print("wall_primes self-test (prime lattice sizes vs the convergence wall -- a Diophantine sieve):")
    beta = 5.0

    a = analyze(-0.6, beta)
    print(f"  peak q* = ({a['qstar'][0]:.3f},{a['qstar'][1]:.3f})pi ; TD wall U_inf = {a['uinf']:.4f}")

    # (1) THE MECHANISM: deviation is the v173 curvature law on the grid-miss distance
    assert a["corr_miss2"] > 0.85, a["corr_miss2"]
    print(f"  [mechanism] corr(grid-miss^2, |U_c-U_inf|) = {a['corr_miss2']:+.2f}  (the v173 curvature law)")

    # (2) primes ride the upper envelope: deviate markedly more than composites
    ratio = a["prime_dev"] / a["comp_dev"]
    assert ratio > 2.0, ratio
    print(f"  [primes]    mean dev: primes={a['prime_dev']:.4f} vs composites={a['comp_dev']:.4f}  (x{ratio:.1f})")

    # (3) the divisor sieve: more divisors -> better capture
    assert a["corr_ndiv"] < -0.3, a["corr_ndiv"]
    print(f"  [sieve]     corr(#divisors(L), dev) = {a['corr_ndiv']:+.2f}  (composites capture; primes do not)")

    # (4) deeper than the v173 parity: holds WITHIN odd L
    odd = [L for L in a["dev"] if L % 2 == 1]
    op = np.mean([a["dev"][L] for L in odd if is_prime(L)]); oc = np.mean([a["dev"][L] for L in odd if not is_prime(L)])
    assert op > oc, (op, oc)
    print(f"  [parity-ctl] within ODD L: primes={op:.4f} > odd-composites={oc:.4f}  (beyond even/odd)")

    # (5) filling dependence: sharp near a low-denominator peak, washed out at a generic-irrational peak
    g = analyze(-2.8, beta)
    ratio_gen = g["prime_dev"] / g["comp_dev"]
    assert ratio_gen < 1.6 < ratio, (ratio_gen, ratio)
    print(f"  [Diophantine] sieve sharp at mu=-0.6 (x{ratio:.1f}) but washes out at generic peak mu=-2.8 (x{ratio_gen:.1f})")
    print("  => prime lattices are the worst-case wall samplers (commensuration-blind); the error is set by the")
    print("     Diophantine grid-miss to q* via the v173 curvature law. Frozen engine untouched. PASS")


if __name__ == "__main__":
    _selftest()
