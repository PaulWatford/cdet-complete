# CROSSCHECK_v182 — GUI: downloadable CSV + copy-as-CLI

**Claims.** (1) sweep cards (eos/docc/chi/wall/propagator) export CSV via export._write_csv (matches `cdet export`
format; attachment headers). (2) every card shows a live, runnable `cdet ...` command with a copy button. (3) eos/docc/
chi cards compute at the suite reference (mu=1,beta=2) so the copied command reproduces the shown value; copied commands
run. (4) front-end only; no new physics. Frozen engine untouched.

**Reproduce.**
```
python3 cdet.py gui --no-browser
curl "http://127.0.0.1:8765/api/eos?N=4&U=1&csv=1"          # CSV download (export format)
python3 cdet.py eos --N 4 --U 1                               # the card's copy-as-CLI command -> 0.4379
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
