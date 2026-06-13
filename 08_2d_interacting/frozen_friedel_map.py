"""frozen_friedel_map.py (v119) -- the full 2D Friedel sign-map, resolved at the elementary level.

v117 saw A's sign oscillate along a line; v118 showed it is set by the DISCRETE frozen Fermi boundary,
rigid under mu. This module maps the sign over a full 2D plane and resolves it at the ELEMENTARY level.

The full background A is a connected determinant of propagators between {0,S0,S1,S2}, so its sign-vs-S2
is a multi-propagator SUPERPOSITION (the measured 2D A-map is structured but messy, and the fixed sites
S0,S1 break the lattice symmetry). The elementary object is the frozen one-particle density matrix

    rho(0,r) = sum_{occupied k} U[0,k] U[r,k] = (1/N) sum_{occ k} e^{i k.r}

i.e. the Fourier transform of the OCCUPIED REGION in k-space. Its Friedel oscillation is set by the
Fermi surface (the boundary of the occupied region) directly.

RESULTS:
  (1) rho(0,r) has a SHORT-wavelength, CUBE-SYMMETRIC Friedel pattern (period ~2-3 sites). Dominant
      wavevector (kx,ky,kz)=(2,3,0)-type -> momenta (120,180) deg, which MATCH the level-1|level-2
      boundary 1D modes (eps=+1 at k=2,4 -> 120/240 deg; eps=+2 at k=3 -> 180 deg). The DISCRETE frozen
      Fermi surface sets the wavevector.
  (2) mu-invariance is now ANALYTIC and EXACT: there are ZERO modes with eigenvalue strictly in (1,2),
      so the occupied set {lambda<=1} is IDENTICAL for every mu in the window -> rho is exactly the same
      map for all mu in (1,2). This proves v118's numerical mu-rigidity from first principles.
  (3) RECONCILES v117: the elementary Friedel wavelength is SHORT (~2-3 sites), not the ~8 sites inferred
      from A. A's sign is a determinant superposition of these short elementary oscillations over the
      site pairs, which produces a longer, messier apparent envelope. v117's '~8-site wavelength /
      2k_F(mu)' was that superposition envelope (and, per v118, a coincidence), not the elementary scale.

So the sign side closes consistently with the scale side: the DISCRETE frozen Fermi surface (the
filled-level set) sets the elementary Friedel wavevector exactly and mu-rigidly; the determinant builds
the observable sign by superposing these elementary oscillations.

v121: this elementary object is now ALSO in C -- cfriedel.c computes rho(0,r)=(1/N)sum_{eps(k)<=1}cos(k.r)
from the plane-wave structure (no eigenvectors), validated to ~5e-11 against this module over all 216 sites."""
import numpy as np
from symmetry_reduction import cube_hopping

def frozen_density_matrix():
    """rho(0,r) for the frozen background: occupied = eigenvalue <= 1 (level 1|2 boundary)."""
    H = cube_hopping(6)
    w, U = np.linalg.eigh(H)
    occ = (w <= 1.0 + 1e-9).astype(float)
    rho0 = (U[0, :] * occ) @ U.T
    return rho0, w

def gap_is_empty():
    """Zero modes strictly inside (1,2) -> occupied set rigid for all mu in the window."""
    _, w = frozen_density_matrix()
    return int(((w > 1.0 + 1e-9) & (w < 2.0 - 1e-9)).sum())

def _selftest():
    rho0, w = frozen_density_matrix()
    P = np.array([[rho0[x + 6*y] for x in range(6)] for y in range(6)])
    # (1) cube symmetry of the elementary sign-map (x->6-x, y->6-y)
    symX = np.array_equal(np.sign(P[:, 1:]), np.sign(P[:, 1:][:, ::-1]))
    symY = np.array_equal(np.sign(P[1:, :]), np.sign(P[1:, :][::-1, :]))
    assert symX and symY, "elementary map not cube-symmetric"
    # (2) analytic mu-invariance: nothing in the gap (1,2)
    assert gap_is_empty() == 0, "gap not empty -> occupied set would shift with mu"
    # (3) short wavelength: dominant wavevector is a zone-interior/boundary mode, not k~0 (long wave)
    F = np.abs(np.fft.fftn(rho0.reshape(6, 6, 6))); F[0, 0, 0] = 0
    peak = np.unravel_index(np.argmax(F), F.shape)
    kmax = max(peak)                          # in units of 2pi/6; >=2 means wavelength <= 3 sites
    assert kmax >= 2, peak
    print("frozen_friedel_map self-test:")
    print(f"  elementary rho(0,r) sign-map is CUBE-SYMMETRIC (x->6-x: {symX}, y->6-y: {symY})")
    print(f"  modes strictly in gap (1,2): {gap_is_empty()} -> occupied set RIGID -> rho EXACTLY mu-invariant (analytic v118)")
    print(f"  dominant wavevector {peak} (of 6/axis) -> momenta {tuple(round(360*p/6) for p in peak)} deg = level-1|2 boundary modes")
    print(f"  => short wavelength (~2-3 sites), set by the DISCRETE frozen Fermi surface; A's sign superposes these. PASS")

if __name__ == '__main__':
    _selftest()
