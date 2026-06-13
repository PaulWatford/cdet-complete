# CROSSCHECK_v181 — a local browser console (sliders + quick runs)

**Claims.** (1) `cdet gui` serves a single-page console (stdlib http, no new deps) with sliders N/U/mu/beta/L and
quick-run cards. (2) Every /api endpoint returns correct values from the same functions as the CLI (propagator 0.19944 =
converge TD limit; validate 5/5). (3) Unknown routes 404; HTML balanced; each card maps to a route. (4) Front-end only;
no new physics. Frozen engine untouched.

**Reproduce.**
```
python3 cdet.py gui --no-browser           # then open http://127.0.0.1:8765/
curl "http://127.0.0.1:8765/api/wall?L=32&beta=5&mu=0"     # -> U_c ~ 1.9752
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
