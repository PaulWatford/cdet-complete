# A local browser console: quick runs with sliders (v181)

**What.** `cdet gui` starts a small stdlib http server and opens a single-page console — a rail of sliders (N, U, μ, β,
L) and one-click quick-run cards over the most-used computations, each showing an instrument-style readout and a small
trace. A "Live" toggle re-runs cards as you move a slider. No new dependencies (Python stdlib + numpy); it drives the
exact same functions as the CLI.

**Quick runs (cards).** Equation of state (density n) · Double occupancy · Susceptibilities (charge κ, spin χ_s) ·
Convergence wall (RPA U_c) · True radius (the complex-U Fisher pair) · Free propagator (L→∞) · Validate (5 gates). Each
card lists the sliders it reads; the two physical limits — the wall and the true radius — are rendered in amber.

**Design.** Grounded in the subject: a numerical instrument. Dark console, monospace tabular readouts, teal
oscilloscope-style traces, amber threshold lines for the physical limits. One accent for action/data (teal), one for
limits (amber); everything else quiet. Responsive to mobile; errors report in the interface's voice rather than crashing.

**Verified (server started, endpoints curled, then stopped).** The page loads; every endpoint returns correct values —
eos density 0.3716, docc 0.2933, κ 0.1826 / χ_s 0.2853, wall U_c 1.9752, true radius 1.5723 (Im=π/β, thermal),
free propagator 0.19944 (matches `converge`'s thermodynamic limit), validate 5/5; unknown routes return 404; every card
maps to a real route; the embedded HTML is balanced. Launches from both `cdet gui` and `python3 cdet_gui.py`.

**Scope.** A front-end over existing computation — it makes the most-used items one click with slider customization. It
adds no new physics and changes nothing the tool computes. Frozen reference engine untouched (194/194).
`cdet_gui.py`, `cdet gui [--port N] [--no-browser]`.
