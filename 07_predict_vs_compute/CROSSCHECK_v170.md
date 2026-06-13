# CROSSCHECK_v170 — native pybind11 bindings

**Claims.** (1) `bindings/cdet_core.cpp` wraps the frozen engine's primitives (G0_atom, density_exact, …) + the 2D
plane-wave propagator (square2d_g0), read-only. (2) Bit-identical to the frozen engine: native G0_atom == a
freshly-compiled frozen-C G0_atom to 0.0e+00; square2d_g0 (L=16 NN) matches the validated plane-wave value. (3)
Eliminates subprocess overhead: ~120 ns native vs ~232 ms compile+subprocess (~2e6×). (4) Opt-in build (pure-python
install stays compiler-free); .so not shipped, rebuilt on target. (5) Frozen engine untouched.

**Reproduce.**
```
pip install "pybind11>=2.10" && python bindings/build.py
python bindings/bindings_check.py        # gate: build + bit-identical parity + benchmark
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
