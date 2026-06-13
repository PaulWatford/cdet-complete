# Upgrade test for the "thermal" claim: two axes support it, the order-cutoff refutes it (v43)

The v42 claim "the near-shell feature is thermal (range ~ T)" was, correctly, only "consistent with
thermal." To upgrade it one must show the scaling survives mechanism-separation (order cutoff, alternative
formulations), spectral consistency, and finite-size control. We ran the decisive ones. Outcome: the
ORDER-2 feature width is thermal-consistent on two independent axes, but the feature is NOT order-robust,
so a UNIVERSAL thermal-broadening claim is NOT established. This corrects/narrows v42.

## Test C -- finite-size and temperature control (the decisive thermal-vs-shell discriminator)
Thermal broadening has width ~ T independent of N; shell spacing scales with N. We measure the sign-flip
detuning delta* (the feature width).
  SIZE (beta=4, n=2):  N=4: delta*=0.24   N=9: delta*=0.26   N=16: delta*=0.21   -> N-INDEPENDENT
    (the level spacing varies strongly across these clusters, yet delta* does not -> not shell-spacing).
  TEMPERATURE (L=2, n=2): beta=2: 0.61   beta=4: 0.24   beta=8: 0.11  (delta*/T = 1.22, 0.97, 0.84)
    -> delta* ~ T.
Both axes are thermal-consistent: at fixed order, the feature width is set by temperature, not by N.

## Test A -- order-cutoff: is it the SAME feature across orders? NO.
R(delta) at L=2, beta=4, by order:
  n=1: monotonic in delta (no peak; crossing near delta=-0.45) -- the Hartree term has no such feature.
  n=2: positive peak at delta=0, sign flip at delta=+0.24.
  n=3: positive peak near delta=+0.2, NEGATIVE below the shell, sign flip near delta=+0.55.
The shape, sign structure, and zero-crossing all change qualitatively with expansion order. There is no
single order-independent feature being broadened -> Test A FAILS.

## Verdict (honest, corrects v42)
- SUPPORTED: the order-2 feature width is N-independent (Test C size) and proportional to T (Test C
  temperature) -- thermal-consistent on two independent axes, ruling out shell-spacing as the width-setter.
- REFUTED: order-robustness (Test A) -- each order has its own delta-structure, so "thermal broadening" is
  not a universal mechanism of a single feature.
- NET: v42's "the near-shell feature is thermal" is downgraded to "the n=2 feature WIDTH is thermal-
  consistent (N-independent, ~T)." As the critique warned, without order-robustness the thermal ORIGIN
  remains underdetermined. The v41 organizing-variable result (R is structured by the detuning delta, at
  fixed order and temperature) is unaffected; only the v42 "thermal mechanism" framing is narrowed.

## Not done
Spectral-function broadening cross-check (Test B) and alternative-estimator reformulations were not run;
given Test A already fails, they would at most support the narrow n=2 sub-claim, not rescue the universal
one. Reproduce: make thermal.
