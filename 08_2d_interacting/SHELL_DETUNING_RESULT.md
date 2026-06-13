# The organizing variable: R is universal in the Fermi-shell detuning (v41)

The critique of v40 was right and sharpening: what we had shown was only that observables from THIS estimator
at THESE cluster sizes inherit the contamination -- "no internally consistent scaling diagnostic at small
clusters." The right question (posed back): what single quantity affects every cluster, differently, in a way
that encodes where the cluster sits? Answer, found here: the Fermi-level DETUNING.

## The finding
Define delta = mu - (nearest non-interacting single-particle shell eps_k). At FIXED temperature, the per-order
sign-cancellation ratio R is a UNIVERSAL function of delta across clusters:
  delta:   -1.00    -0.50    0.00    +0.50    +1.00
  L=2:    -0.038   +0.573  +0.822  -0.714   -0.738
  L=3:    -0.207   +0.368  +0.599  -0.359   -0.317
  L=4:    -0.090   +0.277  +0.502  -0.431   -0.156
Same sign structure in every cluster: positive just below a shell, a positive PEAK when the shell sits at the
Fermi level (delta=0), a sign flip to negative just above it (zero-crossing just above delta=0 for all).
The cluster enters only through (i) where its mu sits -- delta -- and (ii) an amplitude
  A(N) = R(delta=0) = 0.822 (N=4), 0.599 (N=9), 0.502 (N=16),  shrinking with size.
After dividing by A(N) the shapes collapse near the shell (delta=-0.5: 0.55-0.70; delta=+0.5: -0.60..-0.87).

## What this means
The "shell noise" of v39/v40 was never noise: it is one universal curve R(delta) sampled at scattered delta.
R-vs-N looks random only because each cluster's mu sits at a different delta. Organized by delta, the estimator
IS internally consistent -- so the diagnostic the critique said was missing exists; it is R-vs-detuning, not
R-vs-size. This also makes the v40 cure quantitative: to compare clusters consistently, hold delta fixed
(e.g. delta=0, a shell exactly at the Fermi level) -- the precise form of "fix the filling fraction."

## Honest bounds
- The SIGN structure collapses cleanly across clusters; the MAGNITUDE collapses near the shell (|delta|<~0.5)
  and scatters in the wings (small R, more levels contributing, measurement noise).
- Temperature is a SEPARATE axis: beta*delta is NOT a single scaling variable. At matched beta*delta the
  curves do not collapse across beta (L=3: beta*delta=-2 gives +0.37 at beta=4 but -0.05 at beta=2). So delta
  organizes the size/filling dependence at fixed T; folding in temperature needs more than the product.
- Shown at order n=2, beta=4, central shells of L=2,3,4. A universal-curve claim at all orders/temperatures is
  not made; what is established is that delta (not N) is the organizing variable for the size/filling axis.

## Consequence for the program
This converts "no diagnostic" into "the diagnostic is R(delta) at fixed T," and pins the correct controlled
comparison (fixed delta). The next step (v42) is to ride delta=0 across a cluster family and ask how A(N)
scales -- that amplitude, not a raw R, is the clean size-scaling quantity, and the benchmark a variance-
reduction scheme must move. Reproduce: make shell.
