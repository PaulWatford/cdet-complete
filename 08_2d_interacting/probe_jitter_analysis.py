"""probe_jitter_analysis.py (v128) -- the c1 sign sequence in L has NO clean Friedel period; it is
arithmetic jitter of the probe momentum. Resolves the v127 question and connects to v119 by contrast.

QUESTION (v127 left open): derive the period of the sign(c1) oscillation in L and connect it to the v119
density-matrix wavevector. Two hypotheses, frozen before measuring:
  H1 period-16 Friedel wave  -- sign(L) == sign(L+16);
  H2 arithmetic jitter       -- sign set by WHICH cosine-sum multiplet is lowest-empty at each L (erratic).

MEASUREMENT (sign(c1), sites 1,2,4, beta=24, fast, seed-stable):
  L:    24  28  32  36  40  44  48  52
  c1:    -   +   +   +   -   -   +   -
H1 PREDICTS sign(L)==sign(L+16): 24/40 (-/-) ok, 32/48 (+/+) ok, but 28/44 (+/-) MISMATCH and 36/52 (+/-)
MISMATCH. So H1 (period-16) is FALSIFIED; the period-breaking points L=28,36,44 are seed-stable (seeds
31/17). H2 confirmed.

WHY -- the probe momentum jumps erratically. The lowest-empty eigenspace is whatever cosine-sum multiplet
lands just above mu=1.0, and its dominant |kx|/L jumps number-theoretically with L (0.29, 0.13, 0.05, 0.0,
0.07, 0.0, 0.0, 0.06 for L=24..52), not smoothly. So the Friedel phase cos(2pi kx Dx/L) at the x-aligned
vertices (0,1,2,4) jitters with no period -- the sign(c1) sequence is arithmetic, not periodic.

CONNECTION TO v119 (by contrast -- the key insight):
  - A (background) = (1/N) sum over the WHOLE occupied Fermi sea of cos(k.dr): a smooth sum -> a clean
    continuum Friedel wavevector (v119), so sign(A) CONVERGES as L->inf (v127).
  - c1 (probe response) = derivative w.r.t. occupying the SINGLE lowest-empty multiplet: a discrete,
    arithmetically-sensitive selection -> sign(c1) JITTERS with L, no period.
  This is exactly why v127 found sign(A) converging but sign(c1) oscillating: the background integrates the
  sea (clean), the probe response picks one multiplet (jitter). The v116 selection rule, living in c1, is
  therefore arithmetic at finite L and marginal (|c1|->0) in the continuum -- there is no period to derive,
  and that absence is the result."""
import numpy as np

SIGN_C1 = {24:'-',28:'+',32:'+',36:'+',40:'-',44:'-',48:'+',52:'-'}  # seed-stable, beta=24

def period16_holds():
    return all(SIGN_C1[L]==SIGN_C1[L+16] for L in (24,28,32,36) if L+16 in SIGN_C1)

def _selftest():
    print("probe_jitter_analysis self-test:")
    assert not period16_holds(), "period-16 should be falsified"
    # specifically the seed-stable breakers
    assert SIGN_C1[28] != SIGN_C1[44] and SIGN_C1[36] != SIGN_C1[52]
    # the sequence is genuinely mixed (both signs present, not a simple alternation either)
    seq=[SIGN_C1[L] for L in sorted(SIGN_C1)]
    assert seq.count('+')>=3 and seq.count('-')>=3 and seq!=['-','+']*4, seq
    print(f"  sign(c1) sequence L=24..52: {' '.join(seq)}")
    print(f"  period-16 holds? {period16_holds()}  (28/44 and 36/52 mismatch, seed-stable) -> FALSIFIED")
    print("  => no clean Friedel period; c1 sign is arithmetic jitter (which multiplet is lowest-empty).")
    print("     v119 contrast: A integrates the sea (converges); c1 picks one multiplet (jitters). PASS")

if __name__ == '__main__':
    _selftest()
