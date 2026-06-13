# CROSSCHECK_v85 — the resonance atlas: consolidation with integration audit

**Claims.** (1) `resonance_atlas.py` consolidates v80–v84 into one prediction surface: regime
classification (empirical crossover βΔε ≈ 8–12), Class-I flips from stored residue-polynomial
roots, Class-II statics with flow correction. (2) The one-spine statement: every resonance-regime
flip is μ\* = anchor + ln(ratio)/(qβ) — Class I: level + root odds, q=1; Class II: midpoint +
two-residue ratio, q=2. Residues decide attendance; positions geometry-free, multiplicities not.
(3) Integration audit, all stored cross-component collisions: roots(135) → v81 trajectories ≤0.006
(lower, every β) / ≤0.028 (upper, excluding the v81-flagged β=16 point); roots → v80 basin flips
≤0.031 (the v83-flagged edge root excluded); selection-rule flow → v82 statics ≤0.014; regime
classification matches the v80 p-values; a live engine check lands 0.003 from the root prediction.
(4) The honest catch (gate D): the L=6 ~1.8 flip is unclassified — Class-I c drifts 3.1→5.5; 1.8
is neither an L=6 half-integer nor a third; conflated trajectories suspected; recorded openly.
(5) BEST_METHODS v85 edition: the arc's component table, the spine, methodology rules 10–18.

**Reproduce.** `cd 08_2d_interacting && python3 resonance_atlas.py` → audit gates A–F;
"resonance-atlas integration audit (A-F): PASS" (~25 s).

**Scope (honest).** Class-I roots stored for one level (L=6, ε=1, three geometries); one
characterized static; crossover empirical; the open list is explicit in the module docstring.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
