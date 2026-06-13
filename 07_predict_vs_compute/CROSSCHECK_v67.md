# CROSSCHECK_v67 — the sign model: v58 settled; ceiling moved 0.7× → 87–110×

**Claims.** (1) Per-geometry sign survival r_g (bootstrap, survey sizes 36 lines/84 bulk × 40 τ):
1d 0.70 [0.59,0.81], 2d 0.70 [0.58,0.82], bulk 0.34 [0.25,0.47] — non-overlapping CIs; 1d sign(+)
fraction 92% vs bulk 45%; r_g correlates with dim (−0.45) and MST (−0.50). (2) The d≤1 sector (808
of 262,144 configs) carries +0.002949 of the exact +0.003846 total — 77% of the signed answer at
0.3% of configs. (3) Hybrid estimator (exact d≤1 enumeration + signed-σ pilot-Neyman on d=2,3) at
budget 1200 vs the exact truth: 87× (survey) / 110× (self-test seeds) variance reduction over
uniform, bias 0.2–0.7σ. (4) Rejected reading: a 231× magnitude-bin figure ran on a frozen 20k
subsample (selection variance absent) — flagged, not banked. (5) Methodology catch: the first
self-test failed on trimmed sample sizes (bootstrap separation broke); survey sizes restored.

**Reproduce.** `cd 08_2d_interacting && python3 sign_model.py` → the r_g table with CIs, the gates
(CI separation; sign(+)>75%; gain>10×; bias<3σ), "sign-model self-test ... PASS" (~2 min). The 77%
structural fact reproduces from `span_strata` + direct evaluation of the 808 d≤1 configs against
`EXACT_TRUTH_N3` (the v66 fold+cache truth).

**Scope (honest).** One lattice/order/μ/β; line-sign predictability is measured, not derived —
re-measure before reuse; the bulk remainder's sign is a coin flip (the wall's remaining territory).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
