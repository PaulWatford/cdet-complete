# cdet TCI integrator — tensor cross interpolation for the CDet time-integral

The connected determinant's order-n contribution is an n-dimensional integral of
C_V over the vertex times. This tool evaluates it by **tensor cross interpolation
(TCI)** in a **quantics** representation, calling the real cdet `C_V` engine as the
oracle — learning the integrand from a few adaptively chosen points instead of an
exponential grid.

## Why this, and not the other things we tried
- The *count* (2^n subsets per C_V evaluation) is irreducible — measured: the
  subset array is full rank, no selection rule, the symmetry is spent.
- The *time-integral* is the part with exploitable structure. But only after
  **time-ordering**: in box coordinates the integrand has cusps on every
  coincidence diagonal and does NOT compress (pointwise error stuck ~35% at
  rank 40). On the ordered simplex it is smooth and quantics-compressible.

## Validated numbers (atom, beta=5, mu=0.3; vs brute-force grid, same engine)
| n | R | TT rank | TCI evals | full grid | integral err | savings |
|---|---|---------|-----------|-----------|--------------|---------|
| 2 | 5 | 13      | 768       | 1,024     | 4.9e-3       | 1x      |
| 3 | 4 | 21      | 1,828     | 4,096     | 6.3e-3       | 2x      |
| 4 | 4 | 47      | 17,619    | 65,536    | 2.4e-4       | 4x      |
| 5 | 3 | 36      | 7,380     | 32,768    | 4.8e-5       | 4x      |

Savings grow with n (full grid is G^n; TCI evals grow far slower), rank grows
moderately (not 2^n), accuracy reaches ~1e-5. The gap widens at the high orders
where the wall bites — that is TCI's payoff.

## Honest boundaries
- Tested at small n (2-5); high-n behavior needs confirming (trend is right).
- TCI reduces the NUMBER of time-evaluations, not the per-evaluation 2^n. Each
  C_V call still sums its subsets, so at high order run this on top of the
  streaming/sampling engine — TCI compresses the integral, the engine handles
  the per-point cost.
- IMPORTANT — this validated win is ATOM-SPECIFIC. See HEXRING_RESULT.md. The
  imaginary-time simplex map smooths the integrand only because the atom is
  single-site (vertices interchangeable -> integrand symmetric in the times ->
  sorting puts every coincidence cusp on the simplex boundary). On a real
  multi-site lattice (hexring) the vertices sit on different sites, the integrand
  is NOT symmetric in the times, cross-site coincidence cusps stay interior, and
  the tensor-train error PLATEAUS at ~24% no matter how much rank is added
  (measured n=4). The win does NOT transfer to the real lattice as built.
- The TCI algorithm is teneva's (mature, tested); the method is the tensor-train /
  quantics line (Núñez Fernández, Kloss, Parcollet, Waintal, PRX 2022; Shinaoka,
  Ritter, von Delft, Waintal, 2022-2025). Cite those for the method.

## Build & run
```
cc -O2 -std=c99 -I<engine_dir> oracle.c cdet_engine.o -lm -o oracle
pip install teneva
python3 cdet_tci.py
```
