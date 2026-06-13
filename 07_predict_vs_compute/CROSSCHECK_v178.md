# CROSSCHECK_v178 — consolidation: one index for the whole package

**Claims.** (1) INDEX.md catalogs the package (architecture, directory map, all 19 CLI subcommands, the two arcs, where
knowledge lives). (2) Every file reference in INDEX/README resolves to a real file; all 19 subcommands documented; no
orphans. (3) README lists trueradius and points to INDEX. (4) cdet validate 5/5; frozen 194/194; surrogate 3.55e-15. (5)
Frozen engine untouched.

**Reproduce.**
```
cat INDEX.md
python3 cdet.py validate            # 5/5
cd engine && make CC=gcc test        # 194/194
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
