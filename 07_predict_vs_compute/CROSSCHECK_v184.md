# CROSSCHECK_v184 — GUI rebuilt as a thin wrapper over the CLI

**Claims.** (1) the GUI imports no physics (stdlib only); every card runs the real `cdet <subcommand> <flags>` via
subprocess and shows its real output. (2) every subcommand is a card; controls are the command's actual flags; no caps,
no hardcoded params. (3) injection-safe (list argv, allow-listed, values validated). (4) core eos/docc/chi commands
unchanged; calculations untouched. Frozen engine untouched.

**Reproduce.**
```
python3 cdet.py gui --no-browser
curl "http://127.0.0.1:8765/api/run?cmd=eos&N=4&U=1&K=10"     # runs the REAL cdet eos, returns its table
curl "http://127.0.0.1:8765/api/run?cmd=wall&beta=5&mu=0"     # runs the REAL cdet wall
curl "http://127.0.0.1:8765/api/run?cmd=wall&beta=5;rm+-rf+/&mu=0"   # -> rejected, not executed
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
