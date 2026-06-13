# Full dual consolidation at the frontier (v115): both C layers brought current with z(∞)=2; the duality is a chain, and each method covers another's blind spot

Both C layers consolidated with every proven advance through v114, rebuilt, tested, and compared.
Since the last full consolidation (v108) the deep-β program resolved completely (v109–v114), so the
consolidation is substantive, not cosmetic — and a *third* layer, the stable C engine, now sits
between the two.

## What was stale, now current

- **Surrogate**: its live carrier `surr_l6_z_inf()` still returned **1.8818** (the v107 underestimate)
  even though z(∞)=2 was resolved (v111), derived (v112), and Fermi-locked (v114) — 13 caveat layers
  narrated the story while the callable returned the wrong value. Now `surr_l6_z_inf()` = **2.0**
  (the resolved/derived/locked answer), with a new `surr_l6_z_finite(β)` carrying the ln(β)/β
  approach law (z = 2 − 2.6·ln β/β) and `surr_l6_z_inf_legacy()` preserving 1.8818 for the record.
  The menu carriers are explicitly superseded.
- **Brute-force C** (`cdet2d`, `cdet_small`, `cdet_vs_naive`): re-stamped v115; its precision caveat
  now points at the built deep-β layer (`cdet_stable_engine.c`) and records the resolved physics.

## Rebuild test — all green

Surrogate gate (PASS), stable C engine float64 + long double (validate PASS), stable C propagator
(benign + deep PASS), brute drivers (build + benign run vs ED), four analysis modules (PASS), frozen
engine 194/194, constants bit-identical.

## Side-by-side — three layers

| axis | surrogate | brute-force C | stable C engine |
|---|---|---|---|
| z(∞) | **2.0** (carries) | — (too shallow) | **2.0** (derives: flow → 2) |
| benign β | applicable | **exact, ED-validated** | matches brute to machine precision |
| deep β | carries only | **wrong** (naive G0=−0.0 vs −0.0498) | **correct** (mpmath-validated) |
| speed (propagator/carrier) | 7.4 ns | 14.2 ns | 17.4 ns (1.22× brute) |

## The lessons — where each method learns from the others

The "duality" is really a **chain**, and each layer covers a blind spot the others have:

1. **The surrogate cannot compute — only carry.** It was carrying the *wrong* physics (1.8818) and
   would have forever. The stable engine corrected it to z=2. *Lesson: a fast carrier is only as good
   as the engine that grounds it; carriers must be re-grounded when the engine advances.*

2. **The brute-force C cannot go deep — but it is the anchor.** The stable engine is trusted *because*
   it matches the brute-C's ED-validated C_V at benign β to machine precision. Without the brute-C,
   the deep-β numbers would be unverifiable. *Lesson: the exact/shallow layer certifies the fast/deep
   layer at their overlap — that overlap is the whole basis of trust.*

3. **The stable engine cannot self-certify — it is the bridge.** It inherits the brute-C's exactness
   (the log-domain propagator matches at benign β) and extends it where the brute-C's naive propagator
   fails (deep β), producing the resolved physics the surrogate then carries. *Lesson: the cure (the
   log-domain form) is what lets one method's correctness propagate into another's reach.*

4. **The deepest lesson: the cross-validation between the three is what caught every error.** The
   heavy-tail bias (v109: stable-C vs Python), the precision walls (v110: stable-C vs mpmath), and the
   resolution of z(∞)=2 (v111–v114) were each found at a *seam between methods*, never inside one.
   No single layer would have found them: the surrogate would have carried 1.8818, the brute-C cannot
   see deep β, and the stable-C without the brute anchor would be an unverified extrapolation. The
   improvement each gained this turn — the surrogate's z=2 + ln(β)/β law, the brute-C's clarified
   anchor role, the stable-C's confirmed production status — is the chain tightening on itself.

None of this moves the wall. The ideal stack is now complete and current: **brute-C (exact anchor) →
stable-C (fast deep production) → surrogate (fast carrier), with mpmath as spot certifier.**

Reproduce: `python3 csurrogate.py` (gate); `gcc … cdet_stable_engine.c && ./cse val < refs` (both
builds); `gcc … cdet_stable_test.c …` (benign+deep). Frozen engine untouched (194/194).
