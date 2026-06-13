# TCI on the real lattice: hexring measurement

Question asked: does the validated atom TCI win (rank stays moderate, integral
converges) transfer to the real multi-site target lattice (hexring), at the
orders where the 2^n wall bites?

Answer: NO, not as built. Measured.

## The decisive contrast (n=4, R=4)

Pointwise error below isolates TENSOR-TRAIN representability: it compares the
reconstructed TT against the exact function on the SAME grid, so it is not a
grid-resolution artifact. It answers only "can a tensor-train of this rank
represent this integrand?"

| lattice  | time map         | TT rank | pointwise error |
|----------|------------------|---------|-----------------|
| atom     | box (raw cube)   | 53      | 50%             |
| atom     | simplex (ordered)| 61      | 0.16%           |
| hexring  | box (raw cube)   | 47      | 44%             |
| hexring  | simplex (ordered)| 20      | 24%             |

And the plateau (hexring, simplex, n=4), brute-force validated, integral error
vs truncation tolerance:

| trunc | rank | int_err | pw_err |
|-------|------|---------|--------|
| 1e-2  | 29   | 2.3e-2  | 11%    |
| 1e-3  | 34   | 2.4e-2  | 11%    |
| 1e-6  | 34   | 2.4e-2  | 11%    |
| 1e-10 | 34   | 2.4e-2  | 11%    |

Adding rank does nothing past 34. The error is stuck.

## Why

The simplex / time-ordering map smooths the integrand by moving the propagator's
imaginary-time coincidence cusps (the jump at tau_i = tau_j) onto the boundary of
the integration simplex, where they stop hurting convergence. That works only
when the integrand is SYMMETRIC in the times.

- Atom: single site, all vertices interchangeable -> integrand symmetric in the
  times -> sorting the times places EVERY coincidence cusp on the boundary ->
  smooth -> converges (0.16%). This is the win that was validated last session.
- Hexring: vertices sit on DIFFERENT sites -> integrand NOT symmetric in the
  times -> sorting lands only the same-site coincidences on the boundary; every
  cross-site coincidence cusp stays in the interior -> integrand stays
  non-smooth -> tensor-train cannot represent it -> plateau at ~24%.

The validated atom win was riding on single-site symmetry. It is special, not
general.

## The real path forward (a build, not a knob)

The obstruction is the propagator's jump in IMAGINARY TIME. In Matsubara
frequency (or the IR / intermediate-representation basis) the propagator is a
smooth rational function 1/(i*omega - eps); the cusps disappear. This is exactly
why the published quantics-TCI line (Shinaoka, Ritter, von Delft, Waintal,
2022-2025; Nunez Fernandez, Kloss, Parcollet, Waintal, PRX 2022) works in a
frequency / IR basis rather than raw imaginary time.

Taking that path requires the oracle to evaluate the integrand at FREQUENCY-space
sample points, i.e. reformulating C_V in frequency. That is a genuine
re-architecture of the engine's inner evaluation, not a parameter change to this
tool. It is the honest next step if the TCI route is to work on real lattices.

## Status summary

- Atom imaginary-time simplex TCI: validated, real, useful — for single-site.
- Real multi-site lattice (hexring), same approach: measured failure (~24% stuck).
- Cause: cross-site coincidence cusps; single-site symmetry was load-bearing.
- Fix that the literature actually uses: frequency / IR basis. Requires building
  a frequency-domain oracle. Not done here.
- Unchanged throughout: TCI (any basis) compresses the TIME-INTEGRAL, never the
  per-evaluation 2^n subset sum, which is combinatorial and measured-irreducible.
