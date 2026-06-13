# Consolidation v156 — the v148–155 arc

A periodic checkpoint (the consolidation rule): re-prove the whole current state coheres. Nothing new is asserted;
everything since the last consolidation (v147) is re-verified against an exact anchor by a single health gate
(`consolidation_v156.py`, ~1s).

## Architecture (unchanged)

- **Frozen reference** — `engine/`, 194/194, never altered: the anchor every claim is checked against.
- **Production engine** — `cdet_planewave_engine.c`: validates == the frozen reference (0.00e+00 at L=6).
- **Surrogate** — `csurrogate.c`: fast pure-arithmetic carriers (addition pole, Friedel edge, interacting pole,
  SU(N) production coeffs).

## What this consolidation adds over v147

**(A) UI control plane (v148–151).** The terminal entry points to every capability:
- `cdet_lab.py` — unified CLI: target × method × model over every capability (10 components).
- `cdet_shell.py` — conversational front-end over cdet_lab (blind-test hardened), cdet_lab as the single source of truth.
- `cdet_study.py` — sweep/stress harness with convergence detection and accuracy/time cutoffs.

**(B) SU(N) EoS — weak → strong → 2D thermodynamic limit → 2nd order (v152–155).**
- `sun_eos_curve.py` (v152): record-predicted weak EoS curve, Padé to U≈1.2.
- `sun_eos_strong.py` (v153): two-point resummation (weak lattice record + strong atom record) reaches U/t=2.3 at 2.4%.
- `sun_eos_2d.py` (v154): the record is lattice-independent; the production formula transfers across geometry to 1e-8;
  2D thermodynamic limit via converged k-integral, no diagonalization (SU(6) n₁ = −0.5116).
- `sun_eos_n2.py` (v155): n₂ = (N−1)²·[self-consistent Hartree, exact in 2D] + (N−1)·[bubble].

## What the gate checks (each tied to an exact anchor)

- **Invariants:** surrogate == production route (SU(N) c₁, n₁); surrogate addition pole == python; fast-minors
  connected determinant == numpy det.
- **UI:** cdet_lab COMPONENTS populated; cdet_shell shares them; cdet_study harness present.
- **EoS:** weak n₀ = free single-flavor density; strong atomic anchor smooth in N + stable two-point; 2D
  n₁ = −0.5116 (k-integral converged); 2D n₂ Hartree part a₂D = 0.005622.

A single command now re-proves the frozen anchor is intact and every claimed capability since v147 is still live
and still agrees with ED. Reproduce: `python3 consolidation_v156.py`.
