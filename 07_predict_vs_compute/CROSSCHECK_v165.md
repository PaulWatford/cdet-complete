# CROSSCHECK_v165 — susceptibilities (charge compressibility + spin)

**Claims.** (1) Charge compressibility κ=∂⟨n⟩/∂μ and spin susceptibility χ_s=∂⟨S_z⟩/∂h for the 2-site SU(N) reference.
(2) Each validated by two independent ED routes (derivative vs fluctuation-dissipation: κ==(β/2N)Var(N̂),
χ_s==β·Var(S_z)) agreeing to ~1e-7. (3) Opposite Mott trends: κ falls with U (0.268→0.084, incompressibility), χ_s
rises (0.268→0.487, local moments). (4) Complex-U weak series + conformal-Borel (χ_s err 3.5e-3 at U=1). (5) Wired as
`cdet chi`; frozen engine untouched.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 susceptibilities.py    # gate
python3 cdet.py chi                                                 # kappa / chi_s table
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
