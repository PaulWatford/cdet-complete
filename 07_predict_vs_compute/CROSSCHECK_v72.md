# CROSSCHECK_v72 — the bulk remainder: μ-controlled Friedel rings; frozen prediction falsified

**Claims.** (1) Frozen zero-evaluation prediction (banked before the crosscheck): monotone decay,
compact shell 86±20% of |signed| content (G1), far bulk "noise without signal" (G2). (2) Exact
orbit-fold shell decomposition over rank≥2 (L=4): G1 exact 39% — FAIL; G2 — FAIL (noise concentrates
at intermediate MST, 61% in 3.5–4.5; far bulk small in both). (3) The structure: alternating-sign
shells +0.000256 / −0.000463 / +0.001080 / −0.000053 at μ=0.5 (total +0.000819 = the v70 reference),
mid-range dominance (58% at 4.5–5.5), inter-shell cancellation 2.3×. (4) Frozen confirmation test
passed: at μ=1.5 the pattern shifts to (−,−,−,+), net −0.005101, 6× larger, cancellation 1.13× —
Friedel rings, μ-controlled, consistent with v68 governance. (5) Rotation complete: all three passes
converged on the orientation phase as the single missing surrogate channel; queued route: learned.

**Reproduce.** `cd 08_2d_interacting && python3 bulk_remainder.py` → exact shells at both μ to
2e-6, alternation gate, μ-shift gate, falsification-reproduction gate;
"bulk-remainder self-test ... PASS" (~1 min). Narrative: BULK_REMAINDER_RESULT.md.

**Scope (honest).** L=4 exact, two μ, one β, fixed times, pre-set bin edges; L=6 shell fold not yet
run; the surrogate was directionally right about the far bulk, radially wrong about everything the
phase touches.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
