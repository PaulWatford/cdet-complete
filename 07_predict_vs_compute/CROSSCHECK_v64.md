# CROSSCHECK_v64 — genericity beyond the 2×2: PH convergence-lock universal; sign alignment cluster-dependent

**Claims.** (1) Coupling axis (2×2, β=8): α\*=U/2 at μ=U/2 at U=2 and U=8 (three couplings with v56's
U=4); all doped points separated (μ_ref at −0.75…−2.0, R 0.13–0.14 vs peak 0.91). (2) Cluster axis
(6-ring, U=2, β=8): blocked sector ED ((N↑,N↓) sectors ≤400) reproduces the dense-eig reference
G=−0.246331 to 4.8e-07 at ~150× speed; the half-filling α sweep gives err@K8 = 8.6e-6 at α=U/2 vs
0.4–1.5 elsewhere (quasi-exact at the PH point, five orders of magnitude), while the sign there is
R=0.14 vs the 6-ring's peak 0.51 at μ_ref=−1.0 — sign alignment fails at half filling, exactly as
predicted before the run from v56's measured landscape. (3) Refined law: PH convergence-lock
universal; sign alignment requires the cluster's sign peak to coincide with the PH point (2×2 yes,
6-ring no).

**Reproduce.** `cd 08_2d_interacting && python3 genericity_cluster.py` → blocked-vs-dense check
(4.8e-07), 6-ring err ratio at K=6 (~6e3), 2×2 U=2 alignment (α\*=1.0); gates as printed;
"cluster-genericity self-test ... PASS" (~2 min). Full tables: GENERICITY_CLUSTER_RESULT.md.

**Scope (honest).** 6-ring at half filling only (49 s/α; doped untested there); one β; the 6-ring
sign landscape is the v56 measurement. New open question logged: the 6-ring sign peak sits ON a
level, not in the PH gap — naive shell logic fails there.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
