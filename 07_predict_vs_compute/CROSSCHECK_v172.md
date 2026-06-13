# CROSSCHECK_v172 — the convergence wall vs lattice size

**Claims.** (1) The leading weak-coupling wall is U_c(L)=1/chi0_max(L), the RPA/Stoner instability, with chi0 the free
static Lindhard susceptibility from the plane-wave dispersion. (2) Computable at any L to 100×100 (the v162 feature).
(3) Near half-filling the small lattice is spuriously pessimistic (U_c=1.64 at 4×4) and growing L pushes the wall back
to the TD value (1.975) — lattice helps. (4) Filling-dependent (incommensurate doping reverses the artifact's sign).
(5) Frozen engine untouched.

**Pre-registered validations (all pass).** chi0(q=0)=DOS sum rule (0.0e+00); vectorized==brute-force O(L^4) (3.3e-16);
bubble series sum_n (U chi0max)^n radius == 1/chi0max == U_c; U_c(64) vs U_c(96) converged (1e-9); half-filling wall
recedes with L.

**Honest scope.** U_c is the leading REAL-axis instability (= the exact bubble-sum radius); the full series radius can
be set by complex-U structure closer than this (v146). The exact many-body Fisher-zero route was tried first and found
ED-limited and estimator-dependent, so the clean, scalable leading-instability route is reported instead.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 wall_vs_size.py     # 5-gate self-test
python3 cdet.py wall --beta 5 --mu 0                             # the wall vs lattice size table
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
