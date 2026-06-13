# Full consolidation: three models at highest capability (v147)

Consolidates the integration arc (v131–v146) and brings all three models to their highest proven capability,
keeping the analysis supplements as separate CLI modules. `consolidation_v147.py` is the single health gate.

## The architecture (what keeps the archive trustworthy)

| layer | file | role | capabilities |
|---|---|---|---|
| **frozen reference** | `engine/` | the validation anchor — **never altered** | 194/194; `make fast` (-O3 -march=native), `make omp` |
| **production engine** | `cdet_planewave_engine.c` | carries capabilities, validates == reference (0.00e+00 @L6) | any-L, `-fast` projector, `-DUSE_LD`, mode-2 freeze, 3 input guards, multi-million sites |
| **surrogate** | `csurrogate.c` | fast pure-arithmetic carriers | lowest_empty (addition pole), friedel_edge, interacting_pole (free+Hartree), **sun_c1, sun_n1 (SU(N) EoS)** |

**Why the frozen reference stays frozen:** its 194/194 is the anchor every result in the archive is checked
against; altering its validated numerics would dissolve that trust chain. It already carries the efficiency
targets (`fast`, `omp`). The production hybrid is the capability-carrying mirror and validates against it
bit-for-bit at L=6.

## Brought up this round

- **Surrogate** gains `surr_sun_c1(N,d)` and `surr_sun_n1(N,d,d')` — the SU(N) production EoS coefficients
  (record × single-flavor amplitude, v144), matching the python production route at N=6. Gate still 3.55e-15.
- **Hybrid** confirmed at highest capability (f64 + LD, `-fast`, guards, freeze) — validates 0.00e+00.
- **Frozen reference** confirmed (194/194, `fast`/`omp` targets).

## Kept as separate CLI modules (better design + end-user configurability)

The analysis supplements — `fast_minors`, `cos_prototype`, `physical_mapping`, `self_energy*`,
`rational_skeleton`, `sun_atom/lattice_record`, `sun_lattice_production`, `sun_resummation_N`,
`rational_lattice_boundary`, `resummation` — stay as standalone modules, each self-testing against ED or the
frozen engine. This is the better design: they are research instruments with their own options, not engine hot
paths.

## Health gate

Three models consistent: surrogate SU(N) carriers == production route (N=6); surrogate addition pole == python
(L=12); fast minors live. Frozen reference 194/194; hybrid validates == it; surrogate gate 3.55e-15.

Reproduce: `python3 consolidation_v147.py`. Frozen engine untouched (194/194).
