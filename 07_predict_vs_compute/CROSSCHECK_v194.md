# CROSSCHECK_v194 — cross-platform sweep (every /tmp removed)

**Claims.** (1) consolidation_v161.py no longer writes to /tmp (fixes `cdet validate` to 5/5 on Windows); (2) all other
modules with hardcoded /tmp were swept to tempfile.gettempdir() + .exe/shutil; (3) no hardcoded /tmp remains in executable
Python; (4) Linux: validate 5/5 and all patched module self-tests still PASS; (5) no physics; frozen engine untouched.

**Reproduce.**
```
cdet validate                                   # 5/5 (Linux/macOS/Windows with gcc+make)
python 08_2d_interacting/consolidation_v161.py  # PASS (was FileNotFoundError /tmp on Windows)
python 08_2d_interacting/fast_minors.py         # PASS
grep -rn "/tmp/" --include=*.py .               # only a docstring example remains
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
