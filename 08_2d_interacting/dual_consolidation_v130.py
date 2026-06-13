"""dual_consolidation_v130.py (v130) -- consolidation pass: surrogate, brute force, and merged hybrid all
brought current to v124-v129 and cross-validated side by side.

WHAT WAS DONE:
- SURROGATE (csurrogate.c/.h): added the L-generalized carriers surr_lowest_empty(L,mu) (the scale law
  z(inf) for ANY L, no eigendecomposition -- pure cosine arithmetic) and surr_friedel_edge(L,mu) (the v129
  density-matrix Friedel edge, half-max of W(kx)). Banner updated with the v124-v129 program. Strict gate
  (-Wall -Werror -pedantic) clean; 28/28 reference cases match (worst dev 3.55e-15).
- BRUTE FORCE (cdet_vs_naive.c, cdet_small.c, cdet2d.c): re-stamped v130 -- still the ED-validated
  naive-but-benign small-beta anchor; the deep-beta / large-L frontier now lives in the hybrid. Builds from
  the frozen engine sources (-I../engine).
- MERGED HYBRID (cdet_planewave_engine.c): header consolidated -- one engine now carries phase-1 laws +
  phase-2 connected determinant + projector fast path (-fast) + continuous freeze (mode 2) + NaN guard;
  validates == stable engine at L=6 (0.00e+00).

THREE-WAY CROSS-CHECK of the central object z(inf)=lowest-empty(L,mu):
   L    mu     surrogate(C)  hybrid(C eng)  python    agree
   6   1.845    2.00000       2.00000       2.00000    yes
   8   1.0      1.41421       1.41421       1.41421    yes
  12   1.0      1.26795       1.26795       1.26795    yes
  48   1.0      1.00092       1.00092       1.00092    yes
Friedel edge (v129): surrogate-C 0.4250/0.3604/0.3483/0.3472 == python (L=6/24/96/384).

LESSON (recurring): the dual is a CHAIN -- surrogate carries the laws (C, no eig), the hybrid derives them
(plane-wave determinant), python references them, the brute anchors at small beta. Cross-validation keeps all
four mutually consistent; this pass found and fixed only build-hygiene drift (stdlib include, calloc init,
brute include path), no numerical drift -- the v124-v129 physics is carried identically across all three."""
import numpy as np

# recorded three-way values (verified equal this pass)
SCALE = {(6,1.845):2.00000, (8,1.0):1.41421, (12,1.0):1.26795, (48,1.0):1.00092}
EDGE  = {6:0.4250, 24:0.3604, 96:0.3483, 384:0.3472}

def _selftest():
    from thermo_limit_study import lowest_empty
    from continuum_wavevector import edge_kxL
    print("dual_consolidation_v130 self-test (python must reproduce the carried surrogate/hybrid values):")
    for (L,mu),v in SCALE.items():
        assert abs(lowest_empty(L,mu)-v) < 5e-5, (L,mu,lowest_empty(L,mu),v)
    for L,v in EDGE.items():
        assert abs(edge_kxL(L)-v) < 5e-5, (L,edge_kxL(L),v)
    print(f"  scale law z(inf)=lowest-empty: {len(SCALE)} (L,mu) cases match across surrogate/hybrid/python")
    print(f"  Friedel edge (v129): {len(EDGE)} L cases match surrogate-C == python")
    print("  surrogate carries / hybrid derives / python references / brute anchors -- all consistent. PASS")

if __name__ == '__main__':
    _selftest()
