# START HERE

A connected-determinant calculator for small Hubbard lattices. Pure C, no
dependencies. Here is the whole thing in one screen.

## Run it (Mac or Linux)

```
sh run_tests_unix.sh
```

That builds everything, runs 194 self-checks, and builds the `cdet` tool. On
Windows, double-click `run_tests_windows.bat` instead.

## Do a calculation

```
./cdet
```

With no arguments it gives you a menu: pick what to compute, pick a lattice,
answer a couple of prompts (press Enter to keep each default). Done.

Prefer the command line?

```
./cdet --help                                          all options, explained
./cdet --task order --lattice hexring --order 2        a perturbative order
./cdet --task det --n 256 --beta 20                    one fast determinant
./cdet --task green --lattice dimer                    the propagator table
./cdet --task anchors                                  both modular anchors + self-dual check
```

The three knobs you will usually turn: `--beta` (inverse temperature), `--mu`
(chemical potential), `--t` (hopping). Everything has a sensible default.


## Verify the numbers yourself (optional)

The 194 self-checks above already compare the C against frozen reference values
in `golden.json`, which **ships in this directory** (16 KB) and is read at runtime
by the test harness. `make CC=gcc test` is the whole verification: 194/194.

Note (self-contained drop): the original golden-regeneration tooling
(`gen_golden.py`, `gen_golden2.py`, and the independent `cdet_reference/` Python
source) is **not bundled here** — the engine is frozen, so the shipped
`golden.json` is authoritative and no regeneration is needed. If you want to
re-derive the goldens independently, reconstruct them from the Python CDet
reference in `08_2d_interacting/` (`cdet_port.py`), which reproduces the same
values to 1e-9.

## If you want more

- `README.md`     full detail: the four lattices, the fast-determinant method,
                  the parallel and dynamic paths, and how to call the library
                  from your own C.
- `golden.json`   the frozen reference values (ships here); `make test` checks
                  the C against them. (The original regeneration scripts and the
                  `cdet_reference/` Python source are not bundled in this frozen
                  drop — see the verification note above.)

## Needs a C compiler

Mac: `xcode-select --install`. Linux: `sudo apt install build-essential`.
That is the only prerequisite.
