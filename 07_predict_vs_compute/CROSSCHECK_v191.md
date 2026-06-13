# CROSSCHECK_v191 — adversarial chaos console test + hardening

**Claims.** (1) injection is inert (CLI no-shell + float casts; GUI allow-list + casters + JSON errors). (2) fixed real
self-DoS/nan: diagmc --nmax cap 8 / floor 1, --samples floor 100, sweep points cap 60 + 120s budget, finite/positive
guards on beta/mu/U. (3) normal use unchanged; frozen engine untouched.

**Reproduce.**
```
cdet diagmc --nmax 99999 --samples 200     # capped at 8, returns immediately (was a hang)
cdet sweep --target eos --var U --values $(seq 1 500)   # caps to 60 + stops on the 120s budget (was a hang)
cdet diagmc --samples 0 --nmax 2           # samples floored to 100 (was nan)
cdet diagmc --beta 0                        # clean "beta must be positive" error
cdet diagmc --U 1.5                         # normal run unchanged
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
