# CROSSCHECK_v62 — 1d channeling confirmed (~2× at matched distance, graded); mechanism ledger updated

**Claims.** (1) With anisotropy controlled exactly (all displacements axis-directed), pairs matched on
MST to 0.01, and identical τ draws per pair: line/bent median paired ratio 1.82–2.04×, line/zig
1.93–2.43×, bent/zig 1.33× — monotone in collinearity, separated from 1. Collinearity itself carries
weight at fixed total distance: 1d channeling is a confirmed mechanism (and is twist-blind, consistent
with the v61 falsification of winding). (2) Ledger: distance decay + τ-interference + anisotropy +
channeling confirmed; winding falsified; composing distance × channeling reaches ~16× of the measured
~75× class gap — a ~4× residual remains unaccounted and is stated as open.

**Reproduce.** `cd 08_2d_interacting && python3 channeling.py` → matched-family paired ratios; gates
line/bent > 1.15 and line/zig > 1.15; "channeling self-test ... PASS" (~2 min). Full table and ledger:
CHANNELING_RESULT.md.

**Scope (honest).** L=6, n=3, one β/μ; matched pairs exist only where the families' MST ranges
overlap; the residual decomposition is v63's open item.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
