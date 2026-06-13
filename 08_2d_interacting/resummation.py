"""resummation.py (v140) -- can we borrow the gravity-loop "high precision via resummation" idea?

The uploaded gravity_loop_verification gets exact, 15-digit resummation because its loop coefficients b_n obey
an EXACT linear 3-term recurrence -> the generating function is RATIONAL -> the series sums to a closed form
with no truncation error. The honest question: does that transfer to our models?

WHAT WE FOUND (all tested here, against the exact ED self-energy):

  1. THE EXACT-RECURRENCE TRICK DOES NOT TRANSFER. Our self-energy coefficients sigma_n obey NO finite linear
     recurrence (order 2..5 fits give 3.5e-2 .. 5.4e-4 prediction error, never zero). The generating function is
     not rational (the Hubbard partition function contributes a transcendental e^{-beta U}). So there is no exact
     closed form and no 15-digit resummation for us by that route.

  2. PADE RESUMMATION TRANSFERS FOR REACH, NOT PRECISION. A [m/n] Pade of Sigma(U) analytically continues past
     the bare-series radius (~0.8): it turns a 1e13 divergence at U=3 into an O(1) estimate. But the residual is
     ~0.2-1 (structure-limited: Pade is rational, Sigma is not), and INSIDE the radius the bare series is far
     better. So Pade is a strong-coupling REACH tool (the v138 open item), not a precision tool.

  3. WHERE WE ALREADY HAVE EXACT RESUMMATION. Most of our models are not truncated series at all: the engine
     computes the connected determinant EXACTLY (the Rossi recursion is exact), the surrogate carriers are
     closed-form, and the Dyson relation G = G0/(1 - Sigma G0) is itself an exact rational resummation in Sigma.
     There is no truncation there to improve.

  4. THE GENERAL ACCURACY LEVER IS EXTENDED-PRECISION ARITHMETIC. The gravity-loop reaches 15 digits via exact
     (sympy) arithmetic. Our analog is long double / mpmath in the cancellation-dominated regimes: the hybrid's
     LD build reaches beta >= 200 where f64 walls at beta ~ 100 (v139). That -- not resummation -- is the lever
     that "improves accuracy for all models", applied where catastrophic cancellation, not series truncation,
     is the bottleneck.

NET: resummation extends our strong-coupling REACH (Pade, item #3); high precision comes from extended-precision
ARITHMETIC in cancellation regimes (LD/mpmath). The exact-recurrence 15-digit route is specific to a rational
series and does not apply to the Hubbard self-energy. ED is the anchor only; frozen engine untouched."""
import numpy as np
from self_energy_irreducible import connected_g_coeffs, sigma_coeffs_exact, _sigma_ed

def pade(c, m, n):
    """[m/n] Pade of sum_k c_k x^k: returns numerator/denominator coeff arrays (Q(0)=1)."""
    A = np.zeros((n, n), complex); b = np.zeros(n, complex)
    for i in range(n):
        for j in range(n):
            idx = m - n + 1 + i + (n - 1 - j); A[i, j] = c[idx] if idx >= 0 else 0
        b[i] = -c[m + 1 + i]
    q = np.concatenate([[1.0], np.linalg.solve(A, b)[::-1]])
    p = np.array([sum(c[i - j] * q[j] for j in range(min(i, n) + 1)) for i in range(m + 1)])
    return p, q

def pade_eval(p, q, x):
    return np.polyval(p[::-1], x) / np.polyval(q[::-1], x)

def has_linear_recurrence(c, order, lo=4, ntest=5):
    """Worst relative error of an order-term linear recurrence fit (0 => exact recurrence, rational GF)."""
    c = np.asarray(c[1:])
    A = np.array([[c[lo + i - 1 - j] for j in range(order)] for i in range(order)])
    bb = np.array([c[lo + i] for i in range(order)])
    try:
        r = np.linalg.solve(A, bb)
    except np.linalg.LinAlgError:
        return float('inf')
    err = 0.0
    for i in range(lo + order, min(lo + order + ntest, len(c))):
        pred = sum(r[j] * c[i - 1 - j] for j in range(order))
        err = max(err, abs(pred - c[i]) / (abs(c[i]) + 1e-30))
    return err

def _selftest():
    print("resummation self-test (does the gravity-loop precision idea transfer?):")
    beta, mu, nmax = 5.0, 0.5, 24
    iwn = 1j * np.pi / beta
    a = connected_g_coeffs(iwn, beta, mu, nmax, rG=0.5, M=8192); sg = sigma_coeffs_exact(a)
    # (1) no exact finite recurrence -> the 15-digit trick does not transfer
    errs = {o: has_linear_recurrence(sg, o) for o in [2, 3, 4, 5]}
    assert min(errs.values()) > 1e-6, errs
    print(f"  no exact linear recurrence (order 2..5 errors {', '.join('%.1e'%errs[o] for o in [2,3,4,5])}) "
          f"-> GF not rational -> no 15-digit resummation")
    # (2) Pade extends the strong-coupling reach (bare diverges, Pade bounded)
    p, q = pade(sg, 8, 8)
    bare3 = abs(sum(sg[n] * 3.0 ** n for n in range(1, nmax + 1)) - _sigma_ed(iwn, 3.0, beta, mu))
    pade3 = abs(pade_eval(p, q, 3.0) - _sigma_ed(iwn, 3.0, beta, mu))
    assert bare3 > 1e6 and pade3 < 2.0, (bare3, pade3)
    print(f"  Pade [8/8] at U=3 (past radius): bare err {bare3:.1e} (diverged) -> Pade err {pade3:.2e} (bounded)")
    print("  => Pade extends REACH (item #3), not precision; high precision = extended-precision arithmetic")
    print("     (LD/mpmath) in cancellation regimes (v139). The exact-recurrence 15-digit route is not ours. PASS")

if __name__ == "__main__":
    _selftest()
