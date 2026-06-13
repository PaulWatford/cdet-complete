# Cross-check (v28) — can the 3^n submask recursion be made contiguous? Literature + a measured POC

The questions: (1) is "random access" a property of memory or of the algorithm? (2) can the scattered
submasks be reordered so the process is contiguous? (3) the C[N-1] "killer" reads every submask --
is there a known process that handles all of this? And: design an out-of-core split of the 2^n
arrays that activates ONLY at the RAM wall. Searched the literature and built a proof of concept.

## The answers (short)
1. Not memory -- the ALGORITHM. RAM is random-access-capable; the naive submask recursion simply HAS
   a scattered (gather) access pattern. A different algorithm over the same array can be strided.
2. Yes. The scattered O(3^n) submask sum is a SUBSET CONVOLUTION, and the fast zeta/Mobius (Yates /
   butterfly) transform computes it in O(2^n n^2) with passes that "touch only contiguous memory --
   no scatter/gather" (FWHT/butterfly structure). Ref: Bjorklund, Husfeldt, Kaski, Koivisto,
   "Fourier meets Mobius: fast subset convolution," STOC 2007 (O(2^n n^2) vs naive O(3^n)).
3. The "killer" dissolves: in the transform form no single entry gathers all its submasks; the
   all-subsets dependency is handled GLOBALLY by n strided sweeps (the zeta propagates partial sums
   across the lattice). The connected-determinant recursion itself (Rossi) is known to scale as
   O(2^n n^3 + 3^n) -- the 3^n is exactly this submask sum, the target of the transform.

## What the POC measured (engine_exp/subset_conv_poc.c; naive 3^n vs ranked butterfly 2^n n^2)
| n  | naive O(3^n) | fast O(2^n n^2) | speedup | max|diff| | max rel |
|----|--------------|------------------|---------|-----------|---------|
| 12 | 0.00118 s    | 0.00298 s        | 0.4x    | 3.7e-14   | 9.2e-13 |
| 14 | 0.00606 s    | 0.0188 s         | 0.3x    | 4.2e-13   | 1.6e-11 |
| 16 | 0.0569 s     | 0.188 s          | 0.3x    | 1.9e-12   | 3.1e-09 |
| 18 | 0.552 s      | 1.06 s           | 0.5x    | 9.1e-12   | 3.1e-09 |
Correctness: the contiguous butterfly REPRODUCES the naive convolution (~1e-12 absolute) -- the
rewrite works. But two honest problems for OUR use:
- SLOWER at reachable orders: the ranked convolution carries n+1 popcount ranks (to enforce disjoint
  T, S\T), so 2(n+1) transforms + ~n^2/2 rank products per element. The constant is large; the
  wall-time crossover where it actually beats 3^n is far out (~n=20-22 extrapolated, the fast/naive
  ratio falls 3.3x -> 1.9x from n=16 to 18), beyond where RAM already walls.
- LESS PRECISE: on benign random data the Mobius alternating +/- already loses ~7 digits (max rel
  3e-9 at n>=16). Our connected value is a CANCELLATION RESIDUAL of large disconnected terms
  (methodology #31), so this is our worst enemy amplified. Practitioners have avoided fast subset
  convolution for exactly this rounding reason (Kohonen & Corander, per the FFT-revisit literature).

## Memory: it makes the RAM wall EARLIER, not later
The ranked embedding needs the array in n+1 popcount slots -> O(2^n * n) memory, ~n/2 times MORE than
the current 2*2^n. So for the RAM question specifically, the fast transform is a time-vs-RAM trade in
the WRONG direction (more RAM), with a far-out time crossover. It is not a RAM-wall fix by itself.

## Out-of-core "cut up the 2^n only at the RAM wall" -- the honest design
- On the SCATTERED form (today): blocking is hopeless -- forming C[mask] reads submasks scattered
  across the whole array, and C[N-1] reads all of it; an mmap/paged version runs but thrashes on
  random I/O. So a clean out-of-core split is not available on the current recursion.
- On the CONTIGUOUS (butterfly) form: each pass is a stride-2^i sweep, which IS blockable. This is the
  one real payoff of the rewrite: external-memory / cache-oblivious butterfly transforms achieve the
  standard O((N/B) log_{M/B}(N/B)) I/O bound and reorganize data between stages for locality (cache-
  conscious WHT). So the viable design is: reorganize to butterfly form, THEN stream blocks from disk
  during each sweep, activating only when 2^n exceeds RAM -- accepting the n-fold memory blowup and
  the precision risk. The access pattern is what makes it feasible; the constants are what make it a
  last resort.

## Verdict (honest)
Your instinct was right and it maps to a real, named technique (fast subset convolution / zeta-Mobius
butterfly): the recursion CAN be made contiguous, and that is exactly the structure external-memory
streaming needs. But for our reachable orders it is a poor trade -- slower (heavy constant, far
crossover), MORE memory (n+1 ranks), and precision-losing on the cancellation residuals we compute.
So: it is the right tool only for "I must exceed RAM and will tolerate slowdown + precision risk,"
and the wrong tool for "go faster within RAM." The lever for going faster within RAM stays REDUCING n
(the atomic reference, v23/v24), because cutting n by 1 saves 2x RAM and ~3x time at once, with no
precision penalty -- the opposite trade. Next (v29): if out-of-core is wanted, prototype the blocked
butterfly + test its precision on REAL cancelling C_V data (benign-random agreement is necessary, not
sufficient); otherwise push the atomic-reference swap into cdet_order_mc (the real RAM/time lever).

## References (searched)
- Bjorklund, Husfeldt, Kaski, Koivisto, "Fourier meets Mobius: fast subset convolution," STOC 2007 --
  O(2^n n^2) subset convolution via zeta/Mobius.
- Rossi, "Determinant Diagrammatic Monte Carlo in the thermodynamic limit," PRL 119, 045701 (2017);
  connected-determinant recursion O(2^n n^3 + 3^n) (the 3^n = the submask sum here).
- FWHT/butterfly locality ("touch only contiguous memory, no scatter/gather"); cache-conscious WHT
  (data reorganization between stages); cache-oblivious / external-memory transforms,
  O((N/B) log_{M/B}(N/B)) I/Os.
