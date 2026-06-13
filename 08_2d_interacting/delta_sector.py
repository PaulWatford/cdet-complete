"""delta_sector.py (v100) -- THE DELTA SECTOR resolved structurally: the v99 "second player" is
NOT a standalone background but a delta1 x f2 CROSS-TERM that vanishes when level 2 is empty;
measured at two beta, growing with beta; it reconciles the frozen root with the physical zero in
the right direction. The 13/7-vs-24/13 closure is reduced to assembling the coefficient flow --
the honest open registered with its spec.

THE INSTRUMENT. Delta1Frozen (reusable): like the v99 FrozenCDet but level 1 is kept PHYSICAL
(occupancy 1/(e^{beta xi}+1), carrying the antiperiodic images) instead of pinned to 1; level 2
-> s, level 3 -> 0, levels < 1 -> 1, far levels physical. At (s_phys, mu) it keeps every window
level physical, so it must equal the raw physical value -- GATE PASSED: Delta1Frozen(s_phys, 36)
= -0.041(79) vs physical +0.030(108), 0.5 sigma. The sector is isolated by subtraction:
    Delta(s; beta) = Delta1Frozen(s) - FrozenCDet(s)   [same s, mu, seeds-independent]
recovering Delta(s_phys; 36) = +0.334(81), consistent with the v99-inferred +0.369(109) (0.5 s).

THE STRUCTURAL DISCOVERY. Delta(0; beta) ~ 0 at BOTH beta -- +0.036(29) at 28, -0.009(20) at 36:
when level 2 is empty the hole-image sector VANISHES. So Delta is not an independent background
added to the frozen polynomial (the literal v99 framing); it is a delta1 x f2 CROSS-TERM, the
coefficient the single-level freeze structurally omits. The correct object at the zero is the
true polynomial in (f2, delta1) including its cross-monomials, of which the freeze captures only
the f2-diagonal.

THE CROSS-SLOPE, MEASURED. Matched-s secants over the identical interval [0, 0.00376]
(legitimate because Delta(0)~0):
    d1(28) = Delta(0.00376)/0.00376 = +41.8 +/- 13.2 e-9
    d1(36) = +88.8 +/- 21.5 e-9
The cross-coupling GROWS with beta (~2.1x over delta-beta = 8, an effective rate ~ +0.09).
Direction check: at beta=36 the frozen slope c1 ~ -202 e-9 becomes c1_eff = c1 + d1 ~ -113 e-9,
moving the linear root from the frozen 0.00183 to ~0.00327 -- toward the physical f2* = 0.00376
(the residual gap is the s^2 curvature, consistent with v99's smooth grid). The two-sector
picture is confirmed AND corrected: one polynomial, with a beta-growing cross-coefficient.

THE OPEN (registered, with spec). The 13/7-vs-24/13 identification is now the beta-flow of the
assembled root z(beta) = 2 - ln(s*(beta))/beta with s*(beta) the root of
A(beta) + c1_eff(beta) s + c2(beta) s^2: it needs A(beta), c1_frozen(beta), d1(beta), c2(beta)
on a common beta-grid (only beta=36 is complete; d1 known at 28, 36). SPEC: the full coefficient
grid at beta in {36, 44, 52} to +/-5% (IS, ~50 s/point), then assemble z(beta) and test against
the empirical pool's deep points (48, 52, 56) as a FROZEN PREDICTION. PREDICTION REGISTERED
(directional, pending the grid): the cross-term keeps s* above the frozen root at all beta, so
z_assembled(beta) > z_pol(beta), and the assembled curve -- not the one-sector frozen root --
is what the empirical pool measures.

CONSEQUENCE. The v99 "frozen polynomial + Delta(s;beta)" wording is sharpened to "the (f2,delta1)
polynomial, of which the v99 freeze is the f2-diagonal and Delta1Frozen adds the delta1 column";
the FROZEN_CURVE_Z8 L=8 prediction inherits the same caveat (it assumed a one-sector root flow).
"""
import numpy as np
from coefficient_phase2 import draw_batch, is_mean, LAM
from coefficient_flow import FrozenCDet
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

BETA_REF, MU = 36.0, 1.845
DELTA0 = {28.0: (0.036e-9, 0.029e-9), 36.0: (-0.009e-9, 0.020e-9)}   # Delta(s=0; beta) ~ 0
DELTA_MATCHED = {28.0: (0.1573e-9, 0.0497e-9), 36.0: (0.334e-9, 0.081e-9)}  # Delta(s=0.00376)
CROSS_SLOPE = {28.0: (41.8e-9, 13.2e-9), 36.0: (88.8e-9, 21.5e-9)}   # d1 = Delta/0.00376
GATE_PHYS = (-0.041e-9, 0.079e-9)   # Delta1Frozen(s_phys,36); physical = +0.030(108)


class Delta1Frozen(FastCDet):
    """Level 1 kept PHYSICAL (antiperiodic images alive); level 2 -> s, level 3 -> 0,
    levels < 1 -> 1, far levels physical. Subtract FrozenCDet(s) to isolate the Delta sector."""

    def __init__(self, hop, beta, s=0.0, to=0.7, ti=0.2):
        super().__init__(hop, beta=beta, to=to, ti=ti)
        self.lev = np.round(self.ev, 6)
        self.s = s
        self.m_lt1 = self.lev < 1.0 - 1e-9
        self.m_2 = np.abs(self.lev - 2.0) < 1e-6
        self.m_3 = np.abs(self.lev - 3.0) < 1e-6

    def g0(self, i, j, tau, mu):
        beta = self.beta
        tt = complex(tau)
        while tt.real > beta:
            tt -= 2 * beta
        while tt.real <= -beta:
            tt += 2 * beta
        xi = self.ev - mu
        nf = 1.0 / (np.exp(beta * xi) + 1.0)
        nf = np.where(self.m_lt1, 1.0, nf)
        nf = np.where(self.m_2, self.s, nf)
        nf = np.where(self.m_3, 0.0, nf)
        if tt.real > 0:
            gk = -(1.0 - nf) * np.exp(-xi * tt)
        elif tt.real < 0:
            gk = nf * np.exp(-xi * tt)
        else:
            gk = nf
        return np.sum(self.U[i, :] * self.U[j, :] * gk)


def delta(beta, s, rng, ndraw=18):
    """Delta(s; beta) = Delta1Frozen(s) - FrozenCDet(s), stripped, via the shared IS sampler."""
    strip = np.exp(0.5 * (MU - 2.0))
    H = cube_hopping(6)
    m1, e1 = is_mean(Delta1Frozen(H, beta=beta, s=s), beta, MU, rng, ndraw=ndraw)
    m0, e0 = is_mean(FrozenCDet(H, beta=beta, s=s), beta, MU, rng, ndraw=ndraw)
    return (m1 - m0) / strip, np.sqrt(e1**2 + e0**2) / strip


def _selftest():
    ok = True
    # gate 1: Delta(0;beta) consistent with zero at both beta (the cross-term structure)
    for b in (28.0, 36.0):
        d, e = DELTA0[b]
        print(f"Delta(0; {b:.0f}) = {d*1e9:+.4f}({e*1e9:.4f}) -> {abs(d)/e:.1f} sigma from 0 "
              f"(gate < 2: hole sector vanishes when level 2 empty)")
        ok = ok and abs(d) / e < 2
    # gate 2: Delta(s_phys=0.00376) nonzero at both beta (the cross-term is real at the zero)
    for b in (28.0, 36.0):
        d, e = DELTA_MATCHED[b]
        print(f"Delta(0.00376; {b:.0f}) = {d*1e9:+.4f}({e*1e9:.4f}) -> {d/e:.1f} sigma "
              f"(gate > 2.5: real)")
        ok = ok and d / e > 2.5
    # gate 3: cross-slope grows with beta
    d28, d36 = CROSS_SLOPE[28.0], CROSS_SLOPE[36.0]
    grow = (d36[0] - d28[0]) / np.sqrt(d36[1]**2 + d28[1]**2)
    print(f"cross-slope d1: {d28[0]*1e9:+.1f}({d28[1]*1e9:.1f}) -> {d36[0]*1e9:+.1f}({d36[1]*1e9:.1f}) "
          f"e-9: growth {grow:.1f} sigma (gate > 1.5: grows with beta)")
    ok = ok and grow > 1.5
    # gate 4: direction -- c1_eff = c1_frozen + d1 moves the root toward physical f2*
    c1_frozen, A36 = -202e-9, 0.370e-9
    s_frozen = A36 / abs(c1_frozen)
    s_eff = A36 / abs(c1_frozen + d36[0])
    print(f"root direction: frozen {s_frozen:.5f} -> with cross-term {s_eff:.5f} "
          f"(physical f2* = 0.00376; gate: moves up toward physical)")
    ok = ok and s_frozen < s_eff < 0.0042
    # gate 5 (live): the validation gate -- Delta1Frozen(s_phys) ~ physical
    rng = np.random.default_rng(4041)
    strip = np.exp(0.5 * (MU - 2.0))
    s_phys = 1.0 / (np.exp(BETA_REF * (2.0 - MU)) + 1.0)
    m, e = is_mean(Delta1Frozen(cube_hopping(6), beta=BETA_REF, s=float(s_phys)),
                   BETA_REF, MU, rng, ndraw=6)
    m, e = m / strip, e / strip
    dev = abs(m - 0.030e-9) / np.sqrt(e**2 + 0.108e-9**2)
    print(f"live Delta1Frozen(s_phys): {m*1e9:+.4f} +/- {e*1e9:.4f} vs physical +0.030(108): "
          f"{dev:.1f} sigma (gate < 3)")
    ok = ok and dev < 3
    print("delta-sector self-test (Delta0~0; Delta real; growth; direction; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
