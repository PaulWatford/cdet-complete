# GUI: downloadable CSV + copy-as-CLI (v182)

Two additions to the browser console, both about taking work *out* of the GUI:

**Download CSV.** The sweep cards (equation of state, double occupancy, susceptibilities, convergence wall, free
propagator) get a **CSV** button. It hits `/api/<card>?...&csv=1`; the server builds the sweep and formats it with the
suite's own `export._write_csv`, so the file is byte-for-byte the same shape as `cdet export` output — a `# <name>` +
JSON-meta header line, a column row, then the data. Returned as a real download (`Content-Disposition: attachment`,
`cdet_<card>.csv`).

**Copy as CLI.** Every card shows the exact `cdet …` command that reproduces it, kept in sync as you move the sliders,
with a **copy** button (clipboard, with a textarea fallback). The commands are real and runnable:
`cdet eos --N 4 --U 1`, `cdet docc --N 2 --U 1`, `cdet chi --N 2 --U 1`, `cdet wall --beta 5 --mu 0`,
`cdet trueradius --beta 2 --mu 0.5`, `cdet converge`, `cdet validate`. The GUI teaches the command line.

**Faithfulness fix.** To make the eos/docc/chi commands reproduce exactly, those cards now call the compute functions at
the suite's reference point (mu=1, beta=2) — identical to what the CLI does — rather than off the mu/beta sliders (which
the `cdet eos/docc/chi` commands don't expose). So each card's "uses" tags shrank to `N U`, and the global mu/beta
sliders now drive only the lattice cards (wall, true radius, propagator), where the CLI does take `--beta --mu`. The
copied command therefore reproduces the displayed number, not an approximation of it.

**Verified (server up, then down).** CSV returns export-formatted text with attachment headers for all five sweep cards;
the page carries the CLI line, copy, and CSV controls; bare eos = 0.437896 (matches `cdet eos`); and the copied commands
run — `cdet eos --N 4 --U 1` → 0.4379, `cdet trueradius --beta 2 --mu 0.5` → radius 1.5723, `cdet wall --beta 5 --mu 0`
reproduces the wall sweep. Front-end only; no new physics. Frozen reference engine untouched (194/194). `cdet_gui.py`.
