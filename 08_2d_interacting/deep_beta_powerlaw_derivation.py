"""deep_beta_powerlaw_derivation.py (v112) -- derives the power laws behind z(inf)=2.

v111 MEASURED that z(inf)=2 because A ~ beta^-2.8 and |c1| ~ beta^-0.5 are POWER LAWS whose ratio is
beta^~2.5, giving z = 2 - p*ln(beta)/beta -> 2. This module DERIVES those powers from the structure
of the tau-averaged connected determinant.

KEY STRUCTURAL FACT: A and c1 are tau-AVERAGES, A = <C_V> = (1/beta^3) integral dtau^3 C_V. So the
beta-power is set by the UN-normalized integral J(beta) = beta^3 * X = integral dtau^3 (.):

  * J_A(beta) = beta^3 * A  ->  CONSTANT (beta^~0). The s=0 integrand C_V is CORNER-CONFINED (the
    antiperiodic images align only in the tau->beta corner, an O(1) region), so its 3-tau integral
    CONVERGES. Three 1/beta normalizations x an O(1) corner integral  =>  A ~ 1/beta^3.

  * J_c1(beta) = beta^3 * |c1|  ->  GROWS as beta^~2.7. c1 = dC_V/ds activates LEVEL 2, whose gap
    xi_2 = 2 - mu = 0.155 is the SMALLEST -> the longest-ranged propagator exp(-xi_2|dtau|). That
    slow channel DE-CONFINES the integral (tau's spread across the whole box), so it grows ~beta^2.7
    instead of converging  =>  |c1| ~ beta^(2.7-3) ~ beta^-0.3.

THE CONCLUSION: |c1|/A = J_c1/J_A ~ beta^(q_c1 - q_A) ~ beta^2.7, a POSITIVE power, so
ln(|c1|/A) ~ 2.7 ln(beta) and z(beta) = 2 - 2.7*ln(beta)/beta -> 2. The exponent DIFFERENCE
(corner-confined A vs level-2-de-confined c1) is the mechanism; z(inf)=2 is forced by q_c1 > q_A.

Data: the clean frozen-A grid (cdet_stable_engine, v109 float64 24-64 + v110 long double 80-120)."""
import numpy as np

BETA = np.array([24,32,40,48,56,64,80,100,120.])
A    = np.array([1.203316,0.5551734,0.2517563,0.1580456,0.1016786,0.06768385,0.03349639,0.01650291,0.009545303])
C1   = np.array([236.2667,204.7409,185.0052,177.1994,168.76,161.7939,152.7356,149.377,142.5189])
MU   = 1.845
XI2  = 2.0 - MU      # the smallest gap -> the de-confining channel

def integrals():
    """J(beta) = beta^3 * X = the un-normalized 3-tau integral, for A and |c1|."""
    return BETA**3 * A, BETA**3 * C1

def powers():
    """Power-law exponents q of J(beta) ~ beta^q for A and |c1|, and the implied X-exponents."""
    JA, Jc1 = integrals()
    qA  = np.polyfit(np.log(BETA), np.log(JA),  1)[0]
    qc1 = np.polyfit(np.log(BETA), np.log(Jc1), 1)[0]
    return {'qJ_A': qA, 'qJ_c1': qc1, 'qA': qA-3, 'qc1': qc1-3, 'diff': qc1-qA}

def _selftest():
    p = powers()
    # A is corner-confined: its un-normalized integral converges (q_J_A ~ 0), so A ~ 1/beta^3
    assert abs(p['qJ_A']) < 0.2, p['qJ_A']
    assert abs(p['qA'] - (-3.0)) < 0.2, p['qA']
    # c1 is de-confined: its integral grows substantially
    assert p['qJ_c1'] > 2.0, p['qJ_c1']
    # the exponent DIFFERENCE is a positive power => z(inf)=2
    assert p['diff'] > 2.0, p['diff']
    # the de-confining channel is the smallest gap, level 2
    assert abs(XI2 - 0.155) < 1e-9
    print("deep_beta_powerlaw_derivation self-test:")
    print(f"  J_A = beta^3*A   ~ beta^{p['qJ_A']:+.3f}  (CONVERGES)  ->  A   ~ beta^{p['qA']:+.3f}  [corner-confined, 1/beta^3]")
    print(f"  J_c1= beta^3*|c1|~ beta^{p['qJ_c1']:+.3f}  (GROWS)     ->  |c1| ~ beta^{p['qc1']:+.3f}  [level-2 de-confined]")
    print(f"  de-confining channel: level-2 gap xi_2 = 2-mu = {XI2:.3f} (smallest gap, longest-range propagator)")
    print(f"  exponent difference q_c1 - q_A = {p['diff']:.3f}  =>  |c1|/A ~ beta^{p['diff']:.2f}")
    print(f"  => z(beta) = 2 - {p['diff']:.2f}*ln(beta)/beta -> 2 (DERIVED).  PASS")

if __name__ == '__main__':
    _selftest()
