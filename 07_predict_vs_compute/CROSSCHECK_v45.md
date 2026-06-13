# Cross-check (v45) — shifted-reference CDet (pole-moving) + closed-shell operating point

Reproduce: 08_2d_interacting (make shift). Turns the v44 literature map into a concrete, exactly-verified
upgrade. All convergence claims are EXACT (exact diagonalisation); independent of the Monte-Carlo layer.

## Scheme
H(xi; alpha) = [H0(mu) + alpha*N] + xi*(U*Hint - alpha*N); H(1;alpha)=physical for ANY alpha. Reference at
mu_ref = mu - alpha. alpha=0 is the bare series. Tuning alpha moves the convergence-limiting pole.

## Verified results
- Hubbard atom (mu=1.3,beta=4,U=3.5,<n>=1.00): bare radius ~1.00 (erratic, errors 3e-2..2.7), shifted
  alpha*=+1.5 radius ~1.81, monotone to 2e-3 at K=8. alpha* vs Hartree U<n>/2=1.75.
- 2-site ring (mu=1.1,beta=4,U=4.0,<n>=1.00): bare DIVERGES (never <1e-3 in 14 orders), shifted alpha*=+1.5
  radius ~2.64 reaches 1e-3 at ORDER 5, 2e-5 by K=12. alpha* vs Hartree U<n>/2=2.00.
- Cost: per-order CDet cost ~2^n, so K_bare->K_shift is ~2^(K_bare-K_shift) fewer determinant evals; when bare
  diverges the shift ENABLES the calculation (not a mere speed-up).
- Operating point (live mc2d, order 2, beta=4): R maximal-positive at the closed shell (2x2 mu=0: R=+0.82;
  3x3 mu=-1: R=+0.60), flips sign just above (the detuning delta*). Best sign at closed shells.

## Conclusion
One physical knob -- the Fermi level vs the shells (the v41/v44 detuning) -- drives both gains: the operating
point sets delta=0 (closed shell, best sign); the shift sets the reference Fermi level to the Hartree-corrected
position (pole moved out, fast convergence). alpha* ~ Hartree scale U<n>/2 confirms "expand around mean field".

## Honesty
EXACT-VERIFIED: shifted scheme, radius extension, order-to-accuracy, alpha*~Hartree. NOT DONE (v46): wiring the
one-body counterterm into the C connected-determinant MC (shifted coefficients computed stochastically). The
shift is shipped as an exact resummation/reference-selection tool; no claim the C engine does shifted CDet
end-to-end. Engine 194/194 and cdet_order constants unchanged (frozen engine untouched).
