# cdet streaming connected-determinant — validated core + design

Goal: compute the order-n connected determinant past the in-RAM wall (3·2ⁿ doubles,
hard-capped at n≈28 / ~6 GB in the stock engine) by an algorithm whose memory can be
streamed to disk — **fast, and exact**.

`cdet_stream.c` is the validated algorithmic core. Build/run:

    cc -O2 -std=c99 -I<engine_dir> cdet_stream.c cdet_engine.o -lm -o cdet_stream
    ./cdet_stream      # prints C_V vs ranked-convolution for n=1..16, with rel.diff

## What it does

The Rossi recursion `C[S] = Dc[S] − Σ_{T⊊S} C[T]·Dv[S\T]` is exactly the subset
convolution `C * Dv = Dc` (with `Dv[∅]=1`). Solving it by the **ranked zeta/Möbius
transform** replaces the O(3ⁿ) scattered-submask recursion with:
1. up-zeta of the ranked Dc, Dv slices — n sequential Yates passes;
2. a per-point truncated power-series division `H = Dc/Dv` (fully local per mask);
3. down-Möbius back — n sequential Yates passes; `C[S] = H[ |S| ][S]`.

Steps 1 and 3 sweep the array in big sequential blocks (stride 2ᵇ per bit) and step 2
is per-mask local — an access pattern that **streams** from disk, unlike the random
submask reads of the direct recursion. Time is O(n²·2ⁿ), faster than O(3ⁿ).

## Validation (the non-negotiable part)

Checked bit-for-bit against the engine's `C_V` (the verified Rossi recursion), atom
propagator, n=1..16:

| precision | max rel. error vs C_V at n=16 | verdict |
|---|---|---|
| float64 | 1.0×10⁻⁷ | exact algorithm, **conditioning-limited** |
| long double (80-bit) | 3.2×10⁻¹² | **PASS** to 1e-9 for all n |

So the reformulation is mathematically exact; the float64 error is pure cancellation in
the zeta→Möbius round trip (large subset-sums formed, then differenced back). It grows
~½ digit per order, so float64 loses *all* precision near n≈28 — the target. **Extended
precision in the transform is mandatory** to keep it 100% accurate. long double (native,
~free on x86) holds it to ~n=35; `__float128` (software, slower) doubles the digits;
arbitrary precision covers any n.

## The two findings that decide the final form

**Finding 1 — precision.** The streaming reformulation must run the transform in extended
precision (validated above). Not optional.

**Finding 2 — storage.** The ranked transform carries an (n+1)× blow-up (it stores n+1
rank slices). Streamed to disk in long double that is large:

| n | direct, in-RAM (2·2ⁿ, double) | ranked, streamed (2·(n+1)·2ⁿ, long double) |
|---|---|---|
| 24 | 0.27 GB | 13.4 GB |
| 26 | 1.07 GB | 58 GB |
| 28 | 4.29 GB | 249 GB |
| 30 | 17.2 GB | 1065 GB |

So the ranked route trades a ~4 GB RAM wall at n=28 for ~250 GB of (sequential, fast)
disk. Practical to ~n=24–26 on an ordinary disk; n≥28 needs a large one.

## The two real paths (this is the decision)

**Path A — ranked convolution + extended precision (this core).** Fast (O(n²2ⁿ)), pure
sequential disk I/O, exact to ~1e-12 in long double. Cost: the (n+1)× storage blow-up
above, and not bit-identical to the stock engine (matches to ~1e-12, not to the last ulp).
Best when disk is plentiful and speed matters.

**Path B — blocked direct recursion.** Keep the frugal 2·2ⁿ footprint (no (n+1)×; ~4 GB
at n=28, streamable to disk in small blocks) and the direct recursion's bit-perfect
stability (no precision issue at all). Stream it via a sub-cube–contiguous ("dimensional
coordinate") block layout so the submask reads have locality. Cost: O(3ⁿ) time (slower
than A) and structured block I/O rather than pure sequential. Best when storage or
bit-identical accuracy is the binding constraint.

## Save points (both paths)

Each popcount layer is **write-once**: `C[mask]` is computed at layer `|mask|` and only
read afterward. So a checkpoint after layer k (dump the array + the marker `k`) is exact
and resumable — restart reloads and continues at k+1. This gives crash-resilience and
staged runs in both paths; in Path B's blocked layout the natural checkpoint is per block.
Checkpointing does not by itself lower peak footprint (lower layers are still read by
higher ones); it buys resumability.

## Status

Delivered and validated: the exact streaming **algorithm** core (Path A, long double).
Not yet built: the disk-backing layer (mmap/chunked files + the per-layer checkpoint
writer) — its final shape is Path A vs Path B, which depends on target n and disk budget.
