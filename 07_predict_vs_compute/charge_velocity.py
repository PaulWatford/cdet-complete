#!/usr/bin/env python3
"""
charge_velocity.py  --  the charge velocity u_rho at n=0.5, the route that finally works.

History: the dressed-energy endpoint slope diverged at weak coupling; the curvature
RATIO (flux stiffness / particle-number curvature) was 10-30% off because the
particle-number curvature is charge-spin contaminated at L<=12. The fix was not a
bigger lattice -- it was using the EXACT K_rho (bethe_Krho.py, v5) in place of the
contaminated curvature:

    D_c = (L/2) d^2E0/dPhi^2          (charge stiffness from a threaded flux Phi)
    u_rho = pi D_c / K_rho            (Luttinger relation, K_rho exact)

This is absolute -- no calibration constant, no U=0 anchor, no open-shell issue. Flux
is a uniform Peierls phase Phi/L per bond (total Phi around the ring); d^2E0/dPhi^2 is
taken from E0(Phi) at small Phi.

VERIFICATION (see CROSSCHECK_v8.md). Right trend sqrt2 -> 2, and cross-checks the
INDEPENDENT Bethe dressed-energy velocity at the U where that method is reliable:
    U=4:  u_rho = 1.840 (L=12), 1.796 (L=16)   vs Bethe 1.83
    U=8:  u_rho = 1.958 (L=12)                  vs Bethe 1.93
U=0 comes out 1.430 with no calibration (1% finite-size error, honestly not forced).
Two unrelated methods (ED flux stiffness + exact Bethe K_rho, vs Bethe dressed energy)
agree to ~1% at strong coupling. Accuracy ~1-2% (finite-size + finite-Phi curvature).
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
import predict_vs_compute as p
import bethe_Krho as bk

def hop_flux(S, idx, L, phi, t=1.0):
    r = []; c = []; v = []
    for n, s in enumerate(S):
        for a in range(L):
            b = (a + 1) % L
            for (i, j) in ((a, b), (b, a)):
                if (s >> j & 1) and not (s >> i & 1):
                    lo, hi = min(i, j), max(i, j); m = ((1 << hi) - 1) ^ ((1 << (lo + 1)) - 1)
                    sg = -1.0 if bin(s & m).count('1') & 1 else 1.0
                    ph = np.exp(1j * phi) if (i == b) else np.exp(-1j * phi)
                    r.append(idx[(s & ~(1 << j)) | (1 << i)]); c.append(n); v.append(-t * sg * ph)
    return sp.csr_matrix((v, (r, c)), shape=(len(S), len(S)), dtype=complex)

def E0_flux(L, Nu, Nd, U, Phi):
    US = p.states(L, Nu); DS = p.states(L, Nd)
    ui = {s: i for i, s in enumerate(US)}; di = {s: i for i, s in enumerate(DS)}
    phi = Phi / L
    Tu = hop_flux(US, ui, L, phi); Td = hop_flux(DS, di, L, phi)
    Iu = sp.identity(len(US)); Id = sp.identity(len(DS))
    docc = np.array([[bin(u & d).count('1') for d in DS] for u in US], float).ravel()
    H = (sp.kron(Tu, Id) + sp.kron(Iu, Td) + sp.diags(U * docc)).tocsr()
    return float(eigsh(H, k=1, which='SA', return_eigenvectors=False)[0])

def u_rho(L, U, Phi=0.4):
    """Charge velocity at n=0.5. WARNING: L=16 is ~3 min per flux solve."""
    e0 = E0_flux(L, L // 4, L // 4, U, 0.0)
    ep = E0_flux(L, L // 4, L // 4, U, Phi)
    Dstiff = 2 * (ep - e0) / Phi ** 2
    K = 1.0 if U == 0 else bk.Krho(U, 0.5)[2]
    return np.pi * (L / 2) * Dstiff / K

def main():
    bethe = {2.0: 1.76, 4.0: 1.83, 8.0: 1.93}  # independent Bethe dressed-energy (trusted U>=2)
    print("charge velocity u_rho at n=0.5  =  pi (L/2) (d2E/dPhi2) / K_rho_exact\n")
    print("  %5s  %12s  %14s" % ("U", "u_rho (L=12)", "Bethe endpoint"))
    for U in [0.0, 1.0, 2.0, 4.0, 8.0]:
        u = u_rho(12, U); b = bethe.get(U)
        print("  %5.1f  %12.4f  %14s" % (U, u, ("%.2f" % b) if b else "-"))
    print("  (U=0 target sqrt2=%.4f, uncalibrated; U->inf target 2)\n" % np.sqrt(2))
    # L=16 confirmation (energies computed separately; flux-code at Phi=0 == real solve)
    E16_0, E16_p = -12.06697, -12.06290   # L=16, U=4, Phi=0 and Phi=0.4
    D16 = 2 * (E16_p - E16_0) / 0.4 ** 2
    u16 = np.pi * 8 * D16 / bk.Krho(4.0, 0.5)[2]
    print("  L=16 confirmation at U=4: u_rho = %.4f  (L=12 gave 1.840; Bethe 1.83)" % u16)
    print("  -> the unlock was the EXACT K_rho, not the lattice size; L=16 confirms.")

if __name__ == '__main__':
    main()
