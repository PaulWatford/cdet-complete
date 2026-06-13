# CROSSCHECK_v66 — the no-brute-force simulator and its measured ceiling

**Claims.** (1) Surrogate ln⟨|C|⟩_τ ≈ a − b·MST + c·ℓ_coll + d·dim calibrated on ~85 τ-averaged
geometries: out-of-sample R² = 0.75–0.76, median per-config error 1.7×. (2) Zero-evaluation
reproduction of the v54 brute weight-share table: 4.8–4.9 / 47.4–48.4 / 46.7–47.8 % vs measured
5.6 / 43.0 / 51.5 % (every class within ~5 points; concentrations within ~30%). (3) Guided
estimation (strata = predicted-weight quantiles) at n=2 vs exact fold+cache truth: 33× over uniform
in the survey run, ≥5× at self-test seeds, bias ≤1σ; defensive IS 12× (weaker, documented).
(4) Measured ceiling: at the cancellation-dominated n=3 total — exact truth over 262,144 configs
computed in 11 s by the consolidated stack (24,958 determinants vs 4.2M brute) — guided estimation
gives no gain (0.7×): variance there is sign-driven and the surrogate models magnitude only. The
wall as an estimator theorem.

**Reproduce.** `cd 08_2d_interacting && python3 surrogate.py` → R², zero-eval table vs banked v54
values, guided gain and bias gates; "surrogate self-test ... PASS" (~2 min). The n=3 ceiling
reproduces via `fold_site_sum_cached` (truth, ~11 s) + `guided_estimate` at n=3 (documented in
SURROGATE_RESULT.md; not gated in the self-test for runtime).

**Scope (honest).** One lattice size for calibration (L=4); coefficients are measured; the gain
numbers are seed-spread in heavy tails (33× survey vs 5× self-test seeds — both above gate);
extending the surrogate past the ceiling requires a SIGN model, which is the open v58 question.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
