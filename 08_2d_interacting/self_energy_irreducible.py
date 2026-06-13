"""self_energy_irreducible.py (v137 -- CORRECTS v136) -- integration #3, step 4: the EXACT irreducible
self-energy coefficients via the Dyson recursion, and an honest correction to the v136 radius claim.

WHAT v136 GOT WRONG. v136 extracted the self-energy coefficients sigma_n by a Cauchy contour on the ED
Sigma(U) at radius rS ~ 1.0-1.5, and claimed the 1PI series converges far past the connected-G radius R_G
(R_Sigma ~ 1.76, "2.2x larger"). That was an ARTIFACT: the contour at rS ~ 1.3 ENCLOSED Sigma's own
singularity (near |U| ~ 0.8), so the extracted numbers were NOT the Taylor coefficients -- they produced a
bounded-but-wrong (~1e-1) result that masqueraded as convergence. RETRACTED.

WHAT IS TRUE (this module). The EXACT sigma_n come from the Dyson coefficient recursion (no contour):
    a_n = connected-G coefficients (a_0 = G0);  sigma_n = a_n/G0^2 - (1/G0) * sum_{m=1}^{n-1} sigma_m a_{n-m}.
These reproduce the ED self-energy to 1.9e-9 at U=0.3 and 6e-5 at U=0.5 -- a correct, exact deliverable.
Their decay gives the TRUE radius:
    R_G     from |a_n|^(1/n)     ~ 0.73
    R_Sigma from |sigma_n|^(1/n) ~ 0.84
So R_Sigma ~ R_G: for the Hubbard atom there is **no significant convergence-radius advantage** of the 1PI
series over the connected-G series. (A marginal ~15% is within the asymptotic drift; nothing like 2.2x.)

WHAT THE SIMKOVIC-KOZIK ADVANTAGE ACTUALLY IS. Not a larger bare-series radius (at least not here). It is
(i) EFFICIENCY -- computing Sigma directly via the irreducible recursion avoids forming and inverting the full
connected G; and (ii) lower MC VARIANCE of the irreducible series. Reaching strong coupling past the
bare-series radius needs resummation (Pade / conformal mapping) or action-shift tricks, which apply to G and
Sigma alike. This corrects the v136 framing.

WHAT STILL STANDS (unaffected by this correction): z(inf) = the free addition pole (v133); the interacting
addition energy = eps + ReSigma, ED-verified (v134); the diagrammatic Sigma converges to ED within its radius
(v135). Those are correct. Only v136's radius-advantage claim is retracted.

ED is the anchor only; frozen engine untouched (194/194)."""
import numpy as np
from self_energy_diagrammatic import _G_matsubara_of_U

def connected_g_coeffs(iwn, beta, mu, nmax, rG=0.5, M=4096):
    """a_n: U^n coefficients of the connected G(iwn;U), contour inside R_G (well-conditioned)."""
    th = 2 * np.pi * np.arange(M) / M
    G = np.array([_G_matsubara_of_U(np.zeros((1, 1)), mu, beta, iwn, rG * np.exp(1j * t)) for t in th])
    return np.array([np.sum(G * np.exp(-1j * n * th)) / (M * rG ** n) for n in range(nmax + 1)])

def sigma_coeffs_exact(a):
    """EXACT self-energy coefficients via the Dyson recursion (no contour proxy)."""
    nmax = len(a) - 1; G0 = a[0]; sig = np.zeros(nmax + 1, complex)
    for n in range(1, nmax + 1):
        sig[n] = a[n] / G0 ** 2 - sum(sig[m] * a[n - m] for m in range(1, n)) / G0
    return sig

def _sigma_ed(iwn, U, beta, mu):
    return (iwn + mu) - 1.0 / _G_matsubara_of_U(np.zeros((1, 1)), mu, beta, iwn, U)

def _radius(coeffs, ns):
    return [1.0 / abs(coeffs[n]) ** (1.0 / n) for n in ns]

def _selftest():
    print("self_energy_irreducible self-test (CORRECTED v137): exact Dyson-recursion sigma_n + honest radius")
    beta, mu, nmax = 5.0, 0.5, 20
    iws = [1j * (2 * k + 1) * np.pi / beta for k in [0, 1, 2, 4, 7]]
    acf = {iwn: connected_g_coeffs(iwn, beta, mu, nmax) for iwn in iws}
    sg = {iwn: sigma_coeffs_exact(acf[iwn]) for iwn in iws}
    errs = {}
    for U in [0.3, 0.5, 0.7]:
        e = max(abs(sum(sg[iwn][n] * U ** n for n in range(1, nmax + 1)) - _sigma_ed(iwn, U, beta, mu))
                for iwn in iws)
        errs[U] = e
        print(f"  exact Sigma series vs ED, U={U}: worst err {e:.1e}")
    assert errs[0.3] < 1e-6, errs[0.3]
    assert errs[0.5] < 1e-3, errs[0.5]
    iwn0 = 1j * np.pi / beta
    RS = _radius(sg[iwn0], [14, 18, 20]); RG = _radius(acf[iwn0], [14, 18, 20])
    print(f"  R_G     ~ {RG[-1]:.2f} (|a_n|^(1/n)) ;  R_Sigma ~ {RS[-1]:.2f} (|sigma_n|^(1/n))")
    assert RS[-1] < 1.2, RS
    assert abs(RS[-1] - RG[-1]) < 0.3, (RS[-1], RG[-1])
    print("  => R_Sigma ~ R_G: no significant radius advantage for the atom. v136's 1.76 RETRACTED.")
    print("     The Simkovic-Kozik advantage is efficiency + MC variance, not a larger bare-series radius.")
    print("     (v133-135 unaffected: z=free addition pole, addition energy=eps+ReSigma, diag-Sigma converges.) PASS")

if __name__ == "__main__":
    _selftest()
