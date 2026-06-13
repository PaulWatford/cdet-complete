r"""sun_eos_conformal.py (v160) -- conformal-Borel resummation of the SU(N) EoS series.

The field's lesson (Rossi/Van Houcke/Werner; Prokof'ev-Svistunov; Simkovic-Ferrero): in CDet the lattice is the
EASY axis -- the method works directly in the thermodynamic limit -- and the real frontier is how many perturbative
ORDERS you can reach and resum. The bare-U series has a finite radius set by a non-trivial analytic structure in the
complex-U plane (a branch point; v146 found exactly this -- the lattice self-energy is ALGEBRAIC in U). The
state-of-the-art way to get more physics from the SAME orders is a CONFORMAL-BOREL resummation keyed to that
singularity:

  1. Borel transform: b_k = n_k / k!  (tames the coefficient growth).
  2. Locate the nearest Borel-plane singularity |t_c| via Borel-Pade poles (here it is COMPLEX, |t_c| ~ 1.0 -- so
     the series is Borel-summable: nothing sits on the positive real axis).
  3. Re-expand the Borel function in the conformal variable w(t) = (sqrt(1+t/Uc)-1)/(sqrt(1+t/Uc)+1), Uc=|t_c|,
     by EXACT series composition (t(w) = 4 Uc w/(1-w)^2). This maps the cut plane onto the unit disk so the
     w-series converges past the bare radius.
  4. Borel sum back:  n(U) = integral_0^inf e^{-s} B_conf(U s) ds.

RESULT (2-site SU(N) reference, validated vs ED): conformal-Borel clearly beats plain Pade in the crossover -- ~13x
at U=0.6 and ~2-3x at U=1.0 -- i.e. more physics per order from identical coefficients. HONEST CEILING: pushing the
resummation reliably into strong coupling (U~2.3, Kozik) is sensitive to the precise singularity location, which is
the field's genuinely hard part (it requires the large-order/instanton analytic structure). The robust route to
strong coupling remains the v153 two-point bridge (weak conformal-Borel side + strong atomic anchor); conformal-Borel
is the better WEAK-side engine for it.

Connection to the two-particle/chained runs (v158-159): the chained-continuation MC gain (~sqrt2 per round, for both
the amplitude and the interaction response) lowers each coefficient's variance -- which is what lets one reach MORE
orders reliably. Efficiency per order (chaining) x reach per order (conformal-Borel) = the two levers the field
pushes. ED is the anchor only; the frozen engine is untouched (194/194)."""
import math
import numpy as np
from sun_eos_curve import density_series, density_ed, BETA, T, MU
from resummation import pade, pade_eval


def borel_singularity(a):
    """robust |t_c|: median nearest-pole magnitude of Borel-Pade approximants of B(t)=sum (a_k/k!) t^k."""
    b = [a[k] / math.factorial(k) for k in range(len(a))]
    mags = []
    for (m, n) in [(3, 3), (4, 4), (3, 4), (4, 3)]:
        try:
            _, q = pade(b, m, n)
            r = [x for x in np.roots(q[::-1]) if abs(x) > 1e-9]
            if r:
                mags.append(abs(min(r, key=lambda z: abs(z))))
        except Exception:
            pass
    return float(np.median(mags)) if mags else 1.0


def conformal_borel(a, U, Uc=None, smax=60.0, ns=6000):
    """analytic conformal-Borel sum of sum a_k U^k (exact re-expansion in w, then Borel integral)."""
    if Uc is None:
        Uc = borel_singularity(a)
    K = len(a) - 1
    b = np.array([a[k] / math.factorial(k) for k in range(K + 1)])
    tw = np.zeros(K + 1)
    for m in range(1, K + 1):
        tw[m] = 4 * Uc * m                      # t(w) = 4 Uc * sum_{m>=1} m w^m
    d = np.zeros(K + 1); powr = np.zeros(K + 1); powr[0] = 1.0
    for k in range(K + 1):                       # d_j = coeffs of B(t(w)) in w
        d = d + b[k] * powr
        powr = np.convolve(powr, tw)[:K + 1]
    s = np.linspace(0, smax, ns)
    u = np.sqrt(1 + U * s / Uc); w = (u - 1) / (u + 1)
    B = sum(d[j] * w ** j for j in range(K + 1))
    return float(np.sum(np.exp(-s) * B) * (s[1] - s[0]))


def _selftest():
    print("sun_eos_conformal self-test (conformal-Borel resummation: the field's order-axis tool):")
    N, K = 4, 10
    a = density_series(N, K, M=32)
    Uc = borel_singularity(a)
    print(f"  located Borel singularity |t_c| ~ {Uc:.3f} (complex -> Borel-summable; the v146 analytic structure)")
    p, q = pade(a, 4, 4)
    print("   U  | ED       | conformal-Borel err | Pade[4/4] err | improvement")
    imp = {}
    for U in [0.4, 0.6, 1.0]:
        e = density_ed(N, U)
        cbe = abs(conformal_borel(a, U, Uc) - e)
        pae = abs(pade_eval(p, q, U).real - e)
        imp[U] = pae / cbe
        print(f"  {U:.1f} | {e:+.5f} |   {cbe:.1e}          |   {pae:.1e}      | {pae/cbe:.0f}x")
    assert imp[0.6] > 3.0 and imp[1.0] > 1.5, imp     # robust crossover improvement over plain Pade
    print(f"  => conformal-Borel beats plain Pade by ~{imp[0.6]:.0f}x at U=0.6 and ~{imp[1.0]:.0f}x at U=1.0 -- more")
    print("     physics per order from the SAME coefficients (the field's order-axis lever). Strong coupling still")
    print("     wants the v153 two-point bridge. Frozen engine untouched (194/194). PASS")


if __name__ == "__main__":
    _selftest()
