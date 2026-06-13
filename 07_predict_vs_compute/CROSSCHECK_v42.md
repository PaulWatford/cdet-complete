# Cross-check (v42) — a hierarchy of scales in R(delta): thermal near-shell feature + background

Reproduce: 08_2d_interacting (make scales). Follows the v41 observation that the collapse holds only near
the shell; tests whether R(delta) separates into contributions with different ranges.

## What was checked (order 2)
- RANGE of the near-shell feature is thermal: on L=2 (isolated shell at 0), the sign-flip detuning delta*
  scales as T=1/beta -- beta=2: delta*=0.609; beta=4: 0.234; beta=8: 0.109 (delta*/T = 1.22, 0.94, 0.88).
- The near-shell feature is a function of beta*delta on an isolated shell (shape collapses across beta=4,8;
  amplitude grows as T drops).
- On dense-spectrum clusters (L>=3) neighbouring shells interfere -> cluster-specific BACKGROUND, the
  separate scale that breaks the global beta*delta collapse and dominates the wings.

## Conclusion
R(delta) = thermal near-shell feature (range ~ T, function of beta*delta on an isolated shell) + a cluster-
specific band-structure background. A hierarchy of energy scales: T = 1/beta < shell spacing/gaps <
bandwidth 8t. Which dominates depends on |delta|/T. This is ordinary multi-scale spectral structure -- the
honest content of the "different forces/ranges" intuition -- with NO connection to the fundamental forces.

## Scope / honesty
Order 2, L=2 isolated shell for the thermal-range measurement; delta*/T is order-one but not exactly
constant (drifts 1.22->0.88 as T drops, higher-T corrections). The decomposition is demonstrated, not a
closed-form law. The analogy to strong/weak/EM forces is structural only (distinct ranges), explicitly not
physical.
