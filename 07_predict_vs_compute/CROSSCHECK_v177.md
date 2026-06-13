# CROSSCHECK_v177 — the true radius is thermal, not the RPA wall

**Claims.** (1) The atom's true radius is a complex-U Fisher pair at Im U=pi/beta; a finder reproduces the analytic
radius to 0.0e+00. (2) The true radius is thermal (Im~pi/beta), not the real-axis RPA instability. (3) It is CLOSER than
the RPA wall (ring L=3: R_true~2.90 < R_RPA~3.42), the v146 caveat. (4) It does not inherit the Diophantine sieve (no
q-grid max). (5) Frozen engine untouched.

**Pre-registered validations (all pass).** atom finder radius==analytic (0.0e+00); atom zero Im==pi/beta; ring L=3
R_true<R_RPA; ring L=3 zero Im in [1,2.5]*pi/beta; structural no-grid-max.

**Honest limitation.** Large-L direct test precluded (sieve needs large L = 2D lattice; R_true needs small L = ED;
complex-zero search delicate, L=3 stable). Case rests on exact atom anchor + thermal nature + structural argument +
small-ring evidence.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 wall_true_radius.py     # 5-gate self-test
python3 cdet.py trueradius --beta 2 --mu 0.5
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
