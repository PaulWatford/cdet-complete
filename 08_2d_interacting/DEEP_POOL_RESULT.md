# Deep-β pool re-anchored (v104): the precision fix needed a robust estimator too — and the pool SURVIVES (v103's "zero moves" retracted)

## The correction

v103 fixed a real per-config precision bug (the certified stable engine stands). But it then drew
a conclusion from a **single importance-sampling draw** — physical(1.845) = −0.1915(48), "the
deep-β zero moves ~4σ" — and that error bar is fiction. The autopsy here shows why: the *stable*
integrand is still heavy-tailed (tail index **α ≈ 1.06**; better than naive's 0.55 but still
infinite-variance), with its mass on **edge** configs (one τ near the boundary — the antiperiodic
image), distinct from naive's clustered mass. Under α≈1, single IS errors are invalid — exactly
the v92 lesson, momentarily un-applied.

## The robust re-measurement

Median-of-means (valid for α>1) over 72 batches (3 seeds × 24): **physical(1.845) = −0.077(60)**
— consistent with zero at 1.3σ (batch-mean range [−0.62, +1.62], the heavy-tail tell). The
re-anchored zero is **z(36) = 1.8428(40)**, a −0.0022 shift from the naive pool 1.8450(30):
**0.4σ — the pool SURVIVES the precision fix.** v103's "the deep-β zero is not where naive placed
it" is **withdrawn**; it was a heavy-tail fluctuation.

## What stands

- The stable **engine** is correct and necessary — naive float64 is genuinely wrong 8–370%
  per-config on corner configs (v103, mpmath-certified). That is untouched.
- The frozen background A(36) = +0.3754(128) (frozen-side; the freeze removes the tails, so it was
  robust already).
- **Faithfulness is still falsified**: robust physical −0.077(60) vs the frozen-side
  frozen(s_phys) −0.348(11) is 4.4σ — the δ₁×f₂ cross-term (two-sector) survives.
- The 13/7-vs-24/13 question at β=36 is essentially unchanged (z=1.843 sits 0.7σ from 24/13,
  ~4σ from 13/7) — one β is not the identification; the flow is.

## Standing protocol (amended)

Every deep-β mean now uses the stable engine **AND** median-of-means with inter-batch errors,
reporting the batch-mean range as the heavy-tail tell. The lesson, twice learned: a precision fix
does not fix heavy tails — you need both, and a single IS draw is never a result under α≈1.

Reproduce: `python3 deep_pool.py` (retraction; re-anchor; faithfulness; live MoM gates; PASS
~30 s). Frozen engine untouched (194/194).
