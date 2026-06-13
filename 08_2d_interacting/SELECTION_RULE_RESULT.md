# Does the v116 sign(A,c1) selection rule survive to large L? (v127)

v116 found a physical root z exists iff **sign(A) ≠ sign(c1)** (the root s* = −A/c1 > 0 needs opposite
signs), and the sign pattern varied by geometry at L=6. Varying L at fixed sites (1,2,4) tests whether
the rule persists into the continuum.

**Frozen prediction (before measuring):** sign(A) is set by the continuum density-matrix Friedel
structure at the vertex displacements, which converges as L→∞, so sign(A)·sign(c1) → a fixed value — the
rule persists uniformly (always physical).

## Result — prediction partially falsified

| L | 8 | 10 | 12 | 16 | 20 | 24 | 32 | 40 | 48 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| sign A | − | − | + | − | − | − | − | − | − | − |
| sign c1 | + | + | − | + | + | **−** | + | **−** | + | + |
| physical? | Y | Y | Y | Y | Y | **N** | Y | **N** | Y | Y |

- **sign(A) converges** (stable −, one small-L flip at L=12) — the bulk background determinant, set by the
  continuum density matrix. As predicted.
- **sign(c1) Friedel-oscillates with L** — 24:−, 32:+, 40:−, 48:+ — and it is **seed-stable** (L=24 −,
  L=32 + reproduce across seeds 31/17/99; L=40 −, L=48 + across 31/17), so it is real Friedel structure,
  not Monte-Carlo noise. The probe eigenspace (the lowest-empty level) is a specific set of momenta that
  shifts around the Fermi surface as L changes (the number theory of which cosine-sum lands just above μ),
  and c1 — the response to occupying that eigenspace — oscillates with the probe momentum's Friedel phase
  at the vertex displacements. Same root cause as v117/v119, now in the **probe channel vs lattice size**.
- So the **selection-rule outcome alternates** yes/no with L. And since |c1| → 0 as the gap closes (the
  probe merges into the Fermi sea), the amplitude of the oscillation vanishes — the selection becomes
  **marginal** in the continuum.

## Correction (banked openly)

The rule does **not** uniformly persist. sign(A) persists; sign(c1) is a Friedel oscillation in L with
vanishing amplitude. **The v116 selection rule is a finite-gap (finite-L) Friedel phenomenon, not a
continuum invariant** — at the thermodynamic scale it dissolves into a marginal, oscillating remnant as
the probe response goes to zero. This sharpens v116/v119: both the background sign (A, geometry) and the
probe-response sign (c1, lattice size / probe momentum) are Friedel oscillations of the same elementary
density matrix; only the background survives to the continuum.

Reproduce: `./cpw grid 24 24 1 12 2048 31 0.002 2 2 1 2 4 1.0 -L <L> -fast` (read signed A at col 2, c1
at col 4) for L in {24,32,40,48}; `python3 selection_rule_continuum.py`. Frozen engine untouched (194/194).
