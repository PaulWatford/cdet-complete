# CROSSCHECK_v102 — surrogate vs brute-force side-by-side; discrepancies on both sides

**Claims.** (1) Out-of-sample, the C surrogate matches exact CDet within scope: sector EXACT
(0/120 disagreements over L=6 and L=4); ln-magnitude median 1.81× (stated scope 1.7–2.3×); the
13/7 deep-static line fits the brute pool (χ²=1.7/6) better than 11/6 (χ²=5.6/6); background
A(36) 0.370(11) vs fresh IS 0.349(19) (1.0σ); one-sector z_pol(36) 1.8249 vs fresh-brute 1.8251
(0.0002); cross-corrected root_linear→1.8410 vs physical ~1.845 (0.004 s² residual). (2)
Discrepancy on the surrogate side: `surr_class2_static` (v84 L=8 K-flow, falling toward 1.8284)
disagrees with the v100 brute root-flow reread (rising) by up to 0.021 with opposite slope —
flagged stale via supersession notes; the deep L=8 scan is the arbiter. (3) Discrepancy on the
glue side: a s→z sign error (z = 2 + ln s\*/β is correct), caught because the surrogate value
was trustworthy. (4) The ln-magnitude tail is the documented deep-bulk regime limit (over-
prediction up to 64×), not a regression.

**Reproduce.** `cd 08_2d_interacting && python3 surrogate_vs_brute.py` (PART 1 magnitude gate;
PARTS 2/3 documented in SURROGATE_VS_BRUTE_RESULT.md). Surrogate gate still PASS
(`python3 csurrogate.py`); supersession notes do not change any computed surrogate value.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
