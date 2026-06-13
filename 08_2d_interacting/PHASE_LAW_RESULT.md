# The quantitative phase law (v69): two reductions falsified under frozen protocol — the phase lives at the determinant level

**The target.** v68 established the phenomenology: the orientation of coherent line geometries is a
filling-controlled phase (94% negative at μ=0.5 → 75–100% positive at μ=1.5, same geometries). The
formula-grade question: can the phase be predicted from objects *cheaper than the order-n
determinant*? Protocol: calibrate predictor choice + one global sign on a single cell (L=6, μ=0.5,
extent 3), freeze, predict every other (L, μ, extent) cell per-geometry. **Gate pre-set: ≥75% mean
out-of-calibration accuracy.**

**Candidate 1 — static Friedel (τ-averaged single-particle objects).** Four predictors: per-leg sign
products (star, chain-of-gaps), the determinant of the τ-averaged propagator matrix over the point
set, and the dominant permutation term with parity. All saturate the calibration cell (93%) and
collapse out of calibration: **mean 34%** (survey; 25% at self-test cells), with anti-correlated
cells down to 7%. **Falsified, diagnostically:** ⟨C⟩_τ averages the *product* of propagators, not
the product of averages — and the τ-averaged free sign pattern along the axis is ++−++ at *all*
fillings tested, so static tables cannot even represent the measured μ-flip. The phase requires the
joint-τ structure (v60's 40% interference channel, again).

**Candidate 2 — the τ-integrated dominant chain (Matsubara loop, no determinants).** Full joint-τ
structure of one pairing: calibration 93%, out-of-calibration **mean 64–66%** — real partial signal
(two cells at 100%/93%) but **fails the gate**, with one cell anti-correlated (21%). The
cell-dependent reversals are the fingerprint of **competing pairings of opposite permutation
parity**: the chain carries part of the phase; exchange terms flip it elsewhere.

**Standing conclusion.** As far as these reductions reach, the orientation phase is an interference
effect at the level of the full determinant — the sum over all pairings with parities. The contrast
is sharp and falsifiable: **the magnitude obeys a two-coefficient law (v63); the phase resisted
every sub-determinant reduction tested.** That asymmetry is a precise statement of where the sign
problem's hardness sits in this representation: not in how big the contributions are, but in how
they interfere.

**Honest scope.** Axis lines, n=3, one β, 14 geometries/cell. "Irreducible" means "both tested
reductions failed a frozen gate" — not a proof; the full free-diagram sum (the engine itself)
trivially reproduces the phase, so the open question is whether *any* object strictly cheaper than
the determinant carries it. The v68 phenomenology (ξ_s ≈ 3; μ-flip) stands untouched.

Reproduce: `python3 phase_law.py` (gates: both calibrations >80%, static OOS <62%, chain OOS <75%,
chain > static; PASS, ~2 min). Frozen engine untouched (194/194).
