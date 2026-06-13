# CROSSCHECK_v179 — Tier 0: the connected-determinant recursion, validated

**Claims.** (1) Implemented Rossi's connectedness recursion C(V)=D(V)-sum_{v* in S} C(S)D(V\S) with det-square weights.
(2) Linked-cluster identity D(V)=sum_partitions prod C(B) holds to machine precision (no quadrature), n=2..5. (3) Atom
lnZ U-series orders 1..5 == closed form (machine precision). (4) 2-site lattice lnZ U-series orders 1..3 == ED (~1e-9).
(5) Faithful low-order CDet, explicitly NOT a sign-problem result. Frozen engine untouched.

**Pre-registered validations (all pass).** linked-cluster identity worst 2e-16 (n=2..5); atom orders 1..5 worst 6e-17;
2-site order1 1e-12 / order2 2e-12 / order3 1e-9.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 cdet_connected.py     # 3-gate self-test
python3 cdet.py connected
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
