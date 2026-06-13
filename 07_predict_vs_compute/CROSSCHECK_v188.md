# CROSSCHECK_v188 — blind expert test (Möller) + benchmark surfacing

**Claims.** (1) the named expert capabilities verify: engine 194/194, bench_qss speedup table, fast_minors O(2^n n^2) vs
engine, self_energy R_Σ~R_G (retraction kept), lab control plane, cv.py MC ~70-80x, size-axis oracles. (2) a new
`cdet bench` surfaces the benchmark suite from one command; it appears in info/README/QUICKSTART/GUI/assistant. (3) the
"run benchmarks" query routes to the benchmark suite, not the `run` command. (4) interface/docs only; frozen engine
untouched.

**Reproduce.**
```
cd engine && make bench            # 12655x speedup at n=2048, agreement ~1e-13, linear to 1M
cd .. && ./cdet bench              # the engine benchmark + a reproducible index of the rest
python3 08_2d_interacting/fast_minors.py        # O(2^n n^2) vs engine, 3e-15
cd 02_control_variate && python3 cv.py          # MC control variate ~70-80x (theory 1/(1-rho^2))
python3 08_2d_interacting/cdet_assistant.py     # 14 query + 6 behaviour checks PASS
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
