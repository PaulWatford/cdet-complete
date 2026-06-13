"""wall_twist.py (v175) -- "half-integer" lattices: twisted boundary conditions and rectangular supercells.

You cannot have a fractional number of sites, but there are two standard ways to get a "half-integer" lattice, and they
let us ask whether the v173/v174 tide-and-sieve is a real feature of the wall or just a sampling artifact:

  (A) TWISTED boundary conditions: single-particle momenta k = 2*pi*(n+theta)/L, theta in [0,1) a flux through the torus.
      theta=0 is periodic; theta=1/2 is ANTI-PERIODIC -- the literal "half-integer" half-shifted grid.
  (B) RECTANGULAR / tilted supercells Lx x Ly: the momentum-transfer grid becomes (2*pi*mx/Lx, 2*pi*my/Ly) -- non-square,
      effectively non-integer linear resolution.

VERDICT (beta=5, mu=-0.6, peak q*=(0.783,1.000)pi):
  * Twist does NOT heal the sieve. In the particle-hole susceptibility the twist cancels in k -> k+q differences, so the
    momentum-TRANSFER grid q = 2*pi*m/L is theta-INDEPENDENT. The peak (pi,pi) stays on-grid only for even L whatever the
    twist; anti-periodic does not flip the parity, and twist-averaging cuts the prime error only ~7%. The sieve is a
    q-RESOLUTION effect, not a k-quadrature one.
  * Rectangular supercells DO heal it. A non-square q-grid can place a point exactly on q*: 23x46 nails q*=(0.783,1.000)
    (error 4e-4) even though 23 is PRIME, where the square 17x17 misses badly (error 6e-2).
  * The unifying rule is DIOPHANTINE: a lattice captures q* in a direction iff q*_comp * L / 2 is near an integer.
    Composite/even L satisfy this more often when q* is near a low-denominator rational (the v174 sieve); a rectangular
    cell lets you satisfy it per-direction for ANY size.

So the tide and the sieve are finite-size SAMPLING artifacts of the q-grid relative to the nesting vector, removable by
choosing a supercell whose q-grid hits q* -- not properties of the true (thermodynamic-limit) wall. Frozen engine untouched.
"""
import numpy as np
import wall_vs_size as _w


def chi0_max(Lx, Ly, beta, mu, thx=0.0, thy=0.0, t=1.0):
    """peak of the free static susceptibility on an Lx x Ly grid with twist (thx,thy); returns (chi0_max, q-index).
    Routes through the canonical wall_vs_size core so the whole wall suite shares one implementation."""
    return _w.chi0_max_rect(Lx, Ly, beta, mu, thx, thy, t)


def wall(Lx, Ly, beta, mu, thx=0.0, thy=0.0):
    return 1.0 / chi0_max(Lx, Ly, beta, mu, thx, thy)[0]


def twist_avg_wall(L, beta, mu, n=4):
    """boundary-condition (twist) averaged wall on an L x L lattice, n x n theta grid."""
    th = np.linspace(0, 1, n, endpoint=False)
    return float(np.mean([wall(L, L, beta, mu, tx, ty) for tx in th for ty in th]))


def _selftest():
    print("wall_twist self-test (half-integer lattices: twisted BC + rectangular supercells vs the sieve):")
    beta = 5.0
    mu = -0.6
    uinf = wall(90, 90, beta, mu)
    print(f"  TD wall U_inf = {uinf:.4f}")

    # (1) anti-periodic (theta=1/2) does NOT flip the half-filling parity: the q-transfer grid is twist-independent
    h0 = wall(9, 9, beta, 0.0, 0.0, 0.0); ha = wall(9, 9, beta, 0.0, 0.5, 0.5)
    assert abs(h0 - ha) < 0.05 and h0 > 2.2, (h0, ha)
    print(f"  [twist]      half-filling L=9: periodic U_c={h0:.3f} == anti-periodic U_c={ha:.3f} (parity NOT flipped)")
    # the peak q-index is identical for theta=0 and theta=1/2 (transfer grid is theta-independent)
    q0 = chi0_max(9, 9, beta, 0.0, 0.0, 0.0)[1]; qa = chi0_max(9, 9, beta, 0.0, 0.5, 0.5)[1]
    assert q0 == qa, (q0, qa)
    print(f"  [mechanism]  peak q-index theta-independent: {q0} == {qa}  (twist cancels in p-h differences)")

    # (2) twist-averaging only marginally reduces the prime error -> the sieve is a q-resolution bottleneck
    e0 = abs(wall(17, 17, beta, mu) - uinf); ea = abs(twist_avg_wall(17, beta, mu) - uinf)
    assert ea > 0.7 * e0, (e0, ea)
    print(f"  [twist-avg]  prime L=17 error: theta=0 {e0:.4f} -> twist-avg {ea:.4f}  (NOT healed; q-resolution bound)")

    # (3) rectangular supercell DOES heal it: a tuned q-grid hits q* even with a prime dimension
    e_sq = abs(wall(17, 17, beta, mu) - uinf)
    e_rect = abs(wall(23, 46, beta, mu) - uinf)         # 23 prime; q*=(18/23, 46/46) lands on-grid
    assert e_sq > 0.05 and e_rect < 0.01, (e_sq, e_rect)
    qr = chi0_max(23, 46, beta, mu)[1]
    print(f"  [rectangular] 17x17 error {e_sq:.4f}  vs  23x46 error {e_rect:.4f}  (q-grid placed on q*, prime dim OK)")

    # (4) the Diophantine rule: capture <=> q*_x * L / 2 near an integer
    qstar_x = 2 * chi0_max(90, 90, beta, mu)[1][0] / 90      # ~0.783
    def dioph(L):  # distance of q*_x*L/2 to nearest integer
        v = qstar_x * L / 2.0; return abs(v - round(v))
    good = [L for L in range(16, 49) if dioph(L) < 0.06]; bad = [L for L in range(16, 49) if dioph(L) > 0.40]
    eg = np.mean([abs(wall(L, L, beta, mu) - uinf) for L in good])
    eb = np.mean([abs(wall(L, L, beta, mu) - uinf) for L in bad])
    assert eg < eb, (eg, eb)
    print(f"  [Diophantine] q*_x*L/2 near integer -> small error: good-L {eg:.4f} < bad-L {eb:.4f}")
    print("  => twist (the literal half-integer BC) does NOT heal the sieve; a rectangular supercell whose q-grid hits")
    print("     q* does. The tide/sieve are q-sampling artifacts, not properties of the true wall. Frozen engine untouched. PASS")


if __name__ == "__main__":
    _selftest()
