#!/usr/bin/env python3
"""
spin_stiffness_qf.py  (v13)  --  u_sigma at quarter filling, the robust independent way
(and it CORRECTS the v12 extraction).

v12 left u_sigma "extracted, not verified": it came from the 2k_F gap via a naive CFT
decomposition gap(2k_F) = (2 pi/L)(K_rho u_rho/2 + u_sigma/2). v13 measures u_sigma a
second, independent way -- the SPIN STIFFNESS -- and they DISAGREE for U>0. The cross-
check did its job: the spin stiffness is the trustworthy route, and the v12 u_sigma
numbers are superseded.

Method (pure-spin, integrated ground-state energy -- the robust kind, real_patterns #13):
thread a SPIN flux, i.e. opposite Peierls phases for the two spins (up: +Phi/L per bond,
down: -Phi/L). This twists the spin sector only; the charge sector is untouched. Then
    D_sigma = (L/2) d^2 E0/dPhi^2 ,   u_sigma = pi (L/2) D_sigma   (K_sigma = 1, SU(2)).
No operator-dimension assumption, no boundary slope -- just ground-state energies, which
ED gets accurately.

Validation of the method: at U=0 the spin twist and the charge twist act identically on
free fermions (up:+Phi, down:-Phi vs both:+Phi give the same E0 by up/down symmetry), so
u_sigma(U=0) MUST equal the v8 charge value u_rho(U=0). It does, to all digits (1.4304).
That fixes the prefactor with no free constant.

Why it supersedes v12: u_sigma(spin stiffness) and u_sigma(v12 gap extraction) agree at
U=0 but split to ~40% by U=8. The 2k_F finite-size gap does NOT cleanly decompose into
(K_rho u_rho/2 + u_sigma/2) at L=12 (marginal/log corrections of the SU(2) spin sector;
the asymptotic operator dimension is not yet reached), so the v12 extraction was biased.
The spin stiffness has no such assumption.

Result (L=12, n=0.5): with u_rho from the v8 CHARGE stiffness and u_sigma from the SPIN
stiffness -- the SAME robust route, charge vs spin twist -- the two coincide at U=0
(= v_F, no separation) and split with U: u_rho 1.43 -> 1.96, u_sigma 1.43 -> 0.71, ratio
1.0 -> 2.8. Spin-charge separation, now from one consistent integrated method on both legs.

Open (v14): an EXACT anchor for u_sigma at U>0 -- the Bethe-ansatz spin (dressed-energy)
velocity, the spin analogue of bethe_Krho.py -- to lift u_sigma from "robustly measured"
to "verified against exact", as u_rho already is (v8 vs the Bethe charge velocity).
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
import predict_vs_compute as p
import charge_velocity as cv          # hop_flux + v8 charge velocity u_rho
import spin_charge_velocities as scv  # v12 extracted u_sigma (for the supersession table)


def E0_spinflux(L, Nu, Nd, U, Phi):
    US = p.states(L, Nu); DS = p.states(L, Nd)
    ui = {s: i for i, s in enumerate(US)}; di = {s: i for i, s in enumerate(DS)}
    Tu = cv.hop_flux(US, ui, L, Phi / L)      # up:  +Phi/L
    Td = cv.hop_flux(DS, di, L, -Phi / L)     # down: -Phi/L   (opposite -> spin twist)
    Iu = sp.identity(len(US)); Id = sp.identity(len(DS))
    docc = np.array([[bin(u & d).count('1') for d in DS] for u in US], float).ravel()
    H = (sp.kron(Tu, Id) + sp.kron(Iu, Td) + sp.diags(U * docc)).tocsr()
    return float(eigsh(H, k=1, which='SA', return_eigenvectors=False)[0])


def u_sigma(L, U, Phi=0.4):
    e0 = E0_spinflux(L, L // 4, L // 4, U, 0.0)
    ep = E0_spinflux(L, L // 4, L // 4, U, Phi)
    Dsig = 2 * (ep - e0) / Phi ** 2
    return np.pi * (L / 2) * Dsig             # u_sigma = pi(L/2) D_sigma, K_sigma = 1


def main():
    L = 12
    vF = 2 * np.sin(np.pi / 4)
    print("u_sigma at quarter filling -- SPIN STIFFNESS (independent of the 2k_F gap)\n")
    print("  u_sigma = pi (L/2) D_sigma,  D_sigma = (L/2) d^2E0/dPhi_spin^2   [pure spin]")
    print("  anchor: U=0 -> u_sigma = u_rho = v_F = %.4f (spin twist == charge twist)\n" % vF)
    print("  %5s %12s %12s %12s %11s %12s" %
          ("U", "u_rho(v8)", "u_sig(stiff)", "u_sig(v12)", "u_rho/u_sig", "v12 error"))
    for U in [0.0, 1.0, 2.0, 4.0, 8.0]:
        us = u_sigma(L, U)
        ur = cv.u_rho(L, U)
        _, _, _, _, us12 = scv.velocities(L, U)
        print("  %5.1f %12.4f %12.4f %12.4f %11.3f %11.0f%%"
              % (U, ur, us, us12, ur / us, 100 * abs(us12 / us - 1)))
    print("\n  u_sig(stiff) is the robust value; u_sig(v12) is the superseded 2k_F-gap")
    print("  extraction -- they agree at U=0 and diverge to ~40% by U=8, so the v12 2k_F")
    print("  decomposition was biased (finite-size/marginal corrections). With both legs")
    print("  now from flux stiffness, spin-charge separation is clean: coincide at U=0,")
    print("  split with U (u_rho up, u_sigma down). Open (v14): exact Bethe spin velocity")
    print("  to verify u_sigma at U>0, as u_rho is already verified against Bethe (v8).")


if __name__ == '__main__':
    main()
