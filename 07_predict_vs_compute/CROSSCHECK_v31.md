# Cross-check (v31) — out-of-core C_V by bit-split blocking: accurate, RAM-bounded, HDD-overflow

Decision + question from the user: (a) shelve the butterfly (it trades away accuracy and RAM, the two
criteria, to buy speed, which is not a criterion); (b) "we process the 2^n in a specific order -- why
can't we schedule HDD<->RAM the same way?" Answer: you can, and it is the right tool here. Reproduce:
engine_exp/blocked_cv.c (built against engine_exp; needs the buffers-gone determinants).

## Correction of an earlier overclaim
v28/v29 said out-of-core on the scattered recursion is "hopeless." That was true for NAIVE paging
(let the OS fault on random addresses -> thrash). It is FALSE for a scheduled blocking, because the
processing order is known and the submask lattice FACTORIZES over a bit-split. The user was right.

## The factorization
Split the n bits into nH high + nL low; mask=(h,l). Then sm subset mask  <=>  sm_H subset h AND
sm_L subset l. So the recursion becomes a BLOCK-LEVEL subset recursion (each element a contiguous
2^nL block, the product a low-block subset convolution):
    C[h,.] = Dc[h,.] - SUM_{hs proper-subset h} C[hs,.] (low-conv) Dv[h\hs,.]  - (within-block low recursion)
Process h in increasing order (hs subset h => hs < h): to build block h, load only blocks hs subset h
and h\hs, one at a time. The schedule is predictable (sequential block reads, no random thrash); the
arithmetic is the EXACT direct sum (no Mobius), so accuracy equals the flat engine.

## Validation (disk-backed; blocks written to a scratch dir, streamed in/out)
| n  | split (nL,nH) | flat C_V vs blocked | peak RAM | flat 2*2^n | reduction |
|----|---------------|---------------------|----------|------------|-----------|
| 12 | 6, 6          | diff 2e-20          | 3 blocks (0.0015 MB) | 0.066 MB | 43x  |
| 16 | 10, 6         | diff 4e-21          | 3 blocks (0.025 MB)  | 1.05 MB  | 43x  |
| 18 | 10, 8         | diff 3e-21          | 3 blocks (0.025 MB)  | 4.19 MB  | 171x |
Two facts: (1) the blocked result matches flat C_V to ~1e-20 -- full accuracy, no loss (the opposite
of the butterfly). (2) peak RAM is a FIXED 3 blocks = O(2^nL), independent of n -- so the reduction
grows without bound with n (at n=27, nL=10: flat ~2 GB vs blocked 0.025 MB, ~80000x). The full 2^n
lives on disk; RAM holds only the working blocks.

## Why this fits the criteria (and the butterfly does not)
Criteria: maximum n at the highest accuracy, RAM minimized, HDD used only on overflow, speed not a
concern (a huge-lattice run may take many hours). Blocking delivers exactly this: exact arithmetic
(accuracy), peak RAM = O(2^nL) you choose to fit memory (RAM), the 2^n on disk only when n exceeds
RAM (HDD overflow), at the cost of total block I/O ~3^nH and more time (acceptable). The butterfly is
the inverse trade (less accuracy, MORE RAM, faster in a narrow window) -- shelved as a niche option.

## Honest cost and scope
- Cost: total block reads ~ SUM_h 2^popcount(h) ~ 3^nH, each a sequential 2^nL block; disk holds O(2^n)
  for Dv and C. So it is I/O- and time-heavy, RAM-light -- by design. Use the flat in-RAM C_V for
  small n (fast), the blocked path only when 2^n exceeds RAM (the huge runs).
- Scope: blocked_cv.c blocks ONE fixed-vertex C_V evaluation (the 2^n RAM object). Wiring it under
  cdet_order_mc (so each high-order MC sample that overflows RAM runs out-of-core) and pushing it to
  very large n on real disk is the deployment step. The factorization and the RAM bound are proven
  here; the integration is mechanical but untested at scale.

## Status
VALIDATED (v31): the bit-split blocking reproduces flat C_V to ~1e-20 (full accuracy) with peak RAM
fixed at 3 blocks = O(2^nL), independent of n (43x-171x less at n=12-18, growing). This is the
accuracy-first, RAM-bounded, HDD-overflow path the criteria call for; the butterfly is shelved.
Earlier "out-of-core hopeless" claim corrected: scheduled blocking works because the lattice
factorizes over a bit-split. NEXT: wire under cdet_order_mc for the huge-lattice high-order runs.
