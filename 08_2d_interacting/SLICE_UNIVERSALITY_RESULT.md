# Universality test (v58): weight concentration universal; sign hierarchy downgraded

**The test (frontier advice taken):** the v57 hierarchy was one order, one coupling, one observable.
Swept across order (n=2,3,4), temperature (β=2,4,8), filling (μ=0, 0.5, 1.5) and the observable
((t_o,t_i)=(0.7,0.2)→(1.5,2.5)) on the L=6 cube; U is exactly universal by the banked theorem (C_V
contains no U).

**Result 1 — weight universality (STANDS, strengthened).** The 1d/bulk per-configuration weight ratio
exceeds 10× in every cell: mean-based 10×–223×; **median-based (heavy-tail robust) 11×–184×,
seed-stable** (β=8: 66×/55×/61× at seeds 11/42/77; self-test reproduces 52–82×). The concentration is
a property of propagator geometry, not a numerical coincidence.

**Result 2 — the sign hierarchy is DOWNGRADED on the record.** The module's first self-test FAILED:
the same cell (L=6, β=8) gave R(1d)=0.44 at 500 samples and 0.02 at 400 samples, same seed. That
failure was the discovery: R = |mean|/mean|·| over these heavy-tailed |C| distributions is dominated
by rare large configurations and is NOT a stable estimator at these sample sizes. The robust
count-coherence S = |2f₋−1| sits near the binomial floor in most cells (S(1d) 0.008–0.196, S(bulk)
0.007–0.055). HONEST STATUS: v54/v57's per-class sign statements ("the sign hierarchy persists and
narrows") are downgraded to **OPEN** — the weighted sign structure is real physics (R is the quantity
that matters; it weights by |C|) but is not reliably measured yet; it needs weighted-bootstrap error
bars or much larger samples. v57's flagged L=8 bulk anomaly was the same instability showing itself.

**Lessons banked:** (i) a ratio of means over a heavy-tailed distribution is not a measurement until
its estimator is shown stable; (ii) gate self-tests on robust statistics; (iii) a failing gate is
data.

Reproduce: `python3 slice_universality.py` (gates: median-ratio universality across the β flip +
seed stability; the non-robust R columns are printed as the fragility warning; PASS, ~90 s). Frozen
engine untouched (194/194).
