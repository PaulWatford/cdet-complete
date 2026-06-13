# CROSSCHECK_v180 — UX polish from a blind-user review

**Claims.** (1) bare `cdet run` works (auto beta-hi + customize hint). (2) `cdet sweep` shows per-point progress. (3)
run/sweep/lab have worked-examples help. (4) shell has more synonyms + friendlier no-match message. (5) README has a
"Try this first" block + folders-are-internals note. (6) engine/physics unchanged: validate 5/5, frozen 194/194.

**Reproduce.**
```
python3 cdet.py run                                   # works with no args
python3 cdet.py sweep --target addition-pole --var L --values 6 12   # [1/2].. progress
python3 cdet.py run --help                             # examples epilog
python3 cdet.py validate                               # still 5/5
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
