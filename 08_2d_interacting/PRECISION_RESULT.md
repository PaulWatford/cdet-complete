# Precision (v103): naive float64 silently drops the deep-β antiperiodic images; the stable engine fixes it, mpmath certifies it, and it tells both models their final form

## The discovery

Asked whether higher-precision math was needed, the side-by-side pointed straight at it. Mirroring
the exact CDet recursion in 200-digit mpmath and comparing on the **deep-β corner configs**
(clustered τ near β — the configs that carry 95% of the heavy-tailed Monte-Carlo mass) showed
naive float64 wrong by **8% to 370%**, with *zero* correct digits on the worst configs.

The mechanism is a catastrophic cancellation, not a rounding nuisance. The propagator
g0 = Σ_k U U · occ_k · e^(−ξ_k τ). For τ near β and a far **occupied** level (ξ ≪ 0), the
particle branch needs (1−n_f)·e^(−ξτ) = e^(−ξτ − softplus(−βξ)), an O(1) number — but float64
computes (1−n_f) as `1.0 − 1.0 = 0` (n_f rounds to 1), so the term **vanishes**. Those dropped
terms are exactly the antiperiodic images that carry the deep-β structure.

## The fix (the brute force's true final form)

Assemble each term's exponent in the **log domain** before exponentiating, so every term is
bounded and nothing huge is ever formed:
  particle (τ>0): −e^(−ξτ − softplus(−βξ)) · particle, hole (τ<0): +e^(−ξτ − softplus(βξ)).
`stable_cdet.StableCDet` / `StableFrozen` do this in pure float64 — **certified against mpmath-200
to ~1e-9** on the corner configs (vs 370% for naive), at the same 2.2 ms/call. mpmath is not a
production engine (it needs dps≈120–200 for deep β, ~10⁴–10⁵× too slow for MC); its role is the
**certifier**, `mp_cdet.MPCDet`.

## What survives certification, and what moves

Re-measured at β=36 with the stable engine (importance sampled):

| quantity | naive (v96–v100) | stable (certified) | verdict |
|---|---|---|---|
| frozen background A(36) | 0.370(11) | **0.3754(128)** | survives (0.3σ) — the freeze removes far images anyway |
| δ₁×f₂ cross-term Δ(s_phys) | +0.334(81) | **+0.453(135)** | survives (0.8σ) — the two-sector mechanism is real |
| faithfulness gap | 3.4σ falsified | **3.2σ falsified** | survives — the v96 "faithful" claim stays dead |
| physical value at μ=1.845 | +0.030(108) | **−0.1915(48)** | **MOVES ~4σ; error bar halves** |

So the **frozen-side** of the coefficient program (A, the polynomial, the two-sector mechanism)
is sound. The **physical-side** is not: physical(1.845) is decisively nonzero in the certified
engine, meaning the deep-β zero is **not at the naive-measured location** — and the empirical
pool {z(36)=1.8450(30), …} that anchors the 13/7-vs-24/13 menu was measured in naive float64 on
exactly the corner-dominated samples that were corrupted. **The pool, and therefore the menu
identification, must be re-measured with the stable engine.** (The error bar halving is the tell:
the float64 garbage on corner configs was inflating variance as well as biasing the mean.)

## What this says about the final form of both models

- **Brute force.** Its final form is the stable log-domain engine, mpmath-certified. The
  "precision wall" was an algorithm artifact (forming huge intermediates that cancel), not a
  fundamental need for bignum — the fix is exact and free. Everything deep-β must run on it.
- **Surrogate.** Its frozen-side carriers (A, z_pol, the cross-slope mechanism) survive. Its
  physical-side carriers — anything fit to the empirical pool (the menu lines, the static family
  numerics) — inherit a **precision caveat** and a pending re-fit once the pool is re-measured.
  The L=8 carrier discrepancy flagged in v102 now has a second reason to wait for a stable scan.
- **Both converge to one object** — the coefficient polynomial and its root flow — and the data's
  message is that the *measuring instrument* underneath both was systematically wrong on the
  dominant configs. None of this touches the wall: R and the 2ⁿ are unchanged. This is a theory of
  *where* the sign structure sits, now measured correctly.

Reproduce: `python3 stable_cdet.py` (benign; mpmath-certified corner; speed; PASS ~30 s);
`python3 mp_cdet.py` (certifier; PASS ~60 s). Frozen engine untouched (194/194).
