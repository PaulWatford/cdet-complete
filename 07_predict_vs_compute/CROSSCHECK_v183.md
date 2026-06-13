# CROSSCHECK_v183 — GUI: a recent-runs memory (+ high-N hang fix)

**Claims.** (1) a server-side `recent` strip remembers explicit runs (chips: card + sliders + result), click to restore
+rerun, clear empties. (2) only explicit Run (log=1) is remembered, not Live auto-reruns; consecutive identical dedupe;
cap 8. (3) fixed the v181 high-N hang: GUI N capped at 4 + sweeps trimmed + server clamp; routes sub-second. (4) larger
SU(N) via copy-as-CLI. (5) front-end only. Frozen engine untouched.

**Reproduce.**
```
python3 cdet.py gui --no-browser
curl "http://127.0.0.1:8765/api/wall?L=24&beta=5&mu=0&log=1"   # logged
curl "http://127.0.0.1:8765/api/_recent"                        # -> the chip list
curl "http://127.0.0.1:8765/api/eos?N=8&U=2"                    # clamps to N=4, sub-second (no hang)
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
