# CROSSCHECK_v141 — fold-in + the rational self-energy hint

**Claims.** (1) Fold-in: surrogate gains surr_interacting_pole(L,μ,U,nσ) = free pole + Hartree shift U·nσ; the
Σ=0 limit recovers surr_lowest_empty exactly (gate check added; surrogate gate 3.55e-15). v139 guards + LD
already folded. (2) The rational hint (live): at FIXED density the atom self-energy is rational — exact 1-term
recurrence σ_{k+1}=[(1−n)/(iω+μ)]σ_k (dev 2e-10), [2/1] closed form exact to 1.3e-15 at U≤3 (past any bare
radius). The grand-canonical nd(U) was the only non-rational piece; the 15-digit route lives in the skeleton /
bold expansion. Lattice skeleton rationality: open.

**Reproduce.** `cd 08_2d_interacting && python3 rational_skeleton.py`; surrogate `gcc … csurrogate_test.c
csurrogate.c -lm && ./a.out`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
