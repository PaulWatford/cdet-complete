# CROSSCHECK_v134 — integration #3 step 1: the self-energy as the interacting upgrade of z

**Claims.** (1) ED self-energy Σ=G₀⁻¹−G⁻¹ (Lehmann Matsubara G) matches the closed-form atomic Σ to 1e-15.
(2) Dimer (free levels ∓t): the spectral-weight-averaged addition energy of the lowest-empty mode equals
ε_free=z(∞) at U=0 (to 1e-9) and ε_free+ReΣ at U>0 (Hartree-led: 1.271/1.563/2.236/2.995 at U=0.5/1/2/3).
(3) z is the Σ=0 limit of the interacting addition energy — #3 supplements z, doesn't replace it. ED is the
verification anchor only.

**Reproduce.** `cd 08_2d_interacting && python3 self_energy.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
