# Cross-check (v39) — the scaling law of R: right metric, no clean law at accessible sizes

Reproduce: 08_2d_interacting (make scaling). Tests the suggestion to fit R ~ e^{-aL}/e^{-b*beta}/e^{-f(L,beta)}.

## What was checked (order 3, fixed density n=0.80, mu tuned per point, R with stat. errors)
- SIZE (beta=4): |R| vs N = 0.79, 0.35, 0.35, 0.05 for L=2,3,4,5 -> plateau then collapse (shell
  structure), NOT exponential; forced fit a~0.13 R^2~0.87 is fitting a non-exponential shape.
- TEMPERATURE (3x3): at fixed density |R| grows slightly with beta (b=-0.05); at fixed mu it fell
  (b=+0.35, R^2=0.98) -- that clean fit was DENSITY DRIFT. Temperature exponent is ensemble-dependent.
- SEPARABILITY: predict |R|(16,6) from e^{-(aN+b*beta)} anchored at (9,4): 0.157 predicted vs 0.452
  measured = 29 sigma. (N,beta) does not factorize.

## Conclusion
The FRAMING is right (judge schemes by R's decay, not order reached) but there is NO honest clean scaling
law for the per-order-3 R at L=2-5: it is shell-dominated and ensemble-sensitive, and the separable
exponential form fails by 29 sigma. Reporting a single (a,b) here would fit shell structure, not physics.
Clean scaling is asymptotic (large N at fixed density), exactly where R is too small to measure -- the wall
blocks measuring the wall.

## Corrects / stands
CORRECTS: the tempting fixed-mu fits (R^2 up to 0.98) are ensemble artifacts, not benchmarks; and v37's
cost-vs-beta at fixed mu conflated temperature with density drift. STANDS: the v37 wall is real and v38's
order-vs-size separation is unaffected; only the claim of a clean parametric FORM for R is withdrawn.

## Honest scope
Single order (n=3), small clusters (N<=25), one density (0.80); R measurable only where not yet tiny.
No claim of asymptotic exponents -- the point is precisely that they are not cleanly accessible here.
