# Cross-check (v43) — upgrade test for "thermal": size/temperature support it, order-cutoff refutes it

Reproduce: 08_2d_interacting (make thermal). Tests whether v42's "thermal" claim survives the demanded
mechanism-separation / finite-size controls.

## Results
- TEST C (finite-size, beta=4, n=2): delta* = 0.24, 0.26, 0.21 for N=4,9,16 -> N-INDEPENDENT (level
  spacing varies strongly across these clusters; delta* does not) -> thermal, not shell-spacing.
- TEST C (temperature, L=2, n=2): delta* = 0.61, 0.24, 0.11 for beta=2,4,8 (delta*/T = 1.22,0.97,0.84)
  -> delta* ~ T.
- TEST A (order-cutoff, L=2, beta=4): the feature is NOT the same across orders -- n=1 monotonic (no peak),
  n=2 peak at delta=0 (crossing +0.24), n=3 peak at +0.2 with opposite sign below the shell (crossing
  +0.55). Shape/sign/zero-crossing change qualitatively with order -> Test A FAILS.

## Verdict (corrects v42)
SUPPORTED: the order-2 feature WIDTH is N-independent and ~ T (thermal-consistent on two axes).
REFUTED: order-robustness -- no single feature is being broadened.
NET: v42's "the near-shell feature is thermal" -> "the n=2 feature width is thermal-consistent." Without
order-robustness the thermal ORIGIN is underdetermined, exactly as the critique warned. v41 (R organized
by detuning delta at fixed order/T) stands; only the v42 thermal-mechanism framing is narrowed.

## Not done
Spectral-broadening cross-check and alternative-estimator reformulations were not run; with Test A already
failing they could only support the narrow n=2 sub-claim.
