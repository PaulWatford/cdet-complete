# CROSSCHECK_v193 — cross-platform gates (Windows/macOS/Linux)

**Claims.** (1) the validate/converge/run gates build to a cross-platform temp path (.exe on Windows) and launch it
portably; (2) cp -> shutil, `PYTHONPATH=. python3` -> sys.executable + env; (3) Linux still 5/5; (4) docs note the per-OS
compiler requirement; (5) no physics changed, frozen engine untouched.

**Reproduce.**
```
cdet validate          # 5/5 on Linux/macOS with gcc+make; on Windows with w64devkit/MSYS2 on PATH
cdet --selftest        # exercises the cross-platform temp output paths
cdet converge ; cdet run
```
On Windows without a compiler the C gates FAIL but all Python commands (eos, diagmc, gui, ...) still work.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
