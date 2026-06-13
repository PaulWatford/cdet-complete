#!/usr/bin/env python3
"""
locality_prune_test.py  (v22)  --  can the PROVEN output-locality (folder 04) be used to prune the
connected-determinant recursion and beat the per-order 3^n? Tested here. The answer is NO, for a
concrete and important reason -- and the test points to the lever that DOES work.

The idea under test (the natural one): folder 04 proved on the real engine that the connected
determinant is exponentially local -- |C_spread|/|C_compact| ~ exp(-separation/xi). The recursion
C[mask] = D_corr[mask] - sum_{sm subset mask} C[sm] * D_vac[mask\\sm] costs 3^n (the submask sum).
If distant subset-pairs cancel, prune them: skip the term C[sm]*D_vac[complement] when the cut
between sm and its complement is spatially long-range. In 1D this would turn 3^n into ~polynomial.

The test (faithful to the engine's C_V recursion; kernel decays in space like the engine's G0):
take a CHAIN of n vertices (a connected order-n diagram that spans space), compute the exact
connected value with the full recursion, then with the locality-pruned recursion at cutoff R, and
compare value AND operation count.

RESULT -- pruning FAILS:
  chain n=12: C_exact = 3.64e-4, full ops = 527345.
    prune R=5: keeps 81% of the ops but gives 74% error.
    and the error GROWS with order n at fixed R (more cancellation at higher n).
Keeping 81% of the work and still being 74% wrong means the ~19% of "long-range" terms carry the
answer. They are individually LARGE; only their full sum cancels down to the small connected
residual. So:

  LOCALITY IS A PROPERTY OF THE OUTPUT, NOT OF THE COMPUTATION.
The connected value is local (folder 04), but the recursion that produces it cannot be localized --
every term matters for the cancellation. The per-config 3^n is irreducible; you cannot prune it by
spatial distance without destroying the cancellation that defines the connected part.

WHERE THIS REDIRECTS US (the lever that does not fight the cancellation):
Cost ~ 3^n in the ORDER n, so shaving delta-n off the order needed is worth a factor 3^(delta-n) --
exponential. That is reachable WITHOUT touching the per-config recursion, by reducing n:
  (1) Control variate from the learned IR physics: subtract a reference that already carries the
      known long-distance/low-energy structure (the exact K_rho power law, the velocities, the CFT
      tail) so the residual series converges at lower order.
  (2) Expand around the ATOMIC limit, not U=0: the engine already ships G_exact_atom; a strong-
      coupling/atomic reference converges in fewer orders at the U where we operate.
Neither relies on per-term locality, so neither breaks the cancellation. That is the v23 direction.
Locality still helps -- but on the SAMPLING side (compact configs dominate, so confine the vertex
integration), reducing variance, not the per-config cost.
"""
import numpy as np

XI = 1.6


def G0(xa, ta, xb, tb):
    d = abs(xa - xb)
    return -0.5 if (xa == xb and ta == tb) else np.exp(-d / XI) * np.exp(-0.7 * abs(ta - tb))


def Dv(vs):
    m = len(vs)
    if m == 0:
        return 1.0
    return np.linalg.det(np.array([[G0(*vs[a], *vs[b]) for b in range(m)] for a in range(m)]))


def Dc(vs, ext):
    pts = [ext] + list(vs); m = len(pts)
    return np.linalg.det(np.array([[G0(*pts[a], *pts[b]) for b in range(m)] for a in range(m)]))


def C_full(vs, ext):
    n = len(vs); N = 1 << n; C = [0.0] * N
    Dvv = [Dv([vs[i] for i in range(n) if m >> i & 1]) for m in range(N)]; ops = 0
    for k in range(n + 1):
        for mask in range(N):
            if bin(mask).count("1") != k:
                continue
            val = Dc([vs[i] for i in range(n) if mask >> i & 1], ext); sm = (mask - 1) & mask
            while True:
                if sm != mask:
                    val -= C[sm] * Dvv[mask ^ sm]; ops += 1
                if sm == 0:
                    break
                sm = (sm - 1) & mask
            C[mask] = val
    return C[N - 1], ops


def _pos(mask, vs, n):
    return [vs[i][0] for i in range(n) if mask >> i & 1]


def C_pruned(vs, ext, R):
    n = len(vs); N = 1 << n; C = [0.0] * N; ops = 0; Dvv = {}

    def connR(mask):
        ps = sorted(_pos(mask, vs, n))
        return all(ps[i + 1] - ps[i] <= R for i in range(len(ps) - 1)) if ps else True

    def cutd(a, b):
        return min((abs(pa - pb) for pa in a for pb in b), default=0)

    for k in range(n + 1):
        for mask in range(N):
            if bin(mask).count("1") != k or not connR(mask):
                continue
            val = Dc([vs[i] for i in range(n) if mask >> i & 1], ext); sm = (mask - 1) & mask
            while True:
                if sm != mask and connR(sm):
                    comp = mask ^ sm
                    if cutd(_pos(sm, vs, n) or [ext[0]], _pos(comp, vs, n)) <= R:
                        if comp not in Dvv:
                            Dvv[comp] = Dv([vs[i] for i in range(n) if comp >> i & 1])
                        val -= C[sm] * Dvv[comp]; ops += 1
                if sm == 0:
                    break
                sm = (sm - 1) & mask
            C[mask] = val
    return C[N - 1], ops


def main():
    rng = np.random.default_rng(3)
    print("Can output-locality prune the connected-determinant recursion? (chain configs)\n")
    print("  n   C_exact     full_ops |  R   pruned_C    rel.err   ops(%full)")
    for n in [8, 10, 12]:
        vs = [(i, rng.uniform(0, 1)) for i in range(n)]; ext = (0, 0.0)
        exact, opf = C_full(vs, ext)
        rows = []
        for R in [2, 3, 5]:
            cp, opp = C_pruned(vs, ext, R)
            rows.append((R, cp, abs(cp - exact) / (abs(exact) + 1e-300), 100 * opp / opf))
        print("  %-2d  %.3e  %8d |  2  %.3e  %6.0f%%   %5.1f%%"
              % (n, exact, opf, rows[0][1], 100 * rows[0][2], rows[0][3]))
        for R, cp, er, pc in rows[1:]:
            print("  %-2s  %-10s %8s |  %d  %.3e  %6.0f%%   %5.1f%%" % ("", "", "", R, cp, 100 * er, pc))
    print("\n  Pruning keeps most of the work yet is badly wrong, and the error GROWS with n.")
    print("  Locality is a property of the connected OUTPUT, not of the recursion's terms: the")
    print("  per-config 3^n cancellation is irreducible. The cost lever is reducing the ORDER n")
    print("  (control variate from the learned IR physics; atomic-limit expansion) -- not pruning.")


if __name__ == '__main__':
    main()
