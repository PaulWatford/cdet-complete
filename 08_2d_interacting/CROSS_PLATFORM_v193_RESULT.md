# Cross-platform fix: the gates now run on Windows, macOS and Linux (v193)

A blind install on a real Windows machine (Python 3.13 + the w64devkit gcc/make toolchain) exposed that the validation
harness was Linux-only: `cdet validate` reported the C-engine gates as FAIL even though the underlying C compiled and ran
perfectly (`gcc ... csurrogate_test.c csurrogate.c` built, and the binary printed "ALL CASES MATCH ... worst dev
3.55e-15"). The science was correct; the harness was not portable.

**Root cause.** The compile-and-run gates hardcoded Unix conventions:
- built to `/tmp/_cdet_*` (there is no `/tmp` on Windows) and ran that literal path (a Windows gcc binary is `*.exe`);
- used `cp spectrum_l6.bin /tmp/` (`cp` is a Unix command);
- launched the consolidation gate with `PYTHONPATH=. python3 ...` (inline env-var assignment is Unix-shell syntax, and
  the interpreter is `python`, not `python3`, on Windows).
Only the frozen-engine gate passed there, because it goes through `make`, which manages its own paths.

**Fix (cdet.py only).** Added small cross-platform helpers and rewrote every build/run site to use them:
- `_binpath(name)` -> a temp path from `tempfile.gettempdir()` with a `.exe` suffix on Windows, so the built program can
  actually be launched;
- `_q(path)` -> shell-quotes paths (handles spaces in Windows temp dirs);
- `_stage_tmp(file, dir)` -> copies a needed data file with `shutil.copy` instead of `cp`;
- `_sh(..., env=...)` -> passes environment via subprocess instead of inline `VAR=value` shell syntax, and the
  consolidation/shell gates now run `sys.executable` (the running interpreter) rather than a literal `python3`.
This covers `validate` (all four compile gates + consolidation), `converge`, `run`, the interactive-shell fallback, and
the `--selftest` temp output paths. The `&&` chaining and `<` stdin redirect used by the gates work in both `cmd.exe` and
POSIX shells, so they were left as-is.

**Docs.** README and QUICKSTART now carry a Platforms note: the Python commands need no compiler on any OS, and the C
gates need gcc + make -- `build-essential` on Linux, `xcode-select --install` on macOS, and w64devkit or MSYS2 on
Windows (download, unzip, add `bin` to PATH). This is the gap the same blind test flagged: the docs assumed a Unix box.

**Verified.** On Linux all five gates still pass (`5/5 gates passed`), `--selftest`, `converge`, `run`, `crosscheck`,
`bench`, the diagmc and surrogate gates, and the frozen 194/194 all pass unchanged. The fix is pure portability plumbing
-- no physics changed, the frozen reference engine is untouched. `cdet.py`, `README.md`, `QUICKSTART.md`.
