# CROSSCHECK_v70 — scalable sector machinery; exact-moment methodology; the v67 gain correction

**Claims.** (1) The coherent rank≤1 sector is constructible from direction classes in O(N²) without
config-space enumeration: 808 of 262,144 (L=4), 3,774 of 10,077,696 (L=6, 0.037%); exact L=4 sector
sum +0.002949 (77% of truth); per-config rank classification vectorizes (exact strata counts over
all 10M L=6 configs, ~6 s; counts 3,774 / 902,136 / 9,171,786). (2) Exact second moments via the
orbit fold give exact design variances: uniform std 1.08e-2 at B=1200 (seed-set measurements ranged
2.75e-3 to 3.0e-2 — both unreliable); v67-design std 4.30e-3 → **TRUE gain ≈6×; the banked v67
"87–110×" is CORRECTED** (lucky-high baseline; structural facts untouched; correction note added
atop SIGN_MODEL_RESULT.md). (3) Exact decomposition: 96% of uniform's E[C²] is sector rarity (the
all-external config alone 34%); bulk 4%. (4) L=6 exact sector sum −5.87e-4 — negative: the v68
μ=0.5 phase flip in exact arithmetic; total estimate −2.3e-3 ± 4.5e-3 (error bar > value: the
machinery scales, the sign problem scales faster). (5) r_pred channel banked (OOS R²=0.32, implied
ξ_s=2.2) with its honest role. (6) Two construction bugs caught by own gates (13-direction family ≠
rank-1 sector; dropped all-external config).

**Reproduce.** `cd 08_2d_interacting && python3 sector_estimator.py` → sector gates, exact-moment
total (1e-7), corrected-gain gate [3,12], L=6 flip gate; "sector-estimator self-test ... PASS"
(~2 min). The L=6 pilot estimate: `pilot_neyman_estimate(cd6, 6, [0.5,1.9,3.3], 0.5)`.

**Scope (honest).** Gain correction is exact at L=4/B=1200 for the analyzed designs; r_pred R² is
modest by nature of per-geometry sign noise; the L=6 signed total remains noise-dominated at this
budget — no claim of beating the wall at scale.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
