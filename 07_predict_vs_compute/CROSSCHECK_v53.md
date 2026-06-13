# CROSSCHECK_v53 — interior of the 2ⁿ: mask-fold (honest negative) + subset cache (29.9× win)

**Claim 1 (mask-fold, honest negative for the generic case).** A symmetry folds the masks *inside*
one C_V only if it maps the vertex set to itself. Verified exact on a symmetric config (vertices on
diagonal-partner sites with equal times: mask pairs 001↔010 and 101↔110 have identical D_vac and
D_corr to 1e-12). A generic config (distinct continuous times) has trivial stabilizer, so the interior
fold fires only on a measure-zero subset — not a generic 2ⁿ cut.

**Claim 2 (subset cache, the generic win).** D_vac/D_corr depend only on the vertex subset. Across the
enumerated n=3 site sum on the 4×4 at fixed times, only 4913 of 32768 subsets are distinct (6.7× raw
redundancy). Memoizing them and composing with the orbit fold: total matches brute force to **5.0e-15**
with **2194 unique determinants vs 65536 brute subset evaluations (29.9× fewer)** — orbit fold 6.15× ×
cache 4.86×, independent and multiplicative; 13.9× wall-clock measured (15.0 s → 1.1 s).

**Reproduce.** `cd 08_2d_interacting && python3 symmetry_reduction.py` → the final lines print the
fold+cache composition (match 5.0e-15, 29.9× fewer) and "fold+cache composition self-test: PASS"
(~35 s total). The symbolic audit is unchanged from v52: `python3 symmetry_audit_sympy.py` → PASS.

**Scope (honest).** The cache removes recomputation across an enumerated/quadrature site sum (shared
times); it does not reduce the asymptotic 2ⁿ of one isolated C_V on generic continuous times (Claim 1
is the measured reason). The physical sign is untouched.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; `cdet_order` constants
bit-identical (−0.5082750022348369  0.44040518398732875). All new code wraps the engine via the
validated `cdet_port.py` (bit-identical to the frozen ring port at 0.00e+00).
