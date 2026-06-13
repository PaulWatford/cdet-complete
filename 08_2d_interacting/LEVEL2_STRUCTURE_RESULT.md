# The two-class structure (v82): the fired prediction fails — and exposes static midpoint crossings

**The fired prediction.** On record before measuring: if c = ln(deg)/2 universally, L=8 level 2
hosts a flight pair at 2 ± ln(39)/2β = 2 ± 1.832/β. (Phase-0 catch en route: the exact degeneracy
is **39**, not the hand-count 63 — the script corrected the prediction before firing.)

**The verdict: falsified as universal.** Windowed trajectories (grid 0.0125, NT=120, β=12–28, two
geometries) show **no flips at 2 ± 1.832/β**. The candidate stands as a one-level fit (L=6 ε=1,
0.4%) whose generality died on contact with new data — which is exactly what a no-free-parameter
prediction is for.

**What the data shows instead — two mechanism classes:**

| Class | Δk | signature | evidence |
|---|---|---|---|
| **I — flight pairs** | 1 | μ\*± = ε ± c_ε/β → levels | v81's level-1 fits (best rms 0.004); central pinned flips at the level, both L (L=8: 2.05→1.99→1.98) |
| **II — static crossings** | 2 | μ\* = (ε_a+ε_b)/2, **β-independent** (ΔE/Δk) | L=8: flip flat at 1.819 ± 0.009 across β=12–24, vs (0.828+2.828)/2 = **1.828**; late-β flips at 2.09–2.12 ≈ (1.414+2.828)/2 = 2.121 and ≈2.29–2.33 ≈ (2+2.586)/2 = 2.293 (edge-registrations excluded as a documented artifact class) |

**The retroactive cleanup:** v80's L=8 "1.81 cluster" was this Class-II static all along; the v80
"midpoint law" resurrects in selective, refined form — *specific* level-pair midpoints, not all.

**The selection-rule puzzle, sharply posed (open):** at L=6 the Class-II positions are
half-integers and v80's test **killed** them (p=0.33) — the statics are residue-suppressed on L=6
axis lines while prominent at L=8. Which crossings actually produce a sign flip is a sign condition
on residue pairs, lattice- and geometry-dependent. Deriving it joins the queue alongside the
Class-I residue ratio (the c-formula, now open again).

**Honest scope.** Level-2 region of L=8 plus the v81 L=6 corpus; two geometries per measurement;
midpoint identifications within grid + jitter (~0.02; the strongest static sits 0.009 from flat and
0.009 from its midpoint); β=28 multiplicity splitting flagged; upper-window statics appear only at
large β (residue-weight thresholds, presumably).

Reproduce: `python3 level2_structure.py` (gates: static flatness ≤0.02 and midpoint match ≤0.035;
the fired prediction's failure reproduced; central flips at the level; edge-excluded midpoint
matches ≥half; a live-engine static check at β=20; PASS, ~30 s). Frozen engine untouched (194/194).
