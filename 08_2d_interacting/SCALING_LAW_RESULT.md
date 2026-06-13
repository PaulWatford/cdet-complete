# The scaling law of R: right metric, but no clean law at accessible sizes (v39)

The suggestion: stop tracking "what order did I reach" and instead fit the decay law of the sign-
cancellation ratio R -- R ~ e^{-aL}, e^{-b*beta}, or e^{-f(L,beta)} -- to get a quantitative model of where
the method dies, which becomes the benchmark any variance-reduction scheme must move. The FRAMING is right
and we adopt it. The empirical finding, honestly, is that at accessible cluster sizes the per-order R does
NOT follow a clean scaling law -- and the clean-looking fit you get first is an artifact.

## What we measured (order 3, fixed density n=0.80, mu tuned per point; R with statistical errors)
SIZE axis (beta=4), |R| vs N:  L=2:0.79  L=3:0.35  L=4:0.35  L=5:0.05  (high-stat confirmed).
  -> plateaus (L=3 ~ L=4) then collapses -- shell/filling structure, NOT an exponential. A forced
     exponential fit gives a~0.13 with R^2~0.87, i.e. it is fitting a non-exponential shape.
TEMPERATURE axis (3x3), |R| vs beta: at fixed density |R| GROWS slightly with beta (b = -0.05 +/- 0.004).
  -> the sign of the temperature exponent is ENSEMBLE-DEPENDENT: at fixed mu=0.5 we first got a clean-
     looking b = +0.35 (R^2=0.98), but that was largely DENSITY DRIFT, not temperature. 'The' temperature
     exponent is not well-defined without fixing the ensemble.
SEPARABILITY: predict |R|(N=16,beta=6) from R ~ e^{-(aN+b*beta)} anchored at (N=9,beta=4):
  predicted 0.157, measured 0.452 -- a 29-sigma failure. (N,beta) does NOT factorize.

## Why -- and the catch-22
Clean sign-problem scaling (R ~ e^{-c N beta}, the space-time-volume law) is ASYMPTOTIC. At L=2-5 the
discrete momentum shells dominate R: changing L (even at fixed density) partially fills a new shell and
moves R non-monotonically; changing the ensemble (fixed mu vs fixed density) flips trends. There is no
honest single (a,b) here -- reporting one fits shell structure, not physics. And the regime where the law
WOULD be clean (large N at fixed density) is exactly where R is exponentially small and unmeasurable
without exponentially many samples: the wall blocks measuring the wall.

## What this corrects and what stands
CORRECTS: an earlier tempting read -- the fixed-mu fits look like clean exponentials (R^2 up to 0.98) but
are ensemble artifacts; we do not report them as benchmarks. Also refines v37: its cost-grows-with-beta at
fixed mu conflated temperature with density drift; at fixed density the order-3 R behaves differently.
STANDS: the v37 wall is real (cost to fixed precision does explode with size and, at fixed mu, with beta),
and v38's order-vs-size separation is unaffected. What v39 shows is narrower and honest: the FUNCTIONAL
FORM of that wall is not cleanly captured by e^{-aL}/e^{-b*beta}/e^{-f(L,beta)} for the per-order-3 R at
accessible sizes.

## Refined success criterion (honest)
The concept is correct -- judge a scheme by whether it moves R's decay, not by order reached. But the
observable must be chosen so a clean law exists: the accessible-size per-order R is shell-dominated and
ensemble-sensitive, so it is the wrong thing to fit. A meaningful benchmark needs either larger clusters
at fixed density (currently unmeasurable), or an asymptotically cleaner observable (the resummed sign, or
R extrapolated along a fixed-shell family). Reproduce: make scaling.
