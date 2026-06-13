# The order axis (v88): the spine survives beyond n=3; the C surrogate gets its first higher-order laws

**The question.** Is the resonance structure an n=3 artifact, or an all-orders law? The v83
logit-map extraction was run at n=4 and n=5 (L=6, level ε=1, β=20, full axis-line configs), with
frozen claims: a low-degree polynomial in f fits the crossing region; flips anchor to the level
via μ\* = ε + logit(f\*)/β; the roots are order-dependent while the spine is not.

**n=4 — clean confirmation.** Curve fits at χ/dof 0.04 (degree 6); roots **0.156 / 0.643** — a
pair straddling ½, parameters distinct from every n=3 set (min distance 0.185), same law.
**β-transfer with no refitting:** direct n=4 sign scans at β=14 and 24 land on the predictions at
max dev **0.024** — the β=14 lower flip at 0.001.

**n=5 — the wall arrives where v87 said it would.** Signal 20× smaller, peak s/n 4.3 — yet the
curve is coherent (a definite −3.7σ→+3.3σ crossing): the **lower root 0.402 is resolved and
live-verified** (predicted flip 0.980 at β=20, measured 0.991, dev 0.011); the upper root 0.874
sits in the low-signal tail and is **flagged marginal**, not gated.

**The C surrogate extended:** `ATLAS_ROOTS_N4` / `ATLAS_ROOTS_N5` and `surr_class1_flips_order()`
shipped with the marginality note; the fresh-seed gate and pedantic-C11 build re-passed.

**The round's numerics catch** (the fresh-seed gate doing its job): feature 8 (vol^⅓) used numpy's
float determinant, which returns ~1e-13 noise for singular integer matrices (vol^⅓ ≈ 1e-5 instead
of exactly 0), and the C cofactor noise differed → a real mismatch on a random config. The
min-image displacement matrix is integer-valued by construction, so **both sides now use the exact
integer determinant** (`surrogate2.feats2` corrected with a banked note; effect on the frozen
weights ≈ 1e-4 ln units, negligible against the 2.3× scope).

**Honest scope.** One level, one geometry per order; the n=5 upper root marginal; n ≥ 6 extraction
needs the frozen C engine or variance reduction; how the roots flow with n is a new open
observable (three orders now on record: 0.235/0.832 → 0.156/0.643 → 0.402/0.874 — non-monotone,
geometry changing with n, so the flow question needs matched-geometry sequences).

Reproduce: `python3 order_axis.py` (gates: stored-curve refits, the n=4 transfer table, the n=5
live dev, order-dependence, a live n=4 engine check; PASS, ~25 s). Frozen engine untouched
(194/194).
