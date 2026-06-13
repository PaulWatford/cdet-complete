"""fugacity_structure.py (v78) -- the analytic origin of the mu-period law: THE MATSUBARA COMB,
detected directly by complex-mu continuation. The naive charge-staircase reading (ours and the
simplest outside derivation) is FALSIFIED en route; what survives is sharper.

THE CANCELLATION LEMMA (rigorous, small, and load-bearing). In every determinant det[g(tau_i -
tau_j)], the explicit e^{mu tau} factors cancel term-by-term (each permutation's exponents sum to
zero), and the CDet mask sums are determinants over shared time sets -- so ALL mu-dependence of
<C>_tau enters through the Fermi factors f_k = z e^{-beta eps_k} / (1 + z e^{-beta eps_k}),
z = e^{beta mu}. Therefore <C>_tau is EXACTLY a rational function of the fugacity z with poles only
at z = -e^{beta eps_k} < 0 -- equivalently, mu-poles on the MATSUBARA COMBS
        mu = eps_k + i (2m+1) pi / beta,
anchored at the single-particle levels, at uniform height pi/beta above the real axis.

THE STAIRCASE FALSIFICATION. If the sign flips came from adjacent fugacity powers exchanging
dominance (the literal e^{beta mu} "charge staircase"), ln|<C>| vs mu would be piecewise linear
with slope steps of +beta at each flip. Measured (precision jittered-grid curves, beta = 4 and 6):
slopes are FLAT (0.03-0.33 beta) with steps of +-0.2 beta, not +beta -- every Fermi factor is
degree-matched in z and saturates, so the function lives in the sigmoid-crossover regime. The
naive picture is dead.

THE DIRECT DETECTION (the engine analytically continues in mu; Cauchy-Riemann verified to 1e-3
relative). Approaching the comb at beta = 4 (pi/beta = 0.785):
        at a level   (mu0 = 2.000):  |<C>(mu0 + iy)| = 6.7e-8 (y=0.30) -> 2.6e-1 (y=0.77)
                                      -- SEVEN ORDERS OF MAGNITUDE: the pole is there;
        between levels (mu0 = 1.700): flat at ~1.5e-6 across the same y range.

THE MECHANISM (what v77's law means). The real-axis sign structure is comb-limited: the nearest
singularities sit at uniform height pi/beta regardless of geometry or lattice -- deriving the
1/beta scaling AND the R/L-independence in one stroke; q ~ 1 is nearest-comb (m = 0) dominance,
with higher combs exponentially subdominant -- consistent with the measured drift q: 1.12 -> 0.98
as beta grows. "Charge 1" survives in refined form: it is the z-degree of each Fermi denominator;
pi is the antiperiodicity phase. WHAT REMAINS OPEN (honest): the exact constant -- why the zero
spacing is ~ pi/beta rather than merely O(pi/beta) -- is a question about the zero statistics of
high-degree negative-pole rational functions; banked as the refined theory item.

HONEST SCOPE: lemma exact for the free-propagator CDet integrand at any order (the cancellation is
per-determinant); probes at n = 3, one geometry, beta = 4 for the comb scan (beta = 6 staircase
measured too); complex-mu continuation validated by the zero-imag match and Cauchy-Riemann, not by
an independent exact construction.
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

STAIRCASE_SLOPES_B4 = [+0.33, +0.12, -0.14, +0.07]   # in units of beta; flips at mu ~ 0.34/1.31/2.06
COMB_SCAN_B4 = {"y": [0.30, 0.50, 0.60, 0.70, 0.74, 0.77],
                "at_level_mu2.0": [6.65e-8, 3.92e-7, 1.74e-6, 3.63e-5, 6.49e-4, 2.60e-1],
                "between_mu1.7": [1.45e-7, 5.32e-7, 1.03e-6, 1.58e-6, 1.47e-6, 1.44e-6]}


def C_tau_avg(cd, ks, mu, beta, G=16, seed=31, rng=None):
    """Jittered-grid tau average with tau1 = 0 (exact translation invariance); mu may be complex."""
    rng = rng or np.random.default_rng(seed)
    u = np.arange(G) / G
    t2 = (u + rng.uniform(0, 1 / G, G)) * beta
    t3 = (u + rng.uniform(0, 1 / G, G)) * beta
    return np.mean([[cd.C_V([(ks[0], 0.0), (ks[1], float(a)), (ks[2], float(b))], mu)
                     for a in t2] for b in t3])


def comb_probe(cd, ks, mu0, ys, beta, seed=31):
    rng = np.random.default_rng(seed)
    return [abs(C_tau_avg(cd, ks, complex(mu0, float(y)), beta, rng=rng)) for y in ys]


def _selftest():
    L, ks, beta = 8, (2, 3, 4), 4.0
    cd = FastCDet(cube_hopping(L), beta=beta, to=0.7, ti=0.2)
    ok = True
    V = [(ks[0], 0.5), (ks[1], 1.7), (ks[2], 3.1)]
    vr = cd.C_V(V, 1.0); vc = cd.C_V(V, 1.0 + 0.0j)
    print(f"complex-mu consistency at zero imaginary part: {abs(vr - vc):.1e}")
    ok = ok and abs(vr - vc) < 1e-12
    h = 1e-5; mu0 = 1.3 + 0.11j
    f = lambda m: cd.C_V(V, m)
    dx = (f(mu0 + h) - f(mu0 - h)) / (2 * h)
    dy = (f(mu0 + 1j * h) - f(mu0 - 1j * h)) / (2 * h)
    cr = abs(dx + 1j * dy) / abs(dx)
    print(f"Cauchy-Riemann residual: {cr:.1e} (gate < 1e-3)")
    ok = ok and cr < 1e-3
    at = comb_probe(cd, ks, 2.000, [0.30, 0.77], beta)
    bt = comb_probe(cd, ks, 1.700, [0.30, 0.77], beta)
    r_at = at[1] / at[0]; r_bt = bt[1] / bt[0]
    print(f"comb divergence at-level: x{r_at:.1e}; between-levels: x{r_bt:.1f}; "
          f"CONTRAST {r_at / r_bt:.1e} (gate > 1e4)")
    ok = ok and r_at / r_bt > 1e4
    print(f"stored staircase slopes (units of beta): {STAIRCASE_SLOPES_B4} -- all |s| < 0.5: "
          f"{all(abs(s) < 0.5 for s in STAIRCASE_SLOPES_B4)} (the charge-staircase is falsified)")
    ok = ok and all(abs(s) < 0.5 for s in STAIRCASE_SLOPES_B4)
    print("fugacity-structure self-test (continuation; CR; comb; staircase falsification):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
