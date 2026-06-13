# Phase 2 of the hybrid: the L-generalized plane-wave determinant engine, and the multi-lattice proof of the scale law (v123)

The hybrid's phase 2 is built: `cdet_planewave_engine.c`, the stable engine with its eigenvector
propagator replaced by the plane-wave form, runs the connected determinant at **arbitrary L with no
stored spectrum**. It proves the scale law across lattice sizes.

## The engine

g0(i,j,τ) = (1/N) Σ_k cos(2π k·Δr/L) · val(ε(k), occ(k), τ), with ε(k) = −2(cos+cos+cos) computed on
the fly. No eigenvectors, no spectrum file. The freeze is generalized to track μ into any gap:
occupied < PROBE, probe = PROBE → s, PROBE+1 frozen empty, ≥ PROBE+2 physical. Everything else (Rossi
recursion, cluster IS, MoM, the log-domain G0_atom) is reused unchanged.

**Validation.** At L=6, PROBE=2 it reproduces the stable engine **exactly** — A=1.341555,
c1=−234.4268 to the last digit, val-mode worst relative deviation 0.00e+00. The plane-wave g0 is a
drop-in for the eigenvector g0.

## The multi-lattice scale law — z(∞) = the lowest-empty-level eigenvalue

| test | lattice | probe | μ | z(β=24,48,72) | → |
|---|---|---|---|---|---|
| 1 | **L=4** (N=64) | 2 | 1.0 ∈ (0,2) | 1.678, 1.800, 1.846 | **2** |
| 2 | L=6 | **3** | 2.5 ∈ (2,3) | 2.773, 2.852, 2.862 | **3** |

Test 1 confirms z(∞)=2 on a **different lattice** (different N, different propagator) — the law is
size-independent. Test 2 confirms z(∞)=**3** at a **different probe level** — so z(∞) is the
lowest-empty level, *not* the constant 2. The mechanism (corner-confined A, smallest-gap de-confined
c1) reproduces on both, with geometry-dependent rates but the predicted asymptote.

## Scaling

Cost is ~linear in N=L³ (one β=24 point, K8 NT1024): L=4 → 2.1 s, L=6 → 7.4 s, L=8 → 16.3 s. The
propagator is O(N); the determinant is over a fixed vertex set. L≈12–16 is feasible per point, with no
stored data.

## The hybrid, complete

- **Phase 1** (`multi_lattice_laws.py`, `cfriedel_L.c`): carries the laws — spectrum, Fermi/probe
  level (→ the z(∞) prediction), Friedel wavevector — for any L, instantly, O(N), no MC.
- **Phase 2** (`cdet_planewave_engine.c`): computes A, c1 on the plane-wave propagator and confirms z
  flows to the phase-1-predicted lowest-empty level.

The handoff is exactly where the surrogate stops being exact: phase 1 hands phase 2 the target (L, μ,
probe), phase 2 returns the coefficient and the validated flow. The dual (surrogate / brute) is
preserved; this is the third engine that spends MC only where the laws run out.

Open: non-crystallographic L (L=5,7,8,…) has an irrational spectrum, so the integer-level freeze
(lround) only approximates the levels — a continuous-threshold freeze is needed to test the scale law
there cleanly. None of this moves the wall, but it makes z(∞)=lowest-empty-level a proven,
lattice-size-independent, probe-level-general law.

Reproduce: `gcc -O2 -Wall -Werror -std=c11 -pedantic -o cpw cdet_planewave_engine.c -lm`;
`./cpw grid 24 72 24 12 2048 31 0.002 0 2 1 2 4 1.0 -L 4` (test 1); `./cpw val <
cdet_stable_engine_refs.txt` (L=6 validation). Frozen engine untouched (194/194).
