# GUI rebuilt as a thin wrapper over the CLI (v184)

**The correction.** Earlier GUI versions (v181–183) quietly grew into a *parallel* implementation: the cards called the
physics functions directly (`density_ed`, `wall`, …), which forced compromises that had no business existing — the
eos/docc/chi cards hardwired mu=1, beta=2; an N cap was bolted on to dodge a slow path; the GUI computed its own sweeps
and CSVs. That was the wrong shape. The GUI should be a front-end over the command line, nothing more.

**What it is now.** `cdet_gui.py` imports **no physics at all** — only the Python standard library. Every card is a real
`cdet` subcommand; its controls are that subcommand's actual flags (a slider per number, a dropdown per choice). Pressing
Run executes `python3 cdet.py <subcommand> <flags>` and shows its real output, ANSI-stripped, exactly as the terminal
would. Sliders just fill in the numbers; the math, the commands, and the results are the CLI's, untouched.

- **Every subcommand is a card** — validate, converge, connected, crosscheck, eos, docc, chi, resum, wall, tide, primes,
  twist, trueradius, run (with the lattice-size `--L`, the β range, `--NT`, …), sweep, export. Nothing is GUI-only and
  nothing is reimplemented; if you can type it, there's a card for it, and vice versa.
- **No caps, no hardcoded parameters.** Whatever you set is passed straight to the command; if a setting is slow, it is
  slow exactly as the CLI is. The GUI adds no parameter the command line doesn't already have.
- **Copy gives the exact command** that was run; the recent strip lists real commands; clicking one restores the controls
  and re-runs.
- **Safe by construction.** The server runs a list-argv subprocess (never a shell), only for allow-listed subcommands,
  with every value cast/validated — a value like `5;rm -rf /` is rejected, not executed (verified).

**Verified (server up, then down).** The eos card runs `cdet eos --N 4 --U 1.0 --K 10` and returns its real table; wall,
trueradius, etc. likewise; an injection attempt is rejected; an unknown command is refused; recent records the real
commands. The core `cmd_eos`/`docc`/`chi` were never changed and still produce identical results. Frozen reference
engine untouched (194/194). `cdet_gui.py`, `cdet gui`.
