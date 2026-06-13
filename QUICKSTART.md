# QUICKSTART — cdet, from zero to verified in minutes

## Start here (the friendly on-ramp)

New to this, or just want it working? Four commands from the `cdet_complete/` folder:

```
cd engine && make CC=gcc test   # 194/194 -> the engine is correct  (use CC=gcc if `make` picks a different compiler)
cd .. && ./cdet validate        # 5/5 gates: the full dashboard
./cdet converge                 # the thermodynamic-limit table, instantly -- a satisfying first result
./cdet gui                      # a browser front-end: sliders fill in the flags and run the real commands
```

In the GUI, toggle the **assistant** (top-right) and just ask -- "what is a lattice?", "what do I do first?",
"what is beta?" It's offline and rule-based, points you to the right command, and runs nothing on its own.
Bare commands work with no flags too: `./cdet eos`, `./cdet wall`, `./cdet docc` each print a result and a
one-line explanation. `./cdet --help` lists everything; `./cdet bench` runs the benchmark suite and `./cdet diagmc` runs the connected-determinant Monte Carlo (and shows the sign wall).

The rest of this file is the deeper build/verify path and the research modules.


You need only a C compiler and make. Python (with numpy) is optional, for the
analysis packages.

## 1. Build and verify the engine (the only step that matters)
```
unzip cdet_complete.zip
cd cdet_complete/engine
make test
```
Expected last line:
```
RESULT: 194 passed, 0 failed, 0 skipped (of 194)
ALL CASES MATCH THE PYTHON REFERENCE TO 1e-09
```
If you see that, the engine is built and correct. `golden.json` ships in the
folder, so the check is self-contained.

## 2. Optimized build (use this for real runs)
```
make fast        # -O3 -march=native
```
Multi-core (optional, needs OpenMP):
```
make omp
```

## 3. See it actually compute (good demo)
```
make bench
./bench_qss
```
Prints the connected-determinant evaluation vs a dense LU cross-check: matching
values to ~1e-15 and the speedup curve as order n grows. This is the clearest
one-screen proof the solver works.

## 4. The analysis packages (optional, need python3 + numpy)
Some analysis scripts (02, 04, 05, and 01's TCI demo) call a small compiled C
oracle that evaluates the engine's connected determinant / propagator. These are
built in place from the bundled sources by one command — nothing is read from
/tmp, so the package is fully self-contained:
```
./build_oracles.sh       # builds engine + every oracle in place (needs gcc + make)
```
Then run any package from its own folder:
```
pip install numpy teneva                          # teneva only needed for 01/02 (TCI)
cd 02_control_variate && python3 cv.py            # ~70x MC variance reduction (seeded, reproducible)
cd 04_locality        && python3 locality.py      # connected diagrams are local
cd 05_2d_lattice      && python3 val2d.py         # 2D torus vs numpy diagonalization
cd 01_tci_integrator  && python3 cdet_tci.py      # tensor-cross-interpolation of the time integral
```
Each oracle folder also has its own `Makefile` if you prefer to build them
individually (`make` inside the folder). Each folder has a RESULT .md stating
what it shows, honestly, including the measured negatives.

## If make fails
The build is plain C99 + libm, no exotic deps. If `make` is unhappy, this does it
by hand:
```
cd cdet_complete/engine
for f in *.c; do cc -O2 -std=c99 -I. -c "$f" -o "${f%.c}.o"; done
CORE=$(for o in *.o; do nm "$o" | grep -q ' T main' || echo "$o"; done)
cc -O2 test_cdet.o $CORE -lm -o test_cdet && ./test_cdet
```

## (Researchers) What to show Möller -- the integration program from his three papers
- `make test` -> 194/194: the engine is a verified Rossi-style connected-determinant
  DiagMC solver for the Hubbard lattice.
- `08_2d_interacting/fast_minors.py`: the connected determinant in O(2^n n^2) (the
  fast-principal-minor + subset-convolution decomposition his CoS / CDet-fast use),
  verified term-by-term against the engine.
- `08_2d_interacting/physical_mapping.py`: our deep-beta z(inf) IS a real spectral
  observable -- the free single-particle addition pole.
- `08_2d_interacting/self_energy.py` + `self_energy_irreducible.py`: the interacting
  upgrade (eps+ReSigma, ED-verified) and the exact 1PI coefficients -- with the honest
  finding that the 1PI (self-energy) series buys no convergence-radius advantage over the
  Green's-function series (R_Sigma ~ R_G on the atom); the Šimkovic-Kozik advantage is
  efficiency and MC variance, and strong coupling still needs resummation. This is exactly
  the Šimkovic-Kozik self-energy direction.
- `consolidation_v138.py`: all three paths (surrogate / plane-wave / python) agree.
- README.md: the honest map of the 2^n wall, and the current integration frontier.

The Hubbard solver stands on its own and is the thing his group can use tomorrow; the
integration modules show our engine on the same observables as his 2024 CoS line.

## 5. Hubbard correlation pattern (standard test + animation)
The interference pattern of many electrons on a lattice, exact, with an animation:
```
./run_pattern.sh                         # writes figures + hubbard_pattern.gif
# or directly:
cd 06_hubbard_pattern && python3 hubbard_pattern.py --anim
```
Needs python3 + numpy + scipy + matplotlib + pillow. At U=0 it self-checks against
the analytic free-fermion result to ~1e-17. See 06_hubbard_pattern/README.md.


## Unified entry point (v148): `cdet_lab.py`

One control plane for every capability, from the terminal:

```
cd 08_2d_interacting
python3 cdet_lab.py list                                              # the full component map
python3 cdet_lab.py validate                                         # three-model health gate
python3 cdet_lab.py --target eos --method record --N 6 --U 1.0 --mu 1.0
python3 cdet_lab.py --target self-energy --method hubbard-i --U 4.0 --mu 2.0 --beta 5.0
python3 cdet_lab.py --target addition-pole --method surrogate --L 12 --mu 1.0
python3 cdet_lab.py --target connected-det --method fast-minors --n 5
```

Swap `--method` to change solver (ed / record / hubbard-i / diagrammatic / surrogate / hybrid / fast-minors /
engine), `--target` to change observable. The frozen reference `engine/` stays the untouched 194/194 anchor.


## Friendliest entry point (v149): `cdet_shell.py`

If you'd rather not memorize flags, just talk to it:

```
cd 08_2d_interacting
python3 cdet_shell.py
home> help
home> self-energy in the mott regime U=4 mu=2 beta=5
        # it shows the command and asks; reply 'yes' to run, 'no' to cancel
home> save mott_run        # name a confirmed run; survives cancels
home> run mott_run         # recall it later
```

It understands plain words (density->eos, sigma->self-energy, mott->hubbard-i), suggests corrections on typos, and
never hides options. Every run still goes through `cdet_lab`, so the frozen reference stays the anchor.


## Sweeps & stress tests (v151): `cdet_study.py`

Scan a parameter, find convergence or where accuracy breaks, with your own cutoffs:

```
cd 08_2d_interacting
# accuracy cutoff: stop where the diagrammatic series stops matching ED (the radius)
python3 cdet_study.py --target self-energy --method diagrammatic --sweep U --range 0.2:1.6:0.1 --beta 5 --mu 1 --accuracy-cutoff 1e-3
# convergence: addition pole -> z(inf)
python3 cdet_study.py --target addition-pole --method surrogate --sweep L --range 8:128:8 --mu 1 --conv-tol 1e-3
# time budget: stop within 10 seconds
python3 cdet_study.py --target connected-det --method fast-minors --sweep n --range 4:16:1 --max-time 10
```

Each run writes `data.csv`, `summary.json`, `plot.png`, and `run.log` to `./cdet_runs/`, and prints an ASCII plot.
Or just say it in the shell: `sweep U from 0.2 to 1.2 for self-energy diagrammatic, stop if accuracy drops below 5e-3`.
