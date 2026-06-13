# CROSSCHECK_v158 — chained two-round run

**Claims.** (1) The hybrid exposes its terminal sampler state (print-only); val still 0.00e+00, numbers unchanged.
(2) Chaining round-1's terminal state into round-2 gives a 1.39× (≈√2) error reduction vs a single run (NT=2000 vs
NT=16000 ref), because the continued stream is independent/non-overlapping; a same-seed rerun is identical (zero
new info). (3) A deterministic result-seeded walk cycles (1–2 configs); the chained-stream continuation sweeps 9/10
(no cycle). Both gains come from continuing the stream. The frozen reference source is untouched.

**Reproduce.** `cd 08_2d_interacting && python3 chained_run.py` (~10s); `./cpw val < cdet_stable_engine_refs.txt` →
0.00e+00.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
