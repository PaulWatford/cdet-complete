# Cross-check proof data (v20) — the sparse FFT solver: small U cracked at half filling, and a
# structural wall named at quarter filling

The v18/v19 dense dressed-energy solver works for U>=2 but fails below (sharp kernels of width
U/4, too costly to refine densely). v20 builds a SPARSE solver and finds out exactly how far small
U can be pushed. Reproduce: `python bethe_spin_velocity_sparse.py`.

## Method — Fourier-diagonal, no dense inversion
The full-line a_2 self-convolution is diagonal in Fourier (hat a_2(omega) = e^{-2u|omega|}), so
(1 + a_2*) sigma = drive is solved as sigma = IFFT( FFT(drive) / (1 + hat a_2) ) -- exact in the
a_2 part, no kernel discretization. A short fixed-point loop handles the a_1 charge<->spin coupling;
mu is fixed by two linear solves (kappa(Q)=0), as in v18. Each step is O(N log N), so a fine grid
(NL=2^13) is cheap -- the resolution the dense solver could not afford. Plateau window scales with
U (~[2,5]*(U/4); the asymptotic regime sets in a few kernel widths out).

## Result 1 — small U CRACKED at half filling (validated vs Bessel)
| U | FFT | Bessel | err |
|---|-----|--------|-----|
| 0.5 | 1.9284 | 1.9187 | 0.5% |
| 1.0 | 1.8353 | 1.8331 | 0.1% |
| 2.0 | 1.6410 | 1.6399 | 0.1% |
The sparse solver reaches the small-U region the dense solver could not, and agrees with the dense
solver at the U=2 overlap (FFT 0.9525 vs dense 0.9512 at quarter filling). FFT (U<=2) and dense
(U>=2) are complementary and cover the full U range at half filling.

## Result 2 — quarter-filling small U is a STRUCTURAL wall, not resolution
The velocity profile |eps_s'|/(2 pi sigma) at quarter filling, small U:
| U | L=0.6 | L=1.0 | L=1.5 | L=2.0 | L=3.0 |
|---|-------|-------|-------|-------|-------|
| 0.5 | 0.575 | 0.877 | 1.077 | 0.009 | 0.000 |
| 1.0 | 0.638 | 0.922 | 0.937 | 1.019 | 0.022 |
It RISES to a peak (~1.0-1.08) then CRASHES into the noise floor (sigma -> 0) with NO flat plateau.
At low filling AND small U the spin density has narrow support, so the Lambda->infinity spin-Fermi-
point region is buried under the density's collapse before any plateau forms. So the exact quarter-
filling u_sigma below U=2 is NOT cleanly extractable by the dressed-energy route; the peak is a
rough lower bound only. This is a DIFFERENT, deeper obstruction than the dense solver's resolution
limit (v18) -- a structural "no plateau" wall, named not papered over.

## Status
PARTIAL (v20): the sparse FFT solver reaches small U at half filling (validated 0.1-0.5% vs
Bessel), proving the small-U region is reachable in principle and giving the half-filling curve to
U=0; but the TARGET -- exact quarter-filling u_sigma below U=2 -- has a structural obstruction (the
velocity profile peaks then crashes; no asymptotic plateau at low filling + small U). The exact
quarter-filling u_sigma stands for U>=2 (v18); U<2 there needs a genuinely different handle (the
weak-coupling field theory v_s = v_F - O(U)), not a finer grid. The wall is now characterized, not
just hit.
