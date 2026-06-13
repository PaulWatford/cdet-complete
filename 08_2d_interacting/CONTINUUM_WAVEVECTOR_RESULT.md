# A's continuum Friedel wavevector: v119's (120°,180°) is a convergent continuum feature (v129)

v119 found the elementary density matrix ρ(0,r) = (1/N) Σ_{ε≤1} cos(k·r) dominated by short-wavelength
(~2–3 site) structure at the level-1|2 boundary, characterized as (120°,180°) at L=6. A's sign
(v127/v128: converges) is a superposition of ρ at the close vertex displacements, so this is the structure
that governs A. Does it converge as L→∞, and does it match v119?

## The Fermi surface is L-independent

The occupied sea {ε≤1} ⟺ cos(kx)+cos(ky)+cos(kz) ≤ −1/2 is a **fixed continuum surface**, independent
of L. v119's specific angles were the L=6 discrete sampling — at L=6 only x-angles {0,60,120,180} exist,
so the boundary modes snap onto 120° and 180°.

## The Friedel edge converges

The dominant short-wavelength of ρ along x is the Fermi-surface edge of the occupied weight W(kx) (the
cosine-transform structure of ρ). Its half-max crossing converges:

| L | 6 | 12 | 24 | 48 | 96 | 192 | 384 |
|---|---|---|---|---|---|---|---|
| edge kx/L | 0.425 | 0.383 | 0.360 | 0.351 | 0.348 | 0.3476 | 0.3472 |

→ **kx/L ≈ 0.347 (≈125°, ~2.9 sites)**, sitting at the 120° (3-site, 1/3) end of v119's (120°,180°)
bracket. (120°,180°) are the 3-site / 2-site wavelengths bracketing the ~2.9-site continuum oscillation —
exactly the shape a short-wavelength Friedel structure should take.

## Conclusion

v119's dominant-wavevector identification is **confirmed as a real continuum feature**: the density-matrix
Friedel structure converges (the Fermi surface is fixed; the edge → kx/L ≈ 0.347 ≈ 120°). The specific
(120°,180°) values were the L=6 sampling; the continuum lands at the 120° (3-site) end.

This is the clean counterpart to v128. **A integrates the whole Fermi sea → this convergent continuum
wavevector (so sign(A) converges, v127). c1 picks the single lowest-empty multiplet → arithmetic jitter
(so sign(c1) has no period, v128).** The same elementary density matrix gives a convergent continuum
wavevector to the background and an arithmetically jittering remnant to the probe response.

Reproduce: `python3 continuum_wavevector.py` (edge_kxL(L) for L=6…384). Frozen engine untouched (194/194).
