# CROSSCHECK_v167 — packaging and CI

**Claims.** (1) `pyproject.toml` makes `pip install -e .` install a working `cdet` console command (entry cdet:main);
verified it runs `cdet validate` from outside the repo (5/5). (2) Runtime deps numpy+mpmath; optional [viz]/[rich]/[all].
(3) GitHub Actions CI runs the frozen 194/194 gate, `cdet validate`, module self-tests, and the CLI self-test on
py3.9/3.11/3.12. (4) MIT LICENSE present. (5) `packaging_check.py` gates the scaffolding. (6) Frozen engine untouched.

**Reproduce.**
```
pip install -e ".[all]" && cdet validate     # installed command, 5/5 gates
PYTHONPATH=. python3 packaging_check.py       # scaffolding gate
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
