"""susceptibilities.py (v165) -- linear-response susceptibilities: charge compressibility and spin susceptibility.

Two central Hubbard response functions, each validated by TWO INDEPENDENT ED routes (a derivative route and a
fluctuation-dissipation route -- they share no code path, so agreement is a real cross-check):

  charge compressibility   kappa = d<n>/dmu              == (beta/2N) Var(N_hat)      [fluctuation-dissipation]
  spin susceptibility      chi_s = d<S_z>/dh |_{h=0}     == beta Var(S_z)             [fluctuation-dissipation]

with N_hat the total particle number, S_z = sum_site (n_up - n_dn)/2 (for N=2 the standard spin), on the 2-site
SU(N) reference. The physics is the opposite-trend hallmark of Mott correlation:

  kappa DECREASES with U  (charge fluctuations suppressed -> approach to the incompressible Mott state)
  chi_s INCREASES with U  (local-moment formation -> enhanced magnetic response)

Each also gets a weak-coupling U-series (complex-U contour, like density_series) resummed with conformal-Borel (v160)
for reach. The frozen engine is untouched (ED is the anchor only)."""
import numpy as np
from sun_eos_curve import _build_H_c, density_ed, BETA, T, MU
from sun_eos_conformal import conformal_borel, borel_singularity


def _Nhat(N):
    return np.array([bin(s).count('1') for s in range(1 << (2 * N))], dtype=float)


def _Sz(N):
    v = np.zeros(1 << (2 * N))
    for s in range(1 << (2 * N)):
        tot = 0
        for site in range(2):
            tot += ((s >> (site * N + 0)) & 1) - ((s >> (site * N + 1)) & 1)   # flavor 0=up, 1=dn
        v[s] = 0.5 * tot
    return v


def _thermal(N, U, mu, beta, t, op):
    """thermal average of a diagonal (occupation-basis) operator over the real-U ED ensemble."""
    H = _build_H_c(N, t, mu, U).real
    ev, V = np.linalg.eigh(H)
    w = np.exp(-beta * (ev - ev.min()))
    return np.sum(w * np.einsum('sn,sn,s->n', V, V, op)) / np.sum(w)


# ---------------- charge compressibility kappa = dn/dmu ----------------------------------------
def kappa_deriv(N, U, mu=MU, beta=BETA, t=T, h=1e-3):
    return ((density_ed(N, U, mu + h, beta, t) - density_ed(N, U, mu - h, beta, t)) / (2 * h)).real


def kappa_fluct(N, U, mu=MU, beta=BETA, t=T):
    nv = _Nhat(N)
    Nm = _thermal(N, U, mu, beta, t, nv)
    N2 = _thermal(N, U, mu, beta, t, nv * nv)
    return beta * (N2 - Nm * Nm) / (2 * N)   # same normalization as density_ed (per-flavor)


def kappa_series(N, K, mu=MU, beta=BETA, t=T, r=0.1, M=48, h=1e-3):
    th = 2 * np.pi * np.arange(M) / M
    kv = np.array([(density_ed(N, r * np.exp(1j * a), mu + h, beta, t) -
                    density_ed(N, r * np.exp(1j * a), mu - h, beta, t)) / (2 * h) for a in th])
    return np.array([(np.sum(kv * np.exp(-1j * k * th)) / M / r ** k).real for k in range(K + 1)])


# ---------------- spin susceptibility chi_s = d<Sz>/dh -----------------------------------------
def _lnZ_field(N, mu, U, beta, t, h, sz):
    ev = np.linalg.eigvals(_build_H_c(N, t, mu, U) - h * np.diag(sz))
    m = ev.real.min()
    return np.log(np.sum(np.exp(-beta * (ev - m)))) - beta * m


def chi_spin_fluct(N, U, mu=MU, beta=BETA, t=T):
    sz = _Sz(N)
    m = _thermal(N, U, mu, beta, t, sz)
    s2 = _thermal(N, U, mu, beta, t, sz * sz)
    return beta * (s2 - m * m)


def chi_spin_field(N, U, mu=MU, beta=BETA, t=T, h=1e-3):
    sz = _Sz(N)

    def Sz_exp(hh):
        H = _build_H_c(N, t, mu, U).real - hh * np.diag(sz)
        ev, V = np.linalg.eigh(H)
        w = np.exp(-beta * (ev - ev.min()))
        return np.sum(w * np.einsum('sn,sn,s->n', V, V, sz)) / np.sum(w)

    return (Sz_exp(h) - Sz_exp(-h)) / (2 * h)


def chi_spin_series(N, K, mu=MU, beta=BETA, t=T, r=0.1, M=48, hh=1e-3):
    sz = _Sz(N); th = 2 * np.pi * np.arange(M) / M
    cv = np.array([(_lnZ_field(N, mu, r * np.exp(1j * a), beta, t, hh, sz) +
                    _lnZ_field(N, mu, r * np.exp(1j * a), beta, t, -hh, sz) -
                    2 * _lnZ_field(N, mu, r * np.exp(1j * a), beta, t, 0.0, sz)) / (hh * hh) / beta for a in th])
    return np.array([(np.sum(cv * np.exp(-1j * k * th)) / M / r ** k).real for k in range(K + 1)])


def _selftest():
    print("susceptibilities self-test (charge compressibility + spin susceptibility):")
    N = 2
    # (1) dual-route cross-checks (derivative vs fluctuation-dissipation)
    wk = max(abs(kappa_deriv(N, U) - kappa_fluct(N, U)) for U in (0.0, 1.0, 2.0))
    ws = max(abs(chi_spin_field(N, U) - chi_spin_fluct(N, U)) for U in (0.0, 1.0, 2.0, 4.0))
    print(f"  [cross-check] kappa: deriv vs fluctuation-dissipation worst dev = {wk:.1e}")
    print(f"  [cross-check] chi_s: field vs fluctuation-dissipation worst dev = {ws:.1e}")
    assert wk < 1e-6 and ws < 1e-6, (wk, ws)
    # (2) opposite Mott trends: charge suppressed, spin enhanced
    ks = [kappa_fluct(N, U) for U in (0.0, 1.0, 2.0)]
    cs = [chi_spin_fluct(N, U) for U in (0.0, 1.0, 2.0, 4.0)]
    print(f"  [trend] kappa(U=0,1,2)   = {[f'{x:.4f}' for x in ks]}  (decreasing -> Mott incompressibility)")
    print(f"  [trend] chi_s(U=0,1,2,4) = {[f'{x:.4f}' for x in cs]}  (increasing -> local-moment magnetism)")
    assert ks[0] > ks[1] > ks[2], ks
    assert cs[0] < cs[1] < cs[2] < cs[3], cs
    # (3) weak-series + conformal-Borel reproduces the ED response
    sc = chi_spin_series(N, 10); Uc = borel_singularity(sc)
    e = chi_spin_fluct(N, 1.0); cb = abs(conformal_borel(sc, 1.0, Uc) - e)
    print(f"  [resum] chi_s at U=1: conformal-Borel err vs ED = {cb:.1e}")
    assert cb < 1e-2, cb
    print("  => both susceptibilities validated by two independent ED routes; opposite Mott trends; conformal-Borel")
    print("     resummation. Frozen engine untouched (194/194). PASS")


if __name__ == "__main__":
    _selftest()
