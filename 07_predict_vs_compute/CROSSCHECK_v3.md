# Cross-check proof data (v3) — principled anchors

v3 replaces the borrowed strong-coupling anchor (a single U=8 Hubbard datapoint)
with the Heisenberg ring correlator — the exact U->infinity limit of the half-filled
Hubbard model, computed in a 2^L space (~60x smaller than the Hubbard ED).

## Convergence proof: Hubbard correlator -> Heisenberg anchor (L=10)
RMS( <S^z_0 S^z_r>_Hubbard(U) - Heisenberg ) :
| U | RMS |
|---|---|
| 8  | 1.14e-02 |
| 16 | 3.17e-03 |
| 32 | 8.17e-04 |
The Hubbard correlator demonstrably flows to the Heisenberg anchor as U grows. The
anchor is a physical limit, not a fit.

## v3 spin model accuracy (anchors = free + Heisenberg, both limits; analytic moment)
| U | RMS vs exact |
|---|---|
| 0.0 | 5.5e-17 |
| 1.0 | 3.0e-03 |
| 2.0 | 4.7e-03 |
| 4.0 | 2.5e-03 |
| 8.0 | 4.7e-04 |
mean RMS 2.2e-03 (~2.7%). Note U=8 is no longer exact-by-construction (the anchor is
U=infinity, not U=8), which is more honest: the model interpolates between the two
true limits and is checked against the exact Hubbard correlator everywhere.

## Status of the spin correlator
EFFECTIVE model, plateaued at ~2.5-2.7% with two limit-anchors and one analytic
scalar. Pushing below this needs a second input (e.g. the nearest-neighbour
correlation), which trades efficiency for accuracy. That is the honest ceiling of a
two-shape model; it is documented, not hidden.
