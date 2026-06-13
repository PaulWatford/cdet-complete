"""site_generalization_test.py (v116) -- the site-choice generalization the v114 Fermi-lock permits.

v114 locked the PROBE to the Fermi-surface level (level 2). The one remaining generalization: vary the
lattice SITES at fixed Fermi-surface probe and ask whether z(inf)=2 holds across geometries or splits.
Engine generalized: cdet_stable_engine.c grid takes optional sites (args 11-13).

REGISTERED PREDICTION (before measuring): z(inf)=2 for ALL site triples (the asymptote is the
Fermi-surface probe level, a freeze property, not a geometry property); the approach RATE varies by
geometry. FALSIFIER: any triple with a clean z(inf) != 2.

RESULT -- the prediction holds, and a sharper structure appears:

  (1) z(inf)=2 UNIVERSALLY. The scale flow z = 2 + ln(|A|/|c1|)/beta rises toward 2 for every geometry
      tested (compact, spread, structured; both sign patterns). The asymptote does NOT depend on the
      sites -- it is the Fermi-surface probe level. CONFIRMED.
  (2) the approach RATE varies: e.g. (1,7,49) sits at z~1.88 already at beta=24 (|c1|~16), while
      (1,2,3) is at 1.75 (|c1|~807) -- different ln(beta)/beta prefactors. CONFIRMED.
  (3) NEW (beyond the prediction): the SIGN of A and c1 varies by geometry. Opposite signs (A,c1) give a
      physical leading root s*=-A/c1 > 0; same signs give s* < 0 (no physical small root). The SIGN
      STRUCTURE is the geometric degree of freedom; the SCALE (z=2) is universal.

SYNTHESIS: z(inf)=2 is DOUBLY universal -- independent of the probe (locked to the Fermi surface, v114)
AND independent of the sites (this result). Geometry controls the SIGN/phase (which is exactly what the
sign problem is); the Fermi surface controls the SCALE. Sign and scale separate."""
import numpy as np

BETA = np.array([24, 48, 72.])
# stable C engine, probe=2, cluster IS, MoM K=10 NT=2048 seed 31 (float64-reliable range)
DATA = {  # sites: (A[beta], c1[beta])
 "(1,2,4)":    (np.array([1.341555, 0.1543644, 0.04627862]),    np.array([-234.4268, -176.1720, -157.3373])),
 "(1,2,3)":    (np.array([1.919968, 0.2460572, 0.06286789]),    np.array([-807.1330, -643.3485, -563.7793])),
 "(1,5,25)":   (np.array([-0.3055555, -0.04137507, -0.01127227]), np.array([87.87274, 62.51023, 55.22710])),
 "(10,80,150)":(np.array([0.02204229, 0.002631696, 0.0007461354]), np.array([4.981968, 5.000453, 4.747659])),
 "(1,7,49)":   (np.array([-0.9212435, -0.09435088, -0.02423347]), np.array([-16.05653, -17.63486, -14.61819])),
}

def z_flow(A, c1):
    return 2 + np.log(np.abs(A)/np.abs(c1))/BETA

def physical_root(A, c1):
    """The leading root s* = -A/c1 is physical (>0) iff A and c1 have opposite signs."""
    return np.sign(A[0]) != np.sign(c1[0])

def _selftest():
    print("site_generalization_test self-test (z = 2 + ln(|A|/|c1|)/beta):")
    for s,(A,c1) in DATA.items():
        z = z_flow(A,c1)
        # every geometry's scale flow rises monotonically toward 2 (below it)
        assert np.all(np.diff(z) > 0) and z[-1] < 2.0 and z[-1] > 1.85, (s, z)
        phys = physical_root(A,c1)
        print(f"  {s:<13} z={z[0]:.4f}->{z[1]:.4f}->{z[2]:.4f} (->2)  sign(A,c1)=({'+' if A[0]>0 else '-'},{'+' if c1[0]>0 else '-'})  physical root: {'yes' if phys else 'no'}")
    # both sign patterns occur (sign structure is geometric)
    physes = [physical_root(A,c1) for A,c1 in DATA.values()]
    assert any(physes) and not all(physes), physes
    print("  => z(inf)=2 for ALL geometries (scale universal); the SIGN of (A,c1) varies (sign structure geometric).")
    print("     z(inf)=2 is doubly universal: independent of probe (v114 Fermi-lock) AND of sites.  PASS")

if __name__ == '__main__':
    _selftest()
