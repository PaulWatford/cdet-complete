# Prime lattice sizes and the wall: a Diophantine sieve (v174)

**Question (Paul).** Jump and reduce the lattice size through primes -- what patterns emerge?

**Mechanism.** v173 fixed the tide's error law: the finite-size deviation of the wall U_c(L)=1/chi0_max(L) is the
curvature of the susceptibility peak times the squared distance from the true peak q* to the nearest grid momentum. That
**grid-miss distance is a Diophantine quantity** -- how well the rational grid {k/L} approximates q*/2pi -- so the lattice
size enters through its number theory.

**Pattern.** Primes are the worst lattices for the wall (beta=5, mu=-0.6, q*=(0.78,1.00)pi):

| L | grid-miss to q* | \|U_c - U_inf\| | type |
|---|---|---|---|
| 17 | 0.071 | 0.061 | prime |
| 19 | 0.070 | 0.067 | prime |
| 18 | 0.006 | 0.004 | 2·3² |
| 36 | 0.006 | 0.0003 | 2²·3² |
| 48 | 0.008 | 0.003 | 2⁴·3 |

- **Primes ride the upper envelope.** Lacking divisors, a prime L cannot place a grid point near any low-denominator
  momentum, so it always misses q* -- mean deviation **~2.7x** that of composite L.
- **The divisor sieve.** Deviation anti-correlates with the divisor count: corr(#divisors(L), dev) = **-0.39**. Highly
  composite L (18, 36, 48, ...) capture the peak; primes do not.
- **Deeper than parity.** It survives controlling for the v173 even/odd effect: within ODD L, primes still deviate more
  than odd-composites (0.022 vs 0.014).
- **It is exactly the v173 curvature law.** corr(grid-miss², dev) = **+0.96** -- the whole prime pattern is the
  Diophantine grid-miss feeding the squared-distance error law.

**Filling dependence (the Diophantine signature).** The sieve is sharp only when q* sits near a low-denominator
commensurate vector (good rational targets for composite L to hit). At a generic-irrational peak (mu=-2.8) no small L
approximates well and the prime/composite gap washes out (x2.7 -> x1.1). This is precisely Diophantine approximation:
some targets are well-approximated by rationals of small denominator, others are not.

**Takeaway.** Stepping the lattice through primes traces the worst-case convergence wall; stepping through highly
composite sizes traces the best. To trust a finite-lattice wall, prefer sizes whose divisors match the nesting vector --
and never read it off a prime lattice.

**Validation (pre-registered gates, all pass).** (1) corr(grid-miss², dev) > 0.85; (2) prime/composite deviation ratio
> 2 at mu=-0.6; (3) corr(#divisors, dev) < -0.3; (4) within odd L, primes > odd-composites; (5) sieve sharp at mu=-0.6
but washed out at the generic peak mu=-2.8. Frozen reference engine untouched (194/194). `wall_primes.py`, `cdet primes`.
