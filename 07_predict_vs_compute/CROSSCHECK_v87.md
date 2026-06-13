# CROSSCHECK_v87 — the C surrogate under test

**Claims.** (1) Self-containment: five files build in a clean room with gcc alone; the clean-room
caught three portability bugs, now fixed in shipped source (M_PI guard for strict C99; a pedantic
const-array error; the POSIX feature macro in the benchmark) — the module builds under
`-std=c99` and `-std=c11 -pedantic`, both `-Wall -Werror`, gate unchanged at 3.6e-15; it
interoperates with the existing Python modules by construction (the gate regenerates references
live from feats2 / classify_true_rank1 / residue_ratio / selection_rule). (2) Efficiency:
features/magnitude 1.5 µs per call (×212 vs Python feats2 at 312 µs); sector 7.2 µs; atlas laws
3–19 ns (52–355 M/s); per ANSWER vs exact computation ~875,000× (1.5 µs vs ~1.3 s per τ-averaged
n=3 coefficient), a ratio growing ~2.6ⁿ. (3) The orders-of-n answer in two ceilings: computational
— the exact C_V cost measured growing ×2.5–3.3 per order (1.75 ms at n=3 → 745 ms at n=9, one
τ-point) while the surrogate is O(1) in n for atlas laws and O(n²) for an n-generalized feature
kernel (0.5 µs at n=3 → 1.7 ms at n=200; scaling probe, not the shipped module); validity — the
shipped laws/weights are n=3-derived, and higher orders need their own v83-machinery extraction,
capped by the exact wall at roughly n ≤ 6–7 τ-averaged. (4) The audit catch: fresh end-to-end
draws (2.72×, 2.67×) exceeded the banked pooled gate; the contamination hypothesis for v79's
favorable draw was tested and EXCLUDED (0/8 verbatim overlap); four independent draws pool to
2.31× with per-draw spread 1.74–2.72× — scope revised openly in csurrogate.h, CSURROGATE_RESULT,
and cdet_surrogate.py (pooled multi-draw ≤ 2.6× holds; single draws can reach ~2.7×).

**Reproduce.** Clean room: copy csurrogate.{c,h}, csurrogate_params.h, csurrogate_refs.h,
csurrogate_test.c; `gcc -O2 -Wall -Werror -std=c11 -pedantic -o t csurrogate_test.c csurrogate.c
-lm && ./t`. Benchmarks: `gcc -O2 -o bench csurrogate_bench.c csurrogate.c -lm && ./bench`.
Standing gate: `python3 csurrogate.py` (PASS).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
