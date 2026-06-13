# The parity table (v97): the A=0 rule falsified by its own frozen test, the suppression pattern banked, the v84 static reread

**The table** (β=28, multi-draw, generalized `WindowFrozen` across both lattices): W6(0,1)
A = −0.023(15) [first-empty deg 36]; W6(1,2) A = +0.839(102) [deg 27, **odd**]; W6(2,3)
A = +0.025(8) with a dead residue [deg 14]; W8(0.828,1.414) A = −0.0208(55) [deg 60];
W8(1.414,2.0) A = +0.497(76) [deg 39, **odd**].

**The falsified rule, honestly scored.** At 4/4 consistency the binary rule "even first-empty
degeneracy ⇒ A = 0" was registered and tested on W8(0.828,1.414): A = −0.0208 ± 0.0055 — 3.8σ
from zero. **The strict rule is dead by its own prediction.** What survives is a robust
suppression pattern: odd-windows carry A ~ +0.5–0.85, even-windows |A| ~ 0.02–0.03 (20–40×
smaller; 4–30× in |A/c₁|) — a five-window observation with the unpaired-mode mechanism as a
hypothesis only.

**The v84 static reread.** At μ = 1.8284, β = 28 the W8(1.414,2.0) background equals ~95% of its
dominant deviation term (|A|/|c₁|s_phys = 0.95): the L=8 "static" is an A-vs-f(2.0) **root-flow
crossing** — the same structure that at L=6 produced an effective anchored law that failed at
deep β. **Frozen prediction registered (untested):** the L=8 deep-β zero rises past 2√2−1 above
β ≈ 32–40, replaying the L=6 crossover.

**Instrument hardening, two catches.** (a) The freeze is exponentially ill-conditioned for
s ≫ nf_phys (a 1e12 blowup at s = 0.02, ξβ = 8.2): conditioning rule s ≲ 10·e^(−βξ_probe).
(b) A 1e-9 mask tolerance against 1e-6 level rounding silently emptied level 1.414 and produced
a false zero in the scout — the occupied-levels check is now gated. Also banked: the W6(2,3)
suppression is not site-projection (uniform weights by translation invariance — honest
negative); both its A and residue are dead, mechanism open.

Reproduce: `python3 parity_table.py` (five gates incl. a live background re-measure; PASS
~35 s). Frozen engine untouched (194/194).
