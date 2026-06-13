#!/usr/bin/env python3
"""bindings_check.py -- gate for the optional native bindings (cdet_core).

Verifies the bindings (1) build, (2) are bit-identical to the FROZEN reference engine (they ARE the frozen functions,
called natively), and (3) eliminate the subprocess/compile overhead for programmatic access."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engine")


def _ensure_built():
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    try:
        import cdet_core  # noqa
        return cdet_core
    except Exception:
        import build
        build.build()
        import importlib
        import cdet_core
        return importlib.reload(cdet_core)


def _frozen_c_value(tau, beta, mu):
    """compile a tiny program against the FROZEN engine and print G0_atom -- the independent reference."""
    src = (f'#include <stdio.h>\n#include "cdet_engine.h"\n'
           f'int main(){{printf("%.17g\\n", G0_atom({tau!r},{beta!r},{mu!r}));return 0;}}')
    open("/tmp/_cdet_fc.c", "w").write(src)
    subprocess.run(["gcc", "-O2", "-I", ENGINE, "/tmp/_cdet_fc.c", os.path.join(ENGINE, "cdet_engine.c"),
                    "-lm", "-o", "/tmp/_cdet_fc"], check=True, capture_output=True)
    return float(subprocess.run(["/tmp/_cdet_fc"], capture_output=True, text=True).stdout)


def _selftest():
    print("bindings_check self-test (native cdet_core vs the frozen engine; no subprocess):")
    cc = _ensure_built()
    print("  [build] cdet_core extension built and imported")

    # (1) bit-identical to the frozen C engine (same compiled function)
    worst = 0.0
    for (tau, beta, mu) in [(0.3, 5.0, 0.7), (1.1, 2.0, 1.0), (0.05, 8.0, -0.3)]:
        worst = max(worst, abs(cc.G0_atom(tau, beta, mu) - _frozen_c_value(tau, beta, mu)))
    print(f"  [parity] native G0_atom vs frozen-C G0_atom: worst dev = {worst:.1e}")
    assert worst == 0.0, worst

    # (2) the 2D plane-wave propagator matches the validated reference value (L=16 NN, beta=5)
    nn16 = cc.square2d_g0(16, 5.0, 0.0, 1.0, 0, 1, 0.0)
    assert abs(nn16 - 0.19929464404065) < 1e-12, nn16
    print(f"  [parity] native square2d_g0 (L=16 NN) = {nn16:.14f}  (matches the validated plane-wave path)")

    # (3) subprocess-elimination benchmark
    n = 200000
    t0 = time.perf_counter()
    for _ in range(n):
        cc.G0_atom(0.3, 5.0, 0.7)
    native_per = (time.perf_counter() - t0) / n
    t0 = time.perf_counter()
    _frozen_c_value(0.3, 5.0, 0.7)              # one compile+spawn (what the gates pay per engine access)
    subproc = time.perf_counter() - t0
    print(f"  [speed] native call: {native_per*1e9:.0f} ns/call; one subprocess compile+run: {subproc*1e3:.0f} ms")
    print(f"          -> ~{subproc/native_per:.2e}x overhead removed per engine access (programmatic loops now native)")
    assert native_per < 1e-5, native_per       # sub-10-microsecond native calls
    print("  => bindings are bit-identical to the frozen engine and remove the subprocess overhead. PASS")


if __name__ == "__main__":
    _selftest()
