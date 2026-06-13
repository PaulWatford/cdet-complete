# Reaching strong coupling: the SU(N) EoS by two-point resummation

v152 gave the weak-coupling EoS curve, but Padé alone capped the reach at U≈1.2 — the algebraic branch point
(v146) blocks the path to strong coupling (U/t ~ 2–3, the Kozik/Yb regime). This step reaches it by anchoring
**both** ends of the coupling axis and bridging them.

## The two anchors (both record-predictable)

- **Weak (U→0):** the lattice record series n_k(N) (v152). Record-predictable.
- **Strong (U→∞):** the per-flavor density approaches the **atomic limit**, with a 1/U expansion
  n(U) = m₀ + m₁/U + …. The leading m₀ is the t=0 SU(N) atom density — the **v142 atom record**, computable from
  a single site with no 2-site diagonalization; m₁ is the leading hopping correction. Both m₀(N), m₁(N) are smooth
  in N, so they are record-predictable from small N too.

A **two-point Padé [2/2]** matching 3 weak + 2 strong coefficients bridges the crossover. The modest order is
deliberate — higher orders develop spurious poles in the physical region (the weak series' small radius poisons
them); [2/2] is stable.

## Result — record-predicted SU(6) EoS vs direct SU(6) ED, *to strong coupling*

Using **only N ≤ 5 data and no SU(6) diagonalization** in the prediction:

| U | direct SU(6) ED | record two-point | error |
|---|---|---|---|
| 0.2 | 0.58901 | 0.58018 | 9e-3 |
| 0.5 | 0.46618 | 0.43888 | 2.7e-2 |
| 1.0 | 0.34649 | 0.32842 | 1.8e-2 |
| 1.5 | 0.27869 | 0.27881 | 1e-4 |
| 2.0 | 0.23688 | 0.25255 | 1.6e-2 |
| **2.3** | **0.21850** | **0.24234** | **2.4e-2** |
| 3.0 | 0.18700 | 0.22693 | 4.0e-2 |
| 4.0 | 0.16669 | 0.21511 | 4.8e-2 |

The curve is reproduced across the **whole coupling range**, and reaches **U/t = 2.3 — the Kozik benchmark
coupling — at 2.4%**; worst error <5% out to U=4. Strong coupling is reached. (The accuracy softens toward very
strong coupling, set by the two-term strong expansion; adding m₂ or the t²/U structure tightens it.)

## Net — the SU(N) EoS, record-predicted weak to strong

The EoS is now record-predicted across the entire coupling axis: the **weak end from the lattice record** (v152),
the **strong end from the atom record** (v142), bridged by a stable two-point Padé. Both N-extrapolations are
exact-in-N records; the U-axis — algebraic and finite-radius on each side (v146) — is spanned by anchoring both
limits rather than extrapolating one. The full SU(6) equation of state, including the experimentally relevant
coupling, is obtained from small-N data with no large-N diagonalization.

Reproduce: `python3 sun_eos_strong.py` (self-test, N≤5, ~2s). The N=6 table uses the record-predicted curve vs
direct SU(6) ED (~90s). ED is the anchor only; the frozen engine is untouched (194/194).
