# Blind intermediate-student test: install + real use (v190)

I installed and used the package blind as an intermediate student -- someone who knows the physics basics and wants to
install it properly and do real work (export data, make figures, run sweeps, try the sampler).

**What works.** `pip install -e ".[all]" --break-system-packages` installs cleanly and puts the `cdet` console script on
PATH; `cdet validate` -> 5/5. `cdet export --format csv` writes `cdet_data/cdet_docc.csv` (and `cdet export eos` / `chi` /
`convergence` / `resummation` via the dataset argument); `cdet plot` writes `cdet_figures/cdet_summary.png`; `cdet diagmc`
runs and shows the sign wall. Each reports the path it wrote and explains the result.

**Friction found, and fixed:**
1. **`cdet sweep` crashed** -- `cdet sweep --target eos --var U --values 0.5 1 1.5` raised
   `TypeError: 'str' object is not a mapping`. `cmd_sweep` passed the `--base` flag string ("L") where `cdet_study.study()`
   expects a dict of fixed base parameters, so `{**base, ...}` failed. A very natural intermediate task (sweep an
   observable over U) was broken, in both the CLI and the GUI sweep card. *Fixed:* pass an empty base-params dict (the
   evaluator already supplies its own defaults for beta/mu/U). Verified across targets (eos, double-occ) and via the GUI.
2. **The documented install lead failed on a modern OS.** `pip install -e ".[all]"` (the README's first option) errors with
   "externally-managed-environment" (PEP 668) on Ubuntu 24. *Fixed:* the README now notes the venv path and
   `--break-system-packages`, and reminds that `python3 cdet.py <cmd>` works with no install at all.
3. **Minor:** `cdet export` defaults to the docc dataset; that you can pass `eos`/`chi`/etc. as a positional argument is
   now surfaced in `cdet info`, the README, and the assistant.

**Verified.** The fixed sweep completes and archives `data.csv`/`summary.json`/`plot.png` under `cdet_runs/`; install +
`cdet` entrypoint work; export/plot/diagmc all produce their outputs. A genuine bug fix plus an install-doc fix; no physics
changed; frozen reference engine untouched (194/194). `cdet.py`, `README.md`, `cdet_assistant.py`.
