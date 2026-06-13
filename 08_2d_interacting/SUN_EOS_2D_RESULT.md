# The SU(N) production route in the 2D thermodynamic limit

All the SU(N) EoS work so far lived on a 2-site reference. The real target — Kozik/Pasqualetti, ¹⁷³Yb SU(6) — is
the **2D square lattice in the thermodynamic limit**. This step makes the jump, on one fact:

> **The record is lattice-independent.** The N-combinatorics — the (N−1) and N(N−1) flavor factors — does not know
> about the lattice. Only the single-flavor input changes.

The leading (Hartree) EoS coefficient is the record times a single-flavor amplitude:

    n₁(N) = −(N−1) · d · d'        d = free single-flavor density,  d' = dd/dμ (compressibility).

## Validated — the formula transfers across geometry

| lattice | direct SU(N) cluster ED n₁ | production −(N−1)d·d' | error |
|---|---|---|---|
| 2-site | −0.19834 | −0.19834 | 3e-8 |
| 1D ring-4 | −0.11421 | −0.11421 | 1e-8 |
| **2D 2×3 square** | **−0.09688** | **−0.09688** | **5e-9** |

The leading SU(N) EoS coefficient on *any* lattice is the record × the free d, d'.

## Thermodynamic limit — replace the cluster by a k-integral

For the infinite 2D square lattice, ε(k) = −2t(cos kₓ + cos k_y), the free density and compressibility are
converged k-integrals (nk = 120 vs 240 identical):

    d(μ=1, β=2)  = 0.671378        d'(μ=1, β=2) = 0.152391

giving the **2D SU(6) leading EoS coefficient**

    n₁(N=6) = −(N−1) d d' = −0.511561        — record × 2D integral, no diagonalization.

## Strong coupling carries over unchanged

The atomic limit (t=0) is a single decoupled site — **lattice-independent** — so the strong-coupling anchor (the
v142 atom record, used in the v153 two-point) is identical in 2D. The two-point construction therefore extends to
the 2D system: weak 2D Hartree + strong atom record bridge the full ⟨n⟩(U). The leading 2D coefficient is exact in
the thermodynamic limit; the full-curve two-point is the production prediction to be benchmarked against the Kozik
DQMC/experiment (⟨n⟩(μ) at T/t=0.3, U/t=2.3, N=6).

## Net

The production route now reaches the real 2D system. The record carries the N-dependence **unchanged** from the
2-site reference to the thermodynamic limit; only the single-flavor amplitude is recomputed as a 2D integral. This
is the bridge from the solvable reference to the experimentally relevant model.

Reproduce: `python3 sun_eos_2d.py` (self-test, ~25s). ED is the anchor only; the frozen engine is untouched
(194/194).
