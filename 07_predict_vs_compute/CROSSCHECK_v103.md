# CROSSCHECK_v103 — precision: float64 drops the deep-β antiperiodic images; stable engine fixes it, mpmath certifies

**Claims.** (1) Naive float64 is wrong by 8–370% on deep-β corner configs (clustered τ near β,
95% of the MC mass), with zero correct digits on the worst — the far-level antiperiodic images
vanish because (1−n_f) computes as 1.0−1.0=0. (2) The log-domain `stable_cdet.StableCDet` fixes
it in pure float64 (~2.2 ms/call), certified against `mp_cdet.MPCDet` (dps 200) to ~1e-9 on
those configs. (3) Re-measured stable at β=36: frozen A(36) +0.3754(128) vs naive 0.370(11)
(0.3σ, survives); Δ(s_phys) +0.453(135) vs naive +0.334(81) (0.8σ, survives); faithfulness
still falsified (3.2σ); but physical(1.845) −0.1915(48) vs naive +0.030(108) (~4σ, error bar
halves). (4) Consequence: the deep-β zero is not at the naive location; the empirical pool
anchoring the 13/7-vs-24/13 menu must be re-measured on the stable engine, and the surrogate's
pool-fit carriers carry a pending re-fit (frozen-side carriers survive).

**Reproduce.** `cd 08_2d_interacting && python3 stable_cdet.py` (benign; mpmath-certified corner;
speed; PASS ~30 s) and `python3 mp_cdet.py` (certifier; PASS ~60 s). Surrogate gate still PASS.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875). (The frozen engine's golden cases are benign-β and
unaffected; the precision issue is specific to deep-β tau-averaging in the analysis layer.)
