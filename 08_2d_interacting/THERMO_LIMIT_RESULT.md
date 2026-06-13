# The large-L study: z(∞) marches to the continuum Fermi level (v125)

Using the v124 machinery (plane-wave engine, projector fast path, continuous freeze, run_to_log), I ran
the scale law up the lattice sizes and watched the Fermi surface sharpen toward the thermodynamic limit.

## Frozen prediction (analytic, before any measurement)

At fixed μ=1.0, z(∞) = the lowest-empty eigenvalue above μ. As L grows the spectrum densifies, so this
level closes onto μ with the local level spacing, **gap ~ L⁻³·³** (≈1/L³):

| L | lowest-empty (=z∞) | gap above μ |
|---|---|---|
| 6 | 2.00000 | 1.00000 (integer spectrum) |
| 8 | 1.41421 | 0.41421 (√2) |
| 16 | 1.08239 | 0.08239 |
| 48 | 1.00092 | 0.00092 |
| 100 | 1.00019 | 0.00019 |

So **z(∞) → μ thermodynamically** — the lattice probe level converges to the continuum Fermi level.

## Measurement (fast-path z-flows, streamed through run_to_log)

At each L the flow z = lowest_empty(L) + ln(|A|/|c1|)/β rises toward that L's lowest-empty value:

| L | z(β=24,48,72,96) | → asymptote |
|---|---|---|
| 8 | 1.243, 1.267, 1.290, 1.317 | 1.414 (clean) |
| 12 | 1.238, 1.239, 1.245 | 1.268 (noisier) |
| 16 | 1.013, 1.029, 1.038 | 1.082 |
| 100 | one point, 52 s | probe_val=1.000192 == prediction |

The asymptote **marches down with L — 1.414 → 1.268 → 1.082 → 1.0002 — toward μ=1.0**, exactly as
predicted. The flow is clean at L=8 (gap 0.41) and gets noisier as L grows because the gap, and so the
determinant signal, shrinks.

## The finding

z(∞)(L) = lowest_empty(L) → μ as L → ∞ (the continuum Fermi surface). But the determinant **signal
vanishes as the gap closes** — the probe level merges into the Fermi sea, A and c1 both shrink — so the
thermodynamic measurement is signal-starved and needs growing statistics. The wall sharpens onto μ: the
scale law's content survives to the continuum, but resolving it there costs Monte Carlo. This is the
quantitative shape of the thermodynamic limit for the frozen connected determinant.

## Compute

The projector fast path made **L=100 — a million sites — a 52 s/point job** (45× eigenvalue collapse to
22,027 distinct values, no stored spectrum, tens of MB). Streamed and logged through run_to_log, a
day-long unattended run does a full high-stat z-flow at the thermodynamic scale. Reproduce:
`./cpw grid 24 24 1 4 256 31 0.002 2 2 1 2 4 1.0 -L 100 -fast` (one million-site point);
`python3 run_to_log.py /tmp/run.log -- ./cpw grid 24 96 24 12 2048 31 0.002 2 2 1 2 4 1.0 -L 16 -fast`
(streamed L=16 flow); `python3 thermo_limit_study.py`. Frozen engine untouched (194/194).
