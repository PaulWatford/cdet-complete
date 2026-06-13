# The anchor test (v92): the law scoped, the floor's heavy tails audited, the question honestly reopened — with the bridge tool edited for the job

**Result 1 (solid): the v90/v91 law is scoped.** Extended scans show the deep trajectory rising
*through* both v90 anchor candidates above β≈32 — the anchored law z = 1.824 − 0.72/β is an
effective intermediate-window form (β ≈ 10–32), not an asymptote. Scope corrections propagated
into `csurrogate` and the atlas.

**Result 2 (solid, methodology): the deep-β heavy-tail audit.** At the cancellation floor the
value distribution has **kurtosis ≈ 4500 with 98% of the variance in the top 0.1% of samples** —
single-draw CLT errors are invalid (per-draw sems on one point ranged 0.02–0.18 e-9; a "+8σ" and
a "−4.5σ" reading at the same point were both outlier artifacts of a true ≈0.00 ± 0.02). Required
protocol, demonstrated: multi-draw means with inter-draw errors AND dense grids (sparse linear
fits are curvature-biased). Two in-flight catches banked en route: the (1,3,5) "universality
broken" call was a window-edge artifact (honest split 1.1σ — undetermined), and the live gates
were redesigned multi-draw.

**Result 3 (open, quantified by the edited bridge tool).** The honest deep record: z(48) =
1.846 ± 0.009 and z(56) = 1.8407 ± 0.0103 (dense grids, 4-draw errors), pooling to
**a∞ = 1.8437 ± 0.0068**; β=44 curvature-biased (grade B); β=64 unresolved (|V| below honest
errors). `anchor_bridge.py` — edited from Paul's `cdet-diagnose-bridge` v0.57, applying its own
null-model and rigid-gate rules — delivers the verdict: the framework-expressible alphabet near
1.84 has mean spacing ~0.011 and **P(random position within 1σ of some member) = 83%** → NOT
RIGID, one-of-many. The octagon chord √(2+√2) = 1.84776 [ℚ(√2), the τ₁ field] is the **leading
candidate at 0.60σ — recorded as leading, not identified.** σ\* for a unique ID: **0.0008**
(≈72× the sample budget; a shifted 12-gon combo sits 0.003 from the chord). Per the tool's
crossover-method rule, the primary route is **structural**: derive the static's position from the
residue/background-zero structure — the derived form's *field* then answers τ₀-vs-τ₁ exactly,
with no σ at all. The withdrawn single-draw preliminary ("plateau 1.8486 ± 0.0052, chord at
0.17σ") is retained in the module as the cautionary record.

Reproduce: `python3 anchor_test.py` (honest pool; bridge verdict; crossover gate; tail audit;
geometry; a multi-draw live bracket; PASS, ~20 s) and `python3 anchor_bridge.py` (the alphabet,
the null numbers, σ\*). Frozen engine untouched (194/194).
