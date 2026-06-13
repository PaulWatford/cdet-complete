# Cross-check (v29) — in RAM (no disk): does the subset-convolution rewrite help, and is the error fixable?

Two questions, dropping the streaming/out-of-core idea entirely: (1) sticking to RAM, is the fast
subset convolution worth it? (2) is the butterfly's inaccuracy a fixed ratio we can correct for, or
can the control-variate idea be reused? Measured both (engine_exp/subset_conv_poc.c).

## Correction to v28
v28 concluded the fast (butterfly) form is "slower in our regime." That was measured only to n=18 --
JUST below the crossover -- so it was too pessimistic. Corrected here with higher-n data.

## (1) In-RAM wall-time crossover is n=19, and the butterfly wins above it
| n  | naive O(3^n) | fast O(2^n n^2) | speedup |
|----|--------------|------------------|---------|
| 18 | 0.53 s       | 1.03 s           | 0.51x (slower) |
| 19 | 1.74 s       | 1.62 s           | 1.08x (crossover) |
| 20 | 6.03 s       | 3.46 s           | 1.74x |
| 21 | 20.3 s       | 7.52 s           | 2.70x |
So in RAM, for n>=19 the contiguous butterfly is genuinely faster and the gain grows with order
(2.7x at n=21). This is a real in-RAM speedup, not a disk trick.

BUT the memory trade is the catch: the ranked form carries n+1 popcount slots, ~(n+1)/2 times more
RAM than the engine's 2*2^n. So its RAM wall lands a few orders earlier (~n=24 vs the naive engine's
~n=27 on 4 GB). Net: a speed-vs-RAM trade in a WINDOW (n~19-23) -- faster there if you have the RAM
headroom, but it surrenders the top few orders to memory. If you are time-bound in that window it
helps; if you are RAM-bound and want the highest reachable order, the naive 2*2^n form wins.

## (2) The inaccuracy is catastrophic cancellation, NOT a fixed ratio -- and it is precision-recoverable
| n  | max-rel (double) | max-rel (long double) | recovered |
|----|------------------|------------------------|-----------|
| 14 | 1.6e-11          | 1.2e-12                | 14x |
| 16 | 3.1e-09          | 7.9e-10                | 4x |
The error is not a fixed correctable ratio: it GROWS with n (9.2e-13 at n=12 -> 6.2e-9 at n=21),
because the Mobius alternating +/- loses significant digits on large intermediate values. Proof that
it is rounding and not a systematic bias: just adding mantissa bits (long double, +11 bits) shrinks
it 4-14x. So the "correction" is computational precision -- double-double (106-bit) would recover
most of it at ~2-4x compute cost -- NOT a cheap post-hoc scale/offset. A fixed ratio would be
immune to precision; this is not.

## Can the control-variate machinery fix it?
Not the Monte-Carlo control variate itself: that reduces the STATISTICAL variance of a random
estimator (02_control_variate), whereas this is DETERMINISTIC rounding (same inputs -> same error
bit-for-bit). Variance reduction does not touch deterministic cancellation.
But the control-variate PRINCIPLE -- subtract a known correlated reference so the residual is small
-- is exactly the cure, and it is the SAME atomic-reference lever (v23/v24): the cancellation is
vicious precisely because the connected value is a tiny residual of huge disconnected terms (#31).
Reformulate around a reference where the residual is not tiny, and the catastrophic cancellation
disappears at its source. (Also note: the naive O(3^n) direct sum has NO alternating-sign
cancellation -- it is well-conditioned -- which is why it stays the safer default below n=19.)

## Verdict
Sticking to RAM, the subset-convolution rewrite IS worth something: a real ~1.7-2.7x speedup for
n>=19, growing with order. Its costs are (a) ~(n+1)/2x more RAM, pulling the RAM wall in a few orders,
and (b) cancellation error ~1e-9 (recoverable to ~1e-12 with long double at ~2x cost). So it is a
usable tool in the n~19-23 window when time-bound, with the precision handled by long double and the
memory cost accepted. It is NOT a way to reach HIGHER orders (it walls on RAM earlier), and it does
not remove the deeper need for a better reference. The penalty-free lever for both speed AND reaching
higher order remains reducing n (the atomic reference): -1 order = 2x less RAM and ~3x less time, no
precision cost -- and it is also the cure for the cancellation. Next (v29+): push the atomic-reference
swap into cdet_order_mc; optionally use the fast buttersfly (long-double Mobius) for the deterministic
high-order term evaluation in the n~19-23 window where it pays.

## Status
MEASURED (v29): in-RAM crossover n=19, fast 2.7x at n=21 (corrects v28's "slower"); fast form costs
~(n+1)/2x RAM (wall a few orders earlier). Error is cancellation (grows with n), recoverable by
precision (long double 4-14x) -- not a fixed ratio, and not fixable by the MC control variate (it is
deterministic); the control-variate PRINCIPLE = the atomic reference, which is the real cure. Gates
intact; POC ships the long-double path.
