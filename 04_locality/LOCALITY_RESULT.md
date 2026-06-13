# Spatial locality of the connected determinant: PROVEN on the engine

Paul's idea: an irregular/large lattice is a symmetric bulk plus a boundary;
work the bulk cheap, handle only the boundary, join them. Computationally this is
domain decomposition + linked-cluster locality. Tested on the REAL engine.

## What was built
The engine was hard-capped at 6 lattice sites (LatticeCtx held 6x6 arrays; the
Jacobi diagonaliser capped at 8x8). Extended with `ring_init(L,...)`:
- bumped the spectral arrays to LMAX=256;
- fills the eigenbasis ANALYTICALLY (ring is circulant: plane-wave modes,
  eps_k = -2t cos(2 pi k/L)), bypassing the diagonaliser entirely;
- numerical spectral-sum path (n_distinct=0).

Validation (non-negotiable, all passed):
- engine verification suite: 194/194 still pass after the change;
- ring_init(6) reproduces the original hexring_init propagator to 4.4e-16
  (machine precision) on a 5-vertex config -> the extension is exact, the C_V
  recursion run on large rings is the same validated recursion.

## The test
Fixed perturbative order n=8. External legs at site 0. Compare, with the SAME
random vertex times (paired):
- compact: all 8 vertices near site 0;
- spread : 4 vertices near site 0, 4 on the opposite side of the ring (site L/2).
Ratio = |C_spread| / |C_compact|, vs ring size L (separation = L/2).

## Result (exact engine C_V)

| ring L | separation | |C_spread|/|C_compact| |
|--------|-----------|------------------------|
| 12     | 6         | 7.3e-3                 |
| 24     | 12        | 5.8e-5                 |
| 48     | 24        | 2.7e-8                 |
| 96     | 48        | 2.2e-11 (num. floor)   |
| 192    | 96        | 2.5e-11 (num. floor)   |

|C_compact| stays ~2e-9 regardless of L. |C_spread| plummets exponentially
(1e-11, 1e-13, 1e-16, 1e-20) until it hits the engine's numerical floor by
separation ~48. An order-8 connected diagram CANNOT use spatially-spread
vertices: it is confined to a correlation blob (~v_F*beta ~ 5-10 sites at beta=5).

## What this wins (and the honest scope)

WINS - the SYSTEM-SIZE axis. Contributing vertex configurations are confined to
a correlation volume around the external legs. The spatial sum runs over one
blob plus its translations, NOT the whole lattice. The method's cost becomes
INDEPENDENT of total lattice size beyond the correlation length: a 10,000-site
lattice (or the thermodynamic limit) costs a correlation volume. This is the real
payoff of the decomposition, and it is why connected-determinant / diagrammatic
methods reach large systems at all. The 6-site toy hid it because 6 < one
correlation length.

DOES NOT WIN - the perturbative-ORDER axis. Inside one compact blob at order n,
the 2^n subset sum remains. Locality bounds the spatial extent (the L-axis), not
the order (the n-axis). The 2^n-in-order is the separate axis addressed by the
control-variate / TCI work (compresses the evaluation count, not the per-call
2^n, which is combinatorial and measured-irreducible).

## Order axis: TESTED, locality does NOT help it (measured)
Question: does locality suppress high ORDER, or only spatial spreading? Held a
small region (3 sites) fixed, pushed order n=4..12, compared compact vs spread.

| order n | med|C_compact| | spread/compact |
|---------|----------------|----------------|
| 4       | 6.7e-6         | 3.5e-7         |
| 8       | 1.4e-8         | 6.3e-8         |
| 12      | 4.1e-10        | 2.0e-9         |

Spreading stays suppressed at every order (locality holds), but compact
high-order diagrams stay HEALTHY (gentle order-by-order decay, not collapse).
You can stack many vertices on few sites at different times -> legitimate compact
high-order diagram -> full 2^n cost. Conclusion: locality bounds spatial EXTENT,
not vertex COUNT. It is the SIZE axis only. The 2^n-in-order stands, consistent
with the full-rank measurements.

## Final map of the wall (this session)
- SIZE axis (lattice sites L): DEMOLISHED by locality. Connected diagrams live in
  a correlation volume; cost independent of total system size. Proven on engine.
- ORDER axis (2^n in perturbative order): IRREDUCIBLE per evaluation (full rank;
  compact high orders healthy). Only the EVALUATION COUNT reduces (control
  variates ~40-80x, TCI) -- never the per-call 2^n.

## Files
- oracle_ring.c, gdump_ring.c : large-L ring C_V oracle and propagator dump
- lattices.c, lattices.h      : the extended engine source (ring_init + LMAX=256)
- locality.py                 : the locality test (this result)
- decomp_largeL.py            : cross-coupling decay + rank vs lattice size
