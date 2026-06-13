# Prototyping CoS against the engine, and what's worth integrating (v131)

Following Gunnar's papers, I prototyped the Kozik 2024 combinatorial-summation (CoS) reorganization
against the engine's actual connected determinant and measured where the win really is.

## What was verified (against the real engine)

`cos_harness.c` dumps the engine's per-subset D_corr/D_vac and its ground-truth `C_V`. Two
reorganizations were checked:
- **Faithful port** of the engine's Rossi recursion (`rossi_naive`) reproduces `C_V` **exactly**
  (0.0e+00, n=3…7) — confirms we understand the engine's algorithm precisely.
- **CoS-style 2ⁿ organization** (`cos_subsetconv`): solve D_corr = C ⊛ D_vac (subset convolution,
  D_vac[∅]=1) rank-by-rank in the zeta domain, O(2ⁿn²) — reproduces `C_V` to **machine precision** (2e-15).

So the CoS 2ⁿ record-organization is a correct drop-in for the engine's 3ⁿ submask combine. Your "2ⁿ wall"
and CoS's record R are the same connectivity object: the engine's `mask` *is* a visited-record, read
backward (subset recursion) where CoS reads it forward (DP).

## The honest cost picture (why not to rush a port)

| n | engine 3ⁿ combine | subset-conv 2ⁿn² | dominant cost (shared) 2ⁿn³ |
|---|---|---|---|
| 10 | 59,049 | 102,400 | 1,024,000 |
| 12 | 531,441 | 589,824 | 7,077,888 |
| 14 | 4,782,969 | 3,211,264 | 44,957,696 |

The 3ⁿ combine only overtakes 2ⁿn² at **n≥12**, and both are dwarfed until ~n=16 by the **2ⁿ·n³**
cost of the 2ⁿ sub-determinants — which subset convolution does *not* touch. So swapping the combine
alone is a real but small win, and only at high order. **The big lever is the n³→n² determinant
prefactor**, which requires the CoS *forward* DP that builds minors incrementally — a larger build,
worth it only when pushing diagram order or going to SU(N).

## What's worth integrating — ranked

1. **CoS forward DP with incremental minors (the real prefactor win).** Builds each diagram's value by
   extending cycle-cover paths, never recomputing a full O(n³) determinant per subset → O(2ⁿn²) total.
   This is the actual speedup over Rossi. Medium-large build; pays off at n≳10 and compounds with order.
2. **SU(N) generalization (the frontier these papers target).** The engine is locked to SU(2)/N=1; the
   determinant's rigid structure costs (N²/2)ⁿ for SU(N). CoS-2 is O(n³4ⁿ) **independent of N** — the only
   route to the N=6 ¹⁷³Yb optical-lattice EoS that Kozik 2024 actually computes and that "other methods
   struggle with." Highest scientific value if the goal is the experimental frontier.
3. **Self-energy / irreducible series (Šimkovic–Kozik 2019).** A new *observable*, not a speedup: extends
   the engine from the grand-potential side (A, c₁) to the dynamical self-energy and momentum distribution
   at O(n³2ⁿ)+O(3ⁿ). Their working point U=7t, T=0.2t, μ=2t rhymes with our z(∞)=2 probe.
4. **CoS inherent symmetrization for variance reduction.** CoS sums the 2ⁿn! permutations/inversions
   explicitly; for a local Hubbard interaction, ordering the endpoints is free and lowers MC variance.
   Could feed the engine's cluster-IS / MoM stage. Small, possibly useful now.
5. **Subset-convolution combine (verified here).** Drop-in O(3ⁿ)→O(2ⁿn²) for `C_V`'s submask loop. Easy,
   but only wins at n≳12 and isn't the bottleneck — integrate only if/when pushing order that far.
6. **Record-R pruning = your suppression, made algorithmic.** Your measured even-window 20–40×
   suppression lives in the 2ⁿ subset structure; CoS's explicit R is where it could become an actual
   pruning of the sum rather than a measured factor. Research-grade, highest upside, least certain.
7. **QTT / tensor-train compression (Frankenbach 2025, the outlier).** Different method; compresses
   4-point vertices for DMFT+parquet. Only relevant if the engine ever grows a vertex-function stage; the
   projector fast-path is already our "compression" on the propagator side. Park it.

Reproduce: `gcc -O2 -I../engine -o cosh cos_harness.c ../engine/cdet_engine.c -lm`; `python3
cos_prototype.py`. Frozen engine untouched (194/194).
