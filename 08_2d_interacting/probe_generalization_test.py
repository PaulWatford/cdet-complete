"""probe_generalization_test.py (v114) -- does the v112-v113 mechanism generalize to other probes?

v112-v113 found z(inf)=2 because level 2 is BOTH the probe (the s-direction) AND the smallest gap.
These are confounded. This module separates them by moving the probe to a different level (the freeze
is generalized in cdet_stable_engine.c: set_freeze uses a PROBE level, grid arg 10). The mechanism's
naive prediction is z(inf) = the probe level, whatever it is.

RESULT -- the mechanism does NOT generalize, and the reason is physical:

  * probe=2 (CONTROL, the Fermi-surface level): c1 is finite and decaying (237 -> 156 over beta=24-72),
    z = 2 + ln(A/|c1|)/beta -> 2. Well-defined.

  * probe=3 (TEST): c1 DIVERGES exponentially, +2.72 per unit beta (3.8e19 -> 1.1e76 over beta=24-72).
    The coefficient is ill-defined.

WHY: probe=3 forces level 2 (the lowest EMPTY level, gap 0.155) to 0 while scanning level 3 (gap 1.155).
Making level 3 occupied with level 2 empty is a POPULATION INVERSION -- forbidden by Fermi statistics --
so the s-response diverges (the free-energy cost of the inversion grows with beta). The background A is
IDENTICAL for both (at s=0 both freezes leave levels 2,3 empty), confirming only the s-DIRECTION differs.

CONCLUSION: z(inf)=2 is LOCKED to level 2 not by coincidence but because level 2 is the unique
physically-scannable probe -- the lowest empty level, the Fermi surface. 'smallest gap' = 'Fermi surface'
= 'the only valid probe' are the same statement. This SHARPENS v113: level 2's smallest-gap property is
not merely why it de-confines most; it is why it is the only consistent probe at all."""
import numpy as np

MU = 1.845
BETA = np.array([24,40,56,72.])
# measured |c1| (stable C engine, fixed sites (1,2,4), cluster IS, MoM K=12 NT=3072, seed 31)
C1_PROBE2 = np.array([237.2577, 186.5545, 166.9956, 156.4076])      # finite, decaying
C1_PROBE3 = np.array([3.758023e19, 1.201473e39, 3.817350e58, 1.144818e76])  # divergent
A_BOTH    = np.array([1.260942, 0.2689339, 0.09095876, 0.04865487])  # identical for probe 2 & 3 (s=0)

def divergence_rate(c1):
    return np.polyfit(BETA, np.log(np.abs(c1)), 1)[0]

def _selftest():
    r2 = divergence_rate(C1_PROBE2)   # ~ 0 (slow decay)
    r3 = divergence_rate(C1_PROBE3)   # strongly positive (divergence)
    assert r2 < 0.05 and abs(r2) < 0.05, r2          # probe=2 c1 nearly flat/decaying
    assert r3 > 2.0, r3                               # probe=3 c1 diverges exponentially
    # background identical (only the s-direction differs)
    z2 = 2 + np.log(A_BOTH/np.abs(C1_PROBE2))/BETA
    assert z2[-1] > 1.85 and np.all(np.diff(z2) > 0)  # probe=2 flow rises toward 2
    xi2, xi3 = 2-MU, 3-MU
    assert xi2 < xi3                                   # level 2 is the lower (Fermi-surface) gap
    print("probe_generalization_test self-test:")
    print(f"  probe=2 (Fermi surface): |c1| rate {r2:+.3f} (finite); z flow -> {z2[-1]:.3f} -> 2.  WELL-DEFINED")
    print(f"  probe=3 (test):          |c1| rate {r3:+.3f} -> DIVERGES (3.8e19 -> 1.1e76); ill-defined")
    print(f"  background A identical for both (s=0): only the s-direction differs")
    print(f"  => population inversion (level 3 occupied, level 2 empty) is Fermi-forbidden -> divergence")
    print(f"  => z(inf)=2 is LOCKED to level 2 = the lowest empty level = the only valid probe.  PASS")

if __name__ == '__main__':
    _selftest()
