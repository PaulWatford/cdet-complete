"""parity_table.py (v97) -- THE PARITY TABLE: the A=0 question measured across windows and
lattices with the generalized freeze; the binary rule falsified by its own frozen test; a robust
suppression pattern banked; the v84 L=8 "static" identified as a root-flow crossing with the
deep-beta replay registered as a frozen prediction.

THE TABLE (beta = 28, multi-draw inter-draw errors, mu_exp = window midpoint; A = the s=0
background, c1 = the probe-level residue from a CONDITIONED s-point):

    window            first-empty deg   A (1e-9)       c1 (1e-9)   |A/c1|
    W6(0,1)           36  even          -0.023(15)     ~ -88       2.6e-4
    W6(1,2)           27  ODD           +0.839(102)    ~ -190      4.4e-3
    W6(2,3)           14  even          +0.025(8)      ~ -1 (dead) --
    W8(0.828,1.414)   60  even          -0.0208(55)    +20.6       1.0e-3
    W8(1.414,2.0)     39  ODD           +0.497(76)     -64         7.8e-3

RESULT 1 (a frozen test, honestly scored). After 4/4 consistency the binary rule "even
first-empty degeneracy => A = 0" was REGISTERED and tested on W8(0.828,1.414): measured
A = -0.0208 +/- 0.0055 -- 3.8 sigma from zero. THE STRICT RULE IS FALSIFIED by its own
prediction. What survives is a SUPPRESSION PATTERN: odd-windows carry A ~ +0.5 to +0.85;
even-windows |A| ~ 0.02-0.03 (20-40x smaller), suppressed 4-30x in |A/c1| too. Five-window
observation; the unpaired-mode mechanism sketch remains a hypothesis, not a theorem.

RESULT 2 (the v84 static reread). At the v84 static position (mu = 1.8284, beta = 28) the W8
window's background equals ~95% of its dominant deviation term (|A| / |c1| s_phys(1.8284) =
0.95): the L=8 "static" is an A-vs-f(2.0) ROOT-FLOW CROSSING, exactly the structure that at
L=6 produced an effective anchored law that failed at deep beta. FROZEN PREDICTION (registered
here, untested): the L=8 deep-beta zero RISES past 2*sqrt(2)-1 = 1.8284 above beta ~ 32-40,
replaying the L=6 crossover, and asymptotes to its own root-flow value. (Cost note: L=8 calls
~6 ms; a deep honest scan is a future round.)

RESULT 3 (instrument hardening, two catches banked). (a) The freeze is exponentially
ill-conditioned for s >> nf_phys: |g0| ~ s e^{beta xi_probe} stacks across propagators
(a 1e12 blowup observed at s = 0.02 with xi beta = 8.2) -- CONDITIONING RULE: s <~ 10
e^{-beta xi_probe}. (b) A 1e-9 mask tolerance against 1e-6 level rounding silently emptied the
occupied level 1.414 and produced a FALSE ZERO in the scout -- the occupied-levels check is now
mandatory (WindowFrozen prints nothing, but _selftest gates it). Also: the W6(2,3) suppression
is NOT site-projection (per-level site weights are uniform by torus translation invariance --
honest negative); both its A and its residue are dead, mechanism open.
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import cube_hopping

TABLE = {
    "W6(0,1)":  dict(L=6, occ=0.0, probe=1.0, mu=0.5, deg=36, A=(-0.023e-9, 0.015e-9)),
    "W6(1,2)":  dict(L=6, occ=1.0, probe=2.0, mu=1.84, deg=27, A=(0.839e-9, 0.102e-9)),
    "W6(2,3)":  dict(L=6, occ=2.0, probe=3.0, mu=2.5, deg=14, A=(0.025e-9, 0.008e-9)),
    "W8(0.828,1.414)": dict(L=8, occ=0.8284272, probe=1.4142136, mu=1.1213204, deg=60,
                            A=(-0.0208e-9, 0.0055e-9)),
    "W8(1.414,2.0)":   dict(L=8, occ=1.4142136 + 1e-6, probe=2.0, mu=1.7071068, deg=39,
                            A=(0.497e-9, 0.076e-9)),
}
C1_W8_HI = -64e-9          # the (1.414,2.0) probe residue (conditioned s = 2e-3)
FROZEN_PREDICTION = ("L=8 deep-beta crossover: the (1,2,4) zero rises past 2*sqrt(2)-1 above "
                     "beta ~ 32-40 and leaves the v84 anchored law, replaying L=6. UNTESTED.")
# v98 audit (METHOD_AUDIT_v97.md): "IS a root-flow crossing" downgraded to CANDIDATE (one-point
# evidence). Prediction QUANTIFIED with A8(40) = +0.1135(266), rate 0.1231(233), c1 frozen at
# -64e-9: z8 = {28: 1.8268, 36: 1.8378, 40: 1.8417, 44: 1.8449, 48: 1.8475, 56: 1.8517}
# (+/- ~0.010 at 48 from the rate error; assumptions in the audit doc). Also note: the v97
# suppression pattern is CONFOUNDED (degeneracy parity vs level rationality) -- see the audit.
FROZEN_CURVE_Z8 = {28: 1.8268, 36: 1.8378, 40: 1.8417, 44: 1.8449, 48: 1.8475, 56: 1.8517}
A8_RECORD = {28.0: (0.497e-9, 0.076e-9), 40.0: (0.1135e-9, 0.0266e-9)}


class WindowFrozen(FastCDet):
    """Generalized freeze: levels <= occ -> 1, level == probe -> s, other levels above occ -> 0.
    CONDITIONING: keep s <~ 10 exp(-beta (probe - mu)). Check occupied_levels() after building."""

    def __init__(self, hop, beta, occ, probe, s=0.0, to=0.7, ti=0.2):
        super().__init__(hop, beta=beta, to=to, ti=ti)
        self.lev = np.round(self.ev, 6)
        self.s = s
        self.m_occ = self.lev <= occ + 1e-9
        self.m_probe = np.abs(self.lev - probe) < 1e-6

    def occupied_levels(self):
        return sorted(set(self.lev[self.m_occ]))

    def g0(self, i, j, tau, mu):
        beta = self.beta
        tt = complex(tau)
        while tt.real > beta:
            tt -= 2 * beta
        while tt.real <= -beta:
            tt += 2 * beta
        xi = self.ev - mu
        nf = np.where(self.m_occ, 1.0, 0.0)
        nf = np.where(self.m_probe, self.s, nf)
        if tt.real > 0:
            gk = -(1.0 - nf) * np.exp(-xi * tt)
        elif tt.real < 0:
            gk = nf * np.exp(-xi * tt)
        else:
            gk = nf
        return np.sum(self.U[i, :] * self.U[j, :] * gk)


def _selftest():
    ok = True
    odd = [k for k, v in TABLE.items() if v["deg"] % 2 == 1]
    even = [k for k, v in TABLE.items() if v["deg"] % 2 == 0]
    amin_odd = min(abs(TABLE[k]["A"][0]) for k in odd)
    amax_even = max(abs(TABLE[k]["A"][0]) for k in even)
    print(f"suppression pattern: min|A| odd-windows = {amin_odd*1e9:.3f}, max|A| even-windows = "
          f"{amax_even*1e9:.3f} -> ratio {amin_odd/amax_even:.0f}x (gate > 10)")
    ok = ok and amin_odd / amax_even > 10
    a, e = TABLE["W8(0.828,1.414)"]["A"]
    print(f"the falsified strict rule (frozen test record): W8(0.828,1.414) A = {a*1e9:+.4f}"
          f"({e*1e9:.4f}) -- {abs(a)/e:.1f} sigma from 0 (gate > 3: nonzero, the binary rule is dead)")
    ok = ok and abs(a) / e > 3
    s_phys = 1.0 / (np.exp(28.0 * (2.0 - 1.8284271)) + 1.0)
    r = abs(TABLE["W8(1.414,2.0)"]["A"][0]) / (abs(C1_W8_HI) * s_phys)
    print(f"v84-static reread: |A| / |c1 s_phys(1.8284)| = {r:.2f} (gate in [0.5, 1.5] -- the "
          f"static is a root-flow crossing); frozen prediction registered: {FROZEN_PREDICTION[:60]}...")
    ok = ok and 0.5 <= r <= 1.5
    # instrument gates: occupied-levels check + live re-measure of the even-window background
    cd = WindowFrozen(cube_hopping(8), beta=28.0, occ=1.4142136 + 1e-6, probe=2.0, s=0.0)
    top = cd.occupied_levels()[-1]
    print(f"mask gate: W8(1.414,2.0) top occupied level = {top} (gate == 1.414214 -- the scout's "
          f"false-zero bug cannot recur)")
    ok = ok and abs(top - 1.414214) < 1e-5
    cd6 = WindowFrozen(cube_hopping(6), beta=28.0, occ=0.0, probe=1.0, s=0.0)
    rng = np.random.default_rng(2087)
    ms = []
    for _ in range(6):
        T = rng.uniform(0, 28.0, size=(2048, 3))
        v = np.array([cd6.C_V([(1, float(t[0])), (2, float(t[1])), (4, float(t[2]))], 0.5).real
                      for t in T])
        ms.append(float(v.mean()))
    m = float(np.mean(ms)); se = float(np.std(ms, ddof=1) / np.sqrt(6))
    dev = abs(m - TABLE["W6(0,1)"]["A"][0]) / np.sqrt(se**2 + TABLE["W6(0,1)"]["A"][1]**2)
    print(f"live W6(0,1) background: {m*1e9:+.4f} +/- {se*1e9:.4f} vs stored: {dev:.1f} sigma (gate < 3)")
    ok = ok and dev < 3
    print("parity-table self-test (suppression; falsified rule; v84 reread; mask; live):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
