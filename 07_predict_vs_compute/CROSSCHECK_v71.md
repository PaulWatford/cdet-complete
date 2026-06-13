# CROSSCHECK_v71 — pairing depth: no finite depth; the complete free determinant fails

**Claims.** (1) The free 4-point τ-integrated determinant decomposes exactly into 24 permutation
terms via Matsubara cycle sums; depth-k predictors under the frozen v69 protocol give OOC means
46% / 46% / 63% / 44% at k = 1 / 2 / 4 / 24 — both pre-registered gates (depth-2 ≥75%; full depth
≥75%) FAIL, and the engine-matched external-time-fixed variant gives identical numbers.
(2) Sharpened localization by elimination: the orientation phase lives in the coupled product of
the two spin determinants over shared vertex times — the engine integrand itself. (3) The reduction
ladder is complete: parity 50–59% → static 34% → chain 64% → any-depth single determinant ≤63%
(full 44%), all frozen-protocol falsifications. (4) Surrogate consequence: no physics-reduced
orientation channel below the engine; a learned statistical channel is the queued alternative.
(5) Standing mode adopted (user directive): surrogate-first experimentation with engine crosscheck.

**Reproduce.** `cd 08_2d_interacting && python3 pairing_depth.py` → depth-2/24 and external-fixed
protocols on a 5-cell subset; gates (calibrations >80%, all OOC <70%);
"pairing-depth self-test ... PASS" (~2 min). Full 8-cell tables: PAIRING_DEPTH_RESULT.md.

**Scope (honest).** Axis lines, n=3, one β, 14 geometries/cell; both time conventions of the free
single determinant tested; dressed-propagator determinants untested.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
