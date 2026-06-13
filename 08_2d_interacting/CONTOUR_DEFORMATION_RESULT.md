# Contour deformation on the CDet sign — does the "evaluate on a contour" tool move the wall? (v49)

**Question.** Of the structured-cancellation tools in the roots-of-unity / circulant-determinant /
nome-on-a-contour family, the one with a real shot at the *sign* wall is Lefschetz-style **contour
deformation** — deform the integration contour so the integrand's phase flattens and the cancellation
shrinks. We tested it on the genuine v48 sign integrand and it is **null**, for a structural reason that
also disposes of the natural follow-up ("use the undeformed axis as a control-variate comparator").

**Setup.** Genuine v48 case: 2×2 square, single-particle levels {−4,0,0,+4}, β=4, U=4, μ=0.5,
externals (t_o,t_i)=(0.7,0.2). Integrand = the frozen engine's connected determinant C_V, evaluated via
`cdet_port.py` (validated bit-identical, 0.00e+00, to the ring port that is itself validated to 1e-16 vs
ED). Reference μ_ref ∈ {0.0 (closed shell, good sign), −1.0 (Hartree, wrecked sign)}.
`contour_deformation.py` reproduces everything below.

**(A) Where the cancellation lives — sector decomposition.** Split the order-1 time integral at the
propagator kinks {0, t_i, t_o, β} (where G₀ switches branch). **Within every analytic sector the sign
quality is R = 1.000** — the integrand does not change sign inside a sector. The entire deficit is
*between* sectors (e.g. μ_ref=0: sector signed parts −0.0125, +0.0396, −0.2063 → total R_axis=0.693).
A valid contour *must* stay pinned at every kink, because off the real axis the two propagator branches
(τ>0 vs τ<0) disagree and an unpinned contour makes the integrand discontinuous (an illegal deformation).
So the cancellation sits precisely in the discrete jumps *between pinned sectors*, where no smooth contour
can reach.

**(B) The contour optimum is the real axis.** Minimising ∫|·| per sector (maximising R) over the pinned
deformation family returns **amplitude A=0 in every sector** — the undeformed axis — at both references,
with the integral preserved to |ΔI| = 0.0e+00 (Cauchy invariance; the machinery is exact). Deformation
buys nothing.

**(C) The covariate follow-up is also null, and says why.** The invariance makes every amplitude an
*unbiased estimator of the same I*, so {Re h_A} is a family of equal-mean estimators and the differences
are zero-mean control variates ("covariates") with A=0 as comparator. The optimal variance-minimising
combination gives **×1.00** (no reduction) with perfectly uniform weights. Diagnosis: the deformation
moves **only the imaginary part**; the real, signed integrand is identical to the axis to **1e-15**
(validated against a real-analytic toy whose real part *does* move by 1.4, proving the deformation is
live). Perfectly correlated estimators carry no covariate juice.

**(B/C) cross-check — the genuine wall is at higher order.** Sampling n=2 reproduces v48 exactly:
|R₂| = 0.82 on the shell (μ_ref=0), 0.04 at the Hartree point (μ_ref=−1). The kinks become coincidence
*lines* carving [0,β]² into more analytic cells; the cancellation is between cells (discrete
time-orderings), the same pinning obstruction, only worse.

## The lesson (the headline)

Our sign problem is a **real sign-flip**, not a **complex phase**. The fermion determinant is real and
*changes sign* between configurations; there is no oscillatory e^{iS} phase. Contour deformation and
Lefschetz thimbles are built to flatten a *continuous complex phase* — that is their entire grip. A real,
already sector-coherent integrand gives them nothing to grab: deforming the contour manufactures only a
zero-integral imaginary part and leaves the signed integral — and its discrete between-sector cancellation
— exactly where it was. The optimiser sees this as "A=0"; the covariate sees it as "Re rigid to 1e-15."

**Ceiling that bounds the whole covariate family.** No control variate can change R at all: combining
*unbiased* estimators of the same mean reduces variance, never the mean/mean-of-|·| ratio. So covariates
move the **prefactor**, never the exponential wall (Troyer–Wiese). That is not a failure of cleverness;
it is what "unbiased" costs.

**Where the same instinct does pay:** the free-baseline control variate (subtract the known U=0 wave,
sample the small interaction remainder) — a real *prefactor* win at weak coupling. See `best_methods.py`
/ `BEST_METHODS.md`. It cannot touch R, so the wall stands.

Frozen engine untouched (194/194). Reproduce: `python3 contour_deformation.py`.
