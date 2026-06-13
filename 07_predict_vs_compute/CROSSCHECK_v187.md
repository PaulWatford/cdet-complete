# CROSSCHECK_v187 — blind student test + onboarding fixes

**Claims.** (1) the assistant now handles beginner questions: new/lost -> getting-started directly; foundational concepts
(lattice, Hubbard model, exact diagonalization, Monte Carlo) answer correctly; "what should I run first" no longer returns
the heavy `cdet run`; "hubbard model" no longer returns the architecture. (2) QUICKSTART has a top on-ramp consistent with
the `./cdet` front door. (3) docs/help only; no physics changed; assistant runs nothing; frozen engine untouched.

**Reproduce.**
```
python3 cdet.py gui --no-browser
curl "http://127.0.0.1:8765/api/assist?q=what%20should%20I%20run%20first"   # -> "New here? Start with these ..."
curl "http://127.0.0.1:8765/api/assist?q=what%20is%20the%20hubbard%20model" # -> the Hubbard model (physics)
curl "http://127.0.0.1:8765/api/assist?q=what%20is%20a%20lattice"           # -> grid of sites
python3 08_2d_interacting/cdet_assistant.py                                  # 14 query + 6 behaviour checks PASS
head -20 QUICKSTART.md                                                       # the friendly on-ramp
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
