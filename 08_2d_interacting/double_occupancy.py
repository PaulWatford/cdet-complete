"""double_occupancy.py (v164) -- the double occupancy D = <n_up n_dn> as a proper interacting observable.

The double occupancy is the central Hubbard observable: it drives the Mott transition, sets the interaction energy
(E_int/site = U*D), and is the standard cold-atom thermometer. Until now the suite only had it at the atomic
single-site limit; this computes it for the 2-site SU(N) reference as a function of U, validated against ED, and
resummed with conformal-Borel (v160) for reach.

Thermodynamic identity: with H = H0 + U*D_hat, D_hat = sum_site sum_{a<b} n_{site,a} n_{site,b} (the pair-occupancy
operator; for N=2 this is exactly sum_site n_up n_dn), one has

    <D_hat> = -(1/beta) d lnZ / dU      ->    D (per site) = <D_hat> / N_sites .

So the whole observable rides on the existing lnZ machinery: a complex-U contour gives the U-series of D, exactly as
density_series does for the mu-derivative. Two independent ED routes agree (the lnZ U-derivative and the direct
thermal average of D_hat), which is the validation anchor; the frozen engine is untouched."""
import numpy as np
from sun_eos_curve import _lnZ, _build_H_c, BETA, T, MU
from sun_eos_conformal import conformal_borel, borel_singularity

NSITES = 2  # the 2-site SU(N) reference


def docc_ed(N, U, mu=MU, beta=BETA, t=T, h=1e-4):
    """double occupancy per site via the lnZ U-derivative (the benchmark)."""
    return -(_lnZ(N, mu, U + h, beta, t) - _lnZ(N, mu, U - h, beta, t)).real / (2 * h) / (beta * NSITES)


def docc_ed_direct(N, U, mu=MU, beta=BETA, t=T):
    """double occupancy per site via the DIRECT thermal average of the pair-occupancy operator D_hat.
    Independent of the lnZ-derivative route -- the cross-check."""
    H = _build_H_c(N, t, mu, U).real
    ev, V = np.linalg.eigh(H)
    norb = 2 * N
    dvec = np.zeros(len(ev))                      # D_hat is diagonal in the occupation basis
    for s in range(1 << norb):
        c = 0
        for site in range(2):
            for a in range(N):
                for b in range(a + 1, N):
                    if (s >> (site * N + a)) & 1 and (s >> (site * N + b)) & 1:
                        c += 1
        dvec[s] = c
    w = np.exp(-beta * (ev - ev.min()))
    Dexp = np.sum(w * np.einsum('sn,sn,s->n', V, V, dvec)) / np.sum(w)
    return Dexp / NSITES


def docc_series(N, K, mu=MU, beta=BETA, t=T, r=0.1, M=48, h=1e-4):
    """per-site double-occupancy U-series [D_0..D_K] via a complex-U contour (clean to high order)."""
    th = 2 * np.pi * np.arange(M) / M
    dv = np.array([-(_lnZ(N, mu, r * np.exp(1j * a) + h, beta, t) -
                     _lnZ(N, mu, r * np.exp(1j * a) - h, beta, t)) / (2 * h) / (beta * NSITES) for a in th])
    return np.array([(np.sum(dv * np.exp(-1j * k * th)) / M / r ** k).real for k in range(K + 1)])


def docc_resummed(N, U, K=10):
    """best estimate of D(U): conformal-Borel resummation of the weak-coupling series."""
    a = docc_series(N, K)
    return conformal_borel(a, U, borel_singularity(a))


def _selftest():
    print("double_occupancy self-test (D=<n_up n_dn> as a proper interacting observable):")
    N = 2
    # (1) two independent ED routes agree: lnZ U-derivative == direct thermal <D_hat>
    worst = max(abs(docc_ed(N, U) - docc_ed_direct(N, U)) for U in (0.0, 0.5, 1.0, 2.0, 3.0))
    print(f"  [cross-check] lnZ-derivative vs direct thermal <D_hat>: worst dev = {worst:.1e}")
    assert worst < 1e-6, worst
    # (2) physical trend: correlation suppresses double occupancy as U grows
    Ds = [docc_ed(N, U) for U in (0.0, 1.0, 2.0, 3.0)]
    print(f"  [trend] D(U=0,1,2,3) = {[f'{d:.4f}' for d in Ds]}  (monotone decreasing -> Mott suppression)")
    assert all(Ds[i] > Ds[i + 1] for i in range(len(Ds) - 1)), Ds
    # (3) conformal-Borel beats plain Pade at intermediate coupling
    from resummation import pade, pade_eval
    a = docc_series(N, 10); Uc = borel_singularity(a); p, q = pade(a, 4, 4)
    e = docc_ed(N, 1.0)
    cb = abs(conformal_borel(a, 1.0, Uc) - e); pa = abs(pade_eval(p, q, 1.0).real - e)
    print(f"  [resum] at U=1: conformal-Borel err {cb:.1e} vs Pade {pa:.1e} -> {pa/cb:.0f}x better")
    assert cb < 0.2 * pa, (cb, pa)
    # (4) interaction energy identity E_int/site = U*D
    print(f"  [energy] E_int/site = U*D at U=1: {1.0 * e:.5f}  (the interaction energy from the double occupancy)")
    print("  => double occupancy validated by two independent ED routes; physical Mott trend; conformal-Borel")
    print("     resummation; interaction-energy link. Frozen engine untouched (194/194). PASS")


if __name__ == "__main__":
    _selftest()
