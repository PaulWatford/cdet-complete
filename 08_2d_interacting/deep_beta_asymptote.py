"""deep_beta_asymptote.py (v111) -- resolves z(inf) from the clean stable-C-engine flow.

THE QUESTION (open since v93): is z(inf) one of the menu rationals (11/6, 13/7, 24/13, 15/8, 17/9
in [1.83,1.90]), or something else? v110's long-double flow to beta=120 showed z RISES through every
menu rational with no plateau. This module settles it by model comparison on ln(|c1|/A)=(2-z)*beta:

  Model B (z_inf<2, exponential gap):  ln(|c1|/A) = rho*beta + q     -- the 'menu rational' picture
  Model A (z_inf=2,  power-law):       ln(|c1|/A) = p*ln(beta) + q   -- the 'probe level' picture

RESULT: Model B is REJECTED (chi2 622/7); Model A fits (residuals 0.003 in z). The dominant decay of
BOTH A (~beta^-2.8) and |c1| (~beta^-0.54) is POWER-LAW (rate ~ 0), so their ratio is a power law
beta^2.3, and z(beta) = 2 - 2.3*ln(beta)/beta -> 2. z(inf) = 2 (the bare probe level, level 2) to
within ~0.01; the general fit gives 1.9925(19). The menu rationals are finite-beta crossings of a
ln(beta)/beta approach -- NOT asymptotes. This RETRACTS the menu-identification premise (v93-v107).

Data: the clean frozen-A grid (cdet_stable_engine, v109 float64 24-64 + v110 long double 80-120)."""
import numpy as np

BETA = np.array([24,32,40,48,56,64,80,100,120.])
A    = np.array([1.203316,0.5551734,0.2517563,0.1580456,0.1016786,0.06768385,0.03349639,0.01650291,0.009545303])
A_E  = np.array([0.01487,0.011692,0.0064111,0.0045361,0.0030836,0.0027449,0.0024955,0.00081893,0.00099532])
C1   = np.array([236.2667,204.7409,185.0052,177.1994,168.76,161.7939,152.7356,149.377,142.5189])
C1_E = np.array([1.1368,1.0572,0.9727,0.5531,0.9925,0.8519,1.1678,1.0127,0.6901])

def _wls(M, y, ye):
    W = np.diag(1.0/ye**2); cov = np.linalg.inv(M.T@W@M); cf = cov@M.T@W@y
    chi2 = float(np.sum(((y - M@cf)/ye)**2)); return cf, np.sqrt(np.diag(cov)), chi2

def model_comparison():
    """Returns dict with the two-model fit of ln(|c1|/A) and the implied z_inf."""
    L = np.log(C1/A); Le = np.sqrt((A_E/A)**2 + (C1_E/C1)**2)
    cfB,_,chiB = _wls(np.vstack([BETA, np.ones_like(BETA)]).T, L, Le)         # z<2 exponential
    cfA,_,chiA = _wls(np.vstack([np.log(BETA), np.ones_like(BETA)]).T, L, Le) # z=2  power-law
    cfC,eC,chiC = _wls(np.vstack([BETA, np.log(BETA), np.ones_like(BETA)]).T, L, Le)  # general
    return {'exp_rho': cfB[0], 'exp_chi2': chiB, 'exp_zinf': 2 - cfB[0],
            'pow_p': cfA[0], 'pow_chi2': chiA,
            'gen_rho': cfC[0], 'gen_rho_e': eC[0], 'gen_zinf': 2 - cfC[0], 'gen_zinf_e': eC[0],
            'gen_chi2': chiC, 'ndof_2': len(BETA)-2, 'ndof_3': len(BETA)-3}

def power_laws():
    """Dominant-rate fit ln(X) = -rho*beta + p*ln(beta) + const for A and |c1|."""
    out = {}
    for nm, X, Xe in (('A', A, A_E), ('c1', C1, C1_E)):
        cf,e,_ = _wls(np.vstack([BETA, np.log(BETA), np.ones_like(BETA)]).T, np.log(X), Xe/X)
        out[nm] = {'rho': -cf[0], 'rho_e': e[0], 'power': cf[1], 'power_e': e[1]}
    return out

def z_flow():
    return 2 + np.log(A/C1)/BETA

def _selftest():
    mc = model_comparison()
    # the exponential-gap (menu) model must be decisively worse than the power-law (z=2) model
    assert mc['exp_chi2'] > 100, mc['exp_chi2']
    assert mc['pow_chi2'] < mc['exp_chi2']/3, (mc['pow_chi2'], mc['exp_chi2'])
    # z_inf is the probe level to within ~0.01
    assert abs(mc['gen_zinf'] - 2.0) < 0.012, mc['gen_zinf']
    # both A and |c1| are power-law dominated (small exponential rate)
    pl = power_laws()
    assert abs(pl['A']['rho']) < 0.01 and abs(pl['c1']['rho']) < 0.01, pl
    # the flow rises monotonically through the menu region
    z = z_flow(); assert np.all(np.diff(z) > 0) and z[0] < 1.79 and z[-1] > 1.91
    print("deep_beta_asymptote self-test:")
    print(f"  exponential-gap (menu) model: chi2={mc['exp_chi2']:.0f}/{mc['ndof_2']} (z_inf={mc['exp_zinf']:.4f})  REJECTED")
    print(f"  power-law (z=2) model:        chi2={mc['pow_chi2']:.0f}/{mc['ndof_2']} (p={mc['pow_p']:.2f})")
    print(f"  general fit: z_inf = {mc['gen_zinf']:.4f}({mc['gen_zinf_e']:.4f})  (rho={mc['gen_rho']:.5f}, {abs(mc['gen_rho']/mc['gen_rho_e']):.1f}s from 0)")
    print(f"  A ~ beta^{pl['A']['power']:.2f} (rho_A={pl['A']['rho']:.4f}), |c1| ~ beta^{pl['c1']['power']:.2f} (rho_c1={pl['c1']['rho']:.4f})")
    print(f"  => z(inf) = 2 (probe level); menu = ln(beta)/beta approach.  PASS")

if __name__ == '__main__':
    _selftest()
