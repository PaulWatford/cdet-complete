# Two-particle chained two-round run

v158 chained a single electron's position into round 2. Two particles is where the physics starts: they obey
**exclusion** (no double occupancy — Pauli) and carry a **pair correlation** — the connected, two-body content the
CDet exists to capture. This repeats the chained protocol for two particles and asks whether the two gains survive
one → two bodies, and whether they reach the *interaction* response, not just the one-body amplitude.

## Expansion (two-particle config walk, exclusion)

The chained RNG continuation moves one of the two particles each round to a free site — never onto the other
(exclusion) — continuing the stream so it never cycles.

| walk | distinct pair-configs (of 10) | exclusion |
|---|---|---|
| two-particle chained continuation | **10 / 10** | **held throughout** |

The continuation sweeps the *full* Pauli-respecting pair-config space.

## Efficiency (hybrid, both observables)

Chaining round 1's terminal stream into round 2 (a clean 2×NT estimate), error vs an NT=20000 reference:

| observable | single NT | chained 2×NT | reduction |
|---|---|---|---|
| A — one-body amplitude | — | — | **1.44×** (≈√2) |
| c₁ — two-body interaction response | — | — | **1.39×** (≈√2) |

The gain reaches the **interaction**, not only the amplitude — the continuation is as useful for the correlated
two-body quantity as for the free one. (An earlier 6-seed read suggested c₁ chained worse; with 12–14 seeds that
was noise — both track √2.)

## Net

The continuation gains carry from one particle to two, and from the amplitude to the interaction; exclusion is
respected throughout. The same mechanism — continue round 1's stream rather than restart — keeps paying off as the
system gains a second, correlated particle.

Reproduce: `python3 two_particle_run.py` (~20s). The frozen reference engine/ (194/194) is untouched (the only
hybrid change remains the v158 print-only terminal_state).
