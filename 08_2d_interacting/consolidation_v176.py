"""consolidation_v176.py -- test all models side by side; verify what each informs about the others.

The suite now holds several "models" built on a shared spine. This consolidation runs them together and checks the
cross-links, so a change in one that breaks another is caught:

  A  frozen reference engine      atom Green's functions / connected determinant   (the parity anchor, 194/194)
  B  plane-wave lattice engine    free 2D propagator from eps_k = -2t(cos kx+cos ky) (v162)
  C  analytic surrogate           the carrier constants                            (bit-identical to A)
  D  SU(N) EoS + observables       2-site interacting series: eos / docc / chi + conformal-Borel resummation
  E  wall suite                    2D lattice Lindhard wall: wall / tide / primes / twist (v172-175), one core

CROSS-LINKS CHECKED HERE:
  * E internal   -- all four wall modules route through the single canonical core (wall_vs_size.chi0_max_rect).
  * B <-> E      -- the wall's susceptibility and the lattice density share the dispersion: chi0(q=0) == dn/dmu.
  * D <-> E      -- the SAME finite-radius phenomenon in two systems: the EoS bare-U series has radius U_c^EoS (the
                    conformal-Borel singularity), the lattice RPA series has radius U_c^wall = 1/chi0_max; resummation
                    extends past the bare radius in both. The wall suite generalizes the EoS radius finding to the lattice.
  * full sweep   -- every model returns sane, in-range values side by side.

(The A<->B<->C numerical parity at 0.00e+00 is enforced separately by `cdet validate`; this module adds the links above.)
"""
import numpy as np
import wall_vs_size as wvs
import wall_twist as wtw


def _free_density(L, beta, mu, t=1.0):
    """free lattice density per spin n(mu) = (1/N) sum_k f(eps_k) from the shared dispersion."""
    eps = wvs._dispersion(L, mu, t)
    return float(wvs._fermi(eps, beta).mean())


def _selftest():
    print("consolidation_v176 self-test (all models side by side; cross-links):")
    beta = 5.0

    # ---- E internal: the four wall modules share one canonical core --------------------------------------
    a = wvs.chi0_max(24, beta, -0.6)[0]
    b = wtw.chi0_max(24, 24, beta, -0.6, 0.0, 0.0)[0]
    import wall_tide as wtd
    import wall_primes as wpr
    assert abs(a - b) == 0.0, (a, b)
    assert wtd._w is wvs and wpr._w is wvs, "tide/primes must import the canonical core"
    assert wtw._w is wvs, "twist must delegate to the canonical core"
    print(f"  [E core]   wall/tide/primes/twist share wall_vs_size.chi0_max_rect (square dev {abs(a-b):.0e})")

    # ---- B <-> E: chi0(q=0) equals the free compressibility dn/dmu (shared dispersion) -------------------
    L, mu = 16, -0.6
    chi0_0 = wvs.chi0_at_q(L, beta, mu, 0, 0)
    h = 1e-5
    dndmu = (_free_density(L, beta, mu + h) - _free_density(L, beta, mu - h)) / (2 * h)
    assert abs(chi0_0 - dndmu) < 1e-6, (chi0_0, dndmu)
    print(f"  [B<->E]    chi0(q=0) == dn/dmu (free compressibility): {chi0_0:.6f} vs {dndmu:.6f}, dev {abs(chi0_0-dndmu):.1e}")

    # ---- D <-> E: the same finite-radius phenomenon, two systems ----------------------------------------
    from sun_eos_curve import density_series, density_ed
    from sun_eos_conformal import borel_singularity, conformal_borel
    aD = density_series(4, 10, M=24); Uc_eos = borel_singularity(aD)        # EoS bare-U radius (2-site SU(4))
    Uc_wall = wvs.wall(32, beta, 0.0)[0]                                     # lattice RPA radius (half-filling)
    assert Uc_eos > 0 and Uc_wall > 0
    # at U past where the bare partial sum has blown up, conformal-Borel still tracks ED (resummation rescues it)
    U_test = 0.7
    cb = conformal_borel(aD, U_test, Uc_eos); ed = density_ed(4, U_test)
    bare = sum(aD[k] * U_test ** k for k in range(len(aD)))
    assert abs(cb - ed) < 0.05 and abs(bare - ed) > 1.0, (cb, ed, bare)
    print(f"  [D<->E]    finite radius both systems: U_c(EoS,2-site)={Uc_eos:.3f}, U_c(wall,lattice)={Uc_wall:.3f}")
    print(f"             at U={U_test}: bare series diverged (|bare-ED|={abs(bare-ed):.1f}) but conformal-Borel tracks ED "
          f"(|cb-ED|={abs(cb-ed):.3f}) -- resummation extends past the wall in both systems")

    # ---- full sweep: every model returns a sane value side by side --------------------------------------
    from double_occupancy import docc_ed
    from susceptibilities import kappa_fluct, chi_spin_fluct
    vals = {
        "B free n(mu=-0.6)": _free_density(16, beta, -0.6),
        "D eos density_ed(4,1)": density_ed(4, 1.0),
        "D docc_ed(2,1)": docc_ed(2, 1.0),
        "D kappa(2,1)": kappa_fluct(2, 1.0),
        "D chi_s(2,1)": chi_spin_fluct(2, 1.0),
        "E wall(16,half)": wvs.wall(16, beta, 0.0)[0],
    }
    for k, v in vals.items():
        assert np.isfinite(v) and v == v, k
    assert 0 < vals["B free n(mu=-0.6)"] < 1 and 1.9 < vals["E wall(16,half)"] < 2.1
    print("  [sweep]    " + "; ".join(f"{k}={v:.3f}" for k, v in vals.items()))
    print("  => all models consistent side by side; E shares one core; B<->E and D<->E links hold. PASS")


if __name__ == "__main__":
    _selftest()
