# Cross-check proof data (v22) — can output-locality prune the connected-determinant recursion? No.

Strategy context: ED is walled (~L=20 = 240M states), so going further needs the DiagMC engine,
whose wall is the per-order cost (the C_V recursion is 3^n: the submask sum, plus 2^n determinant
builds). The natural idea: use the PROVEN output-locality (folder 04: |C_spread|/|C_compact| ~
exp(-sep/xi)) to prune the recursion to spatially-local bipartitions, turning 3^n into ~polynomial
in 1D. v22 tests it. Reproduce: `python 04_locality/locality_prune_test.py`.

## Test
Faithful to the engine's C_V recursion (Dv vacuum blocks, Dc with external legs, C[mask] =
Dc[mask] - sum_{sm} C[sm] Dv[mask\\sm]); kernel decays in space like the engine G0. Use CHAIN
configs (a connected order-n diagram that spans space, so long-range cuts exist to prune). Compare
full vs locality-pruned (cutoff R) on value and operation count.

## Result -- pruning FAILS
| n | C_exact | full ops | R | pruned C | rel.err | ops (% full) |
|---|---------|----------|---|----------|---------|--------------|
| 8 | 9.34e-3 | 6305 | 5 | 9.93e-3 | 6% | 95.7% |
| 10 | 2.52e-3 | 58025 | 5 | 2.96e-3 | 17% | 88.8% |
| 12 | 3.64e-4 | 527345 | 5 | 6.35e-4 | 74% | 80.9% |
(and at smaller R the error is 70-90% for a 10-40% op count.)

Two damning features: (a) keeping 81% of the operations still gives 74% error at n=12 -- the ~19%
of "long-range" terms carry the answer; (b) the error GROWS with order n at fixed cutoff. The
pruned terms are individually LARGE; only their full sum cancels down to the small connected
residual, and pruning destroys that cancellation.

## The lesson
LOCALITY IS A PROPERTY OF THE CONNECTED OUTPUT, NOT OF THE COMPUTATION. The connected value is
exponentially local (folder 04), but the recursion that produces it cannot be localized -- every
term matters for the cancellation. The per-config 3^n is irreducible; it cannot be pruned by
spatial distance without breaking the cancellation that defines the connected part.

## Redirection (the lever that does not fight the cancellation)
Cost ~ 3^n in the ORDER n, so reducing the order needed by delta-n is worth 3^(delta-n) --
exponential -- and is reachable WITHOUT touching the per-config recursion:
- control variate from the learned IR physics (subtract the exact K_rho power law / velocities /
  CFT tail; the residual series converges at lower order);
- expand around the ATOMIC limit, not U=0 (the engine ships G_exact_atom; a strong-coupling
  reference needs fewer orders at the U where we operate).
Locality still helps -- on the SAMPLING side (compact configs dominate, confine the vertex
integration), reducing variance, not per-config cost. The order-reduction lever is the v23 target.

## Status
TESTED AND RULED OUT (v22): locality-pruning the connected-determinant recursion does not work
(output-locality is not term-locality; the 3^n cancellation is irreducible). This saves the effort
of building a pruned engine. The productive cost lever is order reduction (control variate /
atomic-limit expansion), which does not break the cancellation -- v23.
