# Ring-closure test (v61): winding-phase hypothesis falsified — and the unpaired artifact that nearly fooled us

**The hypothesis (banked v60, now tested):** the ~10× closed-line weight enhancement is
ring-closure/winding coherence on the torus.

**The intervention.** An **antiperiodic twist** along one axis: |hopping| and every distance
bit-identical (sanity-gated), only the winding phase of loops along that axis changes. Frozen
predictions before measurement: distance laws → zero change; winding coherence → selective
suppression of the twisted axis's lines, mirrored when the twist moves to y.

**Layer 1 — the unpaired run (the artifact).** With independent τ draws per lattice, the medians
showed x-lines at 0.24× under twist-x vs y-lines at 0.74× — an apparently clean 4× axis-selective
effect.

**Layer 2 — the paired rerun (the truth).** Same sites AND same τ draws on every lattice; median of
per-config ratios:

| class | twist-x/PBC | twist-y/PBC |
|---|---|---|
| x-lines | 0.93× | 0.99× |
| y-lines | 1.14× | 1.45× |
| bulk | 0.70× | 0.73× |

No suppression. No mirror. The 4× was an **unpaired heavy-tail artifact** — the same estimator
pathology documented since v58, caught here by the paired design. (Self-test reproduces: paired
x-line ratio 1.05×, y-line 0.84× under twist-x.)

**Verdict.** Maximally changing the closure phase leaves line weights within ~±40% and axis-blind:
**the winding-phase form of ring closure is falsified.** The ~10× line enhancement is
closure-independent.

**Surviving refined hypothesis (untested — not a result):** **1d channeling** — coherent multi-bounce
propagation along the line's short segments, which needs no winding and is therefore twist-blind.
Candidate v62 test: line configs vs equally-compact non-collinear configs at matched decay-metric MST.

**Lesson, now thrice-earned and promoted to standing methodology:** in heavy-tailed systems, PAIR
every comparison — same sites, same τ draws, per-config ratios — or medians of independent samples
will manufacture multi-× effects.

Reproduce: `python3 ring_closure.py` (gates: |H| identity + the falsification itself; PASS, ~90 s).
Frozen engine untouched (194/194).
