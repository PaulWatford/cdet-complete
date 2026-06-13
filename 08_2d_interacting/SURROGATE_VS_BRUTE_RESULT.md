# Surrogate vs brute-force, side by side (v102): five claims checked against exact CDet, discrepancies on both sides

The C surrogate was run head-to-head against the brute-force exact CDet (the validated ground
truth), fresh and out-of-sample, on both lattices. The existing gate only checks C == Python
*model* (port fidelity); this is the missing check — model == truth (accuracy). Discrepancies
were found on **both** sides: a stale surrogate carrier, and a sign bug in the comparison glue.

## What AGREES (within scope)

| Claim | Surrogate (C) | Brute (exact CDet) | Verdict |
|---|---|---|---|
| sector (rank-1 invariant) | `surr_sector` | `classify_true_rank1` | **EXACT**, 0/120 disagreements (L=6 and L=4, out-of-sample) |
| ln-magnitude | `surr_ln_magnitude` | ln⟨\|C\|⟩_τ, β=4, NT=200 | median **1.81×** (within the stated ~1.7–2.3× scope) |
| deep L=6 static, 13/7 line | `surr_static_l6_deep_alt` | honest pool {36..56} | χ²=1.7/6 — **closer** to brute |
| deep L=6 static, 11/6 line | `surr_static_l6_deep_law` | honest pool | χ²=5.6/6 — disfavored (known) |
| background A(36) | 0.370(11) e-9 | fresh IS 0.349(19) e-9 | 1.0σ — agree |
| one-sector root z_pol(36) | `surr_l6_zpol36` = 1.8249 | fresh IS s\*=0.00184 → 1.8251 | **0.0002** — agree |
| cross-corrected root | `surr_l6_root_linear`→1.8410 | physical zero ~1.845 | 0.004 (the s² residual); closes 80% of the gap, right direction |

## Discrepancy 1 — surrogate side: the L=8 static carrier is STALE

`surr_class2_static` (the v84 K-flow form, z = 1.8284 − 0.355/2β, *decreasing* toward the
midpoint) diverges from the v100 brute-measured **root-flow** curve (FROZEN_CURVE_Z8, *rising*
with β):

    beta:       28      36      40      44
    surrogate   1.8221  1.8235  1.8240  1.8244   (v84 K-flow)
    brute(v100) 1.8268  1.8378  1.8417  1.8449   (root-flow reread)
    dev         0.005   0.014   0.018   0.021

The v84 carrier was never updated when v97/v100 reread the L=8 "static" as an A-vs-f(2.0)
root-flow crossing that rises with β. The two models disagree by up to 0.021 and have *opposite
β-slope*. The decisive arbiter — a deep honest L=8 zero scan — is the already-queued L=8
crossover test; until it runs, the surrogate now carries an explicit supersession note rather
than a silently-wrong value.

## Discrepancy 2 — brute/glue side: a sign error in the s→z conversion

The first comparison harness used z = 2 − ln s\*/β; the correct relation (s\* ≈ e^(−β(2−z))) is
z = 2 **+** ln s\*/β. This produced a spurious 0.35 "discrepancy" at the carriers — caught
precisely *because* the surrogate's z_pol36 = 1.8249 was trustworthy and the brute side wasn't.
Fixed; with the correct sign the carriers agree to 0.0002–0.004 (table above). Lesson: in a
side-by-side, the more-trusted side is the instrument that finds the bug in the other.

## ln-magnitude: where the 1.81× median hides structure

The error is two-directional and concentrated in the deep bulk: the surrogate **over-predicts**
the lowest-magnitude (deep-bulk) configs by up to 64× (it floors near −19.7 while truth reaches
−24), and **under-predicts** the most compact config by ~19× — exactly surrogate2's documented
"deep bulk strictly unpredictable" boundary. The median is in scope; the tail is the known
regime limit, not a regression.

Reproduce: the harness is `surrogate_vs_brute.py` (PART 1 magnitude, PART 2 statics+carriers,
PART 3 sector+L8); ~5 min. Frozen engine untouched (194/194).
