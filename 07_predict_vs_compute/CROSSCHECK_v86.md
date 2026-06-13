# CROSSCHECK_v86 — the core C surrogate

**Claims.** (1) `csurrogate.c/h` is a dependency-free core C module carrying every banked advance,
composing with and never touching the frozen engine: the 10 geometric features and the
transferable magnitude model with frozen trained weights and per-L intercepts (v74/v79); the
wrap-safe coherent-sector test by cyclic-line enumeration (v75); the π/β thermal period (v77/v78);
the regime classifier (v80); Class-I flip prediction from frozen residue-polynomial roots via
μ\* = ε + logit(f\*)/β (v81/v83); the Class-II static with flow correction μ\* = mid + K/2β
(v82/v84); orientation parity stepping (v77/v85). Scopes are stated in the header, including the
standing wall (nothing moves the exponential sign problem). (2) Validation is engine-style and
*live*: the gate `csurrogate.py` regenerates reference vectors with a fresh seed every run —
features via feats2, sector via classify_true_rank1, magnitude via the frozen linear model parsed
back from the header, atlas numbers live from residue_ratio and selection_rule — rebuilds with
`-Wall -Werror`, and demands "ALL CASES MATCH THE PYTHON REFERENCE TO 1e-09"; observed worst
deviation 3.6e-15 over 28 configs ×(10 features + ln-magnitude + sector) + 15 class-1 + 4 static
references + regime/period/orientation API checks. (3) Port notes banked: mst includes the origin
(Prim, min-image); rank in exact integer arithmetic; collinear-group keys are sign-canonicalized
rounded unit vectors — each verified by exact match, not assumption. (4) Generated files shipped:
csurrogate_params.h (frozen weights, seeds 130/131; retraining = documented regeneration path) and
csurrogate_refs.h (rewritten by every gate run).

**Reproduce.** `cd 08_2d_interacting && python3 csurrogate.py` → fresh refs, build, run;
"c-surrogate gate ... PASS" (~20 s). Direct: `gcc -O2 -Wall -Werror -o t csurrogate_test.c
csurrogate.c -lm && ./t`.

**Scope (honest).** The C module predicts; it does not measure (no engine calls): orientation
needs one anchor measurement by design; class-1 roots cover L=6 level 1 (three geometries); the
magnitude scope is the banked ~2.1× pooled transfer error.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
