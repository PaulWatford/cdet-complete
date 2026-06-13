# CROSSCHECK_v190 — blind intermediate-student test + sweep-crash fix

**Claims.** (1) `cdet sweep` works (was crashing with TypeError); fixed by passing a base-params dict. (2) install via pip
works with the PEP 668 note; `python3 cdet.py` needs no install. (3) export/plot/diagmc produce outputs. (4) no physics
changed; frozen engine untouched.

**Reproduce.**
```
cdet sweep --target eos --var U --values 0.5 1 1.5      # completes; archives cdet_runs/.../data.csv,summary.json,plot.png
cdet export eos --format csv                            # writes cdet_data/cdet_eos.csv
cdet plot                                               # writes cdet_figures/cdet_summary.png
python3 -m venv .venv && . .venv/bin/activate && pip install -e ".[all]"   # or add --break-system-packages
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
