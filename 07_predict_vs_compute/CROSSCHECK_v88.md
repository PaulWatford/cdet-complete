# CROSSCHECK_v88 — the order axis: the spine beyond n=3

**Claims.** (1) n=4 extraction ((1,2,3,4), L=6, ε=1, β=20, NT=2048 common random times): the curve
fits a degree-6 polynomial in f at χ/dof 0.04; roots 0.156/0.643 — a pair straddling ½ with
parameters distinct from every n=3 set (min distance 0.185); β-transfer with no refitting verified
by direct n=4 sign scans at β=14 and 24, max dev 0.024 (β=14 lower flip at 0.001). (2) n=5
extraction ((1,2,3,4,5), NT=1024): signal 20× smaller, peak s/n 4.3 — the practical wall exactly
where v87 predicted — but the curve is coherent: the lower root 0.402 is resolved (a −3.7σ→+3.3σ
crossing) and live-verified at β=20 (predicted 0.980, measured 0.991, dev 0.011); the upper root
0.874 is flagged marginal and not gated. (3) The spine — μ\* = ε + logit(f\*)/β with
order-dependent roots — is therefore not an n=3 artifact. (4) The C surrogate is extended with
ATLAS_ROOTS_N4/N5 and surr_class1_flips_order() (marginality documented in the params header);
fresh-seed gate and pedantic-C11 build re-passed. (5) The numerics catch: feature 8 (vol^⅓) used
numpy's float determinant — ~1e-13 noise on singular integer matrices — which mismatched the C
cofactor noise on a random fresh-seed config; both sides now use the exact integer determinant
(feats2 corrected with a banked note; ~1e-4 ln effect on frozen weights, negligible vs the 2.3×
scope; surrogate2 self-test re-passed). (6) New open observable: the root flow with n (three
orders on record, geometry confounded — matched-geometry sequences needed).

**Reproduce.** `cd 08_2d_interacting && python3 order_axis.py` → stored-curve refits, the n=4
transfer table, the n=5 live dev, order-dependence, a live n=4 engine check; "order-axis
self-test ... PASS" (~25 s). The C extension: `python3 csurrogate.py` (PASS, fresh seeds).

**Scope (honest).** One level, one geometry per order; n=5 upper root marginal; n ≥ 6 needs the
frozen C engine or variance reduction.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
