# CROSSCHECK_v192 — lifecycle / interruption resilience

**Claims.** (1) SIGINT on CLI commands is clean ("interrupted.", no traceback). (2) an interrupted `cdet sweep` now keeps
its computed points (incremental data.csv + flushed log + summary.json with a stop reason). (3) restarting the console on a
busy port auto-finds a free port (no OSError traceback). (4) the cache write is atomic. (5) no physics changed; frozen
engine untouched.

**Reproduce.**
```
# interrupt a sweep after a point or two; the run dir keeps a partial data.csv + a labelled summary.json
timeout -s INT 25 cdet sweep --target eos --var U --values 0.3 0.6 0.9 1.2 1.5 1.8
# start two consoles on the same port; the second opens on the next free port with a note (no traceback)
cdet gui --port 8811 --no-browser &  cdet gui --port 8811 --no-browser
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
