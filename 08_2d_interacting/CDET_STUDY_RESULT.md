# Sweeps, stress tests, cutoffs, and graphs: `cdet_study.py` (v151)

Turns the single-shot control plane into a **parameter-sweep stress harness**: scan one variable for a chosen
(target, method), detect convergence or accuracy breakdown, stop on user-defined cutoffs, and emit a log + data +
a graph with the points of interest marked. Drivable from flags or from plain language in the shell.

## What you can study

| study | command sketch | what it shows |
|---|---|---|
| **convergence** | `--target addition-pole --sweep L --range 8:128:8 --conv-tol 1e-3` | the value settling to z(∞); the harness flags the L where it converges |
| **accuracy drop** | `--target self-energy --method diagrammatic --sweep U --range 0.2:1.6:0.1 --accuracy-cutoff 1e-3` | the cheap method's error vs ED climbing past the series radius (~π/β); stops where it stops being trustworthy |
| **cost / time** | `--target connected-det --sweep n --range 4:16:1 --max-time 10` | cost growing with system size; stops inside a wall-clock budget |

## Cutoffs (either or both)

- `--max-time T` — stop once cumulative wall time exceeds **T seconds**.
- `--accuracy-cutoff EPS` — stop once the error vs the natural reference exceeds **EPS** (for methods that have a
  reference: diagrammatic Σ vs ED, record EoS vs ED, fast-minors det vs numpy).
- `--conv-tol TOL` — flag **convergence** when |Δy| < TOL for a few consecutive steps.

## Outputs (in `./cdet_runs/<stamp>_<target>_<var>/`)

- `data.csv` — `x, y, error, step_seconds, elapsed_seconds`
- `summary.json` — the config, the stop reason, and every point of interest (converged / accuracy-drop /
  time-cutoff / max / min)
- `plot.png` — y vs x with the value on the left axis and (when a reference exists) the **error on a log axis**,
  convergence/breakdown/cutoff markers overlaid (matplotlib; degrades gracefully if absent)
- `run.log` — timestamped per-step log ending in a highlighted summary
- an **ASCII plot** printed to the terminal (always — works headless), with a legend for the markers

## Example (the radius-breakdown study)

```
U=0.2  y=+0.19694494  err=2.29e-14   (… )
U=0.4  y=+0.38681403  err=3.43e-09
U=0.6  y=+0.56133423  err=3.77e-06
U=0.8  y=+0.71399879  err=5.32e-04
U=1.0  y=+0.84388939  err=2.33e-02
  -> STOP: accuracy drop: error 2.33e-02 > 0.005 at U=1.0
```

The error climbs by orders of magnitude as U approaches the bare-series radius; the cutoff stops the run exactly
where the diagrammatic method stops being trustworthy, and the point is marked on both the ASCII and PNG plots.

## In the shell (plain language)

```
home> sweep U from 0.2 to 1.2 for self-energy diagrammatic, beta 5 mu 1, stop if accuracy drops below 5e-3
home> scan L from 8 to 128 for the addition pole at mu=1 until it converges
home> vary n from 4 to 14 for connected determinant, stop after 10 seconds
```

The shell interprets the sweep, shows the exact `cdet_study` command (with the cutoffs spelled out), and runs it
after you confirm — saving the run like any other configuration.

Reproduce: `python3 cdet_study.py --selftest` (convergence + accuracy + time cutoffs + ascii plot). Every
evaluation uses the same references as the control plane; the frozen engine stays the anchor (194/194).
