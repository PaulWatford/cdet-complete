# CROSSCHECK_v126 — the signal budget: resolving z(∞) at large L costs ~N

**Claims.** (1) At fixed stats, relErr(A) ~ gap⁰·⁰⁶ (flat), relErr(c1) ~ gap⁻⁰·⁴⁷ (grows) — c1 is the
binding signal. (2) MC budget to hold z-precision ~ gap⁻⁰·⁹ ~ L³ ~ N — polynomial, no exponential wall.
(3) L=100, K5 NT384: c1=5.5e−4±3.9e−4 (~70%), 117s/point; ~5% needs ~170× more samples (~5.5h/point), so a
day-long run gives a coarse million-site z-flow. (4) Launch recipe via run_to_log streams + fsync-logs.

**Reproduce.** `cd 08_2d_interacting && python3 signal_budget_study.py`; the scan: for L in 8..24,
`./cpw grid 24 24 1 12 2048 31 0.002 2 2 1 2 4 1.0 -L <L> -fast`; the launch:
`python3 run_to_log.py /tmp/L100.log -- ./cpw grid 24 144 24 24 8192 31 0.002 2 2 1 2 4 1.0 -L 100 -fast`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
