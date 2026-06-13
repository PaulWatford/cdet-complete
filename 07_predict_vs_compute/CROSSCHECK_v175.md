# CROSSCHECK_v175 — "half-integer" lattices: twisted BC + rectangular supercells

**Claims.** (1) Half-integer lattice = twisted BC (theta=1/2 anti-periodic) or rectangular supercell. (2) Twist does NOT
heal the sieve: the p-h momentum-transfer grid q=2pi m/L is theta-independent (peak q-index same for theta 0 and 1/2);
anti-periodic doesn't flip parity; twist-averaging trims the prime error ~7%. (3) Rectangular supercell DOES heal it:
23x46 hits q* -> err 4e-4 (prime dim) vs 17x17 6e-2. (4) Diophantine rule: capture <=> q*_comp*L/2 near integer. (5)
Tide/sieve are q-sampling artifacts, not properties of the true wall. (6) Frozen engine untouched.

**Pre-registered validations (all pass).** anti-periodic parity not flipped + q-index theta-independent; twist-avg prime
error >0.7x theta=0; rectangular 23x46 <0.01 and 17x17 >0.05; Diophantine good-L error < bad-L error.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 wall_twist.py     # 4-gate self-test
python3 cdet.py twist --mu -0.6                                # twist vs rectangular healing
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
