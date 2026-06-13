# Cross-check (v41) — the organizing variable: R is universal in the Fermi-shell detuning

Reproduce: 08_2d_interacting (make shell). Responds to the critique that v40 had "no internally consistent
scaling diagnostic at small clusters" by finding the variable that makes it consistent.

## What was checked (order 2, beta=4)
delta = mu - (nearest single-particle shell). R vs delta across L=2,3,4 (central shells):
  delta:  -1.0   -0.5   0.0    +0.5   +1.0
  L=2:   -0.04  +0.57  +0.82  -0.71  -0.74
  L=3:   -0.21  +0.37  +0.60  -0.36  -0.32
  L=4:   -0.09  +0.28  +0.50  -0.43  -0.16
Universal SIGN structure: positive below the shell, peak at delta=0, sign flip just above -- same in every
cluster. Amplitude A(N)=R(0)=0.82,0.60,0.50 shrinks with N; R/A collapses near the shell.
Temperature is a separate axis: beta*delta is NOT a single variable (L=3, beta*delta=-2: +0.37 at beta=4 vs
-0.05 at beta=2 -- no collapse across beta).

## Conclusion
The per-cluster "shell noise" of v39/v40 is one universal curve R(delta) sampled at different delta; R-vs-N
looked random only because each cluster sat at a different detuning. Organized by delta (at fixed T) the
estimator IS internally consistent -- the diagnostic exists, it is R-vs-detuning. This makes the v40 "fix the
filling" cure quantitative: hold delta fixed (e.g. delta=0). Honest bounds: magnitude collapse is clean only
near the shell; temperature is a separate axis; shown at n=2, beta=4, central shells of L=2,3,4.

## Refines
v40's "no diagnostic" -> "the diagnostic is R(delta) at fixed T." The clean size-scaling quantity is the
amplitude A(N) at fixed delta=0, not a raw R (v42 target). v39/v37 walls unaffected.
