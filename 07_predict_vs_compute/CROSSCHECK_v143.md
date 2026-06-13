# CROSSCHECK_v143 — SU(N) step 2: the record survives hopping

**Claims.** (1) 2-site SU(N) Hubbard ED: U=0 factorization ln Z(N)=N·single-flavor to 1.3e-14. (2) c1(N) is a
degree-2 polynomial in N — fit N=2,3,4 predicts N=5,6 to 5e-5 (3rd finite-difference over N ~3e-5); c2(N) degree
3 predicts N=6 to ~1e-3 (extraction-noise floor). So the N-polynomial record survives hopping → the CoS
N-independent kernel evaluates at any flavor number on the lattice (the N=6 Yb EoS reachable without
diagonalizing N=6). (3) Production lattice CDet + closed-loop record (v132 fast minors) = remaining engineering.

**Reproduce.** `cd 08_2d_interacting && python3 sun_lattice_record.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
