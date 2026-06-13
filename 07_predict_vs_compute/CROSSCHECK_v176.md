# CROSSCHECK_v176 — consolidation: one wall core, all models side by side

**Claims.** (1) The 4 wall modules share one canonical core wall_vs_size.chi0_max_rect (rect+twist); wall_twist
delegates; square-periodic dev 0.0e+00. (2) README documents the wall suite; `cdet crosscheck` runs the side-by-side
test. (3) Cross-links: E internal (one core); B<->E chi0(q=0)==dn/dmu (7e-13); D<->E same finite-radius phenomenon
(U_c^EoS=1.054, U_c^wall=1.975; resummation extends past both). (4) All models retest green. (5) Frozen engine untouched.

**Pre-registered validations (all pass).** wall modules share the core (dev 0.0e+00); chi0(0)==dn/dmu < 1e-6; at U=0.7
bare EoS diverged (>1) while conformal-Borel tracks ED (<0.05); full sweep returns sane values.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 consolidation_v176.py     # side-by-side cross-check
python3 cdet.py crosscheck
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
