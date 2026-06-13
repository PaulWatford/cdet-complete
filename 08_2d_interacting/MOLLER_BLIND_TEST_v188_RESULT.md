# Blind expert test (Gunnar Möller, from scratch) + benchmark surfacing (v188)

I ran the blind test again from the opposite end: a domain expert (the researcher who motivated the integration
program) starting cold, skeptical, wanting to verify the claims and run benchmarks. Fresh unzip, docs only.

**What an expert finds — and it holds up.** Everything named for him verifies:
- `make test` → 194/194; `make fast` re-verifies. The engine is real.
- `make bench` / `./bench_qss`: the connected-determinant evaluation vs a dense-LU cross-check — **12655× speedup at
  n=2048, agreement to ~1e-13, linear scaling to 1M**. Reproducible and cross-checked.
- `fast_minors.py`: the connected determinant in **O(2^n n^2)**, verified term-by-term against the engine to 3e-15 —
  the CoS / CDet-fast decomposition, substantiated.
- `self_energy.py` + `self_energy_irreducible.py`: eps+ReΣ ED-verified, exact 1PI coefficients — and it **honestly shows
  R_Σ ≈ R_G** (no radius advantage) and keeps the earlier overclaim **retracted**, attributing the Šimkovic-Kozik edge to
  efficiency/variance. An expert respects that the negative is kept.
- `physical_mapping.py` (z(inf) = addition pole, 4e-7), `consolidation_v138.py` (three paths agree), `cdet_lab.py
  validate` + `list` (the full target×method control plane), `resum` (conformal-Borel vs Padé), the size-axis oracles
  (`build_oracles.sh` self-contained build → `val2d.py` 2D vs numpy 3.4e-9; `locality.py` exponential decay → 2e-11), and
  the **Monte-Carlo control-variate benchmark** (`cv.py`: ~70–80× variance reduction, matching theory 1/(1−ρ²)=71×).

**Friction found:**
1. **The benchmarks were scattered** — `make bench`, `cv.py`, `fast_minors.py`, the oracle scripts — with no front-door
   entry. An expert asking "how do I run benchmarks" had to spelunk folders, and `./cdet --help` didn't surface them.
   *Fix:* added a **`cdet bench`** subcommand that runs the headline engine benchmark and prints a reproducible index of
   the rest (MC variance, fast-minors verification, size-axis). Surfaced it in `cdet info`, the README, the QUICKSTART
   on-ramp, the GUI (a bench card), and the assistant (a `bench` command + a "benchmarks" workflow; "run benchmarks" now
   routes there instead of colliding with `cdet run`).
2. **The "What to show Möller" section read like internal lab notes** (version numbers like "v137", "v136 RETRACTED").
   *Fix:* reworded it to be self-contained — plain statements (R_Σ ≈ R_G; the advantage is efficiency/variance) an
   external reader can follow.

**The honest gap (not a quick fix).** The capabilities are a verified engine + deterministic low-order CDet (fast-minors)
+ control-variate MC variance reduction + analysis modules. There is **no production Rossi-style DiagMC sampler** running
at high order in the doped/strong-coupling regime — the thing an expert would benchmark head-to-head against a CoS
production run. The package is explicit about this (the README "honest bottom line": the sign axis is the real,
NP-hard wall; Tier 2 is unbuilt). Worth stating plainly to an expert rather than implying a competitive sampler exists.

**Verified.** `cdet bench` runs (engine table + index); the GUI bench card runs the real command; the assistant routes
benchmark/performance/capability queries to the suite; assistant self-test 14 query + 6 behaviour checks pass (22
commands, 7 workflows). Interface/docs only — no physics changed; frozen engine untouched (194/194). `cdet.py`,
`cdet_gui.py`, `cdet_assistant.py`, `QUICKSTART.md`, `README.md`.
