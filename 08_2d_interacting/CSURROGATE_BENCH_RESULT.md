# The C surrogate under test (v87): clean-room, efficiency, the orders-of-n answer, and a scope revision

**Self-containment (clean-room).** Five files (`csurrogate.{c,h}`, the two generated headers, the
test) copied to an empty directory build with nothing but gcc — and the clean-room immediately paid
for itself with three portability catches, all fixed in the shipped source: `M_PI` is POSIX, not
strict C99 (guard added); a const-array pedantry under `-pedantic` C11 (const dropped on the
internal helper); the benchmark's `clock_gettime` needs the POSIX feature macro. The module now
builds clean under `-std=c99` and `-std=c11 -pedantic`, both `-Wall -Werror`, and the gate still
matches at 3.6e-15. It also interoperates with the existing Python modules by construction — the
gate regenerates its references live from `feats2`, `classify_true_rank1`, `residue_ratio`, and
`selection_rule` every run.

**Efficiency (gcc -O2, this environment):**

| API | per call | rate | Python equivalent |
|---|---|---|---|
| surr_features | 1.47 µs | 0.68 M/s | feats2: 312 µs → **×212** |
| surr_ln_magnitude | 1.49 µs | 0.67 M/s | — |
| surr_sector | 7.2 µs | 0.14 M/s | (O(L⁴) line enumeration) |
| surr_class1_flips | 19 ns | 52 M/s | — |
| surr_class2_static / regime | ~3 ns | ~355 M/s | — |
| surr_orientation | 5.6 ns | 178 M/s | — |

Per **answer** against exact computation: one τ-averaged n=3 coefficient (NT=576 protocol) costs
~1.3 s in the Python engine port; the C magnitude prediction costs 1.5 µs — **~875,000× per
answer**, and the ratio grows as ~2.6ⁿ with order.

**The orders-of-n answer — two ceilings, stated separately.**
- *Computational:* measured exact-C_V cost grows ×2.5–3.3 per order (1.75 ms at n=3 → 745 ms at
  n=9, one τ-point). The surrogate's atlas laws are O(1) in n (ns); the feature kernel generalized
  to n sites is O(n²) in C: 0.5 µs at n=3 → 1.7 ms at n=200 (scaling probe, not the shipped
  module). Computationally the surrogate is effectively unbounded in n.
- *Validity:* the shipped laws and weights are **n=3-derived**. Higher orders need their own
  extraction (the v83 logit-map machinery), which is capped by the exact wall at roughly n ≤ 6–7
  τ-averaged in the Python port — the C engine buys a little more. Until then, n=3 is the honest
  prediction scope; the C code is ready for higher-order parameter sets the moment they exist.

**End-to-end accuracy + the scope revision (the round's audit catch).** Fresh-draw tests of the
frozen C model against live engine measurements: draws at 2.72× and 2.67× exceeded the banked
pooled gate — a calibration-seed contamination hypothesis for v79's favorable 1.74× draw was
**tested and excluded (0/8 config overlap)** — leaving the simple truth: four independent draws
pool to **2.31×** with per-draw spread 1.74–2.72×; the earlier pooled figures (1.88×/2.1×) sat on
the favorable side because one lucky draw dominated the pool. Scope strings revised in
`csurrogate.h`, `CSURROGATE_RESULT.md`, and `cdet_surrogate.py`; pooled multi-draw stays ≤ 2.6×;
single fresh draws can reach ~2.7×.

Reproduce: `gcc -O2 -o bench csurrogate_bench.c csurrogate.c -lm && ./bench`; the clean-room and
n-wall procedures are documented above; the standing gate remains `python3 csurrogate.py`.
Frozen engine untouched (194/194).
