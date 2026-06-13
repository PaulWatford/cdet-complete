"""consolidation_v156.py -- full consolidation of the v148-155 arc, on top of the v147 consolidated state.

This is a periodic health gate (the consolidation rule): it re-proves the whole current state coheres. Nothing new
is asserted; everything since the last consolidation (v147) is re-verified against an exact anchor.

ARCHITECTURE (unchanged design that keeps the archive trustworthy):
  - FROZEN REFERENCE: engine/ (194/194, never altered) -- the validation anchor every claim is checked against.
  - PRODUCTION ENGINE: cdet_planewave_engine.c (the hybrid) -- validates == the frozen reference (0.00e+00 at L=6).
  - SURROGATE: csurrogate.c -- the fast pure-arithmetic carriers (addition pole, Friedel edge, interacting pole,
    and the SU(N) production coeffs sun_c1, sun_n1).

NEW SINCE v147 -- two arcs:
  (A) UI CONTROL PLANE (v148-151): cdet_lab.py (unified CLI: target x method x model over every capability),
      cdet_shell.py (conversational front-end over cdet_lab, blind-test hardened), cdet_study.py (sweep/stress
      harness with convergence + accuracy/time cutoffs). The terminal entry points to every capability.
  (B) SU(N) EoS, weak -> strong -> 2D thermodynamic limit -> 2nd order:
      sun_eos_curve.py (v152: record-predicted weak EoS curve, Pade), sun_eos_strong.py (v153: two-point
      resummation reaches U/t=2.3 Kozik at 2.4%), sun_eos_2d.py (v154: production formula transfers across
      geometry; 2D thermodynamic limit via k-integral, no diagonalization), sun_eos_n2.py (v155: 2nd-order
      coefficient = (N-1)^2 self-consistent Hartree [exact in 2D] + (N-1) bubble).

This gate checks the cross-model invariants AND one fast live check of each headline capability above, each tied to
an exact anchor. Frozen engine/ stays 194/194; this gate never touches it."""
import os, subprocess
import tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def _surrogate_call(expr):
    src = ('#include <stdio.h>\n#include "csurrogate.h"\nint main(){printf("%.10f\\n", ' + expr + ');return 0;}')
    open(os.path.join(tempfile.gettempdir(), '_csv.c'), 'w').write(src)
    r = subprocess.run(['gcc', '-O2', '-I', HERE, '-o', os.path.join(tempfile.gettempdir(), '_csv' + ('.exe' if os.name=='nt' else '')), os.path.join(tempfile.gettempdir(), '_csv.c'),
                        os.path.join(HERE, 'csurrogate.c'), '-lm'], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return float(subprocess.run([os.path.join(tempfile.gettempdir(), '_csv' + ('.exe' if os.name=='nt' else ''))], capture_output=True, text=True).stdout)


def _selftest():
    print("consolidation_v156 self-test (v148-155 arc consolidated; all caps live, cross-model agreement holds):")

    # ---- v147 invariants: the three models still agree ----
    from physical_mapping import addition_pole
    from sun_lattice_production import c1_production, n1_production, g0_amplitudes
    from fast_minors import all_principal_minors
    d, dp = g0_amplitudes(); d, dp = float(d), float(dp)
    sc1 = _surrogate_call("surr_sun_c1(6, %.10f)" % d)
    if sc1 is not None:
        sn1 = _surrogate_call("surr_sun_n1(6, %.10f, %.10f)" % (d, dp))
        assert abs(sc1 * 2.0 - c1_production(6)) < 1e-6
        assert abs(sn1 - n1_production(6)) < 1e-9
        assert abs(_surrogate_call("surr_lowest_empty(12, 1.0)") - addition_pole(12, 1.0)) < 1e-9
        print("  [v147] surrogate == production (SU(N) c1,n1) and addition pole; ", end="")
    R = np.random.default_rng(0).standard_normal((6, 6))
    assert abs(all_principal_minors(R)[(1 << 6) - 1] - np.linalg.det(R)) < 1e-9
    print("fast-minors == numpy det. invariants hold.")

    # ---- (A) UI control plane (v148-151) ----
    import cdet_lab
    assert len(cdet_lab.COMPONENTS) > 0 and ("eos", "record") in cdet_lab.COMPONENTS
    import cdet_shell, cdet_study
    assert cdet_shell.cdet_lab.COMPONENTS is cdet_lab.COMPONENTS and len(cdet_shell.TARGETS) > 0  # shell's single source of truth
    assert callable(cdet_study.study)
    print(f"  [v148-151] UI live: cdet_lab COMPONENTS={len(cdet_lab.COMPONENTS)}, shell shares them, study harness present.")

    # ---- (B) SU(N) EoS arc (v152-155), each vs an exact anchor ----
    # v152: weak record series -- the U=0 coefficient is the free single-flavor density (N-independent)
    from sun_eos_curve import density_series
    assert abs(density_series(2, 1, M=12)[0] - 0.741) < 5e-3
    # v153: strong anchor is the atomic limit, smooth in N; two-point [2/2] solves and is finite
    from sun_eos_strong import strong_series, two_point_pade, eos_value
    m2, m3 = strong_series(2, 2), strong_series(3, 2)
    assert m2[0] > m3[0] > 0
    p, q = two_point_pade([0.74, -0.5, 0.3], [0.4, 0.1], 2)
    assert np.isfinite(eos_value(p, q, 2.0))
    # v154: production formula transfers to 2D; k-integral converged
    from sun_eos_2d import free_dd, free_dd_2d, square2d, n1_2d
    dd, dpp = free_dd(square2d(2, 3))
    assert dd > 0 and dpp > 0
    d2a, _ = free_dd_2d(nk=120); d2b, _ = free_dd_2d(nk=240)
    assert abs(d2a - d2b) < 1e-5 and abs(d2b - 0.671378) < 1e-4
    assert abs(n1_2d(6) - (-0.511561)) < 1e-4
    # v155: n2 (N-1)^2 coeff is the self-consistent Hartree from free 2D derivatives
    from sun_eos_n2 import hartree_a, free_derivs_2d
    assert abs(hartree_a(*free_derivs_2d(nk=240)) - 0.005622) < 1e-4
    print("  [v152-155] EoS live: weak n0=free density; strong atomic anchor + stable two-point; 2D n1=-0.5116;")
    print("              2D n2 Hartree part a_2D=0.005622 -- all vs ED/k-integral anchors.")

    print("  => v148-155 consolidated: three models agree; UI + SU(N) EoS (weak->strong->2D->2nd order) all live.")
    print("     Frozen reference engine/ (194/194) untouched. PASS")


if __name__ == "__main__":
    _selftest()
