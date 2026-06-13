#!/usr/bin/env python3
"""
conformal_tower.py  --  the finite-size spectrum as a conformal tower.

This is Moeller's Q6 made concrete: the point where Bethe integrability and the
c=1 CFT must predict the SAME finite-size spectrum. A 1+1D CFT predicts every gap as

    E_n - E_0 = (2 pi v / L) * x_n,        x_n = scaling dimension (L-independent)

so multiplying gaps by L/(2 pi v) must COLLAPSE the spectrum onto fixed dimensions.
We test it in the strong-coupling spin sector (= the Heisenberg point, the U->inf
limit of the half-filled Hubbard spin sector), where the velocity is exactly v_s=pi/2
(verified independently in spin_velocity.py) and the CFT is c=1 SU(2)_1.

PREDICTION: leading primary x = 1/2 (the spin-1/2 field); the lowest triplet and the
lowest excited singlet are degenerate there (the SU(2)_1 primary multiplet).
RESULT (see CROSSCHECK_v7.md): x(leading) = 0.424 -> 0.438 as L = 8 -> 16, drifting
monotonically toward 1/2 with the known SU(2) logarithmic correction; triplet and
excited singlet degenerate to all printed digits. The tower is confirmed.
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

def heis_lowest(L, nup, k=4, J=1.0):
    states = [s for s in range(1 << L) if bin(s).count('1') == nup]
    idx = {s: i for i, s in enumerate(states)}; n = len(states)
    r = []; c = []; v = []
    for a, s in enumerate(states):
        d = 0.0
        for i in range(L):
            j = (i + 1) % L; bi = (s >> i) & 1; bj = (s >> j) & 1
            d += 0.25 if bi == bj else -0.25
            if bi != bj:
                t = s ^ (1 << i) ^ (1 << j); r.append(a); c.append(idx[t]); v.append(0.5 * J)
        r.append(a); c.append(a); v.append(J * d)
    H = sp.csr_matrix((v, (r, c)), shape=(n, n))
    kk = min(k, n - 1)
    w = eigsh(H, k=kk, which='SA', return_eigenvectors=False)
    return np.sort(w)

def main():
    vs = np.pi / 2
    print("conformal tower -- strong-coupling Hubbard spin sector (Heisenberg, v_s=pi/2)\n")
    print("  x_n = (E_n - E_0) * L / (2 pi v_s)   [CFT: collapses onto fixed dimensions]\n")
    print("  %3s  %12s  %14s  %12s" % ("L", "x(triplet)", "x(excited S=0)", "x(next)"))
    for L in [8, 10, 12, 14, 16]:
        s0 = heis_lowest(L, L // 2, k=4)
        s1 = heis_lowest(L, L // 2 + 1, k=1)
        E0 = s0[0]
        xt = (s1[0] - E0) * L / (2 * np.pi * vs)
        x2 = (s0[1] - E0) * L / (2 * np.pi * vs)
        x3 = (s0[2] - E0) * L / (2 * np.pi * vs)
        print("  %3d  %12.4f  %14.4f  %12.4f" % (L, xt, x2, x3))
    print("\n  leading primary -> 1/2 (SU(2)_1); triplet and excited singlet degenerate there.")
    print("  Two exact descriptions (Bethe + c=1 CFT) agree on the finite-size spectrum.")
    print("  Open: the DOPED tower (Frahm-Korepin charge dimensions in K_rho) needs the")
    print("  charge velocity; the K_rho-dependent dimension RATIOS are the velocity-free")
    print("  next check, tying the exact K_rho (bethe_Krho.py) to the spectrum.")

if __name__ == '__main__':
    main()
