# CROSSCHECK_v98 — the method audit: the confound, the quantified prediction, the reordered queue

**Claims.** (1) The v97 suppression pattern is confounded: odd first-empty degeneracy coincides
with first-empty-level rationality across every measured window (at L=8 the only odd level in
range, 2.0/deg 39, is the only rational one; L=6 is all-rational), and the falsification window
was the one where both hypotheses agree — the next parity window must discriminate. (2) The
deviation ratios A_odd/A_even = 36.5(24), 33.6(12), 23.9(7.3) are underpowered against integer
candidates {36, 24} (60 excluded at 4.9σ); spec: A_even to ±10%. (3) #107's "is a root-flow
crossing" is downgraded to CANDIDATE (one-point evidence). (4) The L=8 prediction is quantified:
A₈(40) = +0.1135(266) (mask gate run before measuring), two-point rate 0.1231(233), frozen
curve z₈ = {36: 1.8378, 40: 1.8417, 44: 1.8449, 48: 1.8475 ± ~0.010, 56: 1.8517}, with
z₈(28) = 1.8268 reproducing the v84 static as a consistency check. (5) The queue is reordered
by leverage: coefficient phase 2 first. Audit outputs in 08_2d_interacting/METHOD_AUDIT_v97.md
(the method itself referenced by name only, not reproduced).

**Reproduce.** `cd 08_2d_interacting && python3 parity_table.py` (gates unchanged, PASS;
FROZEN_CURVE_Z8 and A8_RECORD now carried in the module). The audit document is prose;
its computed entries (ratios, curve) derive from TABLE, A8_RECORD, C1_W8_HI.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
