# The resonance regime (v80): the chain reopened by the KT review — a boundary retracted, a second regime proved

**Provenance.** User-directed KT-RG review of v75–v79 (IS/IS-NOT on discarded anomalies; Phase-0 on
measurement resolution; the escalation ladder on the limit-set hunt). The instruction: "don't count
your hypotheses off yet — that many linked items in a row was going somewhere." It was.

**Phase-0 reversal first.** The fine μ-grid (0.025) gives β=4 median flip spacing **0.625** —
q≈1.26 — the banked 0.70 was coarse-grid inflated and the sub-π/β deviation is *real and larger*
than banked, with two spacing populations visible already at β=4.

**The two-regime law** (two independent significant statistics, frozen uniform nulls):
- **Thermal regime** (small β): geometry-dependent offsets, ~π/β winding (v77, intact).
- **Resonance regime** (large β): flips **attract to levels** (mean-distance ratio 0.87/0.86/0.71–0.84/0.79
  at β=4/8/12/16; **p=0.025 at β=12 and 16** in independent runs) and become **geometry-independent**
  (cross-geometry median nearest-flip distance 0.020 at L=8 β=16, **p=0.032**; 0.025 at L=6,
  **p=0.041**; vs 0.075, p=0.19 at β=4). The old β=12 "0.40 vs 1.50 disagreement" was intra- vs
  inter-cluster spacing — *both real*. **The v77 "β≥12 unmeasurable" protocol boundary is retracted
  as a boundary** (note added to MU_PERIOD_RESULT.md): it was the resonance regime announcing itself.

**The universal limit set — characterized, identification open.** The naive levels∪midpoints law was
**killed** at L=6 (sparse-spectrum discriminator, p=0.33). Flip trajectories vs β are stable and
convergent: 1.988→level 2 exactly; one family flows as **1 + c/β with c ≈ 1.39 ≈ ln 4** (a
log-degeneracy-correction candidate). The L=6 core set {0.94, 1.09, 1.79, 1.99} is
**external-time-independent** (stationary under three (to,ti) pairs — and the pretty 2(to+ti)=1.8
coincidence was killed by its own discriminator: FM-5 caught in the act). Open program:
degeneracy-weighted multi-particle crossing energies ΔE/Δk with ln(g)/β corrections.

**The unlock — and its fine structure.** In the resonance regime flip *positions* are geometry-free,
so calibration transfers across geometries — but flip *multiplicity* (single vs double crossing) is
geometry-dependent (residues): naive transfer is **bimodal** — 79–87% within the
multiplicity-matched cluster, anti-phased (32–47%) against the odd geometry. Refined channel:
transfer the position set + resolve multiplicities with a few parity anchors. "Multiple ratios,
more than one effect, residual ripples" — verbatim.

**Honest scope.** Axis lines, n=3; 4-geometry batteries, grid 0.025–0.05, NT 50–100; estimator
flip-*counts* fluctuate run-to-run at β≥20 while the stable core positions recur; limit-set
identification open.

Reproduce: `python3 resonance_regime.py` (gates: level attraction p<0.05; cross-geometry p<0.05 at
both L; the midpoint kill reproduced; core external-time independence; bimodal transfer; live-engine
core-flip check; PASS, ~30 s). Frozen engine untouched (194/194).
