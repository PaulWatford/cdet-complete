# CROSSCHECK_v92 — the anchor test: scoped law, audited tails, reopened question

**Claims.** (1) The v90/v91 anchored law z = 1.824 − 0.72/β is effective for β ∈ [10,32] only:
extended scans rise through both v90 candidates above β≈32 (scope corrections propagated to
csurrogate and the atlas; gates re-passed). (2) The deep-β heavy-tail audit: at the cancellation
floor, kurtosis ≈ 4500 with 98% of variance in the top 0.1% of samples — single-draw CLT errors
invalid (per-draw sems 0.02–0.18 e-9 on one point; contradictory "±multi-σ" single-draw readings
were outlier artifacts); the mandatory protocol is multi-draw inter-draw errors plus dense grids.
Two in-flight catches banked: a window-edge artifact behind a premature "universality broken"
call (honest (1,3,5)/(1,2,4) split at β=36 is 1.1σ — undetermined), and multi-draw live-gate
redesign. (3) The honest record: z(48) = 1.846 ± 0.009, z(56) = 1.8407 ± 0.0103 → a∞ = 1.8437 ±
0.0068; β=44 grade B (curvature-biased); β=64 unresolved. (4) The bridge verdict
(anchor_bridge.py, edited from cdet-diagnose-bridge v0.57 per the user's directive): the
framework alphabet near 1.84 saturates (rarity 83% within 1σ) → NOT RIGID; the octagon chord
√(2+√2) [ℚ(√2), τ₁-field] is the leading candidate at 0.60σ — leading, not identified; σ\* =
0.0008 for uniqueness; the structural background-zero derivation is the primary route (its
derived form's field answers τ₀-vs-τ₁ with no σ). (5) A withdrawn single-draw preliminary
(plateau 1.8486, chord 0.17σ) is retained in the module as the cautionary record.

**Reproduce.** `cd 08_2d_interacting && python3 anchor_test.py` (honest pool; bridge verdict;
crossover; tail audit; geometry; multi-draw live bracket; PASS ~20 s); `python3 anchor_bridge.py`
(alphabet, null numbers, σ\*).

**Scope (honest).** Constancy beyond β=56 unverified; the alphabet's richness parameters (q≤12,
shift depth 4) bound but do not exhaust the expressible set — which only strengthens the
NOT-RIGID direction; the chord remains a candidate, not a result.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
