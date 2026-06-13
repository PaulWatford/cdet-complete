# CROSSCHECK_v69 — the phase law: double falsification under frozen protocol

**Claims.** (1) Static τ-averaged single-particle predictors (star/chain sign products, det of the
averaged propagator matrix, dominant-permutation-with-parity) calibrate at 93% on one cell and
collapse to 34% mean (survey; 25% at self-test cells) across 7 frozen out-of-calibration cells —
falsified against the pre-set 75% gate; the static free sign pattern (++−++ at all fillings) cannot
represent the measured μ-flip. (2) The fully τ-integrated dominant chain (Matsubara loop, no
determinants): 64–66% mean — real partial signal (cells at 100%/93%) but fails the gate, with an
anti-correlated cell (21%) — the fingerprint of competing pairings of opposite parity.
(3) Conclusion as scoped: the orientation phase is determinant-level interference as far as tested;
magnitude lawful (v63), phase irreducible to the reductions tried — a sharp localization of the
hardness. (4) The v68 phenomenology stands untouched.

**Reproduce.** `cd 08_2d_interacting && python3 phase_law.py` → both frozen protocols on a 6-cell
subset; gates (calibrations >80%; static OOS <62%; chain OOS <75%; chain > static);
"phase-law self-test ... PASS" (~2 min). Full 8-cell tables: PHASE_LAW_RESULT.md.

**Scope (honest).** Axis lines, n=3, one β, 14 geometries/cell; "irreducible" means both tested
reductions failed frozen gates, not a proof; the open question is whether any object strictly
cheaper than the determinant carries the phase (next candidate queued: chain + leading exchange).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
