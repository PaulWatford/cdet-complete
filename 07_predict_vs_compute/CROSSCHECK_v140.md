# CROSSCHECK_v140 — resummation / precision (the gravity-loop question)

**Claims (vs exact ED self-energy).** (1) Our σ_n obey no finite linear recurrence (order 2..5 errors
3.5e-2..5.4e-4, never 0) → GF not rational → no 15-digit resummation (the gravity-loop trick doesn't transfer).
(2) Padé [8/8] extends reach past the bare radius ~0.8: bare err 3.2e13 → Padé 0.23 at U=3 (reach, not
precision). (3) Most models already exact-resummed (engine Rossi recursion, surrogate closed-form, Dyson). (4)
The general accuracy lever is extended-precision arithmetic (LD reaches β≥200 vs f64's ~100, v139).

**Reproduce.** `cd 08_2d_interacting && python3 resummation.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
