"""wall_tide.py (v173) -- the convergence wall is a "tide": its finite-size oscillations and their waves.

v172 showed the weak-coupling wall U_c(L)=1/chi0_max(L) drifts toward a thermodynamic limit. But it does not drift
smoothly -- it OSCILLATES, like a tide, because chi0(q,L) is a Brillouin-zone quadrature on a discrete L x L grid and
whether the peak momentum q* lands on a grid point depends on commensuration with L. This module works out those waves.

THE WAVES (beta=5):
  * PERIOD.  The oscillation period in L equals 2*pi / q*  (q* = peak/nesting momentum = the Fermi surface):
      - half-filling q*=(pi,pi)  -> period 2  (even/odd parity wave)
      - doping moves q* off (pi,pi) -> longer period, e.g. q*x=0.542 pi (mu=-2.8) -> period 2/0.542 = 3.7.
    So the tide's wavelength MEASURES the nesting vector.
  * BRANCH LAWS (commensurate / half-filling). The two interleaved branches converge by DIFFERENT laws:
      - on-grid (even L, peak captured): EXPONENTIAL convergence -- spectral accuracy of the BZ quadrature for the
        smooth finite-T integrand (deviation falls by ~0.5 every dL=2).
      - off-grid (odd L, peak missed by ~pi/L): 1/L^2 convergence -- a smooth peak's curvature times (pi/L)^2.
  * AMPLITUDE (tide height) decays with L: violent in "shallow water" (small L), calm in "deep water" (large L).
    Decreasing the lattice AMPLIFIES the waves; increasing it calms them.

All from the free dispersion (the v162 plane-wave feature); the frozen reference engine is untouched.
"""
import numpy as np
import wall_vs_size as _w


def uc_series(mu, Ls, beta=5.0):
    """U_c(L)=1/chi0_max(L) for each L in Ls."""
    return np.array([_w.wall(int(L), beta, mu)[0] for L in Ls])


def peak_q(mu, beta=5.0, L=48):
    """peak momentum q* (in pi units) at a large even L."""
    _, q = _w.chi0_max(L, beta, mu)
    return (2 * q[0] / L, 2 * q[1] / L)


def tide_period(mu, beta=5.0, Ls=None):
    """measured FFT period of the L-oscillation vs the prediction 2/|q*-component| (the nesting wavelength)."""
    if Ls is None:
        Ls = np.arange(16, 97)
    us = uc_series(mu, Ls, beta)
    det = us - np.polyval(np.polyfit(1.0 / Ls, us, 3), 1.0 / Ls)   # strip the smooth 1/L drift
    F = np.abs(np.fft.rfft(det)); fr = np.fft.rfftfreq(len(det))
    measured = 1.0 / fr[1 + int(np.argmax(F[1:]))]
    qx, qy = peak_q(mu, beta)
    comp = max(abs(qx), abs(qy))                                   # active (largest) incommensurate component
    predicted = 2.0 / comp if comp > 1e-9 else float("inf")
    return predicted, measured


def branch_laws(beta=5.0):
    """at half-filling: odd-branch power p (=> ~ -2 for 1/L^2) and even-branch deviation ratio per dL=2 (<1 => expo)."""
    Uinf = _w.wall(64, beta, 0.0)[0]
    odd = np.array([L for L in range(7, 48, 2)]); od = np.array([_w.wall(L, beta, 0.0)[0] - Uinf for L in odd])
    p = float(np.polyfit(np.log(odd), np.log(od), 1)[0])
    ev = np.array([L for L in range(4, 33, 2)]); evd = np.array([abs(_w.wall(L, beta, 0.0)[0] - Uinf) for L in ev])
    ratio = float(np.median(evd[1:] / evd[:-1]))
    return p, ratio, Uinf


def _selftest():
    print("wall_tide self-test (finite-size oscillations of the convergence wall -- the 'tide'):")
    beta = 5.0

    # (1) period law at half-filling: even/odd parity wave => period 2
    pred_h, meas_h = tide_period(0.0, beta, Ls=np.arange(8, 65))
    assert abs(meas_h - 2.0) < 0.2, meas_h
    print(f"  [period:half]  q*=(pi,pi) -> period 2 (even/odd): measured {meas_h:.2f}")

    # (2) period law incommensurate: period == 2*pi/q* (the nesting wavelength)
    pred_i, meas_i = tide_period(-2.8, beta)
    assert abs(meas_i - pred_i) / pred_i < 0.1, (pred_i, meas_i)
    print(f"  [period:doped] q*x=0.542pi -> predicted {pred_i:.2f}, measured {meas_i:.2f}  (period measures the Fermi surface)")

    # (3)/(4) branch laws: odd ~ 1/L^2, even exponential
    p, ratio, Uinf = branch_laws(beta)
    assert -2.4 < p < -1.5, p
    assert ratio < 0.7, ratio
    print(f"  [branches]     on-grid(even) ratio/dL=2 = {ratio:.2f} (exponential); off-grid(odd) p = {p:.2f} (~1/L^2)")

    # (5) amplitude decays with L (tide calms in deep water); both branches -> same TD limit
    s4 = _w.wall(5, beta, 0.0)[0] - _w.wall(4, beta, 0.0)[0]
    s32 = _w.wall(33, beta, 0.0)[0] - _w.wall(32, beta, 0.0)[0]
    assert s4 > s32 > 0 and s4 > 5 * s32, (s4, s32)
    even_inf = _w.wall(64, beta, 0.0)[0]; odd_inf = _w.wall(63, beta, 0.0)[0]
    assert abs(even_inf - odd_inf) < 0.05, (even_inf, odd_inf)
    print(f"  [amplitude]    wave height: L~4 split={s4:.2f} -> L~32 split={s32:.3f} (calms); branches meet at U_inf={even_inf:.4f}")
    print("  => the wall is a tide: period = 2pi/q* (the nesting vector), even=exponential / odd=1/L^2 branches,")
    print("     amplitude decaying with L. Frozen engine untouched. PASS")


if __name__ == "__main__":
    _selftest()
