"""spectral_channel_test.py (v113) -- tests the 'single de-confined mode' sharpening of v112.

THE PROPOSAL (external, sharpening v112): prove c1(beta) = sum_n a_n exp(-xi_n beta) with
xi_2 < xi_n for all n>2, so the phase fluctuations are entirely carried by the n=2 (level-2) sector
-> 'sign problem = one de-confined mode with gap (2-mu)'.

WHAT SURVIVES (vindicated, = v112):
  * xi_2 < xi_n IS TRUE. The gaps are xi_n = level_n - mu; level 2 (the probe) is the closest level
    to mu=1.845, gap xi_2 = 2-mu = 0.155, smaller than every other level above mu. The phase response
    (c1 = dC_V/ds) is carried by this single smallest-gap channel. The compression of the sign
    structure to one spectral object is REAL.

WHAT IS FALSIFIED (the literal form):
  * c1(beta) is NOT sum_n a_n exp(-xi_n beta). If it were, the n=2 term would make |c1| decay at rate
    xi_2 = 0.155 -> a factor exp(0.155*96) ~ 3e6 over beta=24..120. MEASURED: |c1| drops by 1.66x
    (effective rate 0.0046, 34x too small). The exponential-mode form overpredicts the decay by ~1e6.

WHY (the correction): c1 is a tau-AVERAGE, A=(1/beta^3) integral dtau^3. The level-2 exponential lives
  in the tau-PROPAGATOR, exp(-xi_2|dtau|), and SATURATES under integration:
  integral_0^beta exp(-xi_2 tau) dtau -> 1/xi_2 = 6.45 (converged by beta~48). So the smallest-gap
  channel contributes a beta^0 (rate-0) SATURATING factor, not an exp(-xi_2 beta) mode. That is exactly
  why integrated c1 is a POWER LAW (v112), and why z(beta) -> 2 as a ln(beta)/beta approach rather than
  pinned by an exponential gap. The gap (2-mu) sets the de-confinement RANGE 1/(2-mu)=6.5 in tau, and
  fixes the limit z(inf)=2 (the probe level sits at energy 2) -- but it is NOT a beta-decay rate.

NET: the 'single de-confined channel = level 2' picture is correct and is the real compression; 'with
gap (2-mu)' is right for the RANGE and the limit, wrong as a beta-rate. The object is a saturating
de-confined channel, not an exponential mode."""
import numpy as np

MU = 1.845
BETA = np.array([24,32,40,48,56,64,80,100,120.])
C1   = np.array([236.2667,204.7409,185.0052,177.1994,168.76,161.7939,152.7356,149.377,142.5189])

def gaps():
    """xi_n = level_n - mu for every distinct level; returns dict and the smallest positive gap."""
    g = {lev: lev - MU for lev in range(-6, 7)}
    pos = sorted((v, k) for k, v in g.items() if v > 0)
    return g, pos[0]   # smallest positive gap (value, level)

def test_exponential_form():
    """Compare the exp(-xi_2 beta) prediction to the measured |c1| decay."""
    xi2 = 2 - MU
    predicted_drop = np.exp(xi2 * (BETA[-1] - BETA[0]))
    measured_drop = C1[0] / C1[-1]
    eff_rate = -np.polyfit(BETA, np.log(C1), 1)[0]
    return {'xi2': xi2, 'predicted_drop': predicted_drop, 'measured_drop': measured_drop,
            'overprediction': predicted_drop / measured_drop, 'eff_rate': eff_rate}

def saturation(beta):
    """The tau-integral of the smallest-gap channel: integral_0^beta exp(-xi_2 tau) dtau -> 1/xi_2."""
    xi2 = 2 - MU
    return (1 - np.exp(-xi2 * beta)) / xi2

def _selftest():
    g, (gmin, lmin) = gaps()
    assert lmin == 2 and abs(gmin - (2 - MU)) < 1e-9, (lmin, gmin)         # level 2 is the smallest gap
    t = test_exponential_form()
    assert t['overprediction'] > 1e5, t['overprediction']                 # exponential form falsified
    assert t['eff_rate'] < 0.02, t['eff_rate']                            # measured rate ~ 0, not 0.155
    assert abs(saturation(96) - 1/(2-MU)) < 1e-2                          # channel saturates
    print("spectral_channel_test self-test:")
    print(f"  smallest gap: level {lmin}, xi_2 = {gmin:.3f}  (xi_2 < xi_n for all n>2: TRUE -- phase carried by n=2)")
    print(f"  exp(-xi_2 beta) form: predicts {t['predicted_drop']:.1e}x decay, measured {t['measured_drop']:.2f}x")
    print(f"    -> overpredicts by {t['overprediction']:.1e}x; |c1| effective rate {t['eff_rate']:.4f} (xi_2=0.155)  FALSIFIED")
    print(f"  saturation: integral_0^96 exp(-xi_2 tau) dtau = {saturation(96):.3f} -> 1/xi_2 = {1/(2-MU):.3f} (rate-0 factor)")
    print(f"  => single de-confined CHANNEL (level 2) is real; it SATURATES (not an exp mode); gap (2-mu)")
    print(f"     = the de-confinement range 1/xi_2={1/(2-MU):.1f} and the limit z(inf)=2, NOT a beta-rate.  PASS")

if __name__ == '__main__':
    _selftest()
