"""rational_skeleton.py (v141) -- the live hint toward a rational Hubbard self-energy.

v140 found the bare self-energy series is NOT rational (no exact recurrence) and concluded the gravity-loop
15-digit resummation route does not transfer. That conclusion was for the GRAND-CANONICAL (fixed-mu) series,
and it missed something: the only non-rational ingredient there is the density nd(U), which drifts with U at
fixed mu. Hold the density FIXED and the structure becomes rational.

THE FINDING (atom, verified here). At fixed density n the self-energy is
    Sigma(U) = U n + U^2 n(1-n) / (iw + mu - U(1-n)),
a [2/1] rational function of U. Its Taylor coefficients satisfy an EXACT one-term (geometric) recurrence
    sigma_{k+1} = [(1-n)/(iw+mu)] * sigma_k     for k >= 2,
so the generating function is rational and a [2/1] closed form reproduces Sigma to machine precision (1.3e-15)
at ALL U -- past any bare-series radius. This is exactly the gravity-loop precondition (an exact linear
recurrence -> rational GF -> exact resummation), which v140 showed the grand-canonical series lacks.

WHY THIS IS THE HINT. The non-rationality is not intrinsic to the Hubbard self-energy; it is the
grand-canonical nd(U) dependence. The SKELETON / BOLD expansion -- Sigma as a functional of a FIXED propagator
(fixed density), the Prokof'ev-Svistunov bold-line / Luttinger-Ward object -- removes exactly that dependence.
So the rational / 15-digit-resummation route plausibly lives in the skeleton expansion, not the bare one. This
is a standing research lead, not yet a lattice result: the atom is rational at fixed density; whether the
lattice skeleton self-energy inherits a (higher-order but still finite) rational structure is the open question
to pursue.

SCOPE. Verified: the atom, at fixed density, is exactly rational (1-term recurrence, [2/1] exact). NOT yet
shown: the lattice skeleton self-energy is rational. This module is the bookmark + the verified atom anchor.
ED/closed-form is the anchor only; frozen engine untouched (194/194)."""
import numpy as np

def sigma_fixed_density(U, iwn, mu, n):
    """Atom self-energy at FIXED density n (the skeleton object): [2/1] rational in U."""
    return U * n + U**2 * n * (1 - n) / (iwn + mu - U * (1 - n))

def taylor_coeffs(f, nmax, r=0.3, M=2048):
    th = 2 * np.pi * np.arange(M) / M
    F = np.array([f(r * np.exp(1j * t)) for t in th])
    return np.array([np.sum(F * np.exp(-1j * k * th)) / (M * r**k) for k in range(nmax + 1)])

def geometric_ratio(iwn, mu, n):
    """The exact 1-term recurrence ratio sigma_{k+1}/sigma_k (k>=2) for the fixed-density atom."""
    return (1 - n) / (iwn + mu)

def _selftest():
    print("rational_skeleton self-test (the fixed-density self-energy is rational -- the live hint):")
    beta, mu, n = 5.0, 0.5, 0.40
    iwn = 1j * np.pi / beta
    sig = taylor_coeffs(lambda U: sigma_fixed_density(U, iwn, mu, n), 16)
    ratio = geometric_ratio(iwn, mu, n)
    # sigma_1 = n
    assert abs(sig[1] - n) < 1e-9, sig[1]
    # exact 1-term (geometric) recurrence for k>=2
    rec = max(abs(sig[k + 1] - ratio * sig[k]) for k in range(2, 15))
    assert rec < 1e-7, rec
    print(f"  exact 1-term recurrence sigma_(k+1) = [(1-n)/(iw+mu)] sigma_k (k>=2): worst dev {rec:.1e}")
    # [2/1] closed form exact at all U (past any bare radius)
    q1 = -sig[3] / sig[2]; p1 = sig[1]; p2 = sig[2] + sig[1] * q1
    err = max(abs((p1 * U + p2 * U**2) / (1 + q1 * U) - sigma_fixed_density(U, iwn, mu, n))
              for U in [0.6, 1.0, 1.5, 2.0, 3.0])
    assert err < 1e-12, err
    print(f"  [2/1] rational closed form vs exact, U up to 3 (past any bare radius): worst dev {err:.1e}")
    print("  => fixed-density (skeleton) self-energy IS rational: exact recurrence + closed form.")
    print("     The grand-canonical nd(U) was the only non-rational piece. The 15-digit route lives in the")
    print("     SKELETON / bold expansion -- the standing lead. (Lattice skeleton rationality: open.) PASS")

if __name__ == "__main__":
    _selftest()
