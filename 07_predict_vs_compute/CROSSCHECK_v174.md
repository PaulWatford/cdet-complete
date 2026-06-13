# CROSSCHECK_v174 — prime lattice sizes: a Diophantine sieve on the wall

**Claims.** (1) Prime L are commensuration-blind -> worst-case wall samplers (~2.7x composite deviation at mu=-0.6). (2)
corr(#divisors(L), dev) = -0.39 (composites capture the peak). (3) Deeper than the v173 parity: holds within odd L
(primes 0.022 > odd-composites 0.014). (4) The whole effect is the v173 curvature law on the grid-miss to q*:
corr(grid-miss^2, dev) = +0.96. (5) Filling-dependent (Diophantine): sharp near a low-denominator peak, washed out at a
generic peak. (6) Frozen engine untouched.

**Pre-registered validations (all pass).** corr(miss^2,dev)>0.85; prime/composite ratio>2 at mu=-0.6; corr(#div,dev)
<-0.3; primes>odd-composites within odd L; sieve ratio x2.7 at mu=-0.6 vs x1.1 at the generic peak mu=-2.8.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 wall_primes.py     # 5-gate self-test
python3 cdet.py primes --mu -0.6                                # prime/composite deviation table
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
