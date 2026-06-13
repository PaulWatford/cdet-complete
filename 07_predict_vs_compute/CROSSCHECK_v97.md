# CROSSCHECK_v97 — the parity table: the rule falsified, the pattern banked, the v84 static reread

**Claims.** (1) Five window backgrounds measured across both lattices with the generalized
WindowFrozen (β=28, multi-draw): W6(0,1) −0.023(15); W6(1,2) +0.839(102); W6(2,3) +0.025(8)
with a dead residue; W8(0.828,1.414) −0.0208(55); W8(1.414,2.0) +0.497(76). (2) The binary rule
"even first-empty degeneracy ⇒ A=0" was registered at 4/4 consistency and **falsified by its
own frozen test** (W8(0.828,1.414) nonzero at 3.8σ); the surviving suppression pattern
(odd-windows ~20–40× larger |A|) is a five-window observation, mechanism a hypothesis. (3) At
μ = 1.8284 the W8(1.414,2.0) background equals ~95% of its dominant deviation term: the v84
static is a root-flow crossing, and the L=8 deep-β crossover replay is **registered as a frozen
prediction** (untested). (4) Instrument hardening: the conditioning rule s ≲ 10·e^(−βξ_probe)
(after an observed 1e12 blowup) and the mask-tolerance catch (the scout's false zero — the
occupied-levels check now gated). (5) Honest negative: the W6(2,3) suppression is not
site-projection (uniform weights by translation invariance).

**Reproduce.** `cd 08_2d_interacting && python3 parity_table.py` (five gates incl. a live
background re-measure; PASS ~35 s).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
