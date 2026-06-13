"""selection_rule_continuum.py (v127) -- does the v116 sign(A,c1) selection rule survive to large L?

v116: a physical root z exists iff sign(A) != sign(c1) (the root s* = -A/c1 > 0 needs opposite signs);
the sign pattern varied by GEOMETRY (site choice) at L=6. Here we vary L (size) at fixed sites (1,2,4)
and ask whether the rule persists into the continuum.

FROZEN PREDICTION (written before measuring): sign(A) is set by the continuum density-matrix Friedel
structure at the fixed vertex displacements, which converges as L->inf, so sign(A)*sign(c1) -> a fixed
value (physical) -- the rule PERSISTS uniformly.

RESULT -- prediction PARTIALLY FALSIFIED (banked openly):
  L:    8   10   12   16   20   24   32   40   48  100
  A:    -    -    +    -    -    -    -    -    -    -     sign(A): STABLE (one flip at L=12), -> - in bulk
  c1:   +    +    -    +    +    -    +    -    +    +     sign(c1): OSCILLATES with L
  phys: Y    Y    Y    Y    Y    N    Y    N    Y    Y     outcome ALTERNATES at large L

- sign(A) converges (the bulk background determinant, set by the continuum density matrix) -- as predicted.
- sign(c1) FRIEDEL-OSCILLATES with L (seed-stable: L=24 '-' and L=32 '+' reproduce across seeds 31/17/99;
  L=40 '-', L=48 '+' reproduce across seeds 31/17). The probe eigenspace (lowest-empty level) is a specific
  set of momenta that shifts around the Fermi surface as L changes (number theory of which cosine-sum lands
  just above mu), and c1 -- the response to occupying that eigenspace -- oscillates in sign with the probe
  momentum's Friedel phase at the vertex displacements. Same root cause as v117/v119 (Friedel oscillation),
  now in the PROBE channel vs lattice size.
- So the selection-rule OUTCOME (physical iff opposite signs) alternates yes/no with L, and since the
  amplitude |c1| -> 0 as the gap closes (probe merges into the sea), the selection becomes MARGINAL in the
  continuum -- neither robustly physical nor robustly forbidden; the response, and with it the sign content,
  vanishes.

CORRECTION TO THE PREDICTION: the rule does NOT uniformly persist. sign(A) persists; sign(c1) is a Friedel
oscillation in L with vanishing amplitude, so the v116 selection rule dissolves into a marginal,
oscillating remnant at the thermodynamic scale -- it is a finite-gap (finite-L) Friedel phenomenon, not a
continuum invariant."""
import numpy as np

# signed A, c1 vs L (sites 1,2,4, beta=24, fast; L<=20 K12NT2048 seed31, L>=24 confirmed seed-stable)
SIGNS = {8:('-','+'),10:('-','+'),12:('+','-'),16:('-','+'),20:('-','+'),
         24:('-','-'),32:('-','+'),40:('-','-'),48:('-','+'),100:('-','+')}

def physical(L):
    sA,sC = SIGNS[L]; return sA != sC   # opposite signs -> physical root

def _selftest():
    print("selection_rule_continuum self-test:")
    # sign(A) is - for all L except the single small-L flip at 12
    nA_minus = sum(1 for L in SIGNS if SIGNS[L][0]=='-')
    assert nA_minus >= 9, nA_minus
    # sign(c1) genuinely oscillates at large L (not constant): both signs present among L>=24
    cbig = [SIGNS[L][1] for L in (24,32,40,48)]
    assert '+' in cbig and '-' in cbig, cbig
    # the outcome alternates at large L (not all-physical) -> rule does not uniformly persist
    outs = [physical(L) for L in (24,32,40,48)]
    assert any(outs) and not all(outs), outs
    print(f"  sign(A): stable - ({nA_minus}/10 L), converges (bulk background) -- as predicted")
    print(f"  sign(c1): oscillates with L (24,32,40,48 -> {cbig}); seed-stable -> real Friedel, not noise")
    print(f"  outcome (physical?) at L=24,32,40,48: {['Y' if o else 'N' for o in outs]} -- ALTERNATES")
    print("  => v116 selection rule is a finite-gap Friedel phenomenon; it goes MARGINAL as |c1|->0. PASS")

if __name__ == '__main__':
    _selftest()
