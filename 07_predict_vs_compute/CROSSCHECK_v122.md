# CROSSCHECK_v122 — multi-lattice laws, the plane-wave scaling path, the hybrid

**Claims.** (1) μ-rigidity is crystallographic: integer spectrum iff cos(2π/L) rational iff L∈{1,2,3,4,6};
verified L=2..12 (integer at 2,3,4,6 with gaps 4,3,2,1; irrational at 5,7,8,12 with gaps 0.53,0.15,
0.24,0.20). (2) Scale law z(∞)=lowest-empty-level is universal (L6 μ1.845→2, μ2.5→3, L4 μ1.0→2). (3)
The plane-wave propagator g0=(1/N)Σ cos(k·Δr)G0_atom makes the determinant O(N×MC), L-agnostic, no
eigenvectors/spectrum. (4) cfriedel_L.c runs the structural layer to L=20 (N=8000) in <1s, validated
4.8e-11 vs Python eigh. (5) How big: structural laws L=20+, determinant L~12-16; hybrid = laws (phase 1,
O(N)) → plane-wave determinant (phase 2, O(N×MC)).

**Reproduce.** `cd 08_2d_interacting && python3 multi_lattice_laws.py` (self-test PASS); `gcc -O2 -Wall
-Werror -std=c11 -pedantic -o cfriedel_L cfriedel_L.c -lm && ./cfriedel_L scan` (integer spectrum across
L); `./cfriedel_L test` (validates the plane-wave form vs Python eigh at L=6).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
