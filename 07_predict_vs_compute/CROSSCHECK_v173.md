# CROSSCHECK_v173 — the wall is a tide (finite-size waves)

**Claims.** (1) U_c(L) oscillates around the TD wall (BZ-quadrature commensuration). (2) Period in L = 2*pi/q* (the
nesting vector): half-filling -> 2; mu=-2.8 (q*x=0.542pi) -> 3.68 vs predicted 3.69. (3) Half-filling branches: even L
exponential (ratio ~0.5/dL=2), odd L ~1/L^2 (p=-1.89). (4) Amplitude decays with L; branches meet at U_inf=1.9752. (5)
Frozen engine untouched.

**Pre-registered validations (all pass).** half-filling period==2; incommensurate period==2*pi/q*; odd p in (-2.4,-1.5);
even ratio<0.7; neighbour split L~4 > 5x L~32, and even/odd TD limits agree to <0.05.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 wall_tide.py     # 5-gate self-test
python3 cdet.py tide --mu -2.8                                # tide chart + period = 2pi/q*
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
