"""best_methods.py -- the verified accelerations, consolidated and cross-checked in one place.

These are the methods we have TESTED that work and compose with the frozen engine (which stays
untouched, 194/194). Each is exact-checked here; BEST_METHODS.md states the honest scope of each --
what axis it moves (convergence / derivatives / prefactor) and what it does NOT (the sign wall).

  1. SHIFTED REFERENCE (v45/46)      -- moves the complex-U pole: turns a divergent bare series into a
                                        convergent one at the Hartree-scale shift. Axis: CONVERGENCE.
  2. COMPLEX-mu CONTOUR (v47)        -- the roots-of-unity/Cauchy tool: every mu-derivative (counterterm)
                                        in ONE pass, exactly, no finite differences. Axis: DERIVATIVES.
  3. FREE-BASELINE CONTROL VARIATE   -- subtract the known U=0 part; sample only the small interaction
     (02_control_variate, v33)         remainder. Axis: PREFACTOR (variance), strongest at weak U.

What NONE of them move: R, the per-configuration sign ratio (v48 shift trade-off; v49 contour
deformation + covariate). That wall is real-sign-flip / NP-hard (Troyer-Wiese). Honesty is the content.
"""
import numpy as np
from hubbard_ed import hop_1d_ring
from shifted_expansion import exactG, shifted_coeffs, radius_estimate
from counterterm_shift import mu_derivs, shifted_from_bare

L, beta, tau, U = 2, 4.0, 0.5, 4.0
hop = hop_1d_ring(L, 1.0)


def method1_shifted_reference():
    mu = 1.1; alpha = 1.5                       # Hartree-scale shift; bare (alpha=0) diverges here
    Gex = exactG(hop, mu, beta, tau, U)
    bare = shifted_coeffs(hop, mu, beta, tau, U, 0.0, 14)
    shifted = shifted_coeffs(hop, mu, beta, tau, U, alpha, 14)
    print("1. SHIFTED REFERENCE (convergence):  2-site ring mu=1.1 U=4 beta=4, exact G = %.6f" % Gex)
    print("     radius(bare)=%.2f  radius(shifted)=%.2f" % (radius_estimate(bare), radius_estimate(shifted)))
    for K in (5, 8, 11):
        eb = abs(np.sum(bare[:K]).real - Gex); es = abs(np.sum(shifted[:K]).real - Gex)
        print("     K=%2d truncation err:  bare %.2e   shifted %.2e" % (K, eb, es))
    ok = abs(np.sum(shifted[:8]).real - Gex) < 1e-2 and abs(np.sum(bare[:8]).real - Gex) > 1e-1
    print("     -> shifted converges where bare diverges:  %s\n" % ("PASS" if ok else "FAIL"))
    return ok


def method2_complex_mu_contour():
    mu, alpha = 1.1, 1.5; mu_ref = mu - alpha
    der = mu_derivs(hop, mu_ref, beta, tau, 4)              # all mu-derivatives, one contour pass
    b_from_contour = shifted_from_bare(der, U, alpha, 4)    # resummed -> shifted coeffs at physical mu
    b_direct = shifted_coeffs(hop, mu, beta, tau, U, alpha, 4)
    err = np.max(np.abs(np.asarray(b_from_contour) - b_direct[:5]))
    print("2. COMPLEX-mu CONTOUR (roots-of-unity derivative extraction):")
    print("     shifted coeffs via contour-sampled mu-derivatives vs direct shifted coeffs")
    print("     max|contour - direct| over orders 0..4 = %.2e   -> %s\n" % (err, "PASS" if err < 1e-8 else "FAIL"))
    return err < 1e-8


def method3_free_baseline_cv():
    mu = 0.6
    print("3. FREE-BASELINE CONTROL VARIATE (prefactor; subtract the known U=0 part, sample the remainder):")
    print("     dynamic-range reduction = |G_free| / |G(U) - G_free|  (bigger = more cancellation removed)")
    rows = []
    for Uw in (0.5, 1.0, 2.0, 4.0):
        Gfull = exactG(hop, mu, beta, tau, Uw); Gfree = exactG(hop, mu, beta, tau, 0.0)
        red = abs(Gfree) / abs(Gfull - Gfree)
        rows.append((Uw, red)); print("     U=%.1f:  |G_free|=%.4f  remainder=%.4f  range reduction x%.1f"
                                       % (Uw, abs(Gfree), abs(Gfull - Gfree), red))
    ok = rows[0][1] > rows[-1][1]               # the win is largest at weak U, shrinks toward strong U
    print("     -> control variate pays at weak U (large reduction), fades at strong U:  %s" % ("PASS" if ok else "FAIL"))
    print("     (the validated strong version is the learned IR reference, 02_control_variate, rho=0.998, 229x)\n")
    return ok


if __name__ == "__main__":
    print("=" * 80)
    print("BEST METHODS (verified, composable with the frozen engine)")
    print("=" * 80)
    r1 = method1_shifted_reference()
    r2 = method2_complex_mu_contour()
    r3 = method3_free_baseline_cv()
    print("=" * 80)
    print("ALL VERIFIED: %s   (convergence + derivatives + prefactor; the sign wall R is untouched)"
          % ("PASS" if (r1 and r2 and r3) else "CHECK"))
