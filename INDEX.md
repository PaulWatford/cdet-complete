# INDEX — the cdet suite

A research package for the connected-determinant (CDet) approach to the Hubbard sign problem, built around a frozen,
independently-validated reference engine. Every result is produced under pre-registered gates and cross-checked; the
reference engine is never edited, so all numbers trace back to one anchor.

Start here, then `QUICKSTART.md` to build, then `README.md` for the CLI.

## The one invariant

```
cd engine && make CC=gcc test     ->     RESULT: 194 passed, 0 failed, 0 skipped (of 194)
```

The frozen reference engine passes 194/194 and is never source-edited. Everything else validates against it. The
surrogate carrier constants are bit-identical (−0.5082750022348369, 0.44040518398732875); the plane-wave production
engine matches the reference at 0.00e+00.

## Three-model architecture

| model | where | role |
|---|---|---|
| frozen reference engine | `engine/` (C, 194/194) | the parity anchor; never edited |
| plane-wave production engine | `08_2d_interacting/cdet_planewave_engine.c` | validated == reference; large-L 2D propagator |
| analytic surrogate | `08_2d_interacting/csurrogate.{c,h}` | the carrier constants; bit-identical to the reference |

## Directory map

| dir | contents |
|---|---|
| `engine/` | FROZEN reference engine (`make CC=gcc test` -> 194/194); the parity anchor |
| `05_2d_lattice/` | lattices incl. the O(L) plane-wave propagator `Square2DPW` (reaches 100x100) |
| `08_2d_interacting/` | the main body: SU(N) EoS + observables, resummation, the wall suite, surrogate, plane-wave engine |
| `07_predict_vs_compute/` | the `CROSSCHECK_v5.md` … `CROSSCHECK_v194.md` series (freeze-then-predict records) |
| `bindings/` | optional pybind11 native bindings to the frozen engine (opt-in build) |
| `01_…`–`06_…`, `engine_exp/`, `framework_bridge/` | earlier stages and experiments |

## The unified CLI  (`./cdet <subcommand>`, or `pip install -e .` then `cdet …`)

- **verify**: `validate` (5 gates), `crosscheck` (all models side by side), `info`
- **compute**: `converge`, `resum`, `eos`, `docc`, `chi`, `run`, `sweep`
- **observe / export**: `plot`, `export` (CSV/JSON/HDF5)
- **wall physics**: `wall`, `tide`, `primes`, `twist`, `trueradius`
- **interactive**: `gui` (browser front-end over the CLI), `bench`, `diagmc`, `lab`, `shell`

## The two arcs

**Elevation checklist (v163–171)** — research code → a shippable product:
unified CLI (v163) · double occupancy (v164) · susceptibilities (v165) · figures (v166) · packaging + CI (v167) ·
dual license, free for academic / paid for commercial (v168) · data export CSV/JSON/HDF5 (v169) · native pybind11
bindings, ~10^6x over subprocess (v170) · Docker (v171).

**Wall-physics arc (v172–177)** — where lattice size meets the order axis:
- v172 the wall `U_c(L)=1/chi0_max` moves with L; near half-filling the large lattice reveals a further-out wall.
- v173 the wall is a **tide**: it oscillates with L; period = 2π/q* measures the Fermi nesting vector; even L converges
  exponentially, odd L as 1/L².
- v174 **prime** lattice sizes are the worst samplers — a Diophantine sieve (commensuration with q*).
- v175 "half-integer" lattices: twisted BC don't heal the sieve; rectangular supercells do. Tide and sieve are
  q-sampling artifacts, not properties of the true wall.
- v176 consolidation: one canonical Lindhard core; all models cross-checked side by side.
- v177 the **true** radius (nearest complex-U zero of lnZ) is a **thermal** Fisher pair at Im U≈π/β, closer than the RPA
  wall (the v146 caveat), and — having no q-grid max — free of the sieve.

## Where the knowledge lives

- **Ledger**: `real_patterns_v194.md` — entries #1…#187, the running narrative + every banked correction.
- **Findings**: 127 `*_RESULT.md` files (each a self-contained result with its validation).
- **Predictions**: `07_predict_vs_compute/CROSSCHECK_v5.md` … `CROSSCHECK_v194.md` (freeze-then-predict).
- **Benchmark note**: `bethe_cft_benchmark_note.md` (the cross-check range + running log).

## How to trust it

Every module has a `_selftest()` gate. `cdet validate` runs the 5 architectural gates (frozen 194/194, surrogate,
hybrid plane-wave parity, 2D plane-wave, consolidation); `cdet crosscheck` runs all models side by side; CI runs the
engine gate + `cdet validate` on every push; `packaging_check.py` / `docker_check.py` / `bindings/bindings_check.py`
gate the distribution. Corrections are banked openly in the ledger; overreach is retracted (e.g. v160, and the honest
limitation stated in v177).
