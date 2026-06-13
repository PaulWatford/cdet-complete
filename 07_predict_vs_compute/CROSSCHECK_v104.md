# CROSSCHECK_v104 — deep-β pool re-anchored; robust estimator; v103 "zero moves" retracted

**Claims.** (1) The stable integrand is still heavy-tailed (α≈1.06, infinite variance), mass on
edge configs — so single IS error bars are invalid. (2) Median-of-means (72 batches):
physical(1.845) = −0.077(60), consistent with zero (1.3σ); batch range [−0.62,+1.62]. (3)
Re-anchored z(36) = 1.8428(40) vs naive 1.8450(30): 0.4σ — the pool survives the precision fix;
v103's "zero moves ~4σ" is retracted (a heavy-tail fluctuation from one IS draw). (4) What stands:
the stable engine (mpmath-certified, naive 8–370% wrong per-config); frozen A(36) 0.3754(128);
faithfulness still falsified (robust physical vs frozen-side, 4.4σ — two-sector survives). (5)
Standing protocol amended: deep-β means require the stable engine AND median-of-means with
inter-batch errors.

**Reproduce.** `cd 08_2d_interacting && python3 deep_pool.py` (retraction; re-anchor;
faithfulness; live MoM; PASS ~30 s).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
