# CROSSCHECK_v95 — the degree bound: census-settled, menu corrected, tension dissolved

**Claims.** (1) The maximal deviation weight of the stripped n=3 ⟨C⟩ is 2n+1 = 7, verified by a
symbolic census (the CDet port on symbolic occupancies for window levels {0,1,2,3}; sympy
determinants; exact expansion): 330 monomials = the full weight-≤7 simplex, generic over τ
draws. v93's bound "8" and v94's conjectured "6" were both wrong (matrix dimension vs propagator
count; the missed external vertex). (2) Balance positions come from exponent differences: the
realized menu near the object is {25/14, 9/5, 20/11, 11/6, 24/13, 13/7, 15/8, 17/9} — all
rational; the field theorem stands; the chord stays excluded; the v94 "15/8 structurally
excluded" note is corrected (in the menu, dead only empirically at 4.6σ). (3) 24/13 = 1.84615
(q=13, near-flat 1/(13β) approach) sits 0.26σ from the v94 six-point constant — the
menu-vs-flatness tension is dissolved: the flat reading is the q=13 member (ln r = +0.13(1.07),
χ²/dof 0.48; 13/7 at 0.32; 11/6 at 0.96). (4) Status: identification open among {13/7, 24/13};
the named closing route is the coefficient program (τ-average the 330 census coefficients,
predict the zero outright), with deep-β precision (~0.005 separation at β=72) the measurement
alternative.

**Reproduce.** `cd 08_2d_interacting && python3 degree_bound.py` (gates: census 330/weight-7;
menu; field; fits; PASS ~45 s). Revised modules still pass: `exponent_balance.py`,
`law_sidebyside.py`, `csurrogate.py`, `resonance_atlas.py` (A–I).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
