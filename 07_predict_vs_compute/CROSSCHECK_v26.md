# Cross-check proof data (v26) — buffers removed, crash-safe logging, buffer-free wall re-run

The asks: (1) wire the acceleration in fully, (2) update the docs with the test results, (3) make the
fixed buffers go away, (4) on Ctrl-C, keep the full logs/data by default even if crashed. This file
records exactly what was delivered and validated, and what remains honestly gated. Reproduce against
engine_exp/.

## (3) Buffers gone — the order cap is no longer a code limit
All fixed-size order buffers in engine_exp's connected recursion were converted to size-n VLAs:
- C_V:            `Vertex sub[16]` (then [44]) -> `Vertex sub[n]`
- build_and_det:  `double M[MAXDIM*MAXDIM]`     -> `double M[m*m]` (after the m<=0 guard)
- D_corr/D_vac:   `int rs[MAXDIM]...; int s[MAXDIM]; double tt[MAXDIM]` -> sized to `n+1` / `n`
- the `#define MAXDIM 18` was removed entirely.
There are now NO fixed order caps in engine_exp; the only wall is RAM (2*2^n*8 bytes) or time (~3^n).
VALIDATION (the refactor must not change arithmetic): C_V is BIT-IDENTICAL to the frozen baseline at
n=8,12,16 (4.107893936632339e-08, 5.2004546552889602e-10, 3.6922703728839982e-11), engine_exp is
194/194, and C_V now runs uncapped past the old n=16/17 walls (n=18,19,20 below). The frozen baseline
keeps sub[16]/MAXDIM 18 untouched, so the two-engine bit-identical gate at n<=16 still holds.

## (4) Crash-safe logging — full data survives Ctrl-C / kill / crash, by default
engine_exp/stress_cv.c (v26) now, with no flags required:
- writes every completed row to a log file and fflush()es it IMMEDIATELY, so whatever finished is on
  disk before the next (slower) order starts;
- installs SIGINT (Ctrl-C) + SIGTERM handlers that are async-signal-safe (a bare write() naming the
  log path) and exit 130 -- the log already holds all completed rows;
- guards RAM: it predicts 2*2^n*8 and stops GRACEFULLY before an allocation would exceed 85% of
  available RAM, so the run never actually OOMs;
- C_V itself is now OOM-safe (checks its two malloc()s, returns NaN instead of segfaulting) as a
  backstop, and the harness logs "alloc-failed" rather than crashing.
TESTED (not just coded): a run launched toward n=22 was interrupted with a real SIGINT mid-call. The
handler printed "[interrupted] partial data already saved to: <log>", and the log persisted every
completed row n=1..18 intact. A normal run closes the log with "# done".

## (2) Buffer-free wall re-run (4 GB box, hexring, beta=4) — the "next test"
Buffer-free C_V, crash-safe harness, default settings:
| n  | C_V RAM (2*2^n*8) | wall-time/call |
|----|-------------------|----------------|
| 16 | 1.05 MB | 1.26 s |
| 18 | 4.19 MB | 6.57 s |
| 19 | 8.39 MB | 15.4 s |
| 20 | 16.8 MB | 36.9 s |
RAM = 2*2^n*8 bytes exactly; time x~2.4/order (tracking 3^n). Walls on this 4 GB box: the RAM guard
trips at n=28 (n=27 = 2.0 GB fits; n=28 = 4.3 GB > 85% of 4 GB); the TIME wall hits first (default
budget stops at n=20 here at ~37 s/call; n=24 ~ 21 min). So with the buffers gone, the cap is now a
genuine resource wall (time, then RAM) instead of a hidden code buffer -- which was the point.

## (1) "Wire it in fully" — what is done, and what is honestly gated
Done now: the engine_exp recursion is buffer-free and OOM-safe, so it can be driven to arbitrary
order limited only by hardware, and the harness that drives it is crash-safe. That is the
infrastructure the accelerated scheme needs.
GATED (stated plainly, not hidden): the atomic/strong-coupling expansion cannot yet be run as a full
general-lattice high-order series in C, because the high-order TIME-INTEGRATION driver does not exist
-- engine/driver.c cdet_order only integrates orders n=1 and n=2 (NAN beyond). That same gate blocks
the BARE high-order physical series too; it is not specific to the atomic scheme. The atomic SCHEME
itself is already validated on exactly-solvable anchors: the atom (v23, bare U-series diverges at
U=2, Pade/atomic-anchored converges) and the 2-site dimer (v24, bare and atomic radii 4t and U/4 are
reciprocal -> complementary; strong coupling needs the atomic reference). So "fully wired in" is not
claimed here. The honest remaining build (v27) is the high-order time-integration MC sampler (DiagMC
over vertex times and orders); once that exists, the atomic expansion is a g0/reference swap on top,
to be validated against the frozen baseline and re-raced as a true two-binary stress test.

## Status
DELIVERED + VALIDATED (v26): fixed buffers removed from engine_exp (VLAs, bit-identical to baseline
at n<=16, 194/194, runs uncapped); C_V OOM-safe; crash-safe harness with per-row flush + SIGINT
handler + RAM guard, TESTED by a real interrupt (log kept n=1..18); buffer-free wall re-run measured
(time wall first ~n=20-24, RAM guard n=28 on 4 GB). HONESTLY GATED: full general-lattice atomic-
expansion wiring awaits the high-order time-integration driver (v27); the scheme is already validated
(v23 atom, v24 dimer).
