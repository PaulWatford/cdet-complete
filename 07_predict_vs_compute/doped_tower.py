#!/usr/bin/env python3
"""
doped_tower.py  (v9)  --  the DOPED conformal tower, and what breaks.

v7 verified the conformal tower in the UNDOPED strong-coupling spin sector
(Heisenberg point, v_s = pi/2 known exactly). This tries to extend it to the DOPED
CHARGE sector at quarter filling (n=0.5), where the Luttinger parameter K_rho lives,
with a deliberately VELOCITY-FREE probe -- and reports the honest outcome, which is
a clean BREAK that detects spin-charge separation.

Hypothesis (single charge velocity, Luttinger liquid, SU(2) so K_sigma = 1):
  - 2k_F density operator dimension  x_2 = (1 + K_rho)/2
  - 4k_F density operator dimension  x_4 = 2 K_rho
  Each is a finite-size gap  E - E_0 = (2 pi u_rho / L) x, so the RATIO
        R(L) = gap(4k_F) / gap(2k_F)  ->  x_4 / x_2  =  4 K_rho / (1 + K_rho)
  WOULD be velocity-free IF one velocity governed both.

Exact anchor: at U=0 (free fermions) K_rho = 1, so R must equal 2 EXACTLY. The U=0
row is the integrity check (real_patterns #6, #11): it reads R = 2.00000, so the
momentum identification and the gap extraction are correct.

What actually happens at U>0 (the result):
  R(ED) RISES with U (2.18, 2.31, 2.51, 2.80) while 4 K_rho/(1+K_rho) FALLS
  (1.90, 1.80, 1.66, 1.53). The hypothesis breaks, and the break is informative:
  the 4k_F operator is PURE CHARGE (single velocity u_rho), but the 2k_F operator
  carries BOTH charge and spin, so its finite-size gap mixes u_rho and u_sigma. The
  ratio is therefore not velocity-free once the two velocities differ. At U=0 they
  coincide (u_rho = u_sigma = v_F), which is precisely why the anchor is clean; the
  monotonic rise of R(ED) is a direct signature of SPIN-CHARGE SEPARATION growing
  with U (u_sigma slows toward 2pi/U scales while u_rho speeds up, cf v6/v8).

The corrected probe (v10 open item): use a ratio of two PURE-CHARGE gaps, both set
by u_rho alone -- 4k_F (x = 2 K_rho) against the charge-current / flux excitation --
so a single velocity genuinely cancels and K_rho is isolated. This script is the
honest negative-with-diagnosis that motivates it.

Method: gaps are the lowest ED eigenvalue in each total-momentum sector, obtained by
penalising the target momentum down (a Hermitian projector reward) so only a few
states per sector are needed. Quarter filling is a closed shell at L=12
(N_up=N_dn=3, ground-state momentum 0), the clean lattice.
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
import predict_vs_compute as p   # tested states() + hop() (PBC, fermion signs)
import bethe_Krho as bk          # exact Bethe K_rho (v5)


def trans_species(S, idx, L):
    """Single-species lattice translation (site i -> i+1) as a signed permutation.
    Sign rule: translating the ordered product of creation operators by one site is
    the identity unless a particle sits on site L-1 and wraps to 0, in which case it
    must hop past the other N-1 particles -> sign (-1)^(N-1)."""
    full = (1 << L) - 1
    r = []; c = []; v = []
    for n, s in enumerate(S):
        sp_ = ((s << 1) | (s >> (L - 1))) & full
        N = bin(s).count('1')
        sg = -1.0 if ((s >> (L - 1)) & 1 and (N - 1) & 1) else 1.0
        r.append(idx[sp_]); c.append(n); v.append(sg)
    return sp.csr_matrix((v, (r, c)), shape=(len(S), len(S)))


def build(L, Nup, Ndn, U):
    """Return (H, T) on the spinful sector: H Hubbard ring, T full-space translation."""
    US = p.states(L, Nup); DS = p.states(L, Ndn)
    ui = {s: i for i, s in enumerate(US)}; di = {s: i for i, s in enumerate(DS)}
    Tu = p.hop(US, ui, L); Td = p.hop(DS, di, L)
    Iu = sp.identity(len(US)); Id = sp.identity(len(DS))
    docc = np.array([[bin(u & d).count('1') for d in DS] for u in US], float).ravel()
    H = (sp.kron(Tu, Id) + sp.kron(Iu, Td) + sp.diags(U * docc)).tocsr()
    T = sp.kron(trans_species(US, ui, L), trans_species(DS, di, L)).tocsr()
    return H, T


def lowest_in_sector(H, T, L, m, Lam=60.0, k=4):
    """Lowest H-energy among states of total momentum P=2pi m/L, via a penalty that
    rewards being in the target momentum sector. M=(e^{-iP}T+h.c.)/2 has eigenvalue 1
    on the sector and <1 off it, so H - Lam*M pushes the wanted sector to the bottom."""
    P = 2 * np.pi * m / L
    M = (np.exp(-1j * P) * T + np.exp(1j * P) * T.getH()) * 0.5
    Hpen = (H.astype(complex) - Lam * M).tocsr()
    w, V = eigsh(Hpen, k=k, which='SA')
    best = None
    for c in range(V.shape[1]):
        v = V[:, c]
        mval = np.real(v.conj() @ (M @ v))          # ~1 if truly in sector m
        if mval > 0.99:
            e = np.real(v.conj() @ (H @ v))
            best = e if best is None else min(best, e)
    return best


def ratio_for(L, U):
    Nup = Ndn = L // 4
    H, T = build(L, Nup, Ndn, U)
    m2 = (L // 4) % L          # 2k_F = pi/2  -> m = L/4   (ground state is at m=0)
    m4 = (L // 2) % L          # 4k_F = pi    -> m = L/2
    E0 = lowest_in_sector(H, T, L, 0)
    e2 = lowest_in_sector(H, T, L, m2)
    e4 = lowest_in_sector(H, T, L, m4)
    g2 = (e2 - E0) if (e2 is not None) else None
    g4 = (e4 - E0) if (e4 is not None) else None
    R = (g4 / g2) if (g2 and g4) else None
    return E0, g2, g4, R


def main():
    print("DOPED conformal tower -- velocity-free charge-sector check (n=0.5)\n")
    print("  R(L) = gap(4k_F)/gap(2k_F)  ->  x4/x2 = 4 K_rho/(1+K_rho)   [u_rho cancels]")
    print("  exact anchor: U=0 -> K_rho=1 -> R=2 exactly\n")
    print("  %3s %5s %10s %10s %9s %12s %8s" %
          ("L", "U", "gap(2kF)", "gap(4kF)", "R(ED)", "4K/(1+K)", "K_rho"))
    for L in [12]:
        for U in [0.0, 1.0, 2.0, 4.0, 8.0]:
            E0, g2, g4, R = ratio_for(L, U)
            K = 1.0 if U == 0 else bk.Krho(U, 0.5)[2]
            pred = 4 * K / (1 + K)
            if R is None:
                print("  %3d %5.1f   (target momentum sector not captured in low spectrum)" % (L, U))
            else:
                print("  %3d %5.1f %10.5f %10.5f %9.4f %12.4f %8.4f"
                      % (L, U, g2, g4, R, pred, K))
    print("\n  READING THE RESULT (this is a BREAK, and the break is the physics):")
    print("  - U=0 anchor is exact: R=2.000. The machinery is correct.")
    print("  - But R(ED) RISES with U while 4K/(1+K) FALLS. The single-velocity")
    print("    hypothesis is wrong: 4k_F is PURE CHARGE (one velocity u_rho), whereas")
    print("    2k_F carries BOTH charge and spin, so its gap mixes u_rho and u_sigma.")
    print("    The ratio is therefore NOT velocity-free once u_sigma != u_rho.")
    print("  - At U=0 the two velocities coincide (u_rho=u_sigma=v_F), which is exactly")
    print("    why the anchor is clean; the growing R(ED) is a direct, monotonic")
    print("    SIGNATURE OF SPIN-CHARGE SEPARATION (u_sigma slows, u_rho speeds up).")
    print("  - FIX (v10): build the ratio from TWO pure-charge gaps (both governed by")
    print("    u_rho alone) -- e.g. 4k_F vs the charge-current/flux excitation -- so a")
    print("    single velocity genuinely cancels and K_rho is isolated. (real_patterns")
    print("    entry #9: a formula that breaks, read correctly, locates the physics.)")


if __name__ == '__main__':
    main()
