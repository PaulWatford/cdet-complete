# CROSSCHECK_v164 — double occupancy observable

**Claims.** (1) Double occupancy D=⟨n↑n↓⟩ per site for the 2-site SU(N) reference via D=−(1/β)∂lnZ/∂U/N_sites. (2) Two
independent ED routes agree to ~1e-10: the lnZ U-derivative and the direct thermal average of the pair-occupancy
operator D̂. (3) Physical Mott suppression: D falls 0.549→0.069 across U=0..3 (N=2). (4) Conformal-Borel resums ~65×
better than plain Padé at U=1. (5) Interaction energy per site = U·D. (6) Wired as `cdet docc`; frozen engine untouched.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 double_occupancy.py     # gate
python3 cdet.py docc                                                 # ED / conformal-Borel / E_int table
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
