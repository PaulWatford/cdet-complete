# 2D square-lattice extension + thermodynamic-limit demonstration

Built on the locality result: extended the engine from the 6-site ring to 2D
square tori (the real condensed-matter geometry), and demonstrated the payoff of
locality — the thermodynamic limit at constant cost.

## What was built
`square2d_init(Lx, Ly, beta, mu, t)`: an Lx-by-Ly periodic square lattice.
Separable circulant (H = Hx (x) I + I (x) Hy), so the eigenbasis is the tensor
product of two 1D ring bases and eps = -2t(cos kx + cos ky). Reuses the validated
ring_init for each 1D factor. Site index = y*Lx + x. Up to 256 sites (16x16) at
the current LMAX.

## Validation (all passed)
- engine verification suite: 194/194 still pass after the change;
- the engine's filled 2D eigendecomposition diagonalises the 2D Hamiltonian
  exactly: |H V - V diag(evals)| = 2.4e-16, |V^T V - I| = 4.4e-16 (machine
  precision), on a 4x4. Since lattice_G0 (the spectral sum) was already validated
  on the ring to 1e-13, the 2D propagator is exact.

## Result 1 - thermodynamic limit at constant cost
Fixed compact order-6 observable (vertices pinned near the origin, fixed times),
computed on growing tori:

| lattice | C_V            | change vs prev |
|---------|----------------|----------------|
| 4x4     | 4.63e-10       | (finite-size)  |
| 6x6     | 1.83e-11       | huge           |
| 8x8     | 4.86e-11       | 62%            |
| 10x10   | 5.41e-11       | 10%            |
| 12x12   | 5.20e-11       | 4.0%           |
| 14x14   | 5.17e-11       | 0.6%           |
| 16x16   | 5.19e-11       | 0.4%           |

The local observable CONVERGES to a system-size-independent value (~5.19e-11)
once the lattice exceeds the correlation length (~8-14 sites at beta=5). Small
lattices are dominated by finite-size wrap-around; past ~12x12 it locks in.
The cost of each evaluation is the SAME compact-config C_V (order-6 2^6 subset
sum) regardless of lattice size -> the infinite-lattice answer at finite,
correlation-volume cost. This is the concrete payoff of locality.

## Result 2 - locality confirmed in 2D
16x16 torus, order 6: compact (near origin) vs spread (half dragged to the
opposite corner). median |C_spread|/|C_compact| = 2.0e-2 -> far vertices decouple
(suppression limited only by the modest max separation ~11 sites on a 16x16).

## Scope / honest notes
- WINS the SIZE axis (as in 1D): cost independent of total lattice size beyond the
  correlation length. Now shown in the real 2D geometry, with TD convergence.
- The per-evaluation propagator currently costs O(N) (sum over N=Lx*Ly modes,
  numerical path, n_distinct=0). [DONE v162: square2d_G0_pw implements exactly this -- see SQUARE2D_PW_v162_RESULT.md.] For larger lattices use the closed-form path
  (build_closed_form over the O(L) DISTINCT energies of cos kx + cos ky) or the
  circulant FFT the engine already has -> O(L) or O(log N) per entry. Not needed
  for correctness here.
- The 2^n-in-perturbative-ORDER is unchanged (the order axis; irreducible per the
  full-rank measurements; only evaluation-count levers apply there).
- LMAX=256 caps lattice at 16x16; raising it is just memory (evecs is LMAX^2).

## Files
- oracle_2d.c   : 2D C_V oracle (square2d_init)
- gdump_2d.c    : 2D propagator dump
- evdump2d.c    : dumps the 2D eigendecomposition (used for the exact validation)
- val2d.py      : validation script
- lattices.c/.h : extended engine source (ring_init + square2d_init, LMAX=256)
