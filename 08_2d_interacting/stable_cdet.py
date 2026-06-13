"""stable_cdet.py (v103) -- THE CERTIFIED PRODUCTION ENGINE: a float64 CDet whose propagator is
evaluated in the LOG DOMAIN, so the deep-beta far-level antiperiodic images are NOT lost to
catastrophic cancellation. Certified against mp_cdet.MPCDet (dps 200) to ~1e-9 on the corner
configs where naive float64 is wrong by 8%-370%.

THE BUG IT FIXES. The engine propagator g0(i,j,tau,mu) = sum_k U[i,k] U[j,k] * occ_k * exp(-xi_k tau).
For tau near beta and a far OCCUPIED level (xi << 0), the particle branch needs
(1 - nf) exp(-xi tau) = exp(-xi tau - softplus(-beta xi)), an O(1) number -- but naive float64
computes (1 - nf) as 1.0 - 1.0 = 0 (nf rounds to 1), so the term VANISHES. These dropped terms
are exactly the antiperiodic images that carry the deep-beta structure. Because the corner
configs (clustered tau) dominate the heavy-tailed Monte Carlo (top 1% = 95% of the mass), naive
float64 corrupts every deep-beta tau-average.

THE FIX. Assemble each term's exponent in the log domain BEFORE exponentiating:
    particle (tau>0): amp_k = -exp(-xi_k tau - softplus(-beta xi_k))
    hole     (tau<0): amp_k = +exp(-xi_k tau - softplus( beta xi_k))
    equal-time      : amp_k = +exp(-softplus(beta xi_k))
softplus(x)=log(1+e^x) via np.logaddexp. Every exponent is <= 0 on the dominant branch, so each
term is bounded and the sum carries full float64 precision. No bignum, no speed cost (~2.3 ms/call
at L=6, identical to the naive vectorized engine).

WHAT THIS REVISES (see PRECISION_RESULT.md). The frozen-side coefficients are robust (the freeze
removes the far images anyway): A(36) stable +0.3754(128) vs naive 0.370(11), 0.3 sigma. But the
PHYSICAL-side measurements move: physical(1.845) stable -0.1915(48) vs naive +0.030(108) (~4
sigma, and the error bar HALVES because corner configs no longer inject float64 garbage). The
two-sector structure survives (faithfulness still falsified 3.2 sigma; Delta(s_phys) stable
+0.453(135) vs naive +0.334(81), 0.8 sigma), but the deep-beta ZERO LOCATION appeared to move ~4 sigma
-- but see v104 (deep_pool.py): that was a SINGLE importance-sampling draw whose error bar is
invalid under the stable integrand's residual heavy tail (alpha ~ 1.06). The robust
median-of-means re-measurement gives physical(1.845) = -0.077(60), CONSISTENT WITH ZERO, and the
pool SURVIVES (z(36) = 1.8428(40), 0.4 sigma from naive). The v103 "zero moves" claim is
withdrawn; the ENGINE correctness and the frozen-side results below stand. Deep-beta means now
require BOTH the stable engine AND median-of-means.
"""
import numpy as np
from cdet_port import CDet


def _softplus(x):
    return np.logaddexp(0.0, x)


class StableCDet(CDet):
    """Physical CDet with the log-domain propagator (no frozen occupancies)."""

    def g0(self, i, j, tau, mu):
        beta = self.beta
        tt = complex(tau).real
        while tt > beta: tt -= 2 * beta
        while tt <= -beta: tt += 2 * beta
        xi = self.ev - mu
        if tt > 0:
            amp = -np.exp(-xi * tt - _softplus(-beta * xi))
        elif tt < 0:
            amp = np.exp(-xi * tt - _softplus(beta * xi))
        else:
            amp = np.exp(-_softplus(beta * xi))
        return np.sum(self.U[i, :] * self.U[j, :] * amp)


class StableFrozen(CDet):
    """Log-domain frozen engine: window levels {<=occ -> 1, ==probe -> s, window & >occ -> 0},
    far levels PHYSICAL via the stable amplitude. mode='v99' (level 1 -> 1) or 'delta1' (level 1
    kept physical -- subtract the two to isolate the delta1 x f2 cross-term)."""

    def __init__(self, hop, beta, occ=1.0, probe=2.0, s=0.0, mode='v99', to=0.7, ti=0.2):
        super().__init__(hop, beta=beta, to=to, ti=ti)
        lev = np.round(self.ev, 6)
        self.s = s
        o = np.full(len(lev), np.nan)
        o[lev <= occ + 1e-9] = 1.0
        o[(lev > occ + 1e-9) & (lev <= 3.0 + 1e-9)] = 0.0
        o[np.abs(lev - probe) < 1e-6] = s
        if mode == 'delta1':
            o[np.abs(lev - 1.0) < 1e-6] = np.nan
        self.o = o
        self.frozen = ~np.isnan(o)

    def g0(self, i, j, tau, mu):
        beta = self.beta
        tt = complex(tau).real
        while tt > beta: tt -= 2 * beta
        while tt <= -beta: tt += 2 * beta
        xi = self.ev - mu
        if tt > 0:
            amp = -np.exp(-xi * tt - _softplus(-beta * xi))
            fv = -(1.0 - self.o) * np.exp(-xi * tt)
        elif tt < 0:
            amp = np.exp(-xi * tt - _softplus(beta * xi))
            fv = self.o * np.exp(-xi * tt)
        else:
            amp = np.exp(-_softplus(beta * xi))
            fv = self.o
        val = np.where(self.frozen, fv, amp)
        return np.sum(self.U[i, :] * self.U[j, :] * val)


def _selftest():
    from symmetry_reduction import cube_hopping
    import time
    hop = cube_hopping(6)
    ok = True
    # 1) benign beta=4 matches the naive port
    a = CDet(hop, beta=4.0).C_V([(1, 1.3), (2, 2.7), (4, 3.1)], 0.5).real
    b = StableCDet(hop, beta=4.0).C_V([(1, 1.3), (2, 2.7), (4, 3.1)], 0.5).real
    print(f"benign beta=4: stable vs naive rel dev {abs(a-b)/abs(b):.1e} (gate < 1e-9)")
    ok = ok and abs(a - b) / abs(b) < 1e-9
    # 2) certification against mpmath-200 on corner configs (the configs naive float64 gets wrong)
    try:
        from mp_cdet import MPCDet
        strip = np.exp(0.5 * (1.845 - 2.0))
        stb = StableCDet(hop, beta=36.0)
        rng = np.random.default_rng(11)
        worst_s = worst_n = 0.0
        for _ in range(3):
            taus = sorted(36.0 - rng.uniform(0, 2.0, 3))
            V = [(1, float(taus[0])), (2, float(taus[1])), (4, float(taus[2]))]
            truth = float(MPCDet(hop, beta=36.0, dps=200).C_V(V, 1.845)) / strip
            s = stb.C_V(V, 1.845).real / strip
            n = CDet(hop, beta=36.0).C_V(V, 1.845).real / strip
            worst_s = max(worst_s, abs(s - truth) / max(abs(truth), 1e-30))
            worst_n = max(worst_n, abs(n - truth) / max(abs(truth), 1e-30))
        print(f"deep-beta corner: STABLE rel {worst_s:.1e} (gate < 1e-6) vs naive-float64 rel {worst_n:.1e} (shown wrong)")
        ok = ok and worst_s < 1e-6 and worst_n > 1e-2
    except ImportError:
        print("  (mp_cdet unavailable; skipping mpmath certification)")
    # 3) speed
    t = time.time()
    cd = StableFrozen(hop, beta=36.0)
    for _ in range(50):
        cd.C_V([(1, 34.8), (2, 35.0), (4, 35.7)], 1.845)
    ms = (time.time() - t) / 50 * 1000
    print(f"StableFrozen speed: {ms:.1f} ms/call (gate < 10)")
    ok = ok and ms < 10
    print("stable_cdet self-test (benign; mpmath-certified corner; speed):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
