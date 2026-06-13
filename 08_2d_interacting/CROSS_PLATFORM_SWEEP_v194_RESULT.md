# Cross-platform sweep: every hardcoded /tmp removed (v194)

v193 made the `cdet` CLI gates cross-platform, but a second Windows run showed `cdet validate` still at 4/5: the
**consolidation health gate** failed with `FileNotFoundError: '/tmp/_csv161.c'`. The gate script
(`consolidation_v161.py`) compiled its own helper C file to `/tmp` at runtime -- a Unix-ism one level below the CLI that
v193 had not reached. A tree-wide search then found the same hardcoded `/tmp/` idiom in many more modules.

**Fix.** Removed every hardcoded `/tmp/` from executable Python and replaced it with `tempfile.gettempdir()`, adding a
`.exe` suffix for any binary that is launched on Windows and `shutil.copy` in place of `cp ... /tmp/`:
- the gate dependency `consolidation_v161.py` (this fixes `cdet validate` -> 5/5 on Windows);
- the consolidation siblings `v138`, `v147`, `v156`;
- the benchmark/research modules `fast_minors.py` (the one `cdet bench` points users to), `cos_prototype.py`,
  `triple_benchmark.py`, `two_particle_run.py`, `chained_run.py`, `stress_test_v139.py`, `run_to_log.py`;
- the `_selftest` output paths in `plots.py` and `export.py`;
- the optional C++ bindings (`bindings/bindings_check.py`, `bindings/build.py`).
After the sweep, a tree-wide grep finds no hardcoded `/tmp/` left in any executable line (only an example inside one
module's docstring).

**Verified (Linux).** `validate` 5/5; `crosscheck`, `--selftest`, the diagmc/assistant/surrogate gates and the frozen
194/194 all pass; and the individually patched module self-tests (`consolidation_v138/147/156`, `fast_minors`,
`cos_prototype`, `plots`, `export`) all still PASS. The change is pure portability plumbing -- no physics, frozen
reference engine untouched. Net effect: `cdet validate` now reports 5/5 on Windows (with gcc+make on PATH), and the deep
standalone modules run on Windows/macOS/Linux too.
