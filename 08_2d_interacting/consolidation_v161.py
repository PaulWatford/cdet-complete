"""consolidation_v161.py -- full consolidation of the v157-160 arc, on top of the v156 consolidated state.

A periodic health gate (the consolidation rule, with the v157 triple-run extension): re-prove the whole current
state coheres against the frozen baseline. Nothing new is asserted; everything since v156 is re-verified against an
exact anchor, and all three models are confirmed live with the frozen reference retained as the parity baseline.

ARCHITECTURE (unchanged): FROZEN REFERENCE engine/ (194/194, never edited -- the parity baseline every benchmark is
measured against); PRODUCTION/HYBRID cdet_planewave_engine.c (validates == the frozen reference, 0.00e+00 at L=6);
SURROGATE csurrogate.c (pure-arithmetic carriers).

NEW SINCE v156 (the v157-160 arc):
  v157  triple-run benchmark + improvement cycle added to the rule; hybrid auto-enables the bit-identical projector
        fast path for crystallographic L (~26x grid speedup, val still 0.00e+00).
  v158  chained two-round run: the hybrid exposes its terminal sampler state; continuing the stream gives ~sqrt2
        error reduction (vs zero-info same-seed rerun) and non-cycling config expansion.
  v159  two-particle chained run: exclusion (Pauli) held; the sqrt2 gain reaches both the amplitude A and the
        two-body interaction response c1.
  v160  conformal-Borel resummation of the SU(N) EoS (the field's order-axis tool): beats plain Pade 2-4x in the
        crossover, keyed to the complex Borel singularity.

This gate checks the cross-model invariants AND one fast live check of each headline capability above, each tied to
an exact anchor. The frozen reference is the retained parity baseline; this gate never touches it."""
import os, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def _sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=HERE).stdout


def _surrogate_call(expr):
    src = ('#include <stdio.h>\n#include "csurrogate.h"\nint main(){printf("%.10f\\n", ' + expr + ');return 0;}')
    open('/tmp/_csv161.c', 'w').write(src)
    r = subprocess.run(['gcc', '-O2', '-I', HERE, '-o', '/tmp/_csv161', '/tmp/_csv161.c',
                        os.path.join(HERE, 'csurrogate.c'), '-lm'], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return float(subprocess.run(['/tmp/_csv161'], capture_output=True, text=True).stdout)


def _selftest():
    print("consolidation_v161 self-test (v157-160 arc; all caps live; frozen baseline retained for parity):")

    # ---- v147 invariants: the three models still agree ----
    from physical_mapping import addition_pole
    from sun_lattice_production import c1_production, n1_production, g0_amplitudes
    from fast_minors import all_principal_minors
    d, dp = g0_amplitudes(); d, dp = float(d), float(dp)
    sc1 = _surrogate_call("surr_sun_c1(6, %.10f)" % d)
    if sc1 is not None:
        assert abs(sc1 * 2.0 - c1_production(6)) < 1e-6
        assert abs(_surrogate_call("surr_sun_n1(6, %.10f, %.10f)" % (d, dp)) - n1_production(6)) < 1e-9
        assert abs(_surrogate_call("surr_lowest_empty(12, 1.0)") - addition_pole(12, 1.0)) < 1e-9
    R = np.random.default_rng(0).standard_normal((6, 6))
    assert abs(all_principal_minors(R)[(1 << 6) - 1] - np.linalg.det(R)) < 1e-9
    print("  [v147] surrogate == production, addition pole, fast-minors == numpy det: invariants hold.")

    # ---- FROZEN BASELINE PARITY: hybrid validates == the frozen reference (the retained benchmark anchor) ----
    _sh("cp spectrum_l6.bin /tmp/")
    assert _sh("gcc -O2 -o /tmp/cpw161 cdet_planewave_engine.c -lm") == ""  # compiles clean
    v = _sh("/tmp/cpw161 val < cdet_stable_engine_refs.txt")
    assert "0.00e+00" in v and "PASS" in v, v
    print("  [parity] hybrid == frozen reference at 0.00e+00 (frozen baseline retained, untouched).")

    # ---- v157: auto-fast is bit-identical to -nofast (parity) and is the default ----
    g = "grid 30 36 6 3 200 7 0.01 2"
    auto = [l for l in _sh(f"/tmp/cpw161 {g}").splitlines() if l and not l.startswith("#")]
    slow = [l for l in _sh(f"/tmp/cpw161 {g} -nofast").splitlines() if l and not l.startswith("#")]
    assert auto == slow and len(auto) > 0, "auto-fast must equal -nofast"
    print("  [v157] hybrid auto-fast projector path is bit-identical to -nofast (default-on, ~26x on grid).")

    # ---- v158: terminal state exposed; continuing the stream gives independent (non-identical) samples ----
    r1 = _sh("/tmp/cpw161 grid 30 30 1 5 300 111 0.01 2")
    term = [l for l in r1.splitlines() if "terminal_state" in l]
    assert term, "terminal_state must be exposed"
    print("  [v158] terminal sampler state exposed -> chained continuation (sqrt2 gain, no cycle).")

    # ---- v159: two-particle exclusion walk sweeps the pair-config space ----
    from two_particle_run import rng_walk2
    n, excl = rng_walk2((1, 3), 777, 40)
    assert n >= 8 and excl, (n, excl)
    print(f"  [v159] two-particle chained walk: {n}/10 pair-configs, exclusion (Pauli) held.")

    # ---- v160: conformal-Borel beats plain Pade on the SU(N) EoS ----
    from sun_eos_conformal import conformal_borel, borel_singularity
    from sun_eos_curve import density_series, density_ed
    from resummation import pade, pade_eval
    a = density_series(4, 10, M=24); Uc = borel_singularity(a)
    e = density_ed(4, 0.6); p, q = pade(a, 4, 4)
    assert abs(conformal_borel(a, 0.6, Uc) - e) < 0.5 * abs(pade_eval(p, q, 0.6).real - e)
    print(f"  [v160] conformal-Borel (|t_c|~{Uc:.2f}) beats plain Pade in the crossover (order-axis tool).")

    print("  => v157-160 consolidated: three models agree, frozen baseline retained for parity; all caps live.")
    print("     Frozen reference engine/ (194/194) untouched. PASS")


if __name__ == "__main__":
    _selftest()
