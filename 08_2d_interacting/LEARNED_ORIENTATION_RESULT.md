# The learned orientation channel (v73): fails the same frozen gate — the channel is closed from both directions

**The experiment.** Train on 9 cells (L=6; μ = 0.5, 1.0, 2.0; extent 3–5; 108 labeled line
geometries); evaluate on *entirely held-out* cells — unseen μ=1.5 at all extents AND unseen L=4.
Pre-set gate: ≥75% mean held-out accuracy, the bar the physics ladder failed (best rung: chain, 64%).

**Two hypothesis classes, same protocol, both fail:**

| model | train | held-out mean |
|---|---|---|
| L2-logistic (ks, extent, μ, free filling, trig in πnk) | 74% | **33%** |
| nonlinear MLP (24 hidden; harmonics m=1,2; pairwise interference features) | 74% | **35%** |

The failure pattern is diagnostic: consistent *anti*-prediction at unseen μ=1.5 (down to 0% on one
cell). The models interpolated the μ-trend smoothly between training fillings 1.0 and 2.0 — and the
true orientation at 1.5 is anti-aligned with any smooth interpolant. **A phase wraps; smooth models
cannot interpolate a wrap from sparse samples.** Predicting orientation at unseen μ requires the
μ-period — which is exactly the quantitative phase law that v69/v71 proved has no form below the
coupled two-spin engine integrand. The circle closes: to learn the channel you need the law; the law
does not reduce.

**The orientation channel, closed at this scope, from both directions:**
- derived: parity 50–59% → static 34% → chain 64% → full free determinant 44% (v68/69/71)
- learned: linear-logistic 33% → nonlinear MLP 35% (v73)

**Remaining routes, named honestly:** (i) dense μ-tabulation per target — measurement, not modeling;
(ii) features computed from the engine integrand — defeats the purpose; (iii) the μ-period found
analytically — the open theory item. This is the surrogate program's characterized boundary on
orientation; remaining surrogate-gain avenues are magnitude-side (R² improvements, the L=6 shell
fold, r_pred refinement).

**Honest scope.** Axis lines, n=3, one β, 12 geometries × 16 τ-draws per cell (label noise where r_g
is small; the 74% train ceiling in both classes reflects it); two model classes — not a proof over
all learners, but the wrap argument applies to any smooth interpolator over sparse μ samples.

Reproduce: `python3 learned_orientation.py` (gates: trains in-distribution >65%, held-out <60% —
the closure reproduced; PASS, ~30 s). Frozen engine untouched (194/194).
