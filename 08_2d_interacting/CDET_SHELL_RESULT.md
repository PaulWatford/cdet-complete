# The idiot-proof conversational front-end: `cdet_shell.py` (v149)

A text interface that meets people where they are: describe what you want in plain language, and the shell states
back what it thinks you meant (with every assumed default shown — nothing hidden), presents the exact command, and
runs it only after you confirm. Saying "no" returns you to the start without losing any named/saved configuration.

## Grounded in established CLI design principles

From the Command Line Interface Guidelines (clig.dev) and related best-practice writing, the principles that
matter here — and how this shell implements each:

| principle (clig.dev et al.) | implementation |
|---|---|
| **The CLI is a conversation** | a REPL with a two-state machine: describe → confirm → run |
| **Discoverability; no hidden options** | `help`, `help <topic>`, `list`, `examples`, `configs`; the component map is imported from `cdet_lab` (single source of truth) so nothing can drift or hide |
| **Empathy / graceful errors** | unrecognized input never dead-ends: it returns the valid choices, a "did you mean", and an example of correct syntax |
| **Confirmation before action** | every run is shown as an explicit command and gated on yes/no |
| **Feedback** | the result is printed, then an offer to name/save the configuration |

## The state machine

```
HOME ──(plain language / flags)──▶ interpret ──▶ CONFIRM ──(yes)──▶ run ──▶ HOME
  ▲                                                  │
  └──────────────(no: revert, library kept)──────────┘
```

- **HOME** understands: `help [topic]`, `list`, `examples`, `configs`, `save <name>`, `run <name>`,
  `forget <name>`, `quit` — or a request in plain language or flags.
- **CONFIRM** understands: `yes` | `no` | `save as <name>`. `no` discards only the current draft; the named/saved
  library is never lost.

## Intelligence on imperfect input

- **Synonyms** map plain words to canonical components: "density"/"filling"→`eos`, "sigma"/"spectral"→`self-energy`,
  "mott"/"atomic"→`hubbard-i`, "doublon"→`double-occ`, etc. So "self-energy in the Mott regime" resolves to the
  Hubbard-I solver automatically.
- **Typo-robust**: if any keyword survives ("addtion **pole**"), the request still resolves.
- **Did-you-mean**: when nothing resolves ("selfenrgy …"), the shell suggests the closest observable and shows an
  example. When a user explicitly names an unknown solver ("… via teleport"), it lists the valid solvers.
- **Defaults are shown, not hidden**: the confirmation screen always prints the full command including the method
  and parameters it filled in, so the user sees exactly what will run before saying yes.

## Named, saved configurations

A confirmed run can be named (`save <name>`, or `save as <name>` at the confirm step) into a library that persists
across reverts. `configs` lists them; `run <name>` recalls one (re-presented for confirmation); `forget <name>`
drops it.

## Example session

```
home> self-energy in the mott regime U=4 mu=2 beta=5
Here's what I think you want:
  Sigma(iw) = U n + U^2 n(1-n)/(iw+mu-U(1-n)) -- atomic-limit rational (Mott)
    model=atom, U=4.0, mu=2.0, beta=5.0
  command:  python3 cdet_lab.py --target self-energy --method hubbard-i --model atom --U 4.0 --mu 2.0 --beta 5.0
Run it? [yes / no / save as <name>]
confirm [yes/no]> yes
Sigma (Hubbard-I, rational): U=4.0, mu=2.0, beta=5.0, n=0.5000
  Sigma(i w_0) = +2.000000 -6.366198i   [exact rational; Mott/large-U, real-freq capable]
home> save mott_run
```

Run interactively: `python3 cdet_shell.py`. Scripted self-test (14-step session through the state machine):
`python3 cdet_shell.py --selftest`. Every run routes through `cdet_lab`, so the frozen reference stays the anchor.
