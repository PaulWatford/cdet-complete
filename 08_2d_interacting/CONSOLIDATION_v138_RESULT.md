# Full consolidation of the Möller-paper integration program (v138)

Consolidates v131–v137 (the integrations prompted by Gunnar Möller's three papers) and runs the three
engines / paths side by side. `consolidation_v138.py` is the single health gate.

## The three paths agree

| observable | surrogate-C | plane-wave-C | python | agreement |
|---|---|---|---|---|
| addition pole = lowest-empty level (L=6…48) | ✓ | ✓ (==stable @L6, 0.00e+00) | ✓ | **5e-10** |
| connected determinant | (n/a) | engine ground truth | fast minors == engine 3e-15 | exact |
| self-energy at U=0.3 | (n/a) | (n/a) | exact σ_n vs ED 7e-8 | exact |

All three engines build clean and pass (stable/plane-wave 0.00e+00 on significant refs; surrogate 3.55e-15;
frozen engine 194/194). Every proven advance of v131–v137 is live and self-testing.

## What the three runs taught us (further fixes)

1. **Plane-wave precision floor in the deep-cancellation regime.** At tiny connected-determinant values
   (~5e-11) the plane-wave engine shows ~2e-7 relative deviation vs the stable engine — below the 1e-13
   significance floor (still PASS), but a real near-cancellation characteristic. *Fix (available):* use the
   `-DUSE_LD` long-double build when probing tiny values; document it as the deep-probe path.

2. **The self-energy observable lives in Python/ED, not the C engines.** v134–v137 established the
   interacting addition energy ε+ReΣ and the exact σ_n, but against ED as anchor. *Fix:* wire the
   diagrammatic σ_n into the engine as the production path — and, per the v137 correction, the strong-coupling
   route is **resummation** (Padé / conformal mapping), since the 1PI series buys no radius. This is the next
   real engine-side build for #3.

3. **Fast minors (O(2ⁿn²)) is verified but standalone.** *Fix:* wire it into the engine hot loop behind the
   `val`-mode gate (#5) — the prerequisite is met (term-by-term match to the engine).

4. **The surrogate carries the free addition pole but not the interacting shift.** *Fix (cheap):* the
   surrogate could carry the leading Hartree shift U⟨n₋σ⟩ as a fast interacting-pole estimate, the Σ=0+Hartree
   approximation to the v134 observable.

## Net state after consolidation

The integration arc delivered: #1 (fast minors), the physical mapping (z = free addition pole), and #3
steps 1–4 (self-energy = interacting addition energy, ED-verified; diagrammatic Σ converges; exact 1PI
coefficients; v136's radius overclaim retracted). All supplements — the frozen engine is untouched (194/194)
and the free z-flow remains the Σ=0 limit. Open: #2 (SU(N), the N=6 Yb EoS), #3-resummation, #4
symmetrization, #5 wire-in, #6 R-pruning.

Reproduce: `python3 consolidation_v138.py`. Frozen engine untouched (194/194).
