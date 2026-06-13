# Full dual consolidation at the sign frontier (v120): the surrogate gains a sign side, and the consolidation produces a sharper theorem than the experiments did

Both C layers consolidated with every proven advance through v119. Since v115 the entire **sign side**
opened (v116–v119), and the consolidation closed a real gap: the surrogate was **scale-only**.

## What was missing, now fixed

- **Surrogate had no sign-side presence.** It carried z(∞)=2 but nothing about the sign. The sign side
  lived entirely in Python (the elementary ρ(0,r) in `frozen_friedel_map.py`) and in the C determinant
  engines (which compute A, whose sign is a superposition). Fixed: the surrogate now carries the
  sign-side's analytic core — `surr_l6_gap_modes(lo,hi)` and `surr_l6_occupied(mu)` over the cube's
  integer multiplicities `ATLAS_L6_MULT`, plus the dominant Friedel wavevector — confirmable in C with
  **no eigendecomposition**, matching the Python ground truth exactly (gap(1,2)=0, occ=156=156).
- **Brute-force C** re-stamped v120 with a sign-side pointer (it computes A; the elementary object is
  ρ; the distilled rigidity is the surrogate carrier).
- **Stable engine CLI doc** was stale (no sites/μ args) — fixed.

## The sharper theorem the consolidation produced

Distilling the sign side for a carrier forced the question *why* is μ-rigidity exact. The answer is
cleaner and more general than v118/v119 stated: **the cube_hopping(6) spectrum is integer-valued**
(eigenvalues −6..6, multiplicities {1,6,12,14,27,36,24,36,27,14,12,6,1}, sum 216). Because **no mode
lies in any open unit interval (n,n+1)**, the frozen occupied set is identical for every μ in such an
interval — the freeze is exactly μ-rigid in *any* unit interval, jumping only when μ crosses an
integer. v118/v119 found this for (1,2); the consolidation generalized it and made it a one-line,
eigendecomposition-free check.

## Rebuild test — all green

Surrogate gate, stable C (f64 + long double validate), stable propagator (benign + deep), brute drivers
(benign), five analysis modules (scale + sign side), frozen engine 194/194, constants bit-identical.

## Side-by-side — three layers × two axes

| | surrogate | brute-force C | stable C engine | Python |
|---|---|---|---|---|
| **scale** z(∞) | carries 2.0 | too shallow | derives 2.0 | — |
| **sign** elementary ρ | — | — | — | computes (eig) |
| **sign** determinant A | — | A (benign) | A (deep) | — |
| **sign** μ-rigidity | **carries (no eig)** | — | — | proves (eig) |

Engine-level check: the **occupied set, ρ, and sign(A) are exactly μ-rigid**; z-flow is rigid to ~0.005
(ratio); |A| has a weak residual μ-dependence (~12% over (1,2)) that changes neither the sign nor the
z=2 asymptote.

## The lessons — what the dual story reveals can improve on both

1. **The sign side is a chain, like the scale side.** Elementary ρ (Python, eigendecomposition) →
   determinant A's sign (C engines, superposition) → distilled carriers (surrogate, no eig). The full
   Friedel *map* needs the eig (Python); the *discrete facts* (μ-rigidity, occupied counts) are cheap
   (surrogate); the *observable sign* (the superposition) is the determinant (C). Each layer at its
   level — and before v120 the cheapest level was empty.
2. **Consolidation out-performed experiment.** The integer-spectrum theorem is sharper than anything the
   μ-scans (v118) or the ρ-map (v119) produced; it fell out of asking how to *carry* the result. Forcing
   a fact into the fast layer clarified the physics.
3. **A concrete optimization for the C engines.** Because the structure is integer-spectrum-rigid, a
   μ-scan within a unit interval is redundant for the sign and the occupied set — one evaluation suffices
   (the weak |A| residual aside). The dual story surfaced a real efficiency.
4. **What is still open (honest).** The elementary ρ is Python-only; the surrogate carries distilled
   facts, not the full map. A future fix could port ρ (the FT of the occupied region) to C. For now the
   division of labor is clean and complete on the discrete facts.

None of this moves the wall. The ideal stack is now current on **both** axes: brute-C (exact anchor) →
stable-C (fast deep production) → surrogate (fast carrier, now scale **and** sign), with Python the
elementary-ρ/eigendecomposition certifier and mpmath the deep-β certifier.

Reproduce: `python3 csurrogate.py` (gate); `./cse val < refs` (both builds); `python3
frozen_friedel_map.py` (elementary ρ). Frozen engine untouched (194/194).
