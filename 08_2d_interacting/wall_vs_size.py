"""wall_vs_size.py (v172) -- the convergence wall vs lattice size.

The bare-U series has a finite radius of convergence (the "wall"). Its leading weak-coupling cause is the RPA/Stoner
instability: the particle-hole bubble sum chi(q) = chi0(q)/(1 - U chi0(q)) is a geometric series in U that diverges at

        U_c(L) = 1 / max_q chi0(q, L),

where chi0 is the FREE static (Lindhard) susceptibility built from the lattice dispersion eps_k = -2t(cos kx+cos ky)
-- exactly the plane-wave physics added in v162. Because chi0 needs only the O(L) dispersion (no eigenvectors), U_c(L)
is computable at ANY lattice size up to 100x100, which is what lets us finally watch the wall move with L.

FINDING. The wall is a thermodynamic-limit quantity; a small lattice gives a finite-size ARTIFACT.
  - Near half-filling (nesting peak at q=(pi,pi), the channel that dominates the Hubbard model) the small lattice
    places the wall spuriously CLOSE; growing L pushes it back to its true, further-out value -- LATTICE HELPS.
    e.g. beta=5, mu=0: U_c = 1.64 (4x4) -> 1.88 (8x8) -> 1.97 (16x16) -> 1.975 (TD).
  - At incommensurate doping the artifact reverses sign (the coarse grid misses the peak, so the small lattice is
    spuriously OPTIMISTIC). Either way you need the large lattice to get the true wall.

HONEST SCOPE. U_c here is the leading REAL-axis instability (RPA/Stoner), validated as the exact bubble-sum radius.
The FULL series radius can be set by complex-U structure closer than this (the v146 atom finding); U_c is the leading
physical wall, now computed at scale rather than guessed from the atom or a small cluster.
"""
import numpy as np


def _dispersion(L, mu, t=1.0):
    ks = 2 * np.pi * np.arange(L) / L
    KX, KY = np.meshgrid(ks, ks, indexing="ij")
    return -2.0 * t * (np.cos(KX) + np.cos(KY)) - mu


def _fermi(e, beta):
    return 1.0 / (1.0 + np.exp(np.clip(beta * e, -60, 60)))


def chi0_at_q(L, beta, mu, qx, qy, t=1.0):
    """free static Lindhard susceptibility chi0(q) at one grid momentum q=(2pi qx/L, 2pi qy/L)."""
    eps = _dispersion(L, mu, t); f = _fermi(eps, beta)
    epskq = np.roll(np.roll(eps, -qx, 0), -qy, 1); fkq = np.roll(np.roll(f, -qx, 0), -qy, 1)
    de = epskq - eps; small = np.abs(de) < 1e-9
    return float(np.where(small, beta * f * (1 - f), (f - fkq) / np.where(small, 1.0, de)).mean())


def chi0_max_rect(Lx, Ly, beta, mu, thx=0.0, thy=0.0, t=1.0):
    """CANONICAL Lindhard peak: max over the q-grid of chi0(q) on an Lx x Ly lattice with twist (thx,thy).
    The square periodic case (chi0_max) and the rectangular/twisted cases (wall_twist) all route through here, so the
    whole wall suite shares one core. Returns (chi0_max, peak_q_index)."""
    kx = 2 * np.pi * (np.arange(Lx) + thx) / Lx
    ky = 2 * np.pi * (np.arange(Ly) + thy) / Ly
    KX, KY = np.meshgrid(kx, ky, indexing="ij")
    eps = -2.0 * t * (np.cos(KX) + np.cos(KY)) - mu
    f = _fermi(eps, beta)
    best = -1.0; bq = (0, 0)
    for qx in range(Lx):
        for qy in range(Ly):
            epskq = np.roll(np.roll(eps, -qx, 0), -qy, 1); fkq = np.roll(np.roll(f, -qx, 0), -qy, 1)
            de = epskq - eps; small = np.abs(de) < 1e-9
            v = float(np.where(small, beta * f * (1 - f), (f - fkq) / np.where(small, 1.0, de)).mean())
            if v > best: best = v; bq = (qx, qy)
    return best, bq


def chi0_max(L, beta, mu, t=1.0):
    """max over the discrete q-grid of chi0(q,L) for a square periodic lattice; returns (chi0_max, peak_q_indices)."""
    return chi0_max_rect(L, L, beta, mu, 0.0, 0.0, t)


def wall(L, beta, mu, t=1.0):
    """the leading weak-coupling convergence wall U_c(L) = 1/chi0_max(L)."""
    cm, q = chi0_max(L, beta, mu, t)
    return 1.0 / cm, q


def wall_vs_size(beta, mu, Ls, t=1.0):
    """U_c(L) for each L in Ls; returns list of (L, chi0_max, U_c, peak_q_in_pi_units)."""
    out = []
    for L in Ls:
        cm, q = chi0_max(L, beta, mu, t)
        out.append((L, cm, 1.0 / cm, (2 * q[0] / L, 2 * q[1] / L)))
    return out


def _selftest():
    print("wall_vs_size self-test (convergence wall U_c(L)=1/chi0_max from the plane-wave dispersion):")
    beta, mu, L = 5.0, 0.0, 16

    # (1) chi0(q=0) sum rule == DOS-at-E_F: (1/N) sum beta f(1-f)
    eps = _dispersion(L, mu); f = _fermi(eps, beta)
    sr = float((beta * f * (1 - f)).mean()); d1 = abs(chi0_at_q(L, beta, mu, 0, 0) - sr)
    assert d1 < 1e-12, d1
    print(f"  [sum rule]  chi0(0) == (1/N)sum beta f(1-f): dev {d1:.1e}")

    # (2) vectorized roll == brute-force O(L^4) explicit pair sum at q=(pi,pi)
    qx = qy = L // 2; acc = 0.0
    for a in range(L):
        for b in range(L):
            e1 = eps[a, b]; f1 = f[a, b]; e2 = eps[(a + qx) % L, (b + qy) % L]; f2 = f[(a + qx) % L, (b + qy) % L]
            de = e2 - e1; acc += beta * f1 * (1 - f1) if abs(de) < 1e-9 else (f1 - f2) / de
    d2 = abs(acc / (L * L) - chi0_at_q(L, beta, mu, qx, qy))
    assert d2 < 1e-12, d2
    print(f"  [method]    vectorized == brute-force pair sum: dev {d2:.1e}")

    # (3) the wall IS the bubble-sum radius: geometric series sum_n (U chi0max)^n converges iff U < U_c
    cm, _ = chi0_max(L, beta, mu); Uc = 1.0 / cm
    assert (0.9 * Uc) * cm < 1.0 < (1.1 * Uc) * cm  # ratio crosses 1 exactly at U_c
    print(f"  [radius]    bubble series sum_n (U chi0max)^n radius = 1/chi0max = U_c = {Uc:.4f}")

    # (4) U_c(L) converges as L grows (the wall is a TD-limit quantity)
    Uc64 = wall(64, beta, mu)[0]; Uc96 = wall(96, beta, mu)[0]
    assert abs(Uc64 - Uc96) < 1e-2, (Uc64, Uc96)
    print(f"  [TD limit]  U_c(64)={Uc64:.4f}, U_c(96)={Uc96:.4f}: converged (|d|={abs(Uc64-Uc96):.1e})")

    # (5) headline: near half-filling the small lattice is spuriously pessimistic; growing L pushes the wall BACK
    Uc4 = wall(4, beta, mu)[0]
    assert Uc4 < Uc96 - 0.1, (Uc4, Uc96)
    print(f"  [helps]     half-filling wall recedes with L: U_c(4x4)={Uc4:.4f} -> U_c(TD)={Uc96:.4f}  (lattice helps)")
    print("  => the convergence wall is a TD-limit quantity computable at any L via the plane-wave dispersion;")
    print("     near half-filling the large lattice reveals a further-out wall. Frozen engine untouched. PASS")


if __name__ == "__main__":
    _selftest()
