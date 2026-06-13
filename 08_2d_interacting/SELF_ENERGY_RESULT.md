# Integration #3, first step: the self-energy as the interacting upgrade of z (v134)

The physical mapping (v133) showed z(∞) is the **free** single-particle addition pole (ε_k), because the
propagator carries the free spectrum. The **interacting** addition energy is ε_k + ReΣ(ε_k); the self-energy
Σ is the shift. This step establishes that observable and verifies it exactly against exact diagonalization
— the ground truth the diagrammatic self-energy series (Šimkovic–Kozik) will reproduce.

## Two exact checks against ED

**(A) The self-energy machinery — Hubbard atom.** Σ(iω) = G₀(iω)⁻¹ − G(iω)⁻¹ extracted from the ED Lehmann
Green's function matches the closed-form atomic self-energy
Σ(iω) = U⟨n⟩ + U²⟨n⟩(1−⟨n⟩)/(iω + μ − U(1−⟨n⟩)) to **1e-15**. The Dyson extraction is correct.

**(B) The addition pole — Hubbard dimer (free levels ∓t).** The spectral-weight-averaged addition energy of
the lowest-empty (antibonding) mode:

| U | addition energy | shift = ReΣ | Hartree U⟨n₋σ⟩ |
|---|---|---|---|
| 0.0 | 1.00000 | 0.00000 | 0.00000 |
| 0.5 | 1.27100 | 0.27100 | 0.25577 |
| 1.0 | 1.56254 | 0.56254 | 0.50112 |
| 2.0 | 2.23565 | 1.23565 | 0.99976 |
| 3.0 | 2.99485 | 1.99485 | 1.49752 |

At **U=0 the addition pole is exactly ε_free = z(∞)** — the free pole z measures today. At **U>0 it is
ε_free + ReΣ** — the interacting addition energy — with the leading shift the Hartree term U⟨n₋σ⟩ and the
remainder the correlation part.

## What this means

z and integration #3 are **the same physical target at two resummation levels**: z reports the Σ=0 (free)
addition pole; the self-energy series reports the interacting one. This **supplements** z without touching
it — the free z-flow is exactly the Σ=0 limit, recovered to 1e-9 here. ED is used only as the verification
anchor; the frozen engine is untouched (194/194).

Next sub-step: compute Σ **diagrammatically** (the engine-side irreducible series), reusing the v132
fast-minor machinery, and verify it converges to this ED Σ. This step fixed the observable and its exact
ground truth first.

Reproduce: `python3 self_energy.py`. Frozen engine untouched (194/194).
