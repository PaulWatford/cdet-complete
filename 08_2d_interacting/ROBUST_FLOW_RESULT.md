# The robust deep-β flow (v105): the certified pool rises and fits NO menu line — the assembled root flow is required

## The full robust pool

Re-scanning z(β) on the certified stable engine with median-of-means (the v104 protocol):

    beta:   36          44          52
    z(beta) 1.8428(40)  1.8536(121) 1.8642(61)        [robust]
    naive   1.8450(30)  1.8510(76)  1.8527(52)        [v92 pool, naive float64]

Each z(β) is the μ\* where the stripped ⟨C⟩(μ) crosses zero, located from a 2–3 point μ-scan,
each point a median-of-means (K≈20 batches) — valid under the stable integrand's residual heavy
tail (α≈1.06). The deep static becomes ill-conditioned at high β (the slope of ⟨C⟩(μ) vanishes
while the heavy tail persists), which is why the errors grow with β.

## The flow rises — and no menu law fits

The certified flow **rises monotonically** (1.843 → 1.854 → 1.864), with slope ~0.0013/unit-β
versus the naive pool's nearly-flat ~0.0005/unit. By β=52 it has **passed 13/7 = 1.8571**. Fitting
each single menu law z(β) = μ\* + ln(r)/(qβ):

    11/6: χ²=13.4/2    24/13: χ²=9.4/2    13/7: χ²=6.5/2    CONST: χ²=8.7/2

**None fit** (all χ²/dof > 3). The best, 13/7, fails because the flow overshoots it. The naive
pool's apparent flatness — which had driven four rounds (v93–v95) to converge on {13/7, 24/13} —
was an artifact of corrupted corner configs plus heavy-tail bias giving falsely-flat, falsely-low
high-β points.

## What this means

The single-line menu fit is the wrong model. The certified flow vindicates the **v100 assembled
root flow**: z(β) = 2 + ln s\*(β)/β with s\*(β) the root of A(β) + c1_eff(β)·s + c2(β)·s², where
c1_eff carries the δ₁×f₂ cross-term. The rise and curvature the menu lines can't capture are
exactly what the multi-coefficient flow produces. The identification is **reopened** — and away
from a single rational: it is a flow, not a constant.

**Registered prediction.** If the flow continues, z(64) > 1.87 and the asymptote (if one exists)
lies above 13/7 — nearest menu member 15/8 = 1.875, but more likely the flow is genuinely
multi-term and approaches its limit slowly. The decisive test is to assemble the flow from the
independently-measured certified coefficients and check it reproduces these three points without
fitting.

## Honest limits

Three points, growing errors, an ill-conditioned high-β static. This is suggestive, not a closure:
the rise is a ~2–3σ effect over the range. What is solid: the naive pool's flatness does not
survive certification, so the menu-line identification it supported is withdrawn.

Reproduce: `python3 deep_pool.py` (retraction; re-anchor; faithfulness; live MoM; flow; PASS
~30 s). Frozen engine untouched (194/194).
