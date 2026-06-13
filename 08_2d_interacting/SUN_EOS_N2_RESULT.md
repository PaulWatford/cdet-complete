# The second-order EoS coefficient: record × single-flavor amplitudes, Hartree part exact in 2D

v154 gave the leading 2D coefficient n₁ = −(N−1)d·d'. The full thermodynamic-limit weak series needs the second
order n₂ — and the point of this step is its **decomposition**:

    n₂(N) = (N−1)²·a  +  (N−1)·b

- **a = d(d′² + ½·d·d″)** — the **self-consistent Hartree** iteration, built entirely from the free single-flavor
  density d and its μ-derivatives; no interaction integral. (The naive guess ½d²d″ is *wrong* — it drops the d′²
  term that comes from feeding n₁ back through the Hartree shift, and even has the wrong sign.) This is the
  dominant piece: it grows as (N−1)², i.e. 5× faster than the bubble at N=6.
- **b** — the genuine second-order particle-hole **bubble** (correlation). Subleading in N.

## Validated (2-site reference)

| quantity | value |
|---|---|
| (N−1)² coefficient, fitted from ED | 0.043739 |
| a = d(d′² + ½d·d″) from free derivatives | 0.043739 (err 2e-7) |
| (N−1) coefficient b (bubble) | −0.009464 |
| predicted n₂(N=6) = 25a + 5b | **1.046125** |
| direct SU(6) ED n₂(6) | **1.046266** (err **1.4e-4**) |

The (N−1)² coefficient is reproduced from free single-flavor derivatives alone, and the full decomposition predicts
the SU(6) second-order coefficient to 1e-4 with no SU(6) fit.

## Thermodynamic limit

a is built from d, d′, d″ — all converged free 2D k-integrals (ε(k) = −2t(cos kₓ + cos k_y)):

    a_2D(μ=1, β=2) = 0.005622        →   2D SU(6) n₂ dominant part = 25·a_2D = 0.140544

exact, no diagonalization. The bubble b is the subleading (N−1) correction (computed here on the cluster; its 2D
value is the local G(τ) particle-hole bubble integral — the one remaining single-flavor amplitude).

## Net

Like n₀ and n₁, the second-order EoS coefficient is **record × single-flavor amplitudes**. Its fastest-growing-in-N
piece is pure self-consistent Hartree and is **exact in the 2D thermodynamic limit**; only the subleading bubble
requires an interaction integral. The weak series for the 2D thermodynamic-limit EoS is now exact through the
dominant second order.

Reproduce: `python3 sun_eos_n2.py` (self-test, N≤5, ~6s). The N=6 row uses direct SU(6) ED (~4 min). ED is the
anchor only; the frozen engine is untouched (194/194).
