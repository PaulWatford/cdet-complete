# Genericity beyond the 2×2 (v64): the v56 law splits — PH convergence-lock universal, sign alignment cluster-dependent

**The test (the pivot target):** does "sign and convergence align only at half filling" hold beyond
one cluster and one coupling?

**Axis 1 — second and third coupling (2×2, β=8).** U=2: half filling → α\*=1.0=U/2 → μ_ref=0 = the
sign peak (R=0.91): aligned; doped μ=0.25, 0.0 → μ_ref=−0.75, −1.0 (R=0.13): separated. U=8: half
filling → α\*=4.0=U/2 → μ_ref=0: aligned; doped μ=1.0, 0.0 → μ_ref=−2.0 (R≈0.14): separated.
**α\* = U/2 at μ = U/2 at all three couplings (with v56's U=4) — the mechanism tracks U exactly.**

**Axis 2 — larger cluster (6-site ring, U=2, β=8).** Made feasible by **blocked sector ED**:
(N↑, N↓) conservation splits the 4096-dim Fock space into 49 sectors of ≤400 — validated against a
full dense-eig reference (G = −0.246331, a 120 s computation) to **4.8e-07**, at ~150× the speed
(0.8 s/eval). The frozen prediction, stated before the run from v56's own measured 6-ring sign
landscape (peak R=0.51 at μ_ref=−1.0; R(0)=0.14): the PH mechanism should hold, and sign alignment
should *fail*. Measured α sweep at half filling (err@K8):

| α | 0.0 | 0.5 | **1.0 = U/2** | 1.5 | 2.0 |
|---|---|---|---|---|---|
| err | 1.0e0 | 4.2e-1 | **8.6e-6** | 5.8e-1 | 1.5e0 |

The PH shift wins by **five orders of magnitude** — the error at the PH point sits at the extraction
floor: the shifted series is *quasi-exact* there (a stronger statement than v56 made). But the sign
at μ_ref=0 is R=0.14 vs the peak 0.51 at −1.0: **sign alignment fails at half filling on the
6-ring** — both halves of the prediction confirmed.

**The refined law:**
1. **Universal (2 clusters × 3 couplings):** at half filling the convergence-optimal shift is
   α\* = U/2 — the particle-hole point — and the PH-symmetric reference renders the series
   quasi-exact.
2. **Cluster-dependent:** whether the PH point is *also* the sign optimum depends on whether the
   cluster's sign landscape peaks there. True on the 2×2; false on the 6-ring. **"Sign and
   convergence align at half filling" was a 2×2 coincidence of two different special points.**

Honest scope: 6-ring tested at half filling only (49 s/α; doped untested there, expected separated a
fortiori); one β; the 6-ring sign landscape is the v56 measurement. Curious open thread: the 6-ring's
sign peak at μ_ref=−1.0 sits *on a level*, not in the gap at 0 — the naive shell picture fails on
this cluster, reason unknown.

Reproduce: `python3 genericity_cluster.py` (gates: blocked-vs-dense 1e-5; PH shift ≥10³× better at
K=6 on the 6-ring; α\*=U/2 at U=2 on the 2×2; PASS, ~2 min). Frozen engine untouched (194/194).
