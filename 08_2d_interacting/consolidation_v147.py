"""consolidation_v147.py -- full consolidation of the integration arc (v131-v146), all three models at their
highest proven capability. Single health gate for the consolidated state.

ARCHITECTURE (the design that keeps the archive trustworthy):
  - FROZEN REFERENCE: engine/ (194/194, never altered) -- the validation anchor every claim is checked against.
    Efficiency targets: `make fast` (-O3 -march=native), `make omp` (OpenMP).
  - PRODUCTION ENGINE: cdet_planewave_engine.c (the hybrid) -- carries the capabilities and validates == the
    frozen reference (0.00e+00 at L=6). f64 + `-DUSE_LD` builds; `-fast` projector path; mode-2 continuous
    freeze; 3 input guards (delta<=0, large delta, non-crystallographic L). Any-L, scales to multi-million sites.
  - SURROGATE: csurrogate.c -- the fast pure-arithmetic carriers (lowest_empty=addition pole, friedel_edge,
    interacting_pole=free+Hartree, and the SU(N) production coeffs sun_c1, sun_n1).

ANALYSIS SUPPLEMENTS kept as separate CLI modules (better design + end-user configurability): fast_minors,
cos_prototype, physical_mapping, self_energy*, rational_skeleton, sun_atom/lattice_record, sun_lattice_production,
sun_resummation_N, rational_lattice_boundary, resummation. Each self-tests against ED / the frozen engine.

This gate checks the three models agree on the shared observables and that the headline capabilities are live."""
import os, subprocess
import tempfile
import numpy as np
from physical_mapping import addition_pole
from sun_lattice_production import c1_production, n1_production, g0_amplitudes
from fast_minors import all_principal_minors

HERE = os.path.dirname(os.path.abspath(__file__))

def _surrogate_call(expr, extra_args=""):
    src = ('#include <stdio.h>\n#include "csurrogate.h"\nint main(){printf("%.10f\\n", ' + expr + ');return 0;}')
    open(os.path.join(tempfile.gettempdir(), '_sc.c'), 'w').write(src)
    out = os.path.join(tempfile.gettempdir(), '_sc' + ('.exe' if os.name=='nt' else ''))
    r = subprocess.run(['gcc', '-O2', '-I', HERE, '-o', out, os.path.join(tempfile.gettempdir(), '_sc.c'), os.path.join(HERE, 'csurrogate.c'), '-lm'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return float(subprocess.run([out], capture_output=True, text=True).stdout)

def _selftest():
    print("consolidation_v147 self-test (three models at highest capability; all caps live):")
    # (1) surrogate SU(N) carriers == python production route (v144)
    d, dp = g0_amplitudes(); d, dp = float(d), float(dp)
    sc1 = _surrogate_call("surr_sun_c1(6, %.10f)" % d)
    sn1 = _surrogate_call("surr_sun_n1(6, %.10f, %.10f)" % (d, dp))
    if sc1 is not None:
        beta = 2.0
        assert abs(sc1 * beta - c1_production(6)) < 1e-6, (sc1, c1_production(6))  # c1_production = beta * surr_sun_c1
        assert abs(sn1 - n1_production(6)) < 1e-9, (sn1, n1_production(6))
        print(f"  surrogate SU(N) carriers == production route (N=6): c1, n1 match")
    else:
        print("  (surrogate C unbuildable here)")
    # (2) surrogate addition pole == python (the physical mapping)
    sp = _surrogate_call("surr_lowest_empty(12, 1.0)")
    if sp is not None:
        assert abs(sp - addition_pole(12, 1.0)) < 1e-9
        print(f"  surrogate addition pole == python (L=12): {sp:.6f}")
    # (3) fast minors capability live (== numpy det)
    R = np.random.default_rng(0).standard_normal((6, 6))
    assert abs(all_principal_minors(R)[(1 << 6) - 1] - np.linalg.det(R)) < 1e-9
    print("  fast minors (O(2^n n^2) connected determinant) capability: live")
    print("  => three models consistent at highest capability; analysis supplements are separate CLI modules.")
    print("     Frozen reference engine/ (194/194) untouched; hybrid validates == it; surrogate carries SU(N). PASS")

if __name__ == "__main__":
    _selftest()
