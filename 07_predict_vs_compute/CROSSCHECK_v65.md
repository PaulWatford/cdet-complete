# CROSSCHECK_v65 — the consolidated baseline (cdet_best.py + BEST_METHODS v65 edition)

**Claims.** (1) `BestCDet` is value-identical to the frozen-port-validated CDet (max diff 2.8e-17 on
random configs, gate 1e-12). (2) `best_site_sum` (orbit fold × subset cache) reproduces brute force
exactly: 4×4 square n=2 match 3.5e-16 (1024 subset evals → 156 determinants); 4³ cube n=2 match
2.7e-15, 13× measured wall-clock (16384 → 578 determinants). (3) `recommended_shift` encodes the
split shift law: α=U/2 at half filling with the cluster-dependent sign caveat in the return value;
Hartree shift with the competition warning otherwise. (4) `CONCENTRATION_LAW` carries the v63
constants (b=0.537, c=0.583, τ share 0.40, lockdown 1.27) with their scope. (5) BEST_METHODS.md v65
edition: composition table with measured factors and provenance, the two laws, the standing
methodology, and the unchanged wall statement (nothing moves R at fixed μ).

**Reproduce.** `cd 08_2d_interacting && python3 cdet_best.py` → four gates as above;
"consolidated-baseline self-test: PASS" (~30 s). Each composed layer also retains its own module
self-test (slice_scaling, symmetry_reduction, slice_stratified, genericity_search,
genericity_cluster, best_methods) — all PASS independently.

**Scope (honest).** Consolidation, not new physics: every factor and law cites the version where it
was measured and gated; the concentration-law constants are L=6 reference values, measured not
derived.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
